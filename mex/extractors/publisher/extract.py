from collections.abc import Generator

from mex.common.backend_api.connector import BackendApiConnector
from mex.common.models import MergedItem


def get_merged_items() -> Generator[MergedItem, None, None]:
    """Read merged items from backend."""
    connector = BackendApiConnector.get()

    response = connector.fetch_merged_items(None, None, 0, 1)
    total_item_number = response.total

    item_number_limit = 100  # 100 is the maximum possible number per get-request

    for item_counter in range(0, total_item_number + 1, item_number_limit):
        response = connector.fetch_merged_items(
            query_string=None,
            entity_type=None,
            skip=item_counter,
            limit=item_number_limit,
        )

        yield from response.items
