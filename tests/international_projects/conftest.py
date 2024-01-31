from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest import MonkeyPatch

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPerson, ExtractedPrimarySource
from mex.common.organigram.extract import (
    extract_organigram_units,
    get_unit_merged_ids_by_synonyms,
)
from mex.common.organigram.transform import (
    transform_organigram_units_to_organizational_units,
)
from mex.common.types import OrganizationalUnitID, PrimarySourceID
from mex.international_projects.settings import InternationalProjectsSettings


@pytest.fixture(autouse=True)
def settings() -> InternationalProjectsSettings:
    """Load the settings for this pytest session."""
    return InternationalProjectsSettings.get()


@pytest.fixture
def extracted_person() -> ExtractedPerson:
    """Return an extracted person with static dummy values."""
    return ExtractedPerson(
        email=["fictitiousf@rki.de", "info@rki.de"],
        familyName="Fictitious",
        givenName="Frieda",
        fullName="Dr. Fictitious, Frieda",
        identifierInPrimarySource="frieda",
        hadPrimarySource=PrimarySourceID.generate(seed=40),
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


@pytest.fixture
def unit_stable_target_ids_by_synonym(
    extracted_primary_sources: dict[str, ExtractedPrimarySource]
) -> dict[str, OrganizationalUnitID]:
    """Extract the dummy units and return them grouped by synonyms."""
    organigram_units = extract_organigram_units()
    mex_organizational_units = transform_organigram_units_to_organizational_units(
        organigram_units, extracted_primary_sources["organigram"]
    )
    return get_unit_merged_ids_by_synonyms(mex_organizational_units)
