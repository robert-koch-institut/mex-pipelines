from typing import TypeVar

from pydantic import BaseModel

from mex.grippeweb.connector import GrippewebConnector

ModelT = TypeVar("ModelT", bound=BaseModel)


def extract_sql_table(model: type[ModelT]) -> list[ModelT]:
    """Extract sql tables and parse them into pydantic models.

    Settings:
        model: pydantic ModelT

    Returns:
        list of parsed pydantic ModelT
    """
    connection = GrippewebConnector.get()
    return [model.model_validate(row) for row in connection.parse_rows(model)]
