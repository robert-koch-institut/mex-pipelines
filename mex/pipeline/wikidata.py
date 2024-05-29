from mex.common.exceptions import MExError
from mex.common.identity import get_provider
from mex.common.models import ExtractedOrganization, ExtractedPrimarySource
from mex.common.types import MergedOrganizationIdentifier
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.common.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations,
)
from mex.pipeline import asset
from mex.sinks import load


@asset(group_name="default")
def wikidata_organization_rki() -> WikidataOrganization:
    """Extract WikidataOrganization for Robert Koch-Institut."""
    if org := search_organization_by_label("Robert Koch-Institut"):
        return org
    raise MExError("RKI not found on wikidata, cannot proceed.")


@asset(group_name="default")
def extracted_organization_rki(
    wikidata_organization_rki: WikidataOrganization,
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> ExtractedOrganization:
    """Transforms RKI organization data to extracted organizations and load result."""
    extracted_organization_rki = list(
        transform_wikidata_organizations_to_extracted_organizations(
            [wikidata_organization_rki], extracted_primary_source_wikidata
        )
    )
    load(extracted_organization_rki)
    return extracted_organization_rki[0]


def get_organization_merged_id_by_query(
    wikidata_organizations_by_query: dict[str, WikidataOrganization],
    wikidata_primary_source: ExtractedPrimarySource,
) -> dict[str, MergedOrganizationIdentifier]:
    """Return a mapping from organizations to their stable target ID.

    There may be multiple entries per unit mapping to the same stable target ID.

    Args:
        wikidata_organizations_by_query: dict of Extracted organizations by query string
        wikidata_primary_source: Primary source item for wikidata

    Returns:
        Dict with organization label keys and stable target ID values
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
