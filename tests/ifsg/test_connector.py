import datetime
from unittest.mock import MagicMock

from pyodbc import Connection, Cursor
from pytest import MonkeyPatch

from mex.ifsg.connector import IFSGConnector
from mex.ifsg.models.meta_schema2type import MetaSchema2Type


def test_parse_rows(monkeypatch: MonkeyPatch) -> None:
    def mocked_init(self: IFSGConnector) -> None:
        cursor = MagicMock(spec=Cursor)
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
        self._connection = MagicMock(spec=Connection)
        self._connection.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(IFSGConnector, "__init__", mocked_init)
    connection = IFSGConnector.get()

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
