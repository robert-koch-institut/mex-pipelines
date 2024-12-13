from collections.abc import Generator

from mex.common.logging import watch
from mex.extractors.open_data.connector import OpenDataConnector
from mex.extractors.open_data.models.source import (
    ZenodoParentRecordSource,
    ZenodoRecordVersion,
)


@watch
def extract_parent_records() -> Generator[ZenodoParentRecordSource, None, None]:
    """Load Open Data sources by querying the Zenodo API.

    Get all records of  Zenodo community 'robertkochinstitut'.
    These are called 'parent records'.

    Returns:
        Generator for Zenodo sources
    """
    connector = OpenDataConnector()

    yield from connector.get_parent_sources()


@watch
def extract_record_versions() -> Generator[ZenodoRecordVersion, None, None]:
    """Fetch all the versions of a parent resource.

    Returns:
        Generator for ZenodoRecordVersion items
    """
    connector = OpenDataConnector()

    for parent_source in extract_parent_records():
        if parent_source.id:
            yield from connector.get_record_versions(parent_source.id)


def extract_totals() -> dict[int | None, int]:
    """Fetch all the versions of a parent resource.

    Returns:
        Generator for ZenodoRecordVersion items
    """
    connector = OpenDataConnector()

    totals_dict = {}

    for parent_source in extract_parent_records():
        totals_dict[parent_source.id] = connector.get_totals(parent_source.id)

    return totals_dict
