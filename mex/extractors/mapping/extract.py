from os import PathLike
from typing import Any, cast

import yaml


def extract_mapping_data(path: PathLike[str]) -> dict[str, Any]:
    """Return a nested dictionary with default values.

    Args:
        path: path to mapping json

    Returns:
        mapping model with default value data from specified path
    """
    with open(path, encoding="utf-8") as f:
        return cast(dict[str, Any], yaml.safe_load(f))
