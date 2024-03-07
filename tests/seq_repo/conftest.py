from typing import Any

import pytest

from mex.common.ldap.models.person import LDAPPersonWithQuery
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedDistribution,
    ExtractedPrimarySource,
)
from mex.common.primary_source.extract import extract_seed_primary_sources
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
    transform_seed_primary_sources_to_extracted_primary_sources,
)
from mex.common.types import PersonID
from mex.seq_repo.extract import extract_source_project_coordinator
from mex.seq_repo.filter import filter_sources_on_latest_sequencing_date
from mex.seq_repo.model import SeqRepoSource
from mex.seq_repo.settings import SeqRepoSettings
from mex.seq_repo.transform import (
    transform_seq_repo_access_platform_to_extracted_access_platform,
    transform_seq_repo_activities_to_extracted_activities,
    transform_seq_repo_distribution_to_extracted_distribution,
)


@pytest.fixture(autouse=True)
def settings() -> SeqRepoSettings:
    """Load the settings for this pytest session."""
    return SeqRepoSettings.get()


@pytest.fixture(autouse=True)
def extracted_primary_source_seq_repo() -> ExtractedPrimarySource:
    seed_primary_sources = extract_seed_primary_sources()
    extracted_primary_sources = (
        transform_seed_primary_sources_to_extracted_primary_sources(
            seed_primary_sources
        )
    )

    (extracted_primary_source_seq_repo,) = get_primary_sources_by_name(
        extracted_primary_sources,
        "seq-repo",
    )

    return extracted_primary_source_seq_repo


@pytest.fixture
def seq_repo_sources() -> list[SeqRepoSource]:
    return [
        SeqRepoSource(
            project_coordinators=["max", "mustermann", "yee-haw"],
            customer_org_unit_id="FG99",
            sequencing_date="2023-08-07",
            lims_sample_id="test-sample-id",
            sequencing_platform="TEST",
            species="Severe acute respiratory syndrome coronavirus 2",
            project_name="FG99-ABC-123",
            customer_sample_name="test-customer-name-1",
            project_id="TEST-ID",
        ),
        SeqRepoSource(
            project_coordinators=["jelly", "fish", "turtle"],
            customer_org_unit_id="FG99",
            sequencing_date="2023-08-07",
            lims_sample_id="test-sample-id",
            sequencing_platform="TEST",
            species="Lab rat",
            project_name="FG99-ABC-321",
            customer_sample_name="test-customer-name-2",
            project_id="TEST-ID",
        ),
    ]


@pytest.fixture
def seq_repo_latest_sources(
    seq_repo_sources: list[SeqRepoSource],
) -> dict[str, SeqRepoSource]:
    return filter_sources_on_latest_sequencing_date(seq_repo_sources)


@pytest.fixture
def seq_repo_activity() -> dict[str, Any]:
    return {
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


@pytest.fixture
def seq_repo_distribution() -> dict[str, Any]:
    return {
        "accessRestriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
            }
        ],
        "mediaType": [
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


@pytest.fixture
def seq_repo_access_platform() -> dict[str, Any]:
    return {
        "alternativeTitle": [
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
        "endpointType": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://mex.rki.de/item/api-type-1"]}],
            }
        ],
        "identifierInPrimarySource": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://dummy.url.com/"]}],
            }
        ],
        "landingPage": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"url": "https://dummy.url.com/"}]}],
            }
        ],
        "technicalAccessibility": [
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
        "unitInCharge": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"forValues": ["fg99"], "rule": "dummy rule"}],
            }
        ],
    }


@pytest.fixture
def seq_repo_resource() -> dict[str, Any]:
    return {
        "accessRestriction": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
            }
        ],
        "accrualPeriodicity": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/frequency-15"]}
                ],
            }
        ],
        "anonymizationPseudonymization": [
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
        "resourceTypeGeneral": [
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/resource-type-general-1"]}
                ],
            }
        ],
        "resourceTypeSpecific": [
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
        "stateOfDataProcessing": [
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


@pytest.fixture
def extracted_mex_access_platform(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_access_platform: dict[str, Any],
) -> ExtractedAccessPlatform:
    return transform_seq_repo_access_platform_to_extracted_access_platform(
        seq_repo_access_platform,
        extracted_primary_source_seq_repo,
    )


@pytest.fixture
def extracted_mex_activities_dict(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    seq_repo_activity: dict[str, Any],
) -> dict[str, ExtractedActivity]:
    extracted_mex_activities = transform_seq_repo_activities_to_extracted_activities(
        seq_repo_latest_sources,
        seq_repo_activity,
        extracted_primary_source_seq_repo,
    )

    return {
        activity.identifierInPrimarySource: activity
        for activity in extracted_mex_activities
    }


@pytest.fixture
def extracted_mex_distribution_dict(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    extracted_mex_access_platform: ExtractedAccessPlatform,
    seq_repo_distribution: dict[str, Any],
) -> dict[str, ExtractedDistribution]:
    extracted_mex_distributions = (
        transform_seq_repo_distribution_to_extracted_distribution(
            seq_repo_latest_sources,
            seq_repo_distribution,
            extracted_mex_access_platform,
            extracted_primary_source_seq_repo,
        )
    )
    return {
        distribution.identifierInPrimarySource: distribution
        for distribution in extracted_mex_distributions
    }


@pytest.fixture
def seq_repo_source_project_coordinators(
    seq_repo_latest_sources: dict[str, SeqRepoSource],
) -> list[LDAPPersonWithQuery]:
    """Extract source project coordinators."""
    return list(extract_source_project_coordinator(seq_repo_latest_sources))


@pytest.fixture
def project_coordinators_merged_ids_by_query_string() -> dict[str, list[PersonID]]:
    """Get project coordinators merged ids."""
    return {
        "mustermann": [PersonID("e0Rxxm9WvnMqPLZ44UduNx")],
        "max": [PersonID("d6Lni0XPiEQM5jILEBOYxO")],
        "jelly": [PersonID("buTvstFluFUX9TeoHlhe7c")],
        "fish": [PersonID("gOwHDDA0HQgT1eDYnC4Ai5")],
    }


# @pytest.fixture
# def unit_stable_target_ids_by_synonym(
#     extracted_primary_sources: dict[str, ExtractedPrimarySource],
# ) -> dict[str, OrganizationalUnitID]:
#     """Extract the dummy units and return them grouped by synonyms."""
#     organigram_units = extract_organigram_units()
#     mex_organizational_units = transform_organigram_units_to_organizational_units(
#         organigram_units, extracted_primary_sources["organigram"]
#     )
#     return get_unit_merged_ids_by_synonyms(mex_organizational_units)
