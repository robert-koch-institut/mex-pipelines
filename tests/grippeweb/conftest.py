from typing import TypeVar
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel
from pytest import MonkeyPatch

from mex.grippeweb.connector import GrippewebConnector

ModelT = TypeVar("ModelT", bound=BaseModel)


@pytest.fixture
def mocked_sql_tables() -> dict[str, list[BaseModel]]:
    return {
        "vActualQuestion": {
            "Id": ["AAA", "BBB"],
            "StartedOn": ["2023-11-01 00:00:00.0000000", "2023-12-01 00:00:00.0000000"],
            "FinishedOn": [
                "2023-12-01 00:00:00.0000000",
                "2024-01-01 00:00:00.0000000",
            ],
            "RepeatAfterDays": ["1", "2"],
        },
        "vWeeklyResponsesMEx": {
            "GuidTeilnehmer": [None, None],
            "Haushalt_Registrierer": [None, None],
        },
        "vMasterDataMEx": {
            "GuidTeilnehmer": [None, None],
            "Haushalt_Registrierer": [None, None],
        },
    }


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
