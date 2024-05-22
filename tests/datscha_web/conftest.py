from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.datscha_web.settings import DatschaWebSettings


@pytest.fixture(autouse=True)
def settings() -> DatschaWebSettings:
    """Load the settings for this pytest session."""
    return DatschaWebSettings.get()


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
                    givenName="Rüdiger",
                    displayName="Resolved, Rüdiger",
                    objectGUID=UUID(int=1, version=4),
                    department="PARENT-UNIT",
                )
            ]
        ),
    )
