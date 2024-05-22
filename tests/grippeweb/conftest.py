from typing import Any, TypeVar
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel
from pytest import MonkeyPatch

from mex.common.types import (
    MergedContactPointIdentifier,
    MergedOrganizationalUnitIdentifier,
)
from mex.grippeweb.connector import GrippewebConnector

ModelT = TypeVar("ModelT", bound=BaseModel)


@pytest.fixture
def mocked_sql_tables() -> dict[str, list[BaseModel]]:
    return {
        "vActualQuestion": {
            "Id": ["AAA", "BBB"],
            "StartedOn": ["2023-11-01 00:00:00.0000000", "2023-12-01 00:00:00.0000000"],
            "FinishedOn": [
                "2023-12-01 00:00:00.0000000",
                "2024-01-01 00:00:00.0000000",
            ],
            "RepeatAfterDays": ["1", "2"],
        },
        "vWeeklyResponsesMEx": {
            "GuidTeilnehmer": [None, None],
            "Haushalt_Registrierer": [None, None],
        },
        "vMasterDataMEx": {
            "GuidTeilnehmer": [None, None],
            "Haushalt_Registrierer": [None, None],
        },
    }


@pytest.fixture
def mocked_grippeweb(
    mocked_sql_tables: dict[str, list[BaseModel]], monkeypatch: MonkeyPatch
) -> None:
    """Mock grippeweb connector."""

    def mocked_init(self: GrippewebConnector) -> None:
        cursor = MagicMock()
        cursor.fetchone.return_value = ["mocked"]
        self._connection = MagicMock()
        self._connection.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(GrippewebConnector, "__init__", mocked_init)

    monkeypatch.setattr(
        GrippewebConnector,
        "parse_columns_by_column_name",
        lambda self, model: mocked_sql_tables[model],
    )


@pytest.fixture
def extracted_mex_functional_units_grippeweb() -> (
    dict[str, MergedContactPointIdentifier]
):
    return {"c1@email.de": MergedContactPointIdentifier.generate(42)}


@pytest.fixture
def unit_stable_target_ids_by_synonym() -> (
    dict[str, MergedOrganizationalUnitIdentifier]
):
    """Mock unit stable target ids."""
    return {"C1": MergedOrganizationalUnitIdentifier.generate(seed=44)}


@pytest.fixture
def grippeweb_access_platform() -> dict[str, Any]:
    return {
        "hadPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "locationInPrimarySource": None,
                "examplesInPrimarySource": None,
                "mappingRules": [
                    {
                        "forValues": None,
                        "setValues": None,
                        "rule": "Assign 'stable target id' of primary source with identifier 'grippeweb' in /raw-data/primary-sources/primary-sources.json.",
                    }
                ],
                "comment": None,
            }
        ],
        "identifierInPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "locationInPrimarySource": None,
                "examplesInPrimarySource": None,
                "mappingRules": [
                    {
                        "forValues": None,
                        "setValues": ["primary-source"],
                        "rule": "use value as indicated.",
                    }
                ],
                "comment": None,
            }
        ],
        "contact": [
            {
                "fieldInPrimarySource": "n/a",
                "locationInPrimarySource": None,
                "examplesInPrimarySource": None,
                "mappingRules": [
                    {
                        "forValues": ["c1@email.de"],
                        "setValues": None,
                        "rule": "Match value using ldap extractor",
                    }
                ],
                "comment": None,
            }
        ],
        "technicalAccessibility": [
            {
                "fieldInPrimarySource": "n/a",
                "locationInPrimarySource": None,
                "examplesInPrimarySource": None,
                "mappingRules": [
                    {
                        "forValues": None,
                        "setValues": [
                            "https://mex.rki.de/item/technical-accessibility-1"
                        ],
                        "rule": None,
                    }
                ],
                "comment": None,
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "locationInPrimarySource": None,
                "examplesInPrimarySource": None,
                "mappingRules": [
                    {
                        "forValues": None,
                        "setValues": [{"value": "primary-source", "language": "en"}],
                        "rule": None,
                    }
                ],
                "comment": None,
            }
        ],
        "unitInCharge": [
            {
                "fieldInPrimarySource": "n/a",
                "locationInPrimarySource": None,
                "examplesInPrimarySource": None,
                "mappingRules": [
                    {
                        "forValues": ["C1"],
                        "setValues": None,
                        "rule": "Match value using organigram extractor.",
                    }
                ],
                "comment": None,
            }
        ],
    }


