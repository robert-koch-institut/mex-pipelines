from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPerson
from mex.common.types import Identifier
from mex.ff_projects.settings import FFProjectsSettings


@pytest.fixture(autouse=True)
def settings() -> FFProjectsSettings:
    """Load the settings for this pytest session."""
    return FFProjectsSettings.get()


@pytest.fixture
def extracted_person() -> ExtractedPerson:
    """Return an extracted person with static dummy values."""
    return ExtractedPerson(
        email=["fictitiousf@rki.de", "info@rki.de"],
        familyName="Fictitious",
        givenName="Frieda",
        fullName="Dr. Fictitious, Frieda",
        identifierInPrimarySource="frieda",
        hadPrimarySource=Identifier.generate(seed=40),
    )


@pytest.fixture
def mocked_ldap(monkeypatch: MonkeyPatch) -> None:
    """Mock LDAP connector to return a mocked person and actor."""
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
                    givenName="Roland",
                    displayName="Resolved, Roland",
                    objectGUID=UUID(int=4, version=4),
                    department="PARENT-UNIT",
                )
            ]
        ),
    )
