from collections.abc import Generator
from typing import Any

from mex.common.backend_api.connector import BackendApiConnector


def get_merged_items() -> Generator[dict[str, Any], None, None]:
    """Read merged items from backend."""
    connector = BackendApiConnector.get()

    response = connector.request(
        method="GET", endpoint="merged-item", params={"limit": "1"}
    )
    total_item_number = response["total"]

    item_number_limit = 100  # 100 is the maximum possible number per get-request

    for item_counter in range(0, total_item_number + 1, item_number_limit):
        response = connector.request(
            method="GET",
            endpoint="merged-item",
            params={"limit": str(item_number_limit), "skip": str(item_counter)},
        )

        yield from response["items"]
