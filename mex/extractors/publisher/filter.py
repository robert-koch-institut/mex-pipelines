from collections.abc import Generator, Iterable

from mex.common.models import MergedItem
from mex.extractors.logging import log_processed_merged_items
from mex.extractors.settings import Settings


def filter_merged_items(
    items: Iterable[MergedItem],
) -> Generator[MergedItem, None, None]:
    """Filter to be published items by allow list."""
    settings = Settings.get()

    skipped_items = 0
    total_items = 0

    for item in items:
        if item.entityType in settings.skip_merged_items:
            logging_counter += 1
            total_counter += 1
        if item.entityType not in settings.skip_merged_items:
            total_counter += 1
            yield item

    log_processed_merged_items("filtered out", logging_counter, total_counter)
