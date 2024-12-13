from mex.extractors.open_data.extract import (
    extract_parent_records,
    extract_record_versions,
)
from mex.extractors.open_data.models.source import (
    ZenodoParentRecordSource,
    ZenodoRecordVersion,
)
from mex.extractors.pipeline import asset


@asset(group_name="opendata")
def zenodo_parent_records() -> list[ZenodoParentRecordSource]:
    """Extract parent sources from Zenodo."""
    return list(extract_parent_records())


@asset(group_name="opendata")
def zenodo_record_versions() -> list[ZenodoRecordVersion]:
    """Extract parent sources from Zenodo."""
    return list(extract_record_versions())
