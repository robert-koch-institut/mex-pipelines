from typing import Iterable
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
    extract_sumo_access_platform,
    extract_sumo_activity,
    extract_sumo_organizations,
    extract_sumo_resources_feat,
    extract_sumo_resources_nokeda,
)
from mex.sumo.models.access_platform import SumoAccessPlatform
from mex.sumo.models.cc1_data_model_nokeda import Cc1DataModelNoKeda
from mex.sumo.models.cc1_data_valuesets import Cc1DataValuesets
from mex.sumo.models.cc2_aux_mapping import Cc2AuxMapping
from mex.sumo.models.cc2_aux_model import Cc2AuxModel
from mex.sumo.models.cc2_aux_valuesets import Cc2AuxValuesets
from mex.sumo.models.cc2_feat_projection import Cc2FeatProjection
from mex.sumo.models.resource_feat_model import ResourceFeatModel
from mex.sumo.models.resource_nokeda import ResourceNokeda


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


def test_extract_sumo_resources_nokeda() -> None:
    resources = extract_sumo_resources_nokeda()

    assert resources.model_dump() == {
        "access_restriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
                "comment": "restricted",
            }
        ],
        "accrual_periodicity": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/frequency-15"]}
                ],
                "comment": "daily",
            }
        ],
        "contact": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["email@email.de"],
                        "rule": "Match value to using ldap extractor.",
                    }
                ],
            }
        ],
        "contributing_unit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Abteilung"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
        "description": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "value": "Echtzeitdaten der Routinedokumenation",
                            }
                        ]
                    }
                ],
            }
        ],
        "documentation": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "en",
                                "title": "Confluence",
                                "url": "https://link.com",
                            }
                        ]
                    }
                ],
            }
        ],
        "keyword": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "keyword1"}]},
                    {"setValues": [{"language": "de", "value": "keyword2"}]},
                ],
            }
        ],
        "mesh_id": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["http://id.nlm.nih.gov/mesh/D004636"]}],
                "comment": "Emergency Service, Hospital",
            }
        ],
        "publication": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "title": "Situationsreport",
                                "url": "https://link.com",
                            }
                        ]
                    }
                ],
            }
        ],
        "publisher": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Robert Koch-Institut"],
                        "rule": "Assign 'stable target id' of organization-item with official name as given in forValues.",
                    }
                ],
            }
        ],
        "resource_type_general": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/resource-type-general-1"]}
                ],
                "comment": "Public Health Fachdaten",
            }
        ],
        "resource_type_specific": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"language": "de", "value": "Daten"}]}],
            }
        ],
        "rights": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "value": "Die Daten sind zweckgebunden und können nicht ohne Weiteres innerhalb des RKI zur Nutzung zur Verfügung gestellt werden.",
                            }
                        ]
                    }
                ],
            }
        ],
        "spatial": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "Deutschland"}]}
                ],
            }
        ],
        "state_of_data_processing": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/data-processing-state-2"]}
                ],
                "comment": "Sekundärdaten",
            }
        ],
        "theme": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/theme-11"]},
                    {"setValues": ["https://mex.rki.de/item/theme-35"]},
                ],
                "comment": "Infektionskrankheiten.",
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"langauge": "de", "value": "test_project"}]}
                ],
            }
        ],
        "unit_in_charge": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["FG99"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
    }


def test_extract_sumo_resources_feat() -> None:
    resources = extract_sumo_resources_feat()
    assert resources.model_dump() == {
        "access_restriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
                "comment": "restricted",
            }
        ],
        "accrual_periodicity": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/frequency-17"]}
                ],
                "comment": "irregular",
            }
        ],
        "contact": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["email@email.de"],
                        "rule": "Use value to match with ldap extractor.",
                    }
                ],
            }
        ],
        "contributing_unit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Abteilung"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
        "keyword": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "keyword 1"}]},
                    {"setValues": [{"language": "de", "value": "keyword 2"}]},
                ],
            }
        ],
        "mesh_id": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["http://id.nlm.nih.gov/mesh/D004636"]}],
                "comment": "Emergency Service, Hospital",
            }
        ],
        "resource_type_general": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/resource-type-general-1"]}
                ],
                "comment": "Public Health Fachdaten",
            }
        ],
        "theme": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://mex.rki.de/item/theme-35"]}],
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "Syndrome"}]}
                ],
            }
        ],
        "unit_in_charge": [
            {"fieldInPrimarySource": "n/a", "mappingRules": [{"forValues": ["FG 99"]}]}
        ],
    }


def test_extract_sumo_access_platform() -> None:
    access_platform = extract_sumo_access_platform()
    assert access_platform.model_dump() == {
        "contact": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Roland Resolved"],
                        "rule": "Match value using ldap extractor.",
                    }
                ],
            }
        ],
        "identifier_in_primary_source": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"rule": "Use value as it " "is.", "setValues": ["sumo-db"]}
                ],
            }
        ],
        "technical_accessibility": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/technical-accessibility-1"]}
                ],
                "comment": "internal",
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "SUMO Datenbank"}]}
                ],
            }
        ],
        "unit_in_charge": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Abteilung"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
    }


def test_extract_sumo_activity() -> None:
    activity = extract_sumo_activity()
    expected = {
        "abstract": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "Dummy abstract."}]}
                ],
            }
        ],
        "activity_type": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/activity-type-3"]}
                ],
                "comment": "RKI-internes Projekt",
            }
        ],
        "contact": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["email@email.de"],
                        "rule": "Use value to match with ldap extractor.",
                    }
                ],
            }
        ],
        "documentation": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "title": "SUMO im internen RKI Confluence",
                                "url": "https://url.url",
                            }
                        ]
                    }
                ],
            }
        ],
        "identifier_in_primary_source": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://url.url"]}],
            }
        ],
        "involved_unit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["C1"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
        "publication": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "title": "Dummy title.",
                                "url": "http://url.url",
                            }
                        ]
                    },
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "title": "Dummy title.",
                                "url": "https://url.url",
                            }
                        ]
                    },
                ],
            }
        ],
        "responsible_unit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["C1"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
        "short_name": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"value": "SUMO"}]}],
            }
        ],
        "start": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["2018-07"]}],
            }
        ],
        "theme": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/theme-35"]},
                    {"setValues": ["https://mex.rki.de/item/theme-11"]},
                    {"setValues": ["https://mex.rki.de/item/theme-3"]},
                    {"setValues": ["https://mex.rki.de/item/theme-36"]},
                    {"setValues": ["https://mex.rki.de/item/theme-38"]},
                ],
                "comment": "dummy comment",
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {"language": "de", "value": "SUMO Notaufnahmesurveillance"}
                        ]
                    }
                ],
            }
        ],
        "website": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {
                                "language": "de",
                                "title": "Surveillance Monitor",
                                "url": "https://url.url",
                            }
                        ]
                    }
                ],
            }
        ],
    }
    assert activity.model_dump(exclude_defaults=True) == expected


@pytest.mark.usefixtures("mocked_ldap")
def test_extract_ldap_contact_points_by_emails(
    sumo_resources_feat: ResourceFeatModel, sumo_resources_nokeda: ResourceNokeda
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
    sumo_access_platform: SumoAccessPlatform,
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
    sumo_resources_nokeda: ResourceNokeda,
    wikidata_organization: WikidataOrganization,
) -> None:
    organizations = extract_sumo_organizations(sumo_resources_nokeda)
    assert organizations == {
        "Robert Koch-Institut": wikidata_organization,
    }
