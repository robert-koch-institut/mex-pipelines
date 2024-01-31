from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class BiospecimenSettings(Settings):
    """Settings for the Biospecimen extractor."""

    model_config = SettingsConfigDict(env_prefix="biospecimen_")

    dir_path: AssetsPath = Field(
        AssetsPath("raw-data/biospecimen"),
        description=(
            "Path to the directory with the biospecimen excel files, "
            "absolute path or relative to `assets_dir`."
        ),
    )
    key_col: str = Field(
        "Feldname",
        description="column name of the biospecimen metadata keys",
    )
    val_col: str = Field(
        "zu extrahierender Wert (maschinenlesbar)",
        description="column name of the biospecimen metadata values",
    )
