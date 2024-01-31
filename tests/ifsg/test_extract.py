import pytest

from mex.ifsg.extract import (
    extract_ifsg_variable_group,
    extract_resource_disease,
    extract_resource_parent,
    extract_resource_state,
    extract_sql_table,
)
from mex.ifsg.models.meta_schema2type import MetaSchema2Type


def test_extract_resource_disease() -> None:
    resource_disease = list(extract_resource_disease())
    expected = [
        (
            "access_restriction",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                    ],
                    "comment": "restriktiv",
                }
            ],
        ),
        (
            "accrual_periodicity",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/frequency-17"]}
                    ],
                    "comment": "unregelmäßig",
                }
            ],
        ),
        (
            "alternative_title",
            [
                {
                    "fieldInPrimarySource": "Code",
                    "locationInPrimarySource": "Meta.Disease",
                    "examplesInPrimarySource": ["BAN", "BOB"],
                    "mappingRules": [
                        {"rule": "Use value as it is. Do not assign a language."}
                    ],
                }
            ],
        ),
        (
            "contact",
            [
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
        ),
        ("description", []),
        (
            "identifier_in_primary_source",
            [
                {
                    "fieldInPrimarySource": "IdType",
                    "locationInPrimarySource": "Meta.Disease",
                    "examplesInPrimarySource": ["102"],
                    "mappingRules": [{"rule": "Use value as it is."}],
                }
            ],
        ),
        (
            "instrument_tool_or_apparatus",
            [
                {
                    "fieldInPrimarySource": 'ReferenceDef[A|B|C|D|E]="1"',
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["A=1"],
                            "setValues": [
                                {"language": "de", "value": "Falldefinition A"}
                            ],
                        },
                        {
                            "forValues": ["B=1"],
                            "setValues": [
                                {"language": "de", "value": "Falldefinition B"}
                            ],
                        },
                        {
                            "forValues": ["C=1"],
                            "setValues": [
                                {"language": "de", "value": "Falldefinition C"}
                            ],
                        },
                        {
                            "forValues": ["D=1"],
                            "setValues": [
                                {"language": "de", "value": "Falldefinition D"}
                            ],
                        },
                        {
                            "forValues": ["E=1"],
                            "setValues": [
                                {"language": "de", "value": "Falldefinition E"}
                            ],
                        },
                    ],
                }
            ],
        ),
        (
            "is_part_of",
            [
                {
                    "fieldInPrimarySource": "IFSGBundesland",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {"forValues": ["0"]},
                        {
                            "rule": "Assign 'stable target id' of the item described by /mappings/../ifsg/resource_parent"
                        },
                    ],
                },
                {
                    "fieldInPrimarySource": 'IFSGBundesland="1" and InBundesland',
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["07"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='07' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["09"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='09' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["10"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='10' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["11"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='11' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["12"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='12' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["13"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='13' as  described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["14"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='14' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["15"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='15' as described by mapping/../ifsg/resource_state",
                        },
                        {
                            "forValues": ["16"],
                            "rule": "Assign 'stable target id' of the item with identiferInPrimarySource='16' as described by mapping/../ifsg/resource_state",
                        },
                    ],
                },
            ],
        ),
        (
            "keyword",
            [
                {
                    "fieldInPrimarySource": "DiseaseName",
                    "locationInPrimarySource": "Meta.Disease",
                    "examplesInPrimarySource": ["Milzbrand", "Borreliose"],
                    "mappingRules": [
                        {
                            "rule": "Assign 'de' as default for the language property of the text object."
                        }
                    ],
                },
                {
                    "fieldInPrimarySource": "DiseaseNameEN",
                    "locationInPrimarySource": "Meta.Disease",
                    "examplesInPrimarySource": ["Anthrax", "Lyme disease"],
                    "mappingRules": [
                        {
                            "rule": "Assign 'en' as default for the language property of the text object."
                        }
                    ],
                },
                {
                    "fieldInPrimarySource": "SpecimenName",
                    "locationInPrimarySource": "Meta.Disease",
                    "examplesInPrimarySource": [
                        "Bacillus anthracis",
                        "Borelia burgdorferi",
                    ],
                    "mappingRules": [
                        {"rule": "Use value as it is. Use language detection."}
                    ],
                },
            ],
        ),
        (
            "language",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/language-1"]}
                    ],
                    "comment": "Deutsch",
                }
            ],
        ),
        (
            "publication",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Falldefinitionen",
                                    "url": "https://www.rki.de/DE/Content/Infekt/IfSG/Falldefinition/falldefinition_node.html",
                                }
                            ]
                        }
                    ],
                }
            ],
        ),
        (
            "resource_type_general",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                "https://mex.rki.de/item/resource-type-general-1"
                            ]
                        }
                    ],
                    "comment": "Public Health Fachdaten",
                }
            ],
        ),
        (
            "resource_type_specific",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": [{"language": "de", "value": "Meldedaten"}]}
                    ],
                }
            ],
        ),
        (
            "rights",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {"language": "de", "value": "Gesundheitsdaten."}
                            ]
                        }
                    ],
                }
            ],
        ),
        (
            "spatial",
            [
                {
                    "fieldInPrimarySource": 'IFSGBundesland="0"',
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {"setValues": [{"language": "de", "value": "Deutschland"}]}
                    ],
                },
                {
                    "fieldInPrimarySource": 'IFSGBundesland="1" and InBundesland',
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["07"],
                            "setValues": [
                                {"language": "de", "value": "Rheinland-Pfalz"}
                            ],
                        },
                        {
                            "forValues": ["09"],
                            "setValues": [{"language": "de", "value": "Bayern"}],
                        },
                        {
                            "forValues": ["10"],
                            "setValues": [{"language": "de", "value": "Saarland"}],
                        },
                        {
                            "forValues": ["11"],
                            "setValues": [{"language": "de", "value": "Berlin"}],
                        },
                        {
                            "forValues": ["12"],
                            "setValues": [{"language": "de", "value": "Brandenburg"}],
                        },
                        {
                            "forValues": ["13"],
                            "setValues": [
                                {"language": "de", "value": "Mecklenburg-Vorpommern"}
                            ],
                        },
                        {
                            "forValues": ["14"],
                            "setValues": [{"language": "de", "value": "Sachsen"}],
                        },
                        {
                            "forValues": ["15"],
                            "setValues": [
                                {"language": "de", "value": "Sachsen-Anhalt"}
                            ],
                        },
                        {
                            "forValues": ["16"],
                            "setValues": [{"language": "de", "value": "Thüringen"}],
                        },
                    ],
                },
            ],
        ),
        (
            "theme",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                "https://mex.rki.de/item/theme-17",
                                "https://mex.rki.de/item/theme-2",
                            ]
                        }
                    ],
                    "comment": "Meldewesen, Infektionskrankheiten",
                }
            ],
        ),
        (
            "title",
            [
                {
                    "fieldInPrimarySource": "DiseaseName",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "rule": "Construct the title after the following schema: Meldedaten nach Infektionsschutzgesetz (IfSG) zu [DiseaseName]. Assign 'de' as default for the language property of the text object."
                        }
                    ],
                }
            ],
        ),
        (
            "unit_in_charge",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "forValues": ["FG99"],
                            "rule": "Use value to match with identifier from /raw-data/organigram/organizational-units.json.",
                        }
                    ],
                }
            ],
        ),
    ]
    assert resource_disease == expected


