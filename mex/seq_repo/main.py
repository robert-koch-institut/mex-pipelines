from itertools import tee

from mex.common.cli import entrypoint
from mex.common.ldap.extract import get_merged_ids_by_query_string
from mex.common.ldap.models.person import LDAPPersonWithQuery
from mex.common.ldap.transform import transform_ldap_persons_with_query_to_mex_persons
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedDistribution,
    ExtractedOrganizationalUnit,
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.common.types import (
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
    MergedPersonIdentifier,
)
from mex.common.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations,
)
from mex.mapping.extract import extract_mapping_data
from mex.pipeline import asset, run_job_in_process
from mex.seq_repo.extract import (
    extract_seq_repo_organizations,
    extract_source_project_coordinator,
    extract_sources,
    get_organization_merged_id_by_query,
)
from mex.seq_repo.filter import filter_sources_on_latest_sequencing_date
from mex.seq_repo.model import SeqRepoSource
from mex.seq_repo.settings import SeqRepoSettings
from mex.seq_repo.transform import (
    transform_seq_repo_access_platform_to_extracted_access_platform,
    transform_seq_repo_activities_to_extracted_activities,
    transform_seq_repo_distribution_to_extracted_distribution,
    transform_seq_repo_resource_to_extracted_resource,
)
from mex.sinks import load


