from itertools import tee

from mex.common.cli import entrypoint
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedDistribution,
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.common.types import AssetsPath
from mex.mapping.extract import extract_mapping_model
from mex.pipeline import asset, run_job_in_process
from mex.seq_repo.extract import (
    extract_sources,
)
from mex.seq_repo.filter import filter_sources_on_latest_sequencing_date
from mex.seq_repo.models.source import SeqRepoSource
from mex.seq_repo.settings import SeqRepoSettings
from mex.seq_repo.transform import (
    transform_seq_repo_access_platform_to_extracted_access_platform,
    transform_seq_repo_activities_to_extracted_activities,
    transform_seq_repo_distribution_to_extracted_distribution,
    transform_seq_repo_resource_to_extracted_resource,
)
from mex.sinks import load


@asset(group_name="seq_repo", deps=["extracted_primary_source_mex"])
def extracted_primary_source_seq_repo(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return Seq-Repo primary source."""
    (extracted_primary_source,) = get_primary_sources_by_name(
        extracted_primary_sources, "seq-repo"
    )
    load([extracted_primary_source])

    return extracted_primary_source


@asset(group_name="seq_repo")
def seq_repo_source() -> list[SeqRepoSource]:
    """Extract sources from Seq-Repo."""
    return list(extract_sources())


@asset(group_name="seq_repo")
def seq_repo_latest_source(
    seq_repo_source: list[SeqRepoSource],
) -> dict[str, SeqRepoSource]:
    """Filter latest sources from Seq-Repo source."""
    return filter_sources_on_latest_sequencing_date(seq_repo_source)


@asset(group_name="seq_repo")
def extracted_activity(
    seq_repo_latest_source: dict[str, SeqRepoSource],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
) -> dict[str, ExtractedActivity]:
    """Extract activities from Seq-Repo."""
    settings = SeqRepoSettings.get()
    activity = extract_mapping_model(
        AssetsPath(settings.mapping_path / "activity.yaml"), ExtractedActivity
    ).model_dump()
    mex_activities = transform_seq_repo_activities_to_extracted_activities(
        seq_repo_latest_source, activity, extracted_primary_source_seq_repo
    )
    mex_activities_gens = tee(mex_activities, 2)
    load(mex_activities_gens[0])

    return {
        activity.identifierInPrimarySource: activity
        for activity in mex_activities_gens[1]
    }


@asset(group_name="seq_repo")
def extracted_access_platform(
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
) -> ExtractedAccessPlatform:
    """Extract access platform from Seq-Repo."""
    settings = SeqRepoSettings.get()
    access_platform = extract_mapping_model(
        AssetsPath(settings.mapping_path / "access-platform.yaml"),
        ExtractedAccessPlatform,
    ).model_dump()
    mex_access_platform = (
        transform_seq_repo_access_platform_to_extracted_access_platform(
            access_platform,
            extracted_primary_source_seq_repo,
        )
    )
    load([mex_access_platform])

    return mex_access_platform


@asset(group_name="seq_repo")
def extracted_distribution(
    seq_repo_latest_source: dict[str, SeqRepoSource],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
    extracted_access_platform: ExtractedAccessPlatform,
) -> dict[str, ExtractedDistribution]:
    """Extract distribution from Seq-Repo."""
    settings = SeqRepoSettings.get()
    distribution = extract_mapping_model(
        AssetsPath(settings.mapping_path / "distribution.yaml"),
        ExtractedDistribution,
    ).model_dump()
    mex_distributions = transform_seq_repo_distribution_to_extracted_distribution(
        seq_repo_latest_source,
        distribution,
        extracted_access_platform,
        extracted_primary_source_seq_repo,
    )

    mex_distributions_gens = tee(mex_distributions, 2)
    load(mex_distributions_gens[0])
    return {
        distribution.identifierInPrimarySource: distribution
        for distribution in mex_distributions_gens[1]
    }


@asset(group_name="seq_repo")
def seq_repo_resource(
    seq_repo_latest_source: dict[str, SeqRepoSource],
    extracted_distribution: dict[str, ExtractedDistribution],
    extracted_activity: dict[str, ExtractedActivity],
    extracted_primary_source_seq_repo: ExtractedPrimarySource,
) -> list[ExtractedResource]:
    """Extract resource from Seq-Repo."""
    settings = SeqRepoSettings.get()
    resource = extract_mapping_model(
        AssetsPath(settings.mapping_path / "resource.yaml"),
        ExtractedResource,
    ).model_dump()

    mex_resources = transform_seq_repo_resource_to_extracted_resource(
        seq_repo_latest_source,
        extracted_distribution,
        extracted_activity,
        resource,
        extracted_primary_source_seq_repo,
    )

    mex_sources_list = list(mex_resources)
    load(mex_sources_list)

    return list(mex_sources_list)


@entrypoint(SeqRepoSettings)
def run() -> None:
    """Run the seq-repo extractor job in-process."""
    run_job_in_process("seq_repo")
