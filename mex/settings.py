from pydantic import Field

from mex.common.settings import BaseSettings
from mex.common.types import IdentityProvider
from mex.types import ExtractorIdentityProvider


class Settings(BaseSettings):
    """Settings definition class for extractors and related scripts."""

    skip_partners: list[str] = Field(
        ["test"],
        description="Skip projects with these external partners",
        validation_alias="MEX_SKIP_PARTNERS",
    )
    skip_units: list[str] = Field(
        ["IT", "PRAES", "ZV"],
        description="Skip projects with these responsible units",
        validation_alias="MEX_SKIP_UNITS",
    )
    skip_years_before: int = Field(
        1970,
        description="Skip projects conducted before this year",
        validation_alias="MEX_SKIP_YEARS_BEFORE",
    )
    identity_provider: IdentityProvider | ExtractorIdentityProvider = Field(
        IdentityProvider.MEMORY,
        description="Provider to assign stableTargetIds to new model instances.",
        validation_alias="MEX_IDENTITY_PROVIDER",
    )  # type: ignore[assignment]
