from pydantic import Field

from mex.common.models import EXTRACTED_MODEL_CLASSES, BaseModel
from mex.common.types import AssetsPath


class ArtificialSettings(BaseModel):
    """Artificial settings submodel definition for the artificial data creator."""

    count: int = Field(
        100,
        ge=len(EXTRACTED_MODEL_CLASSES) * 2,
        lt=10e6,
        description=(
            "Amount of artificial entities to create. At least 2 per entity type are "
            "required, to ensure valid linking between the entities."
        ),
    )
    chattiness: int = Field(
        10,
        gt=1,
        le=100,
        description="Maximum amount of words to produce for textual fields.",
    )
    seed: int = Field(0, description="The seed value for faker randomness.")
    locale: list[str] = Field(
        ["de_DE", "en_US"], description="The locale to use for faker."
    )
    mesh_file: AssetsPath = Field(
        AssetsPath("raw-data/artificial/asciimesh.bin"),
        description=(
            "Binary MeSH file, absolute path or relative to `assets_dir`. "
            "MeSH (Medical Subject Headings) are used by the US National Library "
            "of Medicine as a controlled vocabulary thesaurus for indexing articles "
            "in PubMed. See: https://www.ncbi.nlm.nih.gov/mesh"
        ),
    )
