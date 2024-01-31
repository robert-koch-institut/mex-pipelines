from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from mex.settings import Settings


class ConfluenceVvtSettings(Settings):
    """Confluence-vvt settings definition for the Confluence-vvt extractor."""

    model_config = SettingsConfigDict(env_prefix="confluence_vvt_")

    url: str = Field("https://confluence.vvt", description="URL of Confluence-vvt.")
    username: SecretStr = Field(
        SecretStr("username"),
        description="Confluence-vvt user name",
    )
    password: SecretStr = Field(
        SecretStr("password"),
        description="Confluence-vvt password",
    )
    overview_page_id: str = Field(
        "123456", description="Confluence id of the overview page."
    )
