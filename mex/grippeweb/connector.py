import platform
from subprocess import PIPE, STDOUT, Popen
from typing import Any

from mex.common.connector import BaseConnector
from mex.common.logging import echo
from mex.grippeweb.settings import GrippewebSettings

QUERY_BY_TABLE_NAME = {
    "vActualQuestion": "SELECT * FROM GrippeWeb.MEx.vActualQuestion",
    "vMasterDataMEx": "SELECT * FROM GrippeWeb.MEx.vMasterDataMEx",
    "vWeeklyResponsesMEx": "SELECT * FROM GrippeWeb.MEx.vWeeklyResponsesMEx",
}


class GrippewebConnector(BaseConnector):
    """Connector to handle authentication and queries for Grippeweb SQL server."""

    def __init__(self) -> None:
        """Create a new connector instance."""
        # https://github.com/mkleehammer/pyodbc/wiki/Install#installing-on-linux
        import pyodbc  # type: ignore[import-not-found]

        settings = GrippewebSettings.get()
        if platform.system() != "Windows":  # pragma: no cover
            process = Popen(  # noqa: S603
                ["kinit", settings.kerberos_user, "-V"],  # noqa: S607
                stdout=PIPE,
                stdin=PIPE,
                stderr=STDOUT,
                encoding="utf-8",
            )
            stdout, stderr = process.communicate(
                input=settings.kerberos_password.get_secret_value()
            )
            echo(stdout, fg="green")
            echo(stderr, fg="red")
        self._connection = pyodbc.connect(settings.mssql_connection_dsn)

    def parse_columns_by_column_name(self, table_name: str) -> dict[str, list[Any]]:
        """Execute whitelisted queries and zip results to column name."""
        with self._connection.cursor() as cursor:

            cursor.execute(QUERY_BY_TABLE_NAME[table_name])
            table = cursor.fetchall()
            table_columns = list(zip(*table, strict=False))
            return {
                column_name[0]: list(column)
                for column_name, column in zip(
                    cursor.description, table_columns, strict=False
                )
            }

    def close(self) -> None:
        """Close the underlying connection."""
        self._connection.close()
