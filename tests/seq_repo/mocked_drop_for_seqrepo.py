import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest
import requests
from _pytest.monkeypatch import MonkeyPatch

from mex.drop import DropApiConnector


@pytest.fixture
def mocked_drop_for_seqrepo(monkeypatch: MonkeyPatch) -> None:
    """Mock the drop api connector to return dummy data."""
    monkeypatch.setattr(
        DropApiConnector,
        "__init__",
        lambda self: setattr(self, "session", MagicMock(spec=requests.Session)),
    )
    monkeypatch.setattr(
        DropApiConnector,
        "list_files",
        lambda *_, **__: ["one"],
    )

    def get_file_mocked(*_, **__):
        with open(Path(__file__).parent / "test_data" / "default.json") as handle:
            return json.load(handle)

    monkeypatch.setattr(
        DropApiConnector,
        "get_file",
        get_file_mocked,
    )
