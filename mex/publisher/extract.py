from pathlib import Path
from typing import Any

from mex.common.backend_api.connector import BackendApiConnector


def get_and_write_merged_items(ndjson_path: Path) -> None:
    """Read merged items form backend and call ndjson-writer function."""
    connector = BackendApiConnector.get()

    response = connector.request(
        method="GET", endpoint="merged-item", params={"limit": "1"}
    )
    total_item_number = response["total"]

    item_number_limit = 100  # max limit
    item_counter = 0

    while item_counter <= total_item_number:
        response = connector.request(
            method="GET",
            endpoint="merged-item",
            params={"limit": str(item_number_limit), "skip": str(item_counter)},
        )
        write_mergeditems_ndjson(ndjson_path, response["items"])
        item_counter += item_number_limit


def write_mergeditems_ndjson(
    ndjson_path: Path, items_list: list[dict[Any, Any]]
) -> None:
    """Write the incoming items into a new-line delimited JSON file."""
    with open(ndjson_path, "a+", encoding="utf-8") as file:
        for item in items_list:
            file.write(str(item) + "\n")
