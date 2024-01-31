from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from mex.settings import Settings


class BlueAntSettings(Settings):
    """Blue Ant settings definition for the Blue Ant extractor."""

    model_config = SettingsConfigDict(env_prefix="blueant_")

    api_key: SecretStr = Field(
        SecretStr("api-key"),
        description="Json Web Token for authentication with the Blue Ant API",
    )
    url: str = Field("https://blueant", description="URL of Blue Ant instance")
    skip_labels: list[str] = Field(
        ["test"], description="Skip projects with these terms in their label"
    )
    delete_prefixes: list[str] = Field(
        ["_", "1_", "2_", "3_", "4_", "5_", "6_", "7_", "8_", "9_"],
        description="Delete prefixes of labels starting with these terms",
    )
