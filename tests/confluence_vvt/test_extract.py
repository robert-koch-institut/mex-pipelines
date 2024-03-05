import json
import re
from itertools import islice
from typing import Any
from unittest.mock import MagicMock, Mock

import pytest
import requests
from pytest import MonkeyPatch
from requests.models import Response

from mex.confluence_vvt.connector import ConfluenceVvtConnector
from mex.confluence_vvt.extract import fetch_all_data_page_ids, fetch_all_pages_data
from tests.confluence_vvt.conftest import TEST_DATA_DIR


@pytest.mark.integration
def test_fetch_all_data_page_ids() -> None:
    page_ids = list(fetch_all_data_page_ids())
    assert all(re.match(r"\d+", id_) for id_ in page_ids)


@pytest.mark.integration
def test_fetch_all_pages_data() -> None:
    page_ids = list(islice(fetch_all_data_page_ids(), 5))

    response = list(fetch_all_pages_data(page_ids))

    assert len(page_ids) == len(response)
    assert response[0].identifier == page_ids[0]


def test_fetch_all_data_page_ids_mocked(
    monkeypatch: MonkeyPatch,
) -> None:
    # first response with mocked test data
    response1 = Mock(spec=Response, status_code=200)
    with open(TEST_DATA_DIR / "fetch_all_data_page_ids.json") as f:
        response1.json.return_value = json.load(f)

    # second response with empty data
    response2 = Mock(spec=Response, status_code=200)
    response2.json.return_value = {"results": []}

    # mocking connector session
    session = MagicMock(spec=requests.Session)
    session.get = MagicMock(side_effect=[response1, response2])

    monkeypatch.setattr(
        ConfluenceVvtConnector,
        "__init__",
        lambda self: setattr(self, "session", session),
    )

    page_ids = list(fetch_all_data_page_ids())

    expected = ["0101010101", "0202020202", "0303030303", "0404040404"]

    assert page_ids == expected


@pytest.mark.usefixtures("mocked_confluence_vvt_detailed_page_data")
def test_fetch_all_pages_data_mocked(
    monkeypatch: MonkeyPatch, detail_page_data_json: dict[str, Any]
) -> None:
    expected = {
        "abstract": "test description, test test test, test zwecke des vorhabens",
        "contact": ["Test Verantwortliche 1"],
        "identifier": "123456",
        "identifier_in_primary_source": ["001-002"],
        "involved_person": [
            "Test Verantwortliche 1",
            "test ggfs vertreter",
            "Test mitarbeitende 1",
        ],
        "involved_unit": ["Test OE 1", "FG99", "test OE 1"],
        "responsible_unit": ["Test OE 1"],
        "theme": "https://mex.rki.de/item/theme-1",
        "title": "Test Title",
    }

    response = Mock(spec=Response, status_code=200)
    response.json.return_value = detail_page_data_json

    # mocking create_session function
    session = MagicMock(spec=requests.Session)
    session.get = MagicMock(side_effect=[response])

    monkeypatch.setattr(
        ConfluenceVvtConnector,
        "__init__",
        lambda self: setattr(self, "session", session),
    )
    all_pages_data = list(fetch_all_pages_data([str(expected["identifier"])]))

    assert len(all_pages_data) == 1
    assert all_pages_data[0].model_dump(exclude_none=True) == expected
