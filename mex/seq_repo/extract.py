import json
from typing import Generator

from mex.seq_repo.model import (
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
    with open(settings.default_json_file_path, encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            yield SeqRepoSource.model_validate(item)
