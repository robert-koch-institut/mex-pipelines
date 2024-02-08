from typing import Any

from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedDistribution,
    ExtractedPrimarySource,
)
from mex.common.testing import Joker
from mex.common.types import (
    TextLanguage,
    Timestamp,
)
from mex.seq_repo.models.source import SeqRepoSource
from mex.seq_repo.transform import (
    transform_seq_repo_access_platform_to_extracted_access_platform,
    transform_seq_repo_activities_to_extracted_activities,
    transform_seq_repo_distribution_to_extracted_distribution,
    transform_seq_repo_resource_to_extracted_resource,
)


def test_transform_seq_repo_activities_to_extracted_activities(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    seq_repo_activity: dict[str, Any],
) -> None:
    expected = {
        "identifier": Joker(),
        "hadPrimarySource": extracted_primary_source_seq_repo.stableTargetId,
        "identifierInPrimarySource": "TEST-ID",
        "stableTargetId": Joker(),
        "contact": [Joker()],
        "responsibleUnit": [Joker()],
        "theme": [
            "https://mex.rki.de/item/theme-11",
            "https://mex.rki.de/item/theme-34",
        ],
        "title": [{"value": "FG99-ABC-123", "language": TextLanguage.DE}],
    }

    extracted_mex_activities = list(
        transform_seq_repo_activities_to_extracted_activities(
            seq_repo_latest_sources,
            seq_repo_activity,
            extracted_primary_source_seq_repo,
        )
    )

    assert (
        extracted_mex_activities[0].model_dump(exclude_none=True, exclude_defaults=True)
        == expected
    )


def test_transform_seq_repo_distribution_to_extracted_distribution(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    extracted_mex_access_platform: ExtractedAccessPlatform,
    seq_repo_distribution: dict[str, Any],
) -> None:
    extracted_mex_distributions = list(
        (
            transform_seq_repo_distribution_to_extracted_distribution(
                seq_repo_latest_sources,
                seq_repo_distribution,
                extracted_mex_access_platform,
                extracted_primary_source_seq_repo,
            )
        )
    )

    expected = {
        "identifier": Joker(),
        "hadPrimarySource": extracted_primary_source_seq_repo.stableTargetId,
        "identifierInPrimarySource": "test-sample-id.TEST",
        "stableTargetId": Joker(),
        "accessService": extracted_mex_access_platform.stableTargetId,
        "accessRestriction": "https://mex.rki.de/item/access-restriction-2",
        "issued": "2023-08-07",
        "mediaType": "https://mex.rki.de/item/mime-type-12",
        "publisher": Joker(),
        "title": "dummy-fastq-file",
    }

    assert (
        extracted_mex_distributions[0].model_dump(
            exclude_none=True, exclude_defaults=True
        )
        == expected
    )


def test_transform_seq_repo_resource_to_extracted_resource(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_latest_sources: dict[str, SeqRepoSource],
    extracted_mex_distribution_dict: dict[str, ExtractedDistribution],
    extracted_mex_activities_dict: dict[str, ExtractedActivity],
    seq_repo_resource: dict[str, Any],
) -> None:
    extracted_mex_resources = list(
        transform_seq_repo_resource_to_extracted_resource(
            seq_repo_latest_sources,
            extracted_mex_distribution_dict,
            extracted_mex_activities_dict,
            seq_repo_resource,
            extracted_primary_source_seq_repo,
        )
    )

    distribution = extracted_mex_distribution_dict["test-sample-id.TEST"]
    activity = extracted_mex_activities_dict["TEST-ID"]

    expected = {
        "identifier": Joker(),
        "hadPrimarySource": extracted_primary_source_seq_repo.stableTargetId,
        "identifierInPrimarySource": "test-sample-id.TEST",
        "stableTargetId": Joker(),
        "accessRestriction": "https://mex.rki.de/item/access-restriction-2",
        "accrualPeriodicity": "https://mex.rki.de/item/frequency-15",
        "anonymizationPseudonymization": [
            "https://mex.rki.de/item/anonymization-pseudonymization-2"
        ],
        "contact": [Joker()],
        "created": Timestamp("2023-08-07"),
        "distribution": [distribution.stableTargetId],
        "instrumentToolOrApparatus": [{"value": "TEST"}],
        "keyword": [
            {
                "value": "Severe acute respiratory syndrome coronavirus 2",
                "language": TextLanguage.EN,
            }
        ],
        "method": [
            {"value": "Next-Generation Sequencing", "language": TextLanguage.EN},
            {"value": "NGS", "language": TextLanguage.EN},
        ],
        "resourceTypeGeneral": ["https://mex.rki.de/item/resource-type-general-1"],
        "resourceTypeSpecific": [
            {"value": "Sequencing Data", "language": TextLanguage.EN},
            {"value": "Sequenzdaten", "language": TextLanguage.DE},
        ],
        "rights": [{"value": "Dummy rights value.", "language": TextLanguage.DE}],
        "stateOfDataProcessing": ["https://mex.rki.de/item/data-processing-state-1"],
        "theme": [
            "https://mex.rki.de/item/theme-11",
            "https://mex.rki.de/item/theme-34",
        ],
        "title": [
            {
                "value": "FG99-ABC-123 sample test-customer-name-1",
                "language": TextLanguage.EN,
            }
        ],
        "unitInCharge": [Joker()],
        "wasGeneratedBy": activity.stableTargetId,
    }

    assert (
        extracted_mex_resources[0].model_dump(exclude_none=True, exclude_defaults=True)
        == expected
    )


def test_transform_seq_repo_access_platform_to_extracted_access_platform(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    seq_repo_access_platform: dict[str, Any],
) -> None:
    expected = {
        "identifier": Joker(),
        "hadPrimarySource": extracted_primary_source_seq_repo.stableTargetId,
        "identifierInPrimarySource": "https://dummy.url.com/",
        "stableTargetId": Joker(),
        "alternativeTitle": [{"value": "SeqRepo"}],
        "description": [
            {
                "value": "This is just a sample description, don't read it.",
                "language": TextLanguage.EN,
            }
        ],
        "endpointType": "https://mex.rki.de/item/api-type-1",
        "landingPage": [{"url": "https://dummy.url.com/"}],
        "technicalAccessibility": "https://mex.rki.de/item/technical-accessibility-1",
        "title": [{"value": "Sequence Data Repository"}],
    }

    extracted_mex_access_platform = (
        transform_seq_repo_access_platform_to_extracted_access_platform(
            seq_repo_access_platform,
            extracted_primary_source_seq_repo,
        )
    )

    assert (
        extracted_mex_access_platform.model_dump(
            exclude_none=True, exclude_defaults=True
        )
        == expected
    )
