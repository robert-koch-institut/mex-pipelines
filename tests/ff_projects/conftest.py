import pytest

from mex.common.models import ExtractedActivity, ExtractedPerson
from mex.common.types import ActivityType, Identifier
from mex.extractors.mapping.transform import transform_mapping_data_to_model
from mex.extractors.mapping.types import AnyMappingModel


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
def ff_projects_activity() -> AnyMappingModel:
    """Return FF Projects mapping default values."""
    return transform_mapping_data_to_model(
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
                            "rule": "Assign 'stable target id' of primary source with identifier 'ff-project' in /raw-data/primary-sources/primary-sources.json.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "identifierInPrimarySource": [
                {
                    "fieldInPrimarySource": "lfd. Nr.",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["1632", "1754/XX"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Extract original value.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "contact": [
                {
                    "fieldInPrimarySource": "Projektleiter",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["Doe", "Müller-Schmidt"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Match person using ldap extractor. If the value does not match, use the organizational unit given in the field 'RKI-OE'.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "responsibleUnit": [
                {
                    "fieldInPrimarySource": "RKI-OE",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["Präs", "GGBS", "FG 24", "NG 4", "P 3"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Match value using organigram extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "title": [
                {
                    "fieldInPrimarySource": "Thema des Projekts",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": [
                        "EuroBioTox",
                        "Genetische Anpassung von nicht typhoiden Salmonellen im Human- und Tierreservior in sup-Sahara Afrika",
                    ],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Extract original value.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "abstract": [],
            "activityType": [
                {
                    "fieldInPrimarySource": "RKI-AZ",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": None,
                    "mappingRules": [
                        {
                            "forValues": ["1364", "1365", "1367", "1368"],
                            "setValues": [ActivityType["THIRD_PARTY_FUNDED_PROJECT"]],
                            "rule": None,
                        }
                    ],
                    "comment": None,
                }
            ],
            "alternativeTitle": [],
            "documentation": [],
            "end": [
                {
                    "fieldInPrimarySource": "Laufzeit bis",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["31.12.2020"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Extract original value.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "externalAssociate": [],
            "funderOrCommissioner": [
                {
                    "fieldInPrimarySource": "Zuwendungs-/Auftraggeber",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": [
                        "EC",
                        "DFG",
                        "G-BA",
                        "SV Frankfurt",
                        "Charité",
                    ],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Match value using wikidata extractor.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "fundingProgram": [
                {
                    "fieldInPrimarySource": "Förderprogr.(FP7, H2020 etc.) ab 08/2015",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["H2020"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Extract original value.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "involvedPerson": [
                {
                    "fieldInPrimarySource": "Projektleiter",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["Doe", "Müller-Schmidt"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Match person using ldap extractor. If the value does not match, use the organizational unit given in the field 'RKI-OE'.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "involvedUnit": [],
            "isPartOfActivity": [],
            "publication": [],
            "shortName": [],
            "start": [
                {
                    "fieldInPrimarySource": "Laufzeit von",
                    "locationInPrimarySource": None,
                    "examplesInPrimarySource": ["01.06.2017"],
                    "mappingRules": [
                        {
                            "forValues": None,
                            "setValues": None,
                            "rule": "Extract original value.",
                        }
                    ],
                    "comment": None,
                }
            ],
            "succeeds": [],
            "theme": [],
            "website": [],
        },
        ExtractedActivity,
    )
