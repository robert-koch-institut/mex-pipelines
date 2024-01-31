from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class FFProjectsSettings(Settings):
    """Settings for the FF Projects extractor."""

    model_config = SettingsConfigDict(env_prefix="ff_projects_")

    file_path: AssetsPath = Field(
        AssetsPath("raw-data/ff-projects/ff-projects.xlsx"),
        description=(
            "Path to the FF Projects excel file, "
            "absolute path or relative to `assets_dir`."
        ),
    )
    skip_categories: list[str] = Field(
        ["Sonstige"],
        description="Skip sources with these categories",
    )
    skip_funding: list[str] = Field(
        ["Sonstige"], description="Skip sources with this funding"
    )
    skip_topics: list[str] = Field(
        ["Sonstige"],
        description="Skip sources with these topics",
    )
    skip_years_strings: list[str] = Field(
        ["fehlt", "keine", "offen"],
        description="Skip sources with these years",
    )
    skip_clients: list[str] = Field(
        ["Sonstige"],
        description="Skip sources with these clients",
    )
