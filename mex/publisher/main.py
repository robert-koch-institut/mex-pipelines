from pathlib import Path

from mex.common.backend_api.connector import BackendApiConnector
from mex.common.cli import entrypoint
from mex.common.settings import BaseSettings
from mex.pipeline import asset, run_job_in_process
from mex.settings import Settings


def write_mergeditems_ndjson(
    ndjson_path: Path, items_list: list[dict[str, str]]  # how to write "any"?
) -> None:
    """Write the incoming items into a new-line delimited JSON file."""
    file = open(ndjson_path, "a+", encoding="utf-8")

    try:
        for item in items_list:
            file.write(str(item) + "\n")
    finally:
        file.close()


@asset(group_name="publisher")
def publish_merged_items() -> None:
    """Get all merged items from mex-backend and write to ndjson file."""
    settings = BaseSettings.get()
    file_name = Path(settings.work_dir, "publisher.ndjson")

    open(file_name, "w").close()  # empty the file

    connector = BackendApiConnector.get()

    response = connector.request(
        method="GET", endpoint="merged-item", params={"limit": "1"}
    )
    total_item_number = response["total"]  # better way to get total item no?

    item_number_limit = 100  # max limit
    item_counter = 0

    while item_counter <= total_item_number:
        response = connector.request(
            method="GET",
            endpoint="merged-item",
            params={"limit": str(item_number_limit), "skip": str(item_counter)},
        )
        item_counter += item_number_limit
        write_mergeditems_ndjson(file_name, response["items"])


@entrypoint(Settings)
def run() -> None:
    """Run the publisher job in-process."""
    run_job_in_process("publisher")