def test_extract_resource_parent() -> None:
    resource_parent = list(extract_resource_parent())
    expected = [
        (
            "access_restriction",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                    ],
                    "comment": "restriktiv",
                }
            ],
        ),
        (
            "accrual_periodicity",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/frequency-15"]}
                    ],
                    "comment": "täglich",
                }
            ],
        ),
        (
            "alternative_title",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": [{"language": "de", "value": "IfSG Meldedaten"}]}
                    ],
                }
            ],
        ),
        (
            "contact",
            [
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
        ),
        (
            "description",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "value": "Das Infektionsschutzgesetz",
                                }
                            ]
                        }
                    ],
                }
            ],
        ),
        (
            "identifier_in_primary_source",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": ["ifsg-parent"],
                            "rule": "Use value as indicated.",
                        }
                    ],
                }
            ],
        ),
        ("instrument_tool_or_apparatus", []),
        ("is_part_of", []),
        (
            "keyword",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {"language": "de", "value": "Infektionsschutzgesetz"}
                            ]
                        },
                        {
                            "setValues": [
                                {"language": "de", "value": "Infektionsschutz"}
                            ]
                        },
                    ],
                }
            ],
        ),
        (
            "language",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/language-1"]}
                    ],
                    "comment": "Deutsch",
                }
            ],
        ),
        (
            "publication",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Infektionsepidemiologisches Jahrbuch",
                                    "url": "https://www.rki.de/DE/Content/Infekt/Jahrbuch/jahrbuch_node.html",
                                }
                            ]
                        },
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Epidemiologisches Bulletin",
                                    "url": "https://www.rki.de/DE/Content/Infekt/EpidBull/epid_bull_node.html",
                                }
                            ]
                        },
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Falldefinitionen",
                                    "url": "https://www.rki.de/DE/Content/Infekt/IfSG/Falldefinition/falldefinition_node.html",
                                }
                            ]
                        },
                    ],
                }
            ],
        ),
        (
            "resource_type_general",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                "https://mex.rki.de/item/resource-type-general-1"
                            ]
                        }
                    ],
                    "comment": "Public Health Fachdaten",
                }
            ],
        ),
        (
            "resource_type_specific",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": [{"language": "de", "value": "Meldedaten"}]}
                    ],
                }
            ],
        ),
        (
            "rights",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {"language": "de", "value": "Gesundheitsdaten."}
                            ]
                        }
                    ],
                }
            ],
        ),
        (
            "spatial",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": [{"language": "de", "value": "Deutschland"}]}
                    ],
                }
            ],
        ),
        (
            "theme",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/theme-17"]},
                        {"setValues": ["https://mex.rki.de/item/theme-2"]},
                    ],
                    "comment": "Meldewesen, Infektionskrankheiten",
                }
            ],
        ),
        (
            "title",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "value": "Meldedaten nach Infektionsschutzgesetz (IfSG)",
                                }
                            ]
                        }
                    ],
                }
            ],
        ),
        (
            "unit_in_charge",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "forValues": ["FG99"],
                            "rule": "Use value to match identifer using /raw-data/organigram/organizational-units.json.",
                        }
                    ],
                }
            ],
        ),
    ]

    assert resource_parent == expected