@asset(group_name="seq_repo", deps=["extracted_primary_source_mex"])
def extracted_primary_source_seq_repo(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return Seq-Repo primary source."""
    (extracted_primary_source,) = get_primary_sources_by_name(
        extracted_primary_sources, "seq-repo"
    )
    load([extracted_primary_source])

    return extracted_primary_source


@asset(group_name="seq_repo")
def seq_repo_source() -> list[SeqRepoSource]:
    """Extract sources from Seq-Repo."""
    return list(extract_sources())


@asset(group_name="seq_repo")
def seq_repo_latest_source(
    seq_repo_source: list[SeqRepoSource],
) -> dict[str, SeqRepoSource]:
    """Filter latest sources from Seq-Repo source."""
    return filter_sources_on_latest_sequencing_date(seq_repo_source)


@asset(group_name="seq_repo")
def seq_repo_source_resolved_project_coordinators(
    seq_repo_latest_source: dict[str, SeqRepoSource],
) -> list[LDAPPersonWithQuery]:
    """Extract source project coordinators."""
    return list(extract_source_project_coordinator(seq_repo_latest_source))


@asset(group_name="seq_repo")
def project_coordinators_merged_ids_by_query_string(
    seq_repo_source_resolved_project_coordinators: list[LDAPPersonWithQuery],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
) -> dict[str, list[MergedPersonIdentifier]]:
    """Get project coordinators merged ids."""
    extracted_persons = list(
        transform_ldap_persons_with_query_to_mex_persons(
            seq_repo_source_resolved_project_coordinators,
            extracted_primary_source_ldap,
            extracted_organizational_units,
        )
    )
    load(extracted_persons)
    return {
        str(query_string): [MergedPersonIdentifier(id_) for id_ in merged_ids]
        for query_string, merged_ids in get_merged_ids_by_query_string(
            seq_repo_source_resolved_project_coordinators, extracted_primary_source_ldap
        ).items()
    }


@asset(group_name="seq_repo")
def extracted_activity(
    seq_repo_latest_source: dict[str, SeqRepoSource],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_source_resolved_project_coordinators: list[LDAPPersonWithQuery],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    project_coordinators_merged_ids_by_query_string: dict[
        str, list[MergedPersonIdentifier]
    ],
) -> dict[str, ExtractedActivity]:
    """Extract activities from Seq-Repo."""
    settings = SeqRepoSettings.get()
    activity = extract_mapping_data(
        settings.mapping_path / "activity.yaml", ExtractedActivity
    )

    mex_activities = transform_seq_repo_activities_to_extracted_activities(
        seq_repo_latest_source,
        activity,
        seq_repo_source_resolved_project_coordinators,
        unit_stable_target_ids_by_synonym,
        project_coordinators_merged_ids_by_query_string,
        extracted_primary_source_seq_repo,
    )
    mex_activities_gens = tee(mex_activities, 2)
    load(mex_activities_gens[0])
    return {
        activity.identifierInPrimarySource: activity
        for activity in mex_activities_gens[1]
    }


@asset(group_name="seq_repo")
def extracted_access_platform(
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
) -> ExtractedAccessPlatform:
    """Extract access platform from Seq-Repo."""
    settings = SeqRepoSettings.get()
    access_platform = extract_mapping_data(
        settings.mapping_path / "access-platform.yaml",
        ExtractedAccessPlatform,
    )
    mex_access_platform = (
        transform_seq_repo_access_platform_to_extracted_access_platform(
            access_platform,
            unit_stable_target_ids_by_synonym,
            extracted_primary_source_seq_repo,
        )
    )
    load([mex_access_platform])

    return mex_access_platform


@asset(group_name="seq_repo")
def extracted_distribution(
    seq_repo_latest_source: dict[str, SeqRepoSource],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    extracted_access_platform: ExtractedAccessPlatform,
    seq_repo_organization_ids_by_query_string: dict[str, MergedOrganizationIdentifier],
) -> dict[str, ExtractedDistribution]:
    """Extract distribution from Seq-Repo."""
    settings = SeqRepoSettings.get()
    distribution = extract_mapping_data(
        settings.mapping_path / "distribution.yaml",
        ExtractedDistribution,
    )
    mex_distributions = transform_seq_repo_distribution_to_extracted_distribution(
        seq_repo_latest_source,
        distribution,
        extracted_access_platform,
        seq_repo_organization_ids_by_query_string,
        extracted_primary_source_seq_repo,
    )

    mex_distributions_gens = tee(mex_distributions, 2)
    load(mex_distributions_gens[0])
    return {
        distribution.identifierInPrimarySource: distribution
        for distribution in mex_distributions_gens[1]
    }


@asset(group_name="seq_repo")
def seq_repo_organization_ids_by_query_string(
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> dict[str, MergedOrganizationIdentifier]:
    """Extract organizations for Seq-Repo from wikidata and group them by query."""
    wikidata_organizations_by_query = extract_seq_repo_organizations()
    mex_extracted_organizations = (
        transform_wikidata_organizations_to_extracted_organizations(
            wikidata_organizations_by_query.values(), extracted_primary_source_wikidata
        )
    )
    load(mex_extracted_organizations)
    return get_organization_merged_id_by_query(
        wikidata_organizations_by_query, extracted_primary_source_wikidata
    )


@asset(group_name="seq_repo")
def seq_repo_resource(
    seq_repo_latest_source: dict[str, SeqRepoSource],
    extracted_distribution: dict[str, ExtractedDistribution],
    extracted_activity: dict[str, ExtractedActivity],
    seq_repo_source_resolved_project_coordinators: list[LDAPPersonWithQuery],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    project_coordinators_merged_ids_by_query_string: dict[
        str, list[MergedPersonIdentifier]
    ],
    seq_repo_organization_ids_by_query_string: dict[str, MergedOrganizationIdentifier],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
) -> list[ExtractedResource]:
    """Extract resource from Seq-Repo."""
    settings = SeqRepoSettings.get()
    resource = extract_mapping_data(
        settings.mapping_path / "resource.yaml",
        ExtractedResource,
    )

    mex_resources = transform_seq_repo_resource_to_extracted_resource(
        seq_repo_latest_source,
        extracted_distribution,
        extracted_activity,
        resource,
        seq_repo_source_resolved_project_coordinators,
        unit_stable_target_ids_by_synonym,
        project_coordinators_merged_ids_by_query_string,
        extracted_primary_source_seq_repo,
    )

    mex_sources_list = list(mex_resources)
    load(mex_sources_list)

    return list(mex_sources_list)


@entrypoint(SeqRepoSettings)
def run() -> None:
    """Run the seq-repo extractor job in-process."""
    run_job_in_process("seq_repo")
