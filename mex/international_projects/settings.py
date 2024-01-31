from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class InternationalProjectsSettings(Settings):
    """Settings definition for the international projects extractor."""

    model_config = SettingsConfigDict(env_prefix="international_projects_")

    file_path: AssetsPath = Field(
        AssetsPath("raw-data/international-projects/international_projects.xlsx"),
        description=(
            "Path to the international projects excel file, "
            "absolute path or relative to `assets_dir`."
        ),
    )
