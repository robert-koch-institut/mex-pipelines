from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pydantic import BaseModel

from mex.grippeweb.connector import GrippewebConnector


@pytest.fixture
def mocked_grippeweb(
    mocked_sql_tables: dict[str, list[BaseModel]], monkeypatch: MonkeyPatch
) -> None:
    """Mock grippeweb connector."""

    def mocked_init(self: GrippewebConnector) -> None:
        cursor = MagicMock()
        cursor.fetchone.return_value = ["mocked"]
        self._connection = MagicMock()
        self._connection.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(GrippewebConnector, "__init__", mocked_init)

    monkeypatch.setattr(
        GrippewebConnector,
        "parse_columns_by_column_name",
        lambda self, model: mocked_sql_tables[model],
    )
