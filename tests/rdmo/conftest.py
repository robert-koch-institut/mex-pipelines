from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPerson
from mex.common.types import Identifier
from mex.rdmo.connector import RDMOConnector
from mex.rdmo.models.person import RDMOPerson
from mex.rdmo.models.source import RDMOSource
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


@pytest.fixture
def mocked_rdmo(monkeypatch: MonkeyPatch) -> None:
    """Mock the RDMO connector to return dummy data."""
    sources = (
        RDMOSource(id=1, title="Unowned"),
        RDMOSource(
            id=2,
            title="Owned",
            owners=[
                RDMOPerson(
                    email="musterm@rki.de",
                    first_name="Max",
                    id=100,
                    last_name="Muster",
                    username="musterm",
                ),
                RDMOPerson(
                    email="beispielb@rki.de",
                    first_name="Beate",
                    id=200,
                    last_name="Beispiel",
                    username="beispielb",
                ),
            ],
        ),
    )
    monkeypatch.setattr(RDMOConnector, "get_sources", lambda _: iter(sources))

    def get_question_answer_pairs(self: RDMOConnector, project: int) -> dict[str, str]:
        return (
            {
                "/questions/project_proposal/general/project-title/title": "Lorem Ipsum",
                "/questions/project_proposal/general/project-title/acronym": "LI1",
                "/questions/project_proposal/general/project-title/project_type": "rki-internal_Project",
                "questions/project_proposal/general/project-schedule-schedule/project_start": "2004",
                "questions/project_proposal/general/project-schedule-schedule/project_end": "2006-05",
            }
            if project == 2
            else {}
        )

    monkeypatch.setattr(
        RDMOConnector, "get_question_answer_pairs", get_question_answer_pairs
    )

    def __init__(self: RDMOConnector) -> None:
        self.session = MagicMock()
        self.url = "https://mock-rdmo"

    monkeypatch.setattr(RDMOConnector, "__init__", __init__)
