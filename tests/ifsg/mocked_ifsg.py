from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pydantic import BaseModel

from mex.ifsg.connector import IFSGConnector


@pytest.fixture
def mocked_ifsg(
    mocked_sql_tables: dict[str, list[BaseModel]], monkeypatch: MonkeyPatch
) -> None:
    """Mock IFSG connector."""

    def mocked_init(self: IFSGConnector) -> None:
        cursor = MagicMock()
        cursor.fetchone.return_value = ["mocked"]
        self._connection = MagicMock()
        self._connection.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(IFSGConnector, "__init__", mocked_init)

    monkeypatch.setattr(
        IFSGConnector,
        "parse_rows",
        lambda self, model: mocked_sql_tables[model],
    )
