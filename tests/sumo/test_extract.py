from collections.abc import Iterable
from typing import Any
from uuid import UUID

import pytest

from mex.common.wikidata.models.organization import WikidataOrganization
from mex.sumo.extract import (
    extract_cc1_data_model_nokeda,
    extract_cc1_data_valuesets,
    extract_cc2_aux_mapping,
    extract_cc2_aux_model,
    extract_cc2_aux_valuesets,
    extract_cc2_feat_projection,
    extract_ldap_contact_points_by_emails,
    extract_ldap_contact_points_by_name,
    extract_sumo_organizations,
)
from mex.sumo.models.cc1_data_model_nokeda import Cc1DataModelNoKeda
from mex.sumo.models.cc1_data_valuesets import Cc1DataValuesets
from mex.sumo.models.cc2_aux_mapping import Cc2AuxMapping
from mex.sumo.models.cc2_aux_model import Cc2AuxModel
from mex.sumo.models.cc2_aux_valuesets import Cc2AuxValuesets
from mex.sumo.models.cc2_feat_projection import Cc2FeatProjection


def test_extract_cc1_data_model_nokeda() -> None:
    expected = Cc1DataModelNoKeda(
        domain="Datenbereitstellung",
        domain_en="data supply",
        type_json="string",
        element_description="shobidoo",
        element_description_en="shobidoo_en",
        variable_name="nokeda_edis_software",
        element_label="Name des EDIS",
        element_label_en="Name of EDIS",
    )
    extracted_data = list(extract_cc1_data_model_nokeda())
    assert len(extracted_data) == 3
    assert extracted_data[0] == expected


def test_extract_cc1_data_valuesets() -> None:
    expected = Cc1DataValuesets(
        category_label_de="Herzstillstand (nicht traumatisch)",
        sheet_name="nokeda_cedis",
    )
    extracted_data = list(extract_cc1_data_valuesets())
    assert len(extracted_data) == 6
    assert extracted_data[0] == expected


def test_extract_cc2_aux_mapping(
    cc2_aux_model: Iterable[Cc2AuxModel],
) -> None:
    expected = Cc2AuxMapping(
        variable_name_column=["0", "1", "2"], sheet_name="nokeda_age21"
    )
    extracted_data = list(extract_cc2_aux_mapping(cc2_aux_model))
    assert len(extracted_data) == 2
    assert extracted_data[0] == expected


def test_extract_cc2_aux_model() -> None:
    expected = Cc2AuxModel(
        depends_on_nokeda_variable="nokeda_age21",
        domain="age",
        element_description="the lowest age in the age group",
        in_database_static=True,
        variable_name="aux_age21_min",
    )
    extracted_data = list(extract_cc2_aux_model())
    assert len(extracted_data) == 2
    assert extracted_data[0] == expected


def test_extract_cc2_aux_valuesets() -> None:
    expected = Cc2AuxValuesets(label_de="Kardiovaskulär", label_en="Cardiovascular")
    extracted_data = list(extract_cc2_aux_valuesets())
    assert len(extracted_data) == 3
    assert extracted_data[0] == expected


def test_extract_cc2_feat_projection() -> None:
    expected = Cc2FeatProjection(
        feature_domain="feat_syndrome",
        feature_subdomain="RSV",
        feature_abbr="1",
        feature_name_en="respiratory syncytial virus, specific",
        feature_name_de="Respiratorisches Syncytial-Virus, spezifisch",
        feature_description="specific RSV-ICD-10 codes",
    )
    extracted_data = list(extract_cc2_feat_projection())
    assert len(extracted_data) == 3
    assert extracted_data[0] == expected


@pytest.mark.usefixtures("mocked_ldap")
def test_extract_ldap_contact_points_by_emails(
    sumo_resources_feat: dict[str, Any], sumo_resources_nokeda: dict[str, Any]
) -> None:
    expected = {
        "mail": ["email@email.de", "contactc@rki.de"],
        "objectGUID": UUID("00000000-0000-4000-8000-000000000004"),
        "sAMAccountName": "ContactC",
    }
    extracted = list(
        extract_ldap_contact_points_by_emails(
            [sumo_resources_feat, sumo_resources_nokeda]
        )
    )
    assert extracted[0].model_dump() == expected


@pytest.mark.usefixtures("mocked_ldap")
def test_extract_ldap_contact_points_by_name(
    sumo_access_platform: dict[str, Any],
) -> None:
    expected = {
        "person": {
            "sAMAccountName": None,
            "objectGUID": UUID("00000000-0000-4000-8000-000000000004"),
            "mail": [],
            "company": None,
            "department": "PARENT-UNIT",
            "departmentNumber": None,
            "displayName": "Resolved, Roland",
            "employeeID": "42",
            "givenName": ["Roland"],
            "ou": [],
            "sn": "Resolved",
        },
        "query": "Roland Resolved",
    }

    extracted = list(extract_ldap_contact_points_by_name(sumo_access_platform))
    assert extracted[0].model_dump() == expected


@pytest.mark.usefixtures(
    "mocked_wikidata",
)
def test_extract_sumo_organizations(
    sumo_resources_nokeda: dict[str, Any],
    wikidata_organization: WikidataOrganization,
) -> None:
    organizations = extract_sumo_organizations(sumo_resources_nokeda)
    assert organizations == {
        "Robert Koch-Institut": wikidata_organization,
    }
