from pathlib import Path
from typing import Any

from mex.common.cli import entrypoint
from mex.common.models import (
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.primary_source.transform import get_primary_sources_by_name
from mex.mapping.extract import extract_mapping_data
from mex.odk.extract import extract_odk_raw_data
from mex.odk.model import ODKData
from mex.odk.settings import ODKSettings
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


@entrypoint(ODKSettings)
def run() -> None:
    """Run the odk extractor job in-process."""
    run_job_in_process("odk")
