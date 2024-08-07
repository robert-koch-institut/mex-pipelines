from pydantic import Field

from mex.common.models import BaseModel
from mex.common.types import AssetsPath


class InternationalProjectsSettings(BaseModel):
    """Settings submodel definition for the international projects extractor."""

    file_path: AssetsPath = Field(
        AssetsPath(
            "../../../assets/raw-data/international-projects/international_projects.xlsx"
        ),
        description=(
            "Path to the international projects excel file, "
            "absolute path or relative to `assets_dir`."
        ),
    )
