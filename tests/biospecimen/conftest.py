from unittest.mock import MagicMock
from uuid import UUID

import pytest
from pytest import MonkeyPatch

from mex.biospecimen.models.source import BiospecimenResource
from mex.biospecimen.settings import BiospecimenSettings
from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPerson
from mex.common.types import Identifier


@pytest.fixture(autouse=True)
def settings() -> BiospecimenSettings:
    """Load the settings for this pytest session."""
    return BiospecimenSettings.get()


@pytest.fixture
def biospecimen_resources() -> BiospecimenResource:
    """Return a dummy biospecimen resource for testing."""
    return [
        BiospecimenResource(
            offizieller_titel_der_probensammlung=["test_titel"],
            beschreibung=["Testbeschreibung"],
            schlagworte=["Testschlagwort 1, Testschlagwort 2"],
            methoden=["Testmethode"],
            zeitlicher_bezug=["2021-09 bis 2021-10"],
            rechte="Testrechte",
            studienbezug=["1234567"],
            alternativer_titel="alternativer Testitel",
            anonymisiert_pseudonymisiert="pseudonymisiert",
            externe_partner="esterner Testpartner",
            id_loinc=["12345-6"],
            id_mesh_begriff=["D123"],
            kontakt=["test_person@email.de"],
            methodenbeschreibung=["Testmethodenbeschreibung"],
            mitwirkende_fachabteilung="mitwirkende Testabteilung",
            mitwirkende_personen="mitwirkende Testperson",
            raeumlicher_bezug=["räumlicher Testbezug"],
            ressourcentyp_allgemein="allgemeiner Testtyp",
            ressourcentyp_speziell=["spezieller Testtyp"],
            sheet_name="Probe1",
            thema=[],
            tools_instrumente_oder_apparate="Testtool",
            verantwortliche_fachabteilung="PARENT Dept.",
            verwandte_publikation_doi="testverwandedoi",
            verwandte_publikation_titel="testverwandtepublikation",
            vorhandene_anzahl_der_proben="Testanzahl",
            weiterfuehrende_dokumentation_titel="Testdokutitel",
            weiterfuehrende_dokumentation_url_oder_dateipfad="Testdokupfad",
            zugriffsbeschraenkung="Testbeschränkung",
        )
    ]


@pytest.fixture
def mocked_ldap(monkeypatch: MonkeyPatch) -> None:
    """Mock the LDAP connector to return resolved persons and units."""
    persons = [
        LDAPPerson(
            department="PARENT-UNIT",
            employeeID="42",
            sn="Contact",
            givenName="Carla",
            displayName="Contact, Carla",
            objectGUID=UUID(int=4, version=4),
            mail=["test_person@email.de"],
        )
    ]
    monkeypatch.setattr(
        LDAPConnector,
        "__init__",
        lambda self: setattr(self, "_connection", MagicMock()),
    )
    monkeypatch.setattr(LDAPConnector, "get_persons", lambda *_, **__: iter(persons))


@pytest.fixture
def mex_persons() -> list[ExtractedPerson]:
    """Mock and extracted person."""
    return [
        ExtractedPerson(
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="test_id",
            email=["test_person@email.de"],
            familyName=["Müller"],
            fullName=["Müller, Marie"],
            givenName=["Marie"],
        )
    ]
