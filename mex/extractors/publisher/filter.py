from collections.abc import Generator, Iterable

from mex.common.models import MergedItem
from mex.extractors.settings import Settings


def filter_merged_items(
    items: Iterable[MergedItem],
) -> Generator[MergedItem, None, None]:
    """Filter to be published items by allow list."""
    settings = Settings.get()

    for item in items:
        if item.entityType not in settings.skip_merged_items:
            yield item
