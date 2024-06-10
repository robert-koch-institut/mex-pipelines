from pathlib import Path
from typing import Any

from mex.common.cli import entrypoint
from mex.common.models import (
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.mapping.extract import extract_mapping_data
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load
from mex.voxco.extract import extract_voxco_variables
from mex.voxco.model import VoxcoVariable
from mex.voxco.settings import VoxcoSettings


@asset(group_name="voxco", deps=["extracted_primary_source_mex"])
def extracted_primary_source_voxco(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return voxco primary source."""
    (extracted_primary_source,) = get_primary_sources_by_name(
        extracted_primary_sources, "voxco"
    )
    load([extracted_primary_source])

    return extracted_primary_source


@asset(group_name="voxco")
def voxco_sources() -> dict[str, list[VoxcoVariable]]:
    """Extract voxco variables by json file names."""
    return extract_voxco_variables()


@asset(group_name="voxco")
def voxco_resource_mappings() -> list[dict[str, Any]]:
    """Extract voxco resource mappings."""
    settings = VoxcoSettings.get()
    return [
        extract_mapping_data(file, ExtractedResource)
        for file in Path(settings.mapping_path).glob("resource_*.yaml")
    ]


@entrypoint(VoxcoSettings)
def run() -> None:
    """Run the voxco extractor job in-process."""
    run_job_in_process("voxco")
