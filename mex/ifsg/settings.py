from pydantic import Field

from mex.common.models import BaseModel
from mex.common.types import AssetsPath


class IFSGSettings(BaseModel):
    """Settings submodel definition for the infection protection act data."""

    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/ifsg"),
        description=(
            "Path to the directory with the ifsg mapping files containing the default "
            "values, absolute path or relative to `assets_dir`."
        ),
    )
