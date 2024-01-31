from mex.common.cli import entrypoint
from mex.common.ldap.extract import get_merged_ids_by_query_string
from mex.common.ldap.transform import transform_ldap_persons_with_query_to_mex_persons
from mex.common.models import (
    ExtractedActivity,
    ExtractedOrganizationalUnit,
    ExtractedPrimarySource,
)
from mex.common.primary_source.transform import get_primary_sources_by_name
from mex.common.types import OrganizationalUnitID, OrganizationID, PersonID
from mex.common.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations,
)
from mex.ff_projects.extract import (
    extract_ff_project_authors,
    extract_ff_projects_organizations,
    extract_ff_projects_sources,
    filter_out_duplicate_source_ids,
    get_organization_merged_id_by_query,
)
from mex.ff_projects.filter import filter_and_log_ff_projects_sources
from mex.ff_projects.models.source import FFProjectsSource
from mex.ff_projects.settings import FFProjectsSettings
from mex.ff_projects.transform import transform_ff_projects_source_to_extracted_activity
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load


@asset(group_name="ff_projects", deps=["extracted_primary_source_mex"])
def extracted_primary_source_ff_projects(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return FF Projects extracted primary source."""
    (extracted_primary_source_ff_projects,) = get_primary_sources_by_name(
        extracted_primary_sources,
        "ff-projects",
    )
    load([extracted_primary_source_ff_projects])
    return extracted_primary_source_ff_projects


@asset(group_name="ff_projects")
def ff_projects_sources(
    extracted_primary_source_ff_projects: ExtractedPrimarySource,
    unit_stable_target_ids_by_synonym: dict[str, OrganizationalUnitID],
) -> list[FFProjectsSource]:
    """Extract FF Projects sources and filter out invalid items."""
    ff_projects_sources = extract_ff_projects_sources()
    ff_projects_sources = filter_out_duplicate_source_ids(ff_projects_sources)
    ff_projects_sources = filter_and_log_ff_projects_sources(
        ff_projects_sources,
        extracted_primary_source_ff_projects.stableTargetId,
        unit_stable_target_ids_by_synonym,
    )
    return list(ff_projects_sources)


@asset(group_name="ff_projects")
def ff_projects_person_ids_by_query_string(
    ff_projects_sources: list[FFProjectsSource],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
) -> dict[str, list[PersonID]]:
    """Extract authors for FF Projects from LDAP and group them by query."""
    ff_projects_authors = list(extract_ff_project_authors(ff_projects_sources))
    extracted_persons = transform_ldap_persons_with_query_to_mex_persons(
        ff_projects_authors,
        extracted_primary_source_ldap,
        extracted_organizational_units,
    )
    load(extracted_persons)
    return {
        str(query_string): [PersonID(id) for id in merged_ids]
        for query_string, merged_ids in get_merged_ids_by_query_string(
            ff_projects_authors, extracted_primary_source_ldap
        ).items()
    }


@asset(group_name="ff_projects")
def ff_projects_organization_ids_by_query_string(
    extracted_primary_source_wikidata: ExtractedPrimarySource,
    ff_projects_sources: list[FFProjectsSource],
) -> dict[str, OrganizationID]:
    """Extract organizations for FF Projects from wikidata and group them by query."""
    wikidata_organizations_by_query = extract_ff_projects_organizations(
        ff_projects_sources
    )
    mex_extracted_organizations = (
        transform_wikidata_organizations_to_extracted_organizations(
            wikidata_organizations_by_query.values(), extracted_primary_source_wikidata
        )
    )
    load(mex_extracted_organizations)
    return get_organization_merged_id_by_query(
        wikidata_organizations_by_query, extracted_primary_source_wikidata
    )


@asset(group_name="ff_projects")
def extract_ff_projects(
    ff_projects_sources: list[FFProjectsSource],
    extracted_primary_source_ff_projects: ExtractedPrimarySource,
    ff_projects_person_ids_by_query_string: dict[str, list[PersonID]],
    unit_stable_target_ids_by_synonym: dict[str, OrganizationalUnitID],
    ff_projects_organization_ids_by_query_string: dict[str, OrganizationID],
) -> list[ExtractedActivity]:
    """Transform FF Projects to extracted activities and load them to the sinks."""
    extracted_activities = [
        transform_ff_projects_source_to_extracted_activity(
            ff_projects_source,
            extracted_primary_source_ff_projects,
            ff_projects_person_ids_by_query_string,
            unit_stable_target_ids_by_synonym,
            ff_projects_organization_ids_by_query_string,
        )
        for ff_projects_source in ff_projects_sources
    ]
    load(extracted_activities)
    return extracted_activities


@entrypoint(FFProjectsSettings)
def run() -> None:
    """Run the ff-projects extractor job in-process."""
    run_job_in_process("ff_projects")
