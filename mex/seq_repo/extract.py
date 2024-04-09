import json
from collections.abc import Generator

from mex.common.identity import get_provider
from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPersonWithQuery
from mex.common.logging import watch
from mex.common.models import ExtractedPrimarySource
from mex.common.types import (
    MergedOrganizationIdentifier,
)
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.seq_repo.model import SeqRepoSource
from mex.seq_repo.settings import SeqRepoSettings


def extract_sources() -> Generator[SeqRepoSource, None, None]:
    """Extract Seq Repo sources by loading data from source json file.

    Settings:
        default_json_file_path: Path to the seq-repo json file,
                                absolute or relative to `assets_dir`

    Returns:
        Generator for Seq Repo resources
    """
    settings = SeqRepoSettings.get()
    with open(settings.default_json_file_path, encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            yield SeqRepoSource.model_validate(item)


@watch
def extract_source_project_coordinator(
    seq_repo_sources: dict[str, SeqRepoSource],
) -> Generator[LDAPPersonWithQuery, None, None]:
    """Extract LDAP persons with their query string for source project coordinators.

    Args:
        seq_repo_sources: Seq Repo sources

    Returns:
        Generator for LDAP persons with query
    """
    ldap = LDAPConnector.get()
    seen = set()
    for value in seq_repo_sources.values():
        names = value.project_coordinators
        for name in names:
            if not name:
                continue
            if name in seen:
                continue
            seen.add(name)
            persons = list(ldap.get_persons(mail=f"{name}@rki.de"))
            if len(persons) == 1 and persons[0].objectGUID:
                yield LDAPPersonWithQuery(person=persons[0], query=name)


def extract_seq_repo_organizations() -> dict[str, WikidataOrganization]:
    """Search and extract organizations from wikidata.

    Returns:
        Dict with organization label and WikidataOrganization
    """
    result = {}
    organization_title = "Robert Koch-Institut"
    if wikidata_organization := search_organization_by_label(organization_title):
        result[organization_title] = wikidata_organization
    return result


def get_organization_merged_id_by_query(
    wikidata_organizations_by_query: dict[str, WikidataOrganization],
    wikidata_primary_source: ExtractedPrimarySource,
) -> dict[str, MergedOrganizationIdentifier]:
    """Return a mapping from organizations to their stable target ID.

    There may be multiple entries per unit mapping to the same stable target ID.

    Args:
        wikidata_organizations_by_query: Iterable of extracted organizations
        wikidata_primary_source: Primary source item for wikidata

    Returns:
        Dict with organization label and stable target ID
    """
    identity_provider = get_provider()
    organization_stable_target_id_by_query = {}
    for query, wikidata_organization in wikidata_organizations_by_query.items():
        identities = identity_provider.fetch(
            had_primary_source=wikidata_primary_source.stableTargetId,
            identifier_in_primary_source=wikidata_organization.identifier,
        )
        if identities:
            organization_stable_target_id_by_query[query] = (
                MergedOrganizationIdentifier(identities[0].stableTargetId)
            )

    return organization_stable_target_id_by_query
