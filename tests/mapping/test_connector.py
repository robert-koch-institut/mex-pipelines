from mex.common.models import ExtractedAccessPlatform
from mex.common.types import AssetsPath, TechnicalAccessibility, TextLanguage
from mex.mapping.connector import get_mapping_model


def test_get_mapping_model() -> None:
    mapping_path = AssetsPath(
        "assets/mappings/__final__/test_mapping/access-platform.yaml"
    )

    mapping_model = get_mapping_model(mapping_path, ExtractedAccessPlatform)

    expected = {
        "identifier": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"rule": "Assign identifier."}],
            }
        ],
        "hadPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "rule": "Assign 'stable target id' of primary source with identifier 'nokeda' in /raw-data/primary-sources/primary-sources.json."
                    }
                ],
            }
        ],
        "identifierInPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["sumo-db"], "rule": "Use value as it is."}
                ],
            }
        ],
        "stableTargetId": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"rule": "Assign 'stable target id'  of merged item."}
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
        "technicalAccessibility": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [TechnicalAccessibility["INTERNAL"]]}],
                "comment": "internal",
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {"value": "SUMO Datenbank", "language": TextLanguage.DE}
                        ]
                    }
                ],
            }
        ],
        "unitInCharge": [
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
    assert mapping_model.model_dump(exclude_defaults=True) == expected
