import pytest

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
from mex.seq_repo.filter import filter_sources_on_latest_sequencing_date
from mex.seq_repo.models.access_platform import SeqRepoAccessPlatform
from mex.seq_repo.models.activity import SeqRepoActivity
from mex.seq_repo.models.distribution import SeqRepoDistribution
from mex.seq_repo.models.resource import SeqRepoResource
from mex.seq_repo.models.source import SeqRepoSource
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


@pytest.fixture()
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


@pytest.fixture()
def seq_repo_latest_sources(
    seq_repo_sources: list[SeqRepoSource],
) -> dict[str, SeqRepoSource]:
    return filter_sources_on_latest_sequencing_date(seq_repo_sources)


@pytest.fixture()
def seq_repo_activity() -> SeqRepoActivity:
    return SeqRepoActivity(
        theme=[
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
    )


@pytest.fixture()
def seq_repo_distribution() -> SeqRepoDistribution:
    return SeqRepoDistribution(
        access_restriction=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
            }
        ],
        media_type=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/mime-type-12"]}
                ],
            }
        ],
        title=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["dummy-fastq-file"]}],
                "comment": "So there must be rules for titles.",
            }
        ],
        publisher=[
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
    )


@pytest.fixture()
def seq_repo_access_platform() -> SeqRepoAccessPlatform:
    return SeqRepoAccessPlatform(
        alternative_title=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"value": "SeqRepo"}]}],
            }
        ],
        contact=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"forValues": ["fg99"], "rule": "Hmm, where are the rules?"}
                ],
            }
        ],
        description=[
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
        endpoint_type=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://mex.rki.de/item/api-type-1"]}],
            }
        ],
        identifier_in_primary_source=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": ["https://dummy.url.com/"]}],
            }
        ],
        landing_page=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"setValues": [{"url": "https://dummy.url.com/"}]}],
            }
        ],
        technical_accessibility=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/technical-accessibility-1"]}
                ],
            }
        ],
        title=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"value": "Sequence Data Repository"}]}
                ],
            }
        ],
        unit_in_charge=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [{"forValues": ["fg99"], "rule": "dummy rule"}],
            }
        ],
    )


@pytest.fixture()
def seq_repo_resource() -> SeqRepoResource:
    return SeqRepoResource(
        access_restriction=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/access-restriction-2"]}
                ],
            }
        ],
        accrual_periodicity=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/frequency-15"]}
                ],
            }
        ],
        anonymization_pseudonymization=[
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
        method=[
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
        resource_type_general=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/resource-type-general-1"]}
                ],
            }
        ],
        resource_type_specific=[
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
        rights=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": [{"language": "de", "value": "Dummy rights value."}]}
                ],
            }
        ],
        state_of_data_processing=[
            {
                "fieldInPrimarySource": "n/a",
                "mappingRules": [
                    {"setValues": ["https://mex.rki.de/item/data-processing-state-1"]}
                ],
            }
        ],
        publisher=[
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
        theme=[
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
    )


@pytest.fixture()
def extracted_mex_access_platform(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_access_platform: SeqRepoAccessPlatform,
) -> ExtractedAccessPlatform:
    return transform_seq_repo_access_platform_to_extracted_access_platform(
        seq_repo_access_platform,
        extracted_primary_source_seq_repo,
    )


@pytest.fixture()
def extracted_mex_activities_dict(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    seq_repo_activity: SeqRepoActivity,
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


@pytest.fixture()
def extracted_mex_distribution_dict(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    extracted_mex_access_platform: ExtractedAccessPlatform,
    seq_repo_distribution: SeqRepoDistribution,
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
