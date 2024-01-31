from typing import Generator

from mex.blueant.models.source import BlueAntSource
from mex.blueant.settings import BlueAntSettings
from mex.common.logging import watch
from mex.common.types import Identifier
from mex.common.utils import contains_any
from mex.logging import log_filter


@watch
def filter_and_log_blueant_sources(
    sources: Generator[BlueAntSource, None, None], primary_source_id: Identifier
) -> Generator[BlueAntSource, None, None]:
    """Filter Blueant sources and log filtered sources.

    Args:
        sources: BlueantSources Generator
        primary_source_id: Identifier of primary source

    Returns:
        Generator for Blue Ant sources
    """
    for source in sources:
        if filter_and_log_blueant_source(source, primary_source_id):
            yield source


def filter_and_log_blueant_source(
    source: BlueAntSource, primary_source_id: Identifier
) -> bool:
    """Filter a BlueantSource according to settings and log filtering.

    Args:
        source: BlueantSource
        primary_source_id: Identifier of primary source

    Settings:
        skip_labels: Skip source if these terms are in the label
        skip_years: Skip sources starting or ending in these years
        skip_units: Skip sources with these responsible departments

    Returns:
        False if source is filtered out, else True
    """
    settings = BlueAntSettings.get()
    identifier_in_primary_source = source.number
    if contains_any(source.name, settings.skip_labels):
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"Name [{source.name}] in settings.skip_labels",
        )
        return False
    return True
