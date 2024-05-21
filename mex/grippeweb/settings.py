from pydantic import Field
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class GrippewebSettings(Settings):
    """Settings definition for the infection protection act data."""

    model_config = SettingsConfigDict(env_prefix="grippeweb_")

    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/grippeweb"),
        description=(
            "Path to the directory with the Grippeweb mapping files containing the "
            "default values, absolute path or relative to `assets_dir`."
        ),
    )
    mssql_connection_dsn: str = Field(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=domain.tld;DATABASE=database",
        description=(
            "Connection string for the ODBC Driver for SQL Server: "
            "https://learn.microsoft.com/en-us/sql/connect/odbc/"
            "dsn-connection-string-attribute"
        ),
    )
