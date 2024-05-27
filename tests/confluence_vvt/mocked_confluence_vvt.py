from unittest.mock import MagicMock, Mock

import pytest
import requests
from pytest import MonkeyPatch
from requests import Response

from mex.confluence_vvt.connector import ConfluenceVvtConnector


@pytest.fixture
def mocked_confluence_vvt(monkeypatch: MonkeyPatch) -> None:
    """Mock the Confluence-vvt connector to return empty data."""
    response = Mock(spec=Response, status_code=200)
    response.json.return_value = {"results": []}
    session = MagicMock(spec=requests.Session)
    session.get = MagicMock(side_effect=[response])

    monkeypatch.setattr(
        ConfluenceVvtConnector,
        "__init__",
        lambda self: setattr(self, "session", session),
    )
