from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class ODKSettings(Settings):
    """Settings definition for odk data extraction."""

    model_config = SettingsConfigDict(env_prefix="odk_")

    raw_data_path: AssetsPath = Field(
        AssetsPath("raw-data/odk"),
        description=(
            "Path to the directory with the odk excel files, "
            "absolute path or relative to `assets_dir`."
        ),
    )
    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/test_mapping"),
        description=(
            "Path to the directory with the odk mapping files containing the default "
            "values, absolute path or relative to `assets_dir`."
        ),
    )