@pytest.fixture
def grippeweb_resource_mappings() -> list[dict[str, Any]]:
    return [
        {
            "hadPrimarySource": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Assign 'stable target id' of primary source with identifier 'grippeweb' in /raw-data/primary-sources/primary-sources.json.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "identifierInPrimarySource": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["grippeweb-plus"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "accessPlatform": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "assign 'stable target id' of item described by mapping/grippeweb/access-platform",
                        }
                    ],
                    "comment": None,
                }
            ],
            "accessRestriction": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                "https://mex.rki.de/item/access-restriction-2"
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "accrualPeriodicity": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["https://mex.rki.de/item/frequency-15"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "anonymizationPseudonymization": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                "https://mex.rki.de/item/anonymization-pseudonymization-2"
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "contact": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["test_person@email.de"],
                            "setValues": None,
                            "rule": "Match value using ldap extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "contributingUnit": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["C1"],
                            "setValues": None,
                            "rule": "Match identifer using organigram extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "contributor": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["Carla Contact"],
                            "setValues": None,
                            "rule": "Match values using ldap extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "created": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["2020"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "creator": None,
            "description": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "value": "Erreger-spezifische Zusatzinformationen",
                                    "language": "de",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "distribution": None,
            "documentation": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "RKI Website",
                                    "url": "https://www.rki.de",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "externalPartner": None,
            "icd10code": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["J00-J99"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "instrumentToolOrApparatus": None,
            "isPartOf": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Assign 'stable target id' of item described by mapping/../grippeweb/resource_grippeweb",
                        }
                    ],
                    "comment": None,
                }
            ],
            "keyword": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Surveillance", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "language": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["GERMAN"], "rule": None}
                    ],
                    "comment": "Deutsch",
                }
            ],
            "meshId": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                "http://id.nlm.nih.gov/mesh/D012140",
                                "http://id.nlm.nih.gov/mesh/D012141",
                                "http://id.nlm.nih.gov/mesh/D007251",
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "method": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {"value": "Selbstabstriche", "language": "de"}
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "methodDescription": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Stichprobe", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "publication": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "language": "en",
                                    "title": "Feasibility study",
                                    "url": "https://doi.org/10.25646/11292",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "publisher": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["Robert Koch-Institut"],
                            "setValues": None,
                            "rule": "Match value with organization item using wikidata extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "resourceTypeGeneral": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["SURVEILLANCE_DATA"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "resourceTypeSpecific": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Nasenabstrich", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "rights": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Die Daten", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "sizeOfDataBasis": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["500 Teilnehmende (Stand Mai 2023)"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "spatial": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Deutschland", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "stateOfDataProcessing": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["RAW_DATA"], "rule": None}
                    ],
                    "comment": "Rohdaten",
                }
            ],
            "temporal": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["seit 2020"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "theme": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["STUDIES_AND_SURVEILLANCE"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "title": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {"value": "GrippeWeb-Plus", "language": "de"}
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "unitInCharge": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["C1"],
                            "setValues": None,
                            "rule": "Match value using organigram extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "wasGeneratedBy": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["2022-006"],
                            "setValues": None,
                            "rule": "Match value with corresponding identifierInPrimarySource.",
                        }
                    ],
                    "comment": None,
                }
            ],
        },
        {
            "hadPrimarySource": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Assign 'stable target id' of primary source with identifier 'grippeweb' in /raw-data/primary-sources/primary-sources.json.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "identifierInPrimarySource": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["grippeweb"],
                            "rule": "Use value as indicated.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "accessPlatform": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Assign 'stable target id' of item described by mappings/../grippeweb/access-platform",
                        }
                    ],
                    "comment": None,
                }
            ],
            "accessRestriction": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["RESTRICTED"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "accrualPeriodicity": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["DAILY"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "alternativeTitle": None,
            "anonymizationPseudonymization": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["PSEUDONYMIZED"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "contact": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["test_person@email.de"],
                            "setValues": None,
                            "rule": "Match value by using ldap extract extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "contributingUnit": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["C1"],
                            "setValues": None,
                            "rule": "Match value with identifier using organigram extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "contributor": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["Carla Contact"],
                            "setValues": None,
                            "rule": "Match values using ldap extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "created": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["2011"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "creator": None,
            "description": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "GrippeWeb", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "distribution": None,
            "documentation": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "RKI Website",
                                    "url": "https://www.rki.de",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "icd10code": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["J00-J99"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "instrumentToolOrApparatus": None,
            "isPartOf": None,
            "keyword": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {"value": "Citizen Science", "language": "en"}
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "language": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["GERMAN"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "license": None,
            "loincId": None,
            "meshId": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["http://id.nlm.nih.gov/mesh/D012140"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "method": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {"value": "Online-Befragung", "language": "de"}
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "methodDescription": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "value": "Online-Surveillanceintrument",
                                    "language": "de",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "modified": None,
            "publication": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "COVID-19-Raten",
                                    "url": "https://doi.org/10.25646/11292",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "publisher": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["Robert Koch-Institut"],
                            "setValues": None,
                            "rule": "Match value with organization item using wikidata extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "qualityInformation": None,
            "resourceTypeGeneral": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["SURVEILLANCE_DATA"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "resourceTypeSpecific": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [
                                {
                                    "value": "bevölkerungsbasierte Surveillancedaten",
                                    "language": "de",
                                }
                            ],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "rights": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Verfahren", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "sizeOfDataBasis": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["Meldungen"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "spatial": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "Deutschland", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "stateOfDataProcessing": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["SECONDARY_DATA"],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "temporal": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {"forValues": None, "setValues": ["seit 2011"], "rule": None}
                    ],
                    "comment": None,
                }
            ],
            "theme": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": ["STUDIES_AND_SURVEILLANCE"],
                            "rule": None,
                        },
                        {
                            "forValues": None,
                            "setValues": ["INFECTIOUS_DISEASES"],
                            "rule": None,
                        },
                    ],
                    "comment": None,
                }
            ],
            "title": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": [{"value": "GrippeWeb", "language": "de"}],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "unitInCharge": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["C1"],
                            "setValues": None,
                            "rule": "Match value using organigram extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "wasGeneratedBy": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["2022-006"],
                            "setValues": None,
                            "rule": "Match value with corresponding identifierInPrimarySource",
                        }
                    ],
                    "comment": None,
                }
            ],
            "identifier": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Assign identifier.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "stableTargetId": [
                {
                    "fieldInPrimarySource": "n/a",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Assign 'stable target id' of merged item.",
                        }
                    ],
                    "comment": None,
                }
            ],
        },
    ]
