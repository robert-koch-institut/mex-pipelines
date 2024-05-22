from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch

from mex.datscha_web.connector import DatschaWebConnector
from mex.datscha_web.models.item import DatschaWebItem


@pytest.fixture
def mocked_datscha_web(
    monkeypatch: MonkeyPatch,
    datscha_web_item: DatschaWebItem,
    datscha_web_item_without_contributors: DatschaWebItem,
) -> None:
    """Mock the datscha web connector to return dummy data."""
    mock_items = {
        "fake://17": datscha_web_item,
        "fake://92": datscha_web_item_without_contributors,
    }
    monkeypatch.setattr(
        DatschaWebConnector,
        "__init__",
        lambda self: setattr(self, "session", MagicMock()),
    )
    monkeypatch.setattr(
        DatschaWebConnector, "get_item_urls", lambda _: iter(mock_items)
    )
    monkeypatch.setattr(DatschaWebConnector, "get_item", lambda _, n: mock_items[n])
