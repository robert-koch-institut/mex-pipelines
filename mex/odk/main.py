from pathlib import Path
from typing import Any

from mex.common.cli import entrypoint
from mex.common.models import (
    ExtractedPrimarySource,
    ExtractedResource,
    ExtractedVariableGroup,
)
from mex.common.primary_source.transform import get_primary_sources_by_name
from mex.common.types import OrganizationalUnitID, OrganizationID
from mex.mapping.extract import extract_mapping_data
from mex.odk.extract import extract_odk_raw_data
from mex.odk.model import ODKData
from mex.odk.settings import ODKSettings
from mex.odk.transform import (
    get_external_partner_and_publisher_by_label,
    get_variable_groups_from_raw_data,
    transform_odk_data_to_extracted_variables,
    transform_odk_resources_to_mex_resources,
    transform_odk_variable_groups_to_extracted_variable_groups,
)
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load


@asset(group_name="odk", deps=["extracted_primary_source_mex"])
def extracted_primary_source_odk(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return odk primary source and load them to sinks."""
    (extracted_primary_source_odk,) = get_primary_sources_by_name(
        extracted_primary_sources, "odk"
    )
    load([extracted_primary_source_odk])
    return extracted_primary_source_odk


@asset(group_name="odk")
def odk_raw_data() -> list[ODKData]:
    """Extract odk raw data."""
    return extract_odk_raw_data()


@asset(group_name="odk")
def odk_resource_mappings() -> list[dict[str, Any]]:
    """Extract odk resource mappings."""
    settings = ODKSettings.get()
    return [
        extract_mapping_data(file, ExtractedResource)
        for file in Path(settings.mapping_path).glob("resource_*.yaml")
    ]


@asset(group_name="odk")
def external_partner_and_publisher_by_label(
    odk_resource_mappings: list[dict[str, Any]],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> dict[str, OrganizationID]:
    """Extract wikidata for external partner and publisher, load to sinks and return."""
    return get_external_partner_and_publisher_by_label(
        odk_resource_mappings, extracted_primary_source_wikidata
    )


@asset(group_name="odk")
def extracted_resources_odk(
    odk_resource_mappings: list[dict[str, Any]],
    unit_stable_target_ids_by_synonym: dict[str, OrganizationalUnitID],
    extracted_primary_source_international_projects: ExtractedPrimarySource,
    external_partner_and_publisher_by_label: dict[str, OrganizationID],
    extracted_primary_source_mex: ExtractedPrimarySource,
) -> list[ExtractedResource]:
    """Transform odk resources to mex resource, load to sinks and return."""
    extracted_resources_odk = transform_odk_resources_to_mex_resources(
        odk_resource_mappings,
        unit_stable_target_ids_by_synonym,
        extracted_primary_source_international_projects,
        external_partner_and_publisher_by_label,
        extracted_primary_source_mex,
    )
    load(extracted_resources_odk)
    return extracted_resources_odk


@asset(group_name="odk")
def odk_variable_groups(
    odk_raw_data: list[ODKData],
) -> dict[str, list[dict[str, str]]]:
    """Transform odk raw data to odk variable groups and return."""
    return get_variable_groups_from_raw_data(odk_raw_data)


@asset(group_name="odk")
def extracted_variable_groups_odk(
    extracted_resources_odk: list[ExtractedResource],
    odk_variable_groups: dict[str, list[dict[str, str]]],
    extracted_primary_source_odk: ExtractedPrimarySource,
) -> list[ExtractedVariableGroup]:
    """Transform odk variable groups to mex variable groups, load to sinks, return."""
    extracted_variable_groups = (
        transform_odk_variable_groups_to_extracted_variable_groups(
            odk_variable_groups, extracted_resources_odk, extracted_primary_source_odk
        )
    )

    load(extracted_variable_groups)
    return extracted_variable_groups


@asset(group_name="odk")
def extracted_variable_odk(
    extracted_resources_odk: list[ExtractedResource],
    extracted_variable_groups_odk: list[ExtractedVariableGroup],
    odk_variable_groups: dict[str, list[dict[str, str]]],
    odk_raw_data: list[ODKData],
    extracted_primary_source_odk: ExtractedPrimarySource,
) -> None:
    """Transform odk data to mex variables and load to sinks."""
    extracted_variables = transform_odk_data_to_extracted_variables(
        extracted_resources_odk,
        extracted_variable_groups_odk,
        odk_variable_groups,
        odk_raw_data,
        extracted_primary_source_odk,
    )

    load(extracted_variables)


@entrypoint(ODKSettings)
def run() -> None:
    """Run the odk extractor job in-process."""
    run_job_in_process("odk")