def test_extract_resource_state() -> None:
    resource_state = list(extract_resource_state())
    expected = [
        (
            "access_restriction",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                    ],
                    "comment": "restriktiv",
                }
            ],
        ),
        (
            "accrual_periodicity",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/frequency-17"]}
                    ],
                    "comment": "unregelmäßig",
                }
            ],
        ),
        (
            "alternative_title",
            [
                {
                    "fieldInPrimarySource": "InBundesland",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["01"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "value": "Meldedaten Schleswig-Holstein",
                                }
                            ],
                        },
                        {
                            "forValues": ["02"],
                            "setValues": [
                                {"language": "de", "value": "Meldedaten Hamburg"}
                            ],
                        },
                    ],
                }
            ],
        ),
        (
            "contact",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [{"forValues": ["FG99"]}],
                }
            ],
        ),
        ("description", []),
        (
            "identifier_in_primary_source",
            [
                {
                    "fieldInPrimarySource": "InBundesland",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {"forValues": ["01"], "setValues": ["01"]},
                        {"forValues": ["02"], "setValues": ["02"]},
                        {"forValues": ["03"], "setValues": ["03"]},
                        {"forValues": ["04"], "setValues": ["04"]},
                        {"forValues": ["05"], "setValues": ["05"]},
                        {"forValues": ["06"], "setValues": ["06"]},
                        {"forValues": ["07"], "setValues": ["07"]},
                        {"forValues": ["08"], "setValues": ["08"]},
                        {"forValues": ["09"], "setValues": ["09"]},
                        {"forValues": ["10"], "setValues": ["10"]},
                        {"forValues": ["11"], "setValues": ["11"]},
                        {"forValues": ["12"], "setValues": ["12"]},
                        {"forValues": ["13"], "setValues": ["13"]},
                        {"forValues": ["14"], "setValues": ["14"]},
                        {"forValues": ["15"], "setValues": ["15"]},
                        {"forValues": ["16"], "setValues": ["16"]},
                    ],
                }
            ],
        ),
        ("instrument_tool_or_apparatus", []),
        (
            "is_part_of",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "rule": "Use the 'stable target id' of item described by mapping/../ifsg/resource_parent"
                        }
                    ],
                }
            ],
        ),
        (
            "keyword",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {"language": "de", "value": "Infektionsschutzgesetz"}
                            ]
                        },
                        {
                            "setValues": [
                                {"language": "de", "value": "Infektionsschutz"}
                            ]
                        },
                    ],
                }
            ],
        ),
        (
            "language",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/language-1"]}
                    ],
                    "comment": "Deutsch",
                }
            ],
        ),
        (
            "publication",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Infektionsepidemiologisches Jahrbuch",
                                    "url": "https://www.rki.de/DE/Content/Infekt/Jahrbuch/jahrbuch_node.html",
                                },
                                {
                                    "language": "de",
                                    "title": "Epidemiologisches Bulletin",
                                    "url": "https://www.rki.de/DE/Content/Infekt/EpidBull/epid_bull_node.html",
                                },
                                {
                                    "language": "de",
                                    "title": "Falldefinitionen",
                                    "url": "https://www.rki.de/DE/Content/Infekt/IfSG/Falldefinition/falldefinition_node.html",
                                },
                            ]
                        }
                    ],
                },
                {
                    "fieldInPrimarySource": "InBundesland",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["07"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Rheinland-Pfalz",
                                    "url": "http://landesrecht.rlp.de/jportal/portal/page/bsrlpprod.psml?doc.id=jlr-IfSGMeldpflVRPpP1%3Ajuris-lr00&showdoccase=1&doc.hl=1&documentnumber=1",
                                }
                            ],
                        },
                        {
                            "forValues": ["09"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Bayern",
                                    "url": "https://www.gesetze-bayern.de/Content/Document/BayMeldePflV/true",
                                }
                            ],
                        },
                        {
                            "forValues": ["10"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Saarland",
                                    "url": "https://www.saarland.de/msgff/DE/portale/gesundheitundpraevention/leistungenabisz/gesundheitsschutz/infektionsschutzgesetz/infektionsschutzgesetz.html",
                                }
                            ],
                        },
                        {
                            "forValues": ["11"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Berlin",
                                    "url": "https://gesetze.berlin.de/bsbe/document/jlr-IfSGMeldpflVBEpP1",
                                }
                            ],
                        },
                        {
                            "forValues": ["12"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Brandenburg",
                                    "url": "https://bravors.brandenburg.de/verordnungen/infkrankmv_2016",
                                }
                            ],
                        },
                        {
                            "forValues": ["13"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Mecklenburg-Vorpommern",
                                    "url": "https://www.landesrecht-mv.de/bsmv/document/jlr-InfSchAGMVrahmen",
                                }
                            ],
                        },
                        {
                            "forValues": ["14"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Sachsen",
                                    "url": "https://www.revosax.sachsen.de/vorschrift/1307-IfSGMeldeVO",
                                }
                            ],
                        },
                        {
                            "forValues": ["15"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Sachsen-Anhalt",
                                    "url": "https://www.landesrecht.sachsen-anhalt.de/bsst/document/jlr-IfSGMeldpflVST2005rahmen",
                                }
                            ],
                        },
                        {
                            "forValues": ["16"],
                            "setValues": [
                                {
                                    "language": "de",
                                    "title": "Thüringen",
                                    "url": "https://landesrecht.thueringen.de/bsth/document/jlr-IfKrMeldAnpVTHrahmen",
                                }
                            ],
                        },
                    ],
                },
            ],
        ),
        (
            "resource_type_general",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                "https://mex.rki.de/item/resource-type-general-1"
                            ]
                        }
                    ],
                    "comment": "Public Health Fachdaten",
                }
            ],
        ),
        (
            "resource_type_specific",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": [{"language": "de", "value": "Meldedaten"}]}
                    ],
                }
            ],
        ),
        (
            "rights",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "setValues": [
                                {"language": "de", "value": "Gesundheitsdaten."}
                            ]
                        }
                    ],
                }
            ],
        ),
        (
            "spatial",
            [
                {
                    "fieldInPrimarySource": "InBundesland",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["01"],
                            "setValues": [
                                {"language": "de", "value": "Schleswig-Holstein"}
                            ],
                        },
                        {
                            "forValues": ["02"],
                            "setValues": [{"language": "de", "value": "Hamburg"}],
                        },
                        {
                            "forValues": ["03"],
                            "setValues": [{"language": "de", "value": "Niedersachsen"}],
                        },
                        {
                            "forValues": ["04"],
                            "setValues": [{"language": "de", "value": "Bremen"}],
                        },
                        {
                            "forValues": ["05"],
                            "setValues": [
                                {"language": "de", "value": "Nordrhein-Westfalen"}
                            ],
                        },
                        {
                            "forValues": ["06"],
                            "setValues": [{"language": "de", "value": "Hessen"}],
                        },
                        {
                            "forValues": ["07"],
                            "setValues": [
                                {"language": "de", "value": "Rheinland-Pfalz"}
                            ],
                        },
                        {
                            "forValues": ["08"],
                            "setValues": [
                                {"language": "de", "value": "Baden-Württemberg"}
                            ],
                        },
                        {
                            "forValues": ["09"],
                            "setValues": [{"language": "de", "value": "Bayern"}],
                        },
                        {
                            "forValues": ["10"],
                            "setValues": [{"language": "de", "value": "Saarland"}],
                        },
                        {
                            "forValues": ["11"],
                            "setValues": [{"language": "de", "value": "Berlin"}],
                        },
                        {
                            "forValues": ["12"],
                            "setValues": [{"language": "de", "value": "Brandenburg"}],
                        },
                        {
                            "forValues": ["13"],
                            "setValues": [
                                {"language": "de", "value": "Mecklenburg-Vorpommern"}
                            ],
                        },
                        {
                            "forValues": ["14"],
                            "setValues": [{"language": "de", "value": "Sachsen"}],
                        },
                        {
                            "forValues": ["15"],
                            "setValues": [
                                {"language": "de", "value": "Sachsen-Anhalt"}
                            ],
                        },
                        {
                            "forValues": ["16"],
                            "setValues": [{"language": "de", "value": "Thüringen"}],
                        },
                    ],
                }
            ],
        ),
        (
            "theme",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {"setValues": ["https://mex.rki.de/item/theme-17"]},
                        {"setValues": ["https://mex.rki.de/item/theme-2"]},
                    ],
                    "comment": "Meldewesen, Infektionskrankheiten",
                }
            ],
        ),
        (
            "title",
            [
                {
                    "fieldInPrimarySource": "InBundesland",
                    "locationInPrimarySource": "Meta.Disease",
                    "mappingRules": [
                        {
                            "forValues": ["01"],
                            "setValues": [
                                {"language": "de", "value": "Schleswig-Holstein"}
                            ],
                        },
                        {
                            "forValues": ["02"],
                            "setValues": [{"language": "de", "value": "Hamburg"}],
                        },
                        {
                            "forValues": ["03"],
                            "setValues": [{"language": "de", "value": "Niedersachsen"}],
                        },
                        {
                            "forValues": ["04"],
                            "setValues": [{"language": "de", "value": "Bremen"}],
                        },
                        {
                            "forValues": ["05"],
                            "setValues": [
                                {"language": "de", "value": "Nordrhein-Westfalen"}
                            ],
                        },
                        {
                            "forValues": ["06"],
                            "setValues": [{"language": "de", "value": "Hessen"}],
                        },
                        {
                            "forValues": ["07"],
                            "setValues": [
                                {"language": "de", "value": "Rheinland-Pfalz"}
                            ],
                        },
                        {
                            "forValues": ["08"],
                            "setValues": [
                                {"language": "de", "value": "Baden-Württemberg"}
                            ],
                        },
                        {
                            "forValues": ["09"],
                            "setValues": [{"language": "de", "value": "Bayern"}],
                        },
                        {
                            "forValues": ["10"],
                            "setValues": [{"language": "de", "value": "Saarland"}],
                        },
                        {
                            "forValues": ["11"],
                            "setValues": [{"language": "de", "value": "Berlin."}],
                        },
                        {
                            "forValues": ["12"],
                            "setValues": [{"language": "de", "value": "Brandenburg."}],
                        },
                        {
                            "forValues": ["13"],
                            "setValues": [
                                {"language": "de", "value": "Mecklenburg-Vorpommern."}
                            ],
                        },
                        {
                            "forValues": ["14"],
                            "setValues": [{"language": "de", "value": "Sachsen."}],
                        },
                        {
                            "forValues": ["15"],
                            "setValues": [
                                {"language": "de", "value": "Sachsen-Anhalt."}
                            ],
                        },
                        {
                            "forValues": ["16"],
                            "setValues": [{"language": "de", "value": "Thüringen."}],
                        },
                    ],
                }
            ],
        ),
        (
            "unit_in_charge",
            [
                {
                    "fieldInPrimarySource": "n/a",
                    "mappingRules": [
                        {
                            "forValues": ["FG99"],
                            "rule": "Use value to match with identifer in /raw-data/organigram/organizational-units.json.",
                        }
                    ],
                }
            ],
        ),
    ]

    assert resource_state == expected


