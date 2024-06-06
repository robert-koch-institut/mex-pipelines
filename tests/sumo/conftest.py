from uuid import UUID

import pytest
from traitlets import Any

from mex.common.models import (
    ExtractedActivity,
    ExtractedContactPoint,
    ExtractedPerson,
    ExtractedResource,
    ExtractedVariableGroup,
)
from mex.common.types import (
    Identifier,
    MergedContactPointIdentifier,
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
    MergedPrimarySourceIdentifier,
    Text,
    TextLanguage,
)
from mex.sumo.models.cc1_data_model_nokeda import Cc1DataModelNoKeda
from mex.sumo.models.cc1_data_valuesets import Cc1DataValuesets
from mex.sumo.models.cc2_aux_mapping import Cc2AuxMapping
from mex.sumo.models.cc2_aux_model import Cc2AuxModel
from mex.sumo.models.cc2_aux_valuesets import Cc2AuxValuesets
from mex.sumo.models.cc2_feat_projection import Cc2FeatProjection
from mex.sumo.settings import SumoSettings


@pytest.fixture(autouse=True)
def settings() -> SumoSettings:
    """Load the settings for this pytest session."""
    return SumoSettings.get()


@pytest.fixture
def mex_actor_resources() -> ExtractedContactPoint:
    """Return a dummy mex actor resource."""
    return ExtractedContactPoint(
        email="email@email.de",
        hadPrimarySource=MergedPrimarySourceIdentifier.generate(seed=42),
        identifierInPrimarySource="contact point",
    )


@pytest.fixture
def mex_actor_access_platform() -> ExtractedPerson:
    """Return a dummy mex actor access platform."""
    return ExtractedPerson(
        familyName="Mustermann",
        fullName="Erika Mustermann",
        givenName="Erika",
        hadPrimarySource=MergedPrimarySourceIdentifier.generate(seed=42),
        identifierInPrimarySource="access platform",
    )


@pytest.fixture
def unit_merged_ids_by_synonym() -> dict[str, MergedOrganizationalUnitIdentifier]:
    """Return dummy merged ids for units for testing."""
    return {
        "MF4": MergedOrganizationalUnitIdentifier.generate(seed=45),
        "mf4": MergedOrganizationalUnitIdentifier.generate(seed=45),
        "FG32": MergedOrganizationalUnitIdentifier.generate(seed=47),
        "fg32": MergedOrganizationalUnitIdentifier.generate(seed=47),
        "FG99": MergedOrganizationalUnitIdentifier.generate(seed=49),
        "fg99": MergedOrganizationalUnitIdentifier.generate(seed=49),
        "FG 99": MergedOrganizationalUnitIdentifier.generate(seed=49),
    }


@pytest.fixture
def contact_merged_ids_by_emails():
    """Return dummy merged ids for units for testing."""
    return {"email@email.de": MergedContactPointIdentifier.generate(seed=51)}


@pytest.fixture
def organizations_stable_target_ids_by_synonym():
    """Return dummy merged ids for units for testing."""
    return {
        "Register": MergedOrganizationalUnitIdentifier.generate(seed=60),
        "Dummy Associate": MergedOrganizationalUnitIdentifier.generate(seed=61),
        "Robert Koch-Institut": MergedOrganizationalUnitIdentifier.generate(seed=62),
    }


@pytest.fixture
def sumo_resources_feat() -> dict[str, Any]:
    """Return feat SumoResource."""
    return {
        "accessRestriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
                "comment": "restricted",
            }
        ],
        "accrualPeriodicity": [
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
        "contributingUnit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["MF4"],
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
        "meshId": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["http://id.nlm.nih.gov/mesh/D004636"]}],
                "comment": "Emergency Service, Hospital",
            }
        ],
        "resourceTypeGeneral": [
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
        "unitInCharge": [
            {"fieldInPrimarySource": "n/a", "mappingRules": [{"forValues": ["FG 99"]}]}
        ],
    }


@pytest.fixture
def sumo_resources_nokeda() -> dict[str, Any]:
    """Return feat SumoResource."""
    return {
        "accessRestriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
                "comment": "restricted",
            }
        ],
        "accrualPeriodicity": [
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
        "contributingUnit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["MF4"],
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
        "externalPartner": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Register"],
                        "rule": "Use value to match with wikidata extractor.",
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
        "meshId": [
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
        "resourceTypeGeneral": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/resource-type-general-1"]}
                ],
                "comment": "Public Health Fachdaten",
            }
        ],
        "resourceTypeSpecific": [
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
        "stateOfDataProcessing": [
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
                    {"setValues": [{"language": "de", "value": "test_project"}]}
                ],
            }
        ],
        "unitInCharge": [
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


@pytest.fixture
def sumo_access_platform() -> dict[str, Any]:
    """Return Sumo Access Platform."""
    return {
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "SUMO Datenbank"}]}
                ],
            }
        ],
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
        "identifierInPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"rule": "Use value as it " "is.", "setValues": ["sumo-db"]}
                ],
            }
        ],
        "technicalAccessibility": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            "https://mex.rki.de/item/technical-accessibility-1"
                        ],
                        "rule": "Match value using ldap extractor.",
                    }
                ],
            }
        ],
        "unitInCharge": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["mf4"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
    }


