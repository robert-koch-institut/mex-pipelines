from mex.common.cli import entrypoint
from mex.common.ldap.extract import get_merged_ids_by_query_string
from mex.common.ldap.transform import transform_ldap_persons_with_query_to_mex_persons
from mex.common.models import ExtractedOrganizationalUnit, ExtractedPrimarySource
from mex.common.primary_source.transform import get_primary_sources_by_name
from mex.common.types import (
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
    MergedPersonIdentifier,
)
from mex.common.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations,
)
from mex.international_projects.extract import (
    extract_international_projects_funding_sources,
    extract_international_projects_partner_organizations,
    extract_international_projects_project_leaders,
    extract_international_projects_sources,
)
from mex.international_projects.models.source import InternationalProjectsSource
from mex.international_projects.settings import InternationalProjectsSettings
from mex.international_projects.transform import (
    transform_international_projects_sources_to_extracted_activities,
)
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load
from mex.wikidata.extract import (
    get_organization_merged_id_by_query,
    get_organization_merged_id_by_query_with_transform_and_load,
)


@asset(group_name="international_projects", deps=["extracted_primary_source_mex"])
def extracted_primary_source_international_projects(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return international projects primary source."""
    (extracted_primary_source_international,) = get_primary_sources_by_name(
        extracted_primary_sources, "international-projects"
    )
    load([extracted_primary_source_international])
    return extracted_primary_source_international


@asset(group_name="international_projects")
def international_projects_sources() -> list[InternationalProjectsSource]:
    """Extract from international project sources."""
    return list(extract_international_projects_sources())


@asset(group_name="international_projects")
def international_projects_person_ids_by_query(
    international_projects_sources: list[InternationalProjectsSource],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
) -> dict[str, list[MergedPersonIdentifier]]:
    """Transform LDAP persons to extracted persons and group their IDs by query."""
    ldap_project_leaders = list(
        extract_international_projects_project_leaders(international_projects_sources)
    )
    mex_authors = transform_ldap_persons_with_query_to_mex_persons(
        ldap_project_leaders,
        extracted_primary_source_ldap,
        extracted_organizational_units,
    )
    load(mex_authors)
    return get_merged_ids_by_query_string(
        ldap_project_leaders, extracted_primary_source_ldap
    )


@asset(group_name="international_projects")
def international_projects_funding_sources_ids_by_query(
    international_projects_sources: list[InternationalProjectsSource],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> dict[str, MergedOrganizationIdentifier]:
    """Extract funding sources and return their stable target IDs by query string."""
    wikidata_funding_sources_by_query = extract_international_projects_funding_sources(
        international_projects_sources
    )

    return get_organization_merged_id_by_query_with_transform_and_load(
        wikidata_funding_sources_by_query, extracted_primary_source_wikidata
    )


@asset(group_name="international_projects")
def international_projects_partner_organization_ids_by_query(
    international_projects_sources: list[InternationalProjectsSource],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> dict[str, MergedOrganizationIdentifier]:
    """Extract partner organizations and return their IDs grouped by query string."""
    wikidata_partner_organizations_by_query = (
        extract_international_projects_partner_organizations(
            international_projects_sources
        )
    )
    mex_extracted_organizations_partner_organizations = (
        transform_wikidata_organizations_to_extracted_organizations(
            wikidata_partner_organizations_by_query.values(),
            extracted_primary_source_wikidata,
        )
    )
    load(mex_extracted_organizations_partner_organizations)

    return get_organization_merged_id_by_query(
        wikidata_partner_organizations_by_query, extracted_primary_source_wikidata
    )


@asset(group_name="international_projects")
def extract_international_projects(
    international_projects_sources: list[InternationalProjectsSource],
    extracted_primary_source_international_projects: ExtractedPrimarySource,
    international_projects_person_ids_by_query: dict[str, list[MergedPersonIdentifier]],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    international_projects_funding_sources_ids_by_query: dict[
        str, MergedOrganizationIdentifier
    ],
    international_projects_partner_organization_ids_by_query: dict[
        str, MergedOrganizationIdentifier
    ],
) -> None:
    """Transform projects to extracted activities and load them to the sinks."""
    mex_sources = transform_international_projects_sources_to_extracted_activities(
        international_projects_sources,
        extracted_primary_source_international_projects,
        international_projects_person_ids_by_query,
        unit_stable_target_ids_by_synonym,
        international_projects_funding_sources_ids_by_query,
        international_projects_partner_organization_ids_by_query,
    )
    load(mex_sources)


@entrypoint(InternationalProjectsSettings)
def run() -> None:
    """Run the international-projects extractor job in-process."""
    run_job_in_process("international_projects")
