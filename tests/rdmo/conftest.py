from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPerson
from mex.common.types import Identifier
from mex.rdmo.settings import RDMOSettings


@pytest.fixture(autouse=True)
def settings() -> RDMOSettings:
    """Load the settings for this pytest session."""
    return RDMOSettings.get()


@pytest.fixture
def extracted_person() -> ExtractedPerson:
    """Return an extracted person with static dummy values."""
    return ExtractedPerson(
        email="ausgedachta@rki.de",
        familyName="Ausgedacht",
        givenName="Arnold",
        fullName="Arnold Ausgedacht",
        hadPrimarySource=Identifier.generate(seed=43),
        identifierInPrimarySource="arnold",
    )


@pytest.fixture
def mocked_ldap(monkeypatch: MonkeyPatch) -> None:
    """Mock the LDAP connector to return resolved persons and units."""
    persons = [
        LDAPPerson(
            employeeID="42",
            sn="Resolved",
            givenName="Roland",
            displayName="Resolved, Roland",
            objectGUID=UUID(int=4, version=4),
            department="PARENT-UNIT",
        )
    ]
    monkeypatch.setattr(
        LDAPConnector,
        "__init__",
        lambda self: setattr(self, "_connection", MagicMock()),
    )
    monkeypatch.setattr(LDAPConnector, "get_persons", lambda _, **__: iter(persons))
