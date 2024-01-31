from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from mex.settings import Settings


class RDMOSettings(Settings):
    """RDMO settings definition for the RDMO extractor."""

    model_config = SettingsConfigDict(env_prefix="rdmo_")

    url: str = Field("https://rdmo/", description="RDMO instance URL")
    username: SecretStr = Field(
        SecretStr("username"),
        description="RDMO API user name",
    )
    password: SecretStr = Field(
        SecretStr("password"),
        description="RDMO API password",
    )
