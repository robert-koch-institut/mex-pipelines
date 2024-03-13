import datetime
from unittest.mock import MagicMock

from pytest import MonkeyPatch

from mex.ifsg.models.meta_schema2type import MetaSchema2Type
from mex.mssql_server.connector import MSSQLServerConnector


def test_parse_rows(monkeypatch: MonkeyPatch) -> None:
    def mocked_init(self: MSSQLServerConnector) -> None:
        cursor = MagicMock()
        cursor.fetchall.return_value = [
            (
                1,
                0,
                datetime.datetime(2015, 1, 12, 8, 24, 23, 413000),
                b"\x00\x00\x00\x00\x00\x0b\xf6p",
            ),
            (
                1,
                11,
                datetime.datetime(2015, 1, 12, 8, 24, 23, 413000),
                b"\x00\x00\x00\x00\x00\x0b\xf6q",
            ),
        ]
        cursor.description = [["IdSchema"], ["IdType"], ["UpdatedAt"], ["ts"]]
        self._connection = MagicMock()
        self._connection.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(MSSQLServerConnector, "__init__", mocked_init)
    connection = MSSQLServerConnector.get()

    rows = connection.parse_rows(MetaSchema2Type)

    assert rows == [
        {
            "IdSchema": 1,
            "IdType": 0,
            "UpdatedAt": datetime.datetime(2015, 1, 12, 8, 24, 23, 413000),
            "ts": b"\x00\x00\x00\x00\x00\x0b\xf6p",
        },
        {
            "IdSchema": 1,
            "IdType": 11,
            "UpdatedAt": datetime.datetime(2015, 1, 12, 8, 24, 23, 413000),
            "ts": b"\x00\x00\x00\x00\x00\x0b\xf6q",
        },
    ]
