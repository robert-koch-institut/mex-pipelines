from mex.seq_repo.extract import (
    extract_access_platform,
    extract_activity,
    extract_distribution,
    extract_resource,
    extract_sources,
)


def test_extract_sources() -> None:
    sources = list(extract_sources())
    expected = {
        "project_coordinators": ["max", "mustermann", "yee-haw"],
        "customer_org_unit_id": "FG99",
        "sequencing_date": "2023-08-07",
        "lims_sample_id": "test-sample-id",
        "sequencing_platform": "TEST",
        "species": "Severe acute respiratory syndrome coronavirus 2",
        "project_name": "FG99-ABC-123",
        "customer_sample_name": "test-customer-name-1",
        "project_id": "TEST-ID",
    }
    assert sources[0].model_dump() == expected


def test_access_platform() -> None:
    access_platform = extract_access_platform()

    expected = {
        "alternative_title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"value": "SeqRepo"}]}],
            }
        ],
        "contact": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"forValues": ["fg99"], "rule": "Hmm, where are the rules?"}
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
                                "language": "en",
                                "value": "This is just a sample description, don't read it.",
                            }
                        ]
                    }
                ],
            }
        ],
        "endpoint_type": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://mex.rki.de/item/api-type-1"]}],
            }
        ],
        "identifier_in_primary_source": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://dummy.url.com/"]}],
            }
        ],
        "landing_page": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"url": "https://dummy.url.com/"}]}],
            }
        ],
        "technical_accessibility": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/technical-accessibility-1"]}
                ],
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"value": "Sequence Data Repository"}]}
                ],
            }
        ],
        "unit_in_charge": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"forValues": ["fg99"], "rule": "dummy rule"}],
            }
        ],
    }

    assert access_platform.model_dump() == expected


def test_extract_activity() -> None:
    activity = extract_activity()
    expected = {
        "theme": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            "https://mex.rki.de/item/theme-11",
                            "https://mex.rki.de/item/theme-34",
                        ]
                    }
                ],
            }
        ]
    }
    assert activity.model_dump() == expected


def test_extract_distribution() -> None:
    distribution = extract_distribution()
    expected = {
        "access_restriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
            }
        ],
        "media_type": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/mime-type-12"]}
                ],
            }
        ],
        "title": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["dummy-fastq-file"]}],
                "comment": "So there must be rules for titles.",
            }
        ],
        "publisher": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Dummy Publisher"],
                        "rule": "There are rules in life.",
                    }
                ],
            }
        ],
    }
    assert distribution.model_dump() == expected


def test_extract_resource() -> None:
    resource = extract_resource()
    expected = {
        "access_restriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
            }
        ],
        "accrual_periodicity": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/frequency-15"]}
                ],
            }
        ],
        "anonymization_pseudonymization": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            "https://mex.rki.de/item/anonymization-pseudonymization-2"
                        ]
                    }
                ],
            }
        ],
        "method": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {"language": "en", "value": "Next-Generation Sequencing"},
                            {"language": "en", "value": "NGS"},
                        ]
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
            }
        ],
        "resource_type_specific": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            {"language": "en", "value": "Sequencing Data"},
                            {"language": "de", "value": "Sequenzdaten"},
                        ]
                    }
                ],
            }
        ],
        "rights": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "Dummy rights value."}]}
                ],
            }
        ],
        "state_of_data_processing": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/data-processing-state-1"]}
                ],
            }
        ],
        "publisher": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "forValues": ["Dummy Publisher"],
                        "rule": "This rule is just a dummy rule.",
                    }
                ],
            }
        ],
        "theme": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {
                        "setValues": [
                            "https://mex.rki.de/item/theme-11",
                            "https://mex.rki.de/item/theme-34",
                        ]
                    }
                ],
            }
        ],
    }
    assert resource.model_dump() == expected