def test_extract_ifsg_variable_group() -> None:
    ifsg_variable_group = list(extract_ifsg_variable_group())
    expected = [
        (
            "label",
            [
                {
                    "fieldInPrimarySource": 'StatementAreaGroup="Epi|Technical|Clinical|Outbreak|Patient|AdditionalAttributes|NULL|Event|General|Labor|Address"\'',
                    "locationInPrimarySource": "Meta.Field",
                    "mappingRules": [
                        {
                            "forValues": ["Epi"],
                            "setValues": [
                                {
                                    "value": "Epidemiologische Informationen",
                                    "language": "de",
                                }
                            ],
                        },
                        {
                            "forValues": ["Technical"],
                            "setValues": [
                                {"value": "Technische Angaben", "language": "de"}
                            ],
                        },
                        {
                            "forValues": ["Clinical"],
                            "setValues": [
                                {"value": "Klinische Informationen", "language": "de"}
                            ],
                        },
                        {
                            "forValues": ["Outbreak"],
                            "setValues": [
                                {
                                    "value": "Informationen zum Ausbruch",
                                    "language": "de",
                                }
                            ],
                        },
                        {
                            "forValues": ["Patient"],
                            "setValues": [
                                {"value": "Patienteninformationen", "language": "de"}
                            ],
                        },
                        {
                            "forValues": ["Event"],
                            "setValues": [
                                {
                                    "value": "Informationen zum Ereignis",
                                    "language": "de",
                                }
                            ],
                        },
                        {
                            "forValues": ["General"],
                            "setValues": [
                                {"value": "Administrative Angaben", "language": "de"}
                            ],
                        },
                        {
                            "forValues": ["Labor"],
                            "setValues": [
                                {"value": "Laborinformationen", "language": "de"}
                            ],
                        },
                        {
                            "forValues": ["Address"],
                            "setValues": [
                                {"value": "Adressinformationen", "language": "de"}
                            ],
                        },
                    ],
                }
            ],
        )
    ]
    assert ifsg_variable_group == expected


@pytest.mark.usefixtures("mocked_ifsg")
def test_extract_sql_table() -> None:
    meta_schema2type = extract_sql_table(MetaSchema2Type)
    expected = [
        MetaSchema2Type(id_schema=1, id_type=0),
        MetaSchema2Type(id_schema=1, id_type=11),
    ]
    assert meta_schema2type == expected
