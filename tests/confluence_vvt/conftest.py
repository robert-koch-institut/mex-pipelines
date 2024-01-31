import json
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock, Mock
from uuid import UUID

import pytest
import requests
from pytest import MonkeyPatch
from requests.models import Response

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPrimarySource
from mex.common.organigram.extract import (
    extract_organigram_units,
    get_unit_merged_ids_by_synonyms,
)
from mex.common.organigram.transform import (
    transform_organigram_units_to_organizational_units,
)
from mex.common.types import OrganizationalUnitID
from mex.confluence_vvt.connector import ConfluenceVvtConnector
from mex.confluence_vvt.settings import ConfluenceVvtSettings

TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture(autouse=True)
def settings() -> ConfluenceVvtSettings:
    """Load the settings for this pytest session."""
    return ConfluenceVvtSettings.get()


@pytest.fixture
def unit_merged_ids_by_synonym(
    extracted_primary_sources: dict[str, ExtractedPrimarySource]
) -> dict[str, OrganizationalUnitID]:
    """Return unit merged ids by synonym for organigram units."""
    organigram_units = extract_organigram_units()
    mex_organizational_units = transform_organigram_units_to_organizational_units(
        organigram_units, extracted_primary_sources["organigram"]
    )
    return get_unit_merged_ids_by_synonyms(mex_organizational_units)


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


@pytest.fixture
def detail_page_data_html() -> str:
    """Return dummy detail page HTML."""
    with open(TEST_DATA_DIR / "detail_page_data.html", "r", encoding="utf-8") as fh:
        return fh.read()


@pytest.fixture
def detail_page_data_json(detail_page_data_html: str) -> dict[str, Any]:
    """Return dummy detail page JSON."""
    with open(TEST_DATA_DIR / "detail_page_data.json", "r", encoding="utf-8") as fh:
        detail_page = json.load(fh)
    detail_page["body"]["view"]["value"] = detail_page_data_html
    return cast(dict[str, Any], detail_page)


@pytest.fixture
def mocked_confluence_vvt_detailed_page_data(
    monkeypatch: MonkeyPatch, detail_page_data_json: dict[str, Any]
) -> None:
    """Mock the Confluence-vvt connector to return dummy data of the details page."""
    response = Mock(spec=Response, status_code=200)
    response.json.return_value = detail_page_data_json

    session = MagicMock(spec=requests.Session)
    session.get = MagicMock(side_effect=[response])

    monkeypatch.setattr(
        ConfluenceVvtConnector,
        "__init__",
        lambda self, _: setattr(self, "session", session),
    )


@pytest.fixture
def mocked_ldap(monkeypatch: MonkeyPatch) -> None:
    """Mock the LDAP connector to return resolved persons and units."""
    monkeypatch.setattr(
        LDAPConnector,
        "__init__",
        lambda self: setattr(self, "_connection", MagicMock()),
    )
    monkeypatch.setattr(
        LDAPConnector,
        "get_persons",
        lambda *_, **__: iter(
            [
                LDAPPerson(
                    employeeID="42",
                    sn="Resolved",
                    givenName="Renate",
                    displayName="Resolved, Renate",
                    objectGUID=UUID(int=1, version=4),
                )
            ]
        ),
    )
