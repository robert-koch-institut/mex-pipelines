from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from mex.settings import Settings


class DatschaWebSettings(Settings):
    """Custom settings definition for datscha web extractor."""

    model_config = SettingsConfigDict(env_prefix="datscha_web_")

    url: str = Field("https://datscha/", description="URL of datscha web service.")
    vorname: SecretStr = Field(
        SecretStr("first-name"),
        description="First name for login to datscha web service.",
    )
    nachname: SecretStr = Field(
        SecretStr("last-name"),
        description="Last name for login to datscha web service.",
    )
    pw: SecretStr = Field(
        SecretStr("password"),
        description="Password for login to datscha web service.",
    )
    organisation: str = Field(
        "RKI",
        description="Organisation for login to datscha web service.",
    )
