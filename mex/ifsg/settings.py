from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class IFSGSettings(Settings):
    """Settings definition for the infection protection act data."""

    model_config = SettingsConfigDict(env_prefix="ifsg_")
    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/ifsg"),
        description=(
            "Path to the directory with the ifsg mapping files containing the default "
            "values, absolute path or relative to `assets_dir`."
        ),
    )
