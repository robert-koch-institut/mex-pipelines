import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import requests
from pytest import MonkeyPatch

from mex.extractors.drop import DropApiConnector


@pytest.fixture
def mocked_drop(monkeypatch: MonkeyPatch) -> None:
    """Mock the drop api connector to return dummy data."""
    monkeypatch.setattr(
        DropApiConnector,
        "__init__",
        lambda self: setattr(self, "session", MagicMock(spec=requests.Session)),
    )
    monkeypatch.setattr(
        DropApiConnector,
        "list_files",
        lambda _, x_system: [
            path.stem
            for path in (
                Path(__file__).parents[2]
                / "tests"
                / x_system.replace("-", "_")
                / "test_data"
            ).rglob("*.json")
        ],
    )

    def get_file_mocked(
        _self: DropApiConnector, x_system: str, file_id: str
    ) -> dict[str, Any]:
        with open(
            (
                Path(__file__).parents[2]
                / "tests"
                / x_system.replace("-", "_")
                / "test_data"
                / file_id
            ).with_suffix(".json")
        ) as handle:
            return json.load(handle)

    monkeypatch.setattr(
        DropApiConnector,
        "get_file",
        get_file_mocked,
    )
