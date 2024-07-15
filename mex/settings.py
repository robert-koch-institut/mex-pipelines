from pydantic import AnyUrl, Field, SecretStr
from pydantic_core import Url
from pydantic_settings import SettingsConfigDict

from mex.artificial.settings import ArtificialSettings
from mex.biospecimen.settings import BiospecimenSettings
from mex.common.settings import BaseSettings
from mex.common.types import IdentityProvider
from mex.confluence_vvt.settings import ConfluenceVvtSettings
from mex.datscha_web.settings import DatschaWebSettings
from mex.ff_projects.settings import FFProjectsSettings
from mex.grippeweb.settings import GrippewebSettings
from mex.ifsg.settings import IFSGSettings
from mex.international_projects.settings import InternationalProjectsSettings
from mex.odk.settings import ODKSettings
from mex.synopse.settings import SynopseSettings
from mex.types import ExtractorIdentityProvider


class Settings(BaseSettings):
    """Settings definition class for extractors and related scripts."""

    model_config = SettingsConfigDict(env_nested_delimiter="__")

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
    drop_api_key: SecretStr = Field(
        SecretStr("dummy_admin_key"),
        description="Drop API key with admin access to call all GET endpoints",
        validation_alias="MEX_DROP_API_KEY",
    )
    drop_api_url: AnyUrl = Field(
        Url("http://localhost:8081/"),
        description="MEx drop API url.",
        validation_alias="MEX_DROP_API_URL",
    )
    schedule: str = Field(
        "0 0 * * *",
        description="A valid cron string defining when to run extractor jobs",
        validation_alias="MEX_SCHEDULE",
    )

    kerberos_user: str = Field(
        "user@domain.tld",
        description="Kerberos user to authenticate against MSSQL server.",
    )
    kerberos_password: SecretStr = Field(
        SecretStr("password"),
        description="Kerberos password to authenticate against MSSQL server.",
    )
    mssql_connection_dsn: str = Field(
        "DRIVER={ODBC Driver 18 for SQL Server};SERVER=domain.tld;DATABASE=database",
        description=(
            "Connection string for the ODBC Driver for SQL Server: "
            "https://learn.microsoft.com/en-us/sql/connect/odbc/"
            "dsn-connection-string-attribute"
        ),
    )
    artificial: ArtificialSettings = ArtificialSettings()
    biospecimen: BiospecimenSettings = BiospecimenSettings()
    confluence_vvt: ConfluenceVvtSettings = ConfluenceVvtSettings()
    datscha_web: DatschaWebSettings = DatschaWebSettings()
    ff_projects: FFProjectsSettings = FFProjectsSettings()
    grippeweb: GrippewebSettings = GrippewebSettings()
    ifsg: IFSGSettings = IFSGSettings()
    international_projects: InternationalProjectsSettings = (
        InternationalProjectsSettings()
    )
    odk: ODKSettings = ODKSettings()
    synopse: SynopseSettings = SynopseSettings()
