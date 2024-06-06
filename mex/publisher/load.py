import json
from pathlib import Path
from typing import Any

from mex.common.transform import MExEncoder


def write_merged_items(ndjson_path: Path, items_list: list[dict[Any, Any]]) -> None:
    """Write the incoming items into a new-line delimited JSON file."""
    with open(ndjson_path, "a+", encoding="utf-8") as file:
        for item in items_list:
            file.write(json.dumps(item, cls=MExEncoder) + "\n")
