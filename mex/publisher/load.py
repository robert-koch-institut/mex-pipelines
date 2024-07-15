import json
from collections.abc import Iterable
from typing import Any

from mex.common.settings import BaseSettings
from mex.common.transform import MExEncoder


def write_merged_items(items: Iterable[dict[str, Any]]) -> None:
    """Write the incoming items into a new-line delimited JSON file."""
    settings = BaseSettings.get()
    ndjson_path = settings.work_dir / "publisher.ndjson"

    with open(ndjson_path, "w", encoding="utf-8") as file:
        for item in items:
            file.write(json.dumps(item, cls=MExEncoder) + "\n")