@pytest.fixture
def sumo_activity() -> dict[str, Any]:
    """Return Sumo Activity."""
    return {
        "abstract": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "Dummy abstract."}]}
                ],
            }
        ],
        "activityType": [
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
        "externalAssociate": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Dummy Associate"],
                        "rule": "Use value to match with wikidata extractor.",
                    }
                ],
            }
        ],
        "identifierInPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://url.url"]}],
            }
        ],
        "involvedUnit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["mf4"],
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
        "responsibleUnit": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["fg32"],
                        "rule": "Use value to match with identifier in /raw-data/organigram/organizational-units.json.",
                    }
                ],
            }
        ],
        "shortName": [
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
        "succeeds": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Dummy project"],
                        "rule": "Ignore the value, the item is not in MEx.",
                    }
                ],
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


@pytest.fixture
def transformed_activity() -> ExtractedActivity:
    """Return Sumo ExtractedActivity."""
    return ExtractedActivity(
        hadPrimarySource=MergedPrimarySourceIdentifier("hBYPjIX6hKi4FtA5ES5i1a"),
        identifierInPrimarySource="https://url.url",
        abstract=[Text(value="Dummy abstract.", language=TextLanguage.DE)],
        activityType=["https://mex.rki.de/item/activity-type-3"],
        alternativeTitle=[],
        contact=[MergedOrganizationalUnitIdentifier("bFQoRhcVH5DHVf")],
        documentation=[],
        end=[],
        externalAssociate=[MergedOrganizationalUnitIdentifier("bFQoRhcVH5DHVp")],
        funderOrCommissioner=[],
        fundingProgram=[],
        involvedPerson=[],
        involvedUnit=[MergedOrganizationalUnitIdentifier("bFQoRhcVH5DHU9")],
        isPartOfActivity=[],
        publication=[],
        responsibleUnit=[MergedOrganizationalUnitIdentifier("bFQoRhcVH5DHVb")],
        shortName=[Text(value="SUMO", language=TextLanguage.DE)],
        start=[],
        succeeds=[],
        theme=["https://mex.rki.de/item/theme-35"],
        title=[Text(value="SUMO Notaufnahmesurveillance", language=TextLanguage.DE)],
        website=[],
    )


@pytest.fixture
def mex_resources_nokeda() -> ExtractedResource:
    """Return Nokeda ExtractedResources."""
    return ExtractedResource(
        hadPrimarySource=UUID(int=5, version=4),
        identifierInPrimarySource="test_project",
        accessPlatform=[],
        accessRestriction="https://mex.rki.de/item/access-restriction-2",
        accrualPeriodicity="https://mex.rki.de/item/frequency-15",
        contact=[UUID(int=5, version=4)],
        contributingUnit=[UUID(int=5, version=4)],
        description=["Echtzeitdaten der Routinedokumenation"],
        externalPartner=[UUID(int=5, version=4)],
        keyword=["keyword1", "keyword2"],
        meshId=["http://id.nlm.nih.gov/mesh/D004636"],
        publication=["Situationsreport"],
        publisher=[MergedOrganizationIdentifier("bFQoRhcVH5DHU6")],
        resourceTypeGeneral=["https://mex.rki.de/item/resource-type-general-1"],
        resourceTypeSpecific=["Daten"],
        rights=[
            "Die Daten sind zweckgebunden und können nicht ohne Weiteres innerhalb des RKI zur Nutzung zur Verfügung gestellt werden."
        ],
        spatial=["Deutschland"],
        stateOfDataProcessing="https://mex.rki.de/item/data-processing-state-2",
        theme=["https://mex.rki.de/item/theme-11"],
        title=["test_project"],
        unitInCharge=[MergedOrganizationalUnitIdentifier.generate(seed=42)],
    )


