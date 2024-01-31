import json
from typing import Generator

import yaml

from mex.seq_repo.models import (
    SeqRepoAccessPlatform,
    SeqRepoActivity,
    SeqRepoDistribution,
    SeqRepoResource,
    SeqRepoSource,
)
from mex.seq_repo.settings import SeqRepoSettings


def extract_sources() -> Generator[SeqRepoSource, None, None]:
    """Extract Seq Repo sources by loading data from source json file.

    Settings:
        default_json_file_path: Path to the seq-repo json file,
                                absolute or relative to `assets_dir`

    Returns:
        Generator for Seq Repo resources
    """
    settings = SeqRepoSettings.get()
    with open(settings.default_json_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            yield SeqRepoSource.model_validate(item)


def extract_access_platform() -> SeqRepoAccessPlatform:
    """Extract Seq Repo access-platform from mapping.

    Settings:
        mapping_path: Path to the seq-repo activity mappings,
                      absolute or relative to `assets_dir`

    Returns:
        Seq Repo Access_Platform
    """
    settings = SeqRepoSettings.get()
    with open(
        settings.mapping_path / "access-platform.yaml", "r", encoding="utf-8"
    ) as f:
        access_platform = yaml.safe_load(f)
        return SeqRepoAccessPlatform.model_validate(access_platform)


def extract_activity() -> SeqRepoActivity:
    """Extract Seq Repo activity from mapping.

    Settings:
        mapping_path: Path to the seq-repo activity mappings,
                      absolute or relative to `assets_dir`

    Returns:
        Seq Repo Activity
    """
    settings = SeqRepoSettings.get()
    with open(settings.mapping_path / "activity.yaml", "r", encoding="utf-8") as f:
        activity = yaml.safe_load(f)
        return SeqRepoActivity.model_validate(activity)


def extract_distribution() -> SeqRepoDistribution:
    """Extract Seq Repo distribution from mapping.

    Settings:
        mapping_path: Path to the seq-repo activity mappings,
                      absolute or relative to `assets_dir`

    Returns:
        Seq Repo Distribution
    """
    settings = SeqRepoSettings.get()
    with open(settings.mapping_path / "distribution.yaml", "r", encoding="utf-8") as f:
        distribution = yaml.safe_load(f)
        return SeqRepoDistribution.model_validate(distribution)


def extract_resource() -> SeqRepoResource:
    """Extract Seq Repo resource from mapping.

    Settings:
        mapping_path: Path to the seq-repo activity mappings,
                      absolute or relative to `assets_dir`

    Returns:
        Seq Repo Resource
    """
    settings = SeqRepoSettings.get()
    with open(settings.mapping_path / "resource.yaml", "r", encoding="utf-8") as f:
        resource = yaml.safe_load(f)
        return SeqRepoResource.model_validate(resource)
