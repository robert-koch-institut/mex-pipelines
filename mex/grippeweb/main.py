from pathlib import Path
from typing import Any

from mex.common.cli import entrypoint
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedPrimarySource,
    ExtractedResource,
    ExtractedVariableGroup,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.grippeweb.extract import (
    extract_columns_by_table_and_column_name,
)
from mex.grippeweb.settings import GrippewebSettings
from mex.mapping.extract import extract_mapping_data
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load


@asset(group_name="grippeweb", deps=["extracted_primary_source_mex"])
def extracted_primary_sources_grippeweb(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return grippeweb primary source."""
    (extracted_primary_sources_grippeweb,) = get_primary_sources_by_name(
        extracted_primary_sources, "grippeweb"
    )
    load([extracted_primary_sources_grippeweb])

    return extracted_primary_sources_grippeweb


@asset(group_name="grippeweb")
def grippeweb_columns() -> dict[str, dict[str, list[Any]]]:
    """Extract grippe web columns."""
    return extract_columns_by_table_and_column_name()


@asset(group_name="grippeweb")
def access_platform() -> dict[str, Any]:
    """Extract `access_platform` default values."""
    settings = GrippewebSettings.get()
    return extract_mapping_data(
        settings.mapping_path / "access-platform.yaml", ExtractedAccessPlatform
    )


@asset(group_name="grippeweb")
def grippeweb_resource_mappings() -> list[dict[str, Any]]:
    """Extract grippeweb resource mappings."""
    settings = GrippewebSettings.get()
    return [
        extract_mapping_data(file, ExtractedResource)
        for file in Path(settings.mapping_path).glob("resource_*.yaml")
    ]


@asset(group_name="grippeweb")
def variable_group() -> dict[str, Any]:
    """Extract `variable_group` default values."""
    settings = GrippewebSettings.get()
    return extract_mapping_data(
        settings.mapping_path / "variable-group.yaml", ExtractedVariableGroup
    )


@entrypoint(GrippewebSettings)
def run() -> None:
    """Run the IFSG extractor job in-process."""
    run_job_in_process("grippeweb")
