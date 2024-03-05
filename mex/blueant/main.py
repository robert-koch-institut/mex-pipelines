from mex.blueant.extract import extract_blueant_project_leaders, extract_blueant_sources
from mex.blueant.filter import filter_and_log_blueant_sources
from mex.blueant.models.source import BlueAntSource
from mex.blueant.settings import BlueAntSettings
from mex.blueant.transform import transform_blueant_sources_to_extracted_activities
from mex.common.cli import entrypoint
from mex.common.ldap.extract import get_merged_ids_by_employee_ids
from mex.common.ldap.transform import transform_ldap_persons_to_mex_persons
from mex.common.models import ExtractedOrganizationalUnit, ExtractedPrimarySource
from mex.common.primary_source.transform import get_primary_sources_by_name
from mex.common.types import MergedOrganizationalUnitIdentifier, MergedPersonIdentifier
from mex.filters import filter_by_global_rules
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load


@asset(group_name="blueant", deps=["extracted_primary_source_mex"])
def extracted_primary_source_blueant(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return blueant primary source."""
    (extracted_primary_source,) = get_primary_sources_by_name(
        extracted_primary_sources, "blueant"
    )
    load([extracted_primary_source])
    return extracted_primary_source


@asset(group_name="blueant")
def blueant_sources(
    extracted_primary_source_blueant: ExtractedPrimarySource,
) -> list[BlueAntSource]:
    """Extract from blueant sources and filter content."""
    sources = extract_blueant_sources()
    sources = filter_and_log_blueant_sources(
        sources, extracted_primary_source_blueant.stableTargetId
    )
    sources = filter_by_global_rules(
        extracted_primary_source_blueant.stableTargetId, sources
    )
    return list(sources)


@asset(group_name="blueant")
def blueant_project_leaders_by_employee_id(
    blueant_sources: list[BlueAntSource],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
) -> dict[str, list[MergedPersonIdentifier]]:
    """Transform LDAP persons to mex-persons with stable target ID and group them by employee ID."""  # noqa: E501
    ldap_project_leaders = list(extract_blueant_project_leaders(blueant_sources))
    mex_project_leaders = transform_ldap_persons_to_mex_persons(
        ldap_project_leaders,
        extracted_primary_source_ldap,
        extracted_organizational_units,
    )
    load(mex_project_leaders)
    return get_merged_ids_by_employee_ids(
        ldap_project_leaders, extracted_primary_source_ldap
    )


@asset(group_name="blueant")
def extracted_blueant_activities(
    blueant_sources: list[BlueAntSource],
    extracted_primary_source_blueant: ExtractedPrimarySource,
    blueant_project_leaders_by_employee_id: dict[str, list[MergedPersonIdentifier]],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
) -> None:
    """Transform blueant sources to extracted activities and load them to the sinks."""
    extracted_activities = transform_blueant_sources_to_extracted_activities(
        blueant_sources,
        extracted_primary_source_blueant,
        blueant_project_leaders_by_employee_id,
        unit_stable_target_ids_by_synonym,
    )
    load(extracted_activities)


@entrypoint(BlueAntSettings)
def run() -> None:
    """Run the blueant extractor job in-process."""
    run_job_in_process("blueant")
