from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class SumoSettings(Settings):
    """Settings for the SUMO extractor."""

    model_config = SettingsConfigDict(env_prefix="sumo_")

    raw_data_path: AssetsPath = Field(
        AssetsPath("raw-data/sumo"),
        description=(
            "Path to the directory with the sumo excel files, "
            "absolute path or relative to `assets_dir`."
        ),
    )
    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/sumo"),
        description=(
            "Path to the directory with the sumo mapping files containing the default "
            "values, absolute path or relative to `assets_dir`."
        ),
    )
