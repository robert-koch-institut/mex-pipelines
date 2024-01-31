from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from mex.common.types import AssetsPath
from mex.settings import Settings


class IFSGSettings(Settings):
    """Settings definition for the infection protection act data."""

    model_config = SettingsConfigDict(env_prefix="ifsg_")

    kerberos_user: str = Field(
        "user@domain.tld",
        description="Kerberos user to authenticate against MSSQL server.",
    )
    kerberos_password: SecretStr = Field(
        SecretStr("password"),
        description="Kerberos password to authenticate against MSSQL server.",
    )
    mapping_path: AssetsPath = Field(
        AssetsPath("mappings/__final__/ifsg"),
        description=(
            "Path to the directory with the ifsg mapping files containing the default "
            "values, absolute path or relative to `assets_dir`."
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
