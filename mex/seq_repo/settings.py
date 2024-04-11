from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class SeqRepoSettings(Settings):
    """Settings for the SeqRepo extractor."""

    model_config = SettingsConfigDict(env_prefix="seq_repo_")

    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/seq-repo"),
        description=(
            "Path to the directory with the seq-repo mapping files containing the "
            "default values, absolute path or relative to `assets_dir`."
        ),
    )
