from unittest.mock import MagicMock

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector


@pytest.fixture
def mocked_ldap(monkeypatch: MonkeyPatch) -> None:
    """Mock the ldap connector to return empty results."""
    monkeypatch.setattr(
        LDAPConnector,
        "__init__",
        lambda self: setattr(self, "_connection", MagicMock()),
    )
    monkeypatch.setattr(LDAPConnector, "get_persons", lambda *_, **__: iter([]))
