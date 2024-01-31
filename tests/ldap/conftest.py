from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector
from mex.common.public_api.connector import PublicApiConnector
from mex.common.public_api.models import PublicApiMetadataItemsResponse


@pytest.fixture
def mocked_ldap(monkeypatch: MonkeyPatch) -> None:
    """Mock the ldap connector to return empty results."""
    monkeypatch.setattr(
        LDAPConnector,
        "__init__",
        lambda self: setattr(self, "_connection", MagicMock()),
    )
    monkeypatch.setattr(LDAPConnector, "get_persons", lambda *_, **__: iter([]))


@pytest.fixture
def mocked_public_api(monkeypatch: MonkeyPatch) -> None:
    """Mock the public API connector to return empty results."""
    monkeypatch.setattr(
        PublicApiConnector,
        "__init__",
        lambda self: setattr(self, "session", MagicMock()),
    )
    monkeypatch.setattr(
        PublicApiConnector,
        "get_all_items",
        lambda self, **_: PublicApiMetadataItemsResponse(items=[], next=""),
    )
