from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class VoxcoSettings(Settings):
    """Settings for the Voxco extractor."""

    model_config = SettingsConfigDict(env_prefix="voxco_")

    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/voxco"),
        description=(
            "Path to the directory with the voxco mapping files containing the "
            "default values, absolute path or relative to `assets_dir`."
        ),
    )