@pytest.fixture
def mex_resources_feat() -> ExtractedResource:
    """Return feat ExtractedResources."""
    return ExtractedResource(
        hadPrimarySource=UUID(int=5, version=4),
        identifierInPrimarySource="test_project",
        accessRestriction="https://mex.rki.de/item/access-restriction-2",
        accrualPeriodicity="https://mex.rki.de/item/frequency-17",
        contact=[UUID(int=5, version=4)],
        contributingUnit=[UUID(int=5, version=4)],
        keyword=["keyword 1", "keyword 2"],
        meshId=["http://id.nlm.nih.gov/mesh/D004636"],
        resourceTypeGeneral=["https://mex.rki.de/item/resource-type-general-1"],
        theme=["https://mex.rki.de/item/theme-1"],
        title=["Syndrome"],
        unitInCharge=[MergedOrganizationalUnitIdentifier.generate(seed=42)],
    )


@pytest.fixture
def cc1_data_model_nokeda() -> list[Cc1DataModelNoKeda]:
    """Return data model nokeda variables."""
    return [
        Cc1DataModelNoKeda(
            domain="Datenbereitstellung",
            domain_en="data supply",
            type_json="string",
            element_description="shobidoo",
            element_description_en="shobidoo_en",
            variable_name="nokeda_edis_software",
            element_label="Name des EDIS",
            element_label_en="Name of EDIS",
        )
    ]


@pytest.fixture
def cc1_data_valuesets() -> list[Cc1DataValuesets]:
    """Return data valuesets variables."""
    return [
        Cc1DataValuesets(
            category_label_de="Herzstillstand (nicht traumatisch)",
            sheet_name="nokeda_cedis",
        )
    ]


@pytest.fixture
def cc2_aux_mapping() -> list[Cc2AuxMapping]:
    """Return aux mapping variables."""
    return [
        Cc2AuxMapping(variable_name_column=["0", "1", "2"], sheet_name="nokeda_age21"),
        Cc2AuxMapping(
            variable_name_column=["001", "002", "003"], sheet_name="nokeda_cedis"
        ),
    ]


@pytest.fixture
def cc2_aux_model() -> list[Cc2AuxModel]:
    """Return aux model variables."""
    return [
        Cc2AuxModel(
            depends_on_nokeda_variable="nokeda_age21",
            domain="age",
            element_description="the lowest age in the age group",
            in_database_static=True,
            variable_name="aux_age21_min",
        ),
        Cc2AuxModel(
            depends_on_nokeda_variable="nokeda_cedis",
            domain="disease",
            element_description="Core groups as defined in the CEDIS reporting standard",
            in_database_static=True,
            variable_name="aux_cedis_group",
        ),
    ]


@pytest.fixture
def cc2_aux_valuesets() -> list[Cc2AuxValuesets]:
    """Return aux valuesets variables."""
    return [Cc2AuxValuesets(label_de="Kardiovaskulär", label_en="Cardiovascular")]


@pytest.fixture
def cc2_feat_projection() -> list[Cc2FeatProjection]:
    """Return feat projection variables."""
    return [
        Cc2FeatProjection(
            feature_domain="feat_syndrome",
            feature_subdomain="RSV",
            feature_abbr="1",
            feature_name_en="respiratory syncytial virus, specific",
            feature_name_de="Respiratorisches Syncytial-Virus, spezifisch",
            feature_description="specific RSV-ICD-10 codes",
        )
    ]


@pytest.fixture
def mex_variable_groups_nokeda_aux() -> list[ExtractedVariableGroup]:
    """Return nokeda variable groups."""
    return [
        ExtractedVariableGroup(
            containedBy=Identifier.generate(seed=42),
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="age",
            label=Text(value="age", language=TextLanguage.EN),
        ),
        ExtractedVariableGroup(
            containedBy=Identifier.generate(seed=42),
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="disease",
            label=Text(value="disease", language=TextLanguage.EN),
        ),
    ]


@pytest.fixture
def mex_variable_groups_model_nokeda() -> list[ExtractedVariableGroup]:
    """Return nokeda variable groups."""
    return [
        ExtractedVariableGroup(
            containedBy=Identifier.generate(seed=42),
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="Datenbereitstellung",
            label={"value": "Datenbereitstellung"},
        ),
        ExtractedVariableGroup(
            containedBy=Identifier.generate(seed=42),
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="age",
            label={"value": "age"},
        ),
    ]


@pytest.fixture
def mex_variable_groups_model_feat() -> list[ExtractedVariableGroup]:
    """Return model feat variable groups."""
    return [
        ExtractedVariableGroup(
            containedBy=Identifier.generate(seed=42),
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="feat_syndrome RSV",
            label={"value": "feat_syndrome RSV"},
        ),
        ExtractedVariableGroup(
            containedBy=Identifier.generate(seed=42),
            hadPrimarySource=Identifier.generate(seed=42),
            identifierInPrimarySource="feat_syndrome RSV",
            label={"value": "feat_syndrome RSV"},
        ),
    ]
