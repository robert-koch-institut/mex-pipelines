from typing import TypeVar

from pydantic import BaseModel

from mex.ifsg.connector import IFSGConnector

ModelT = TypeVar("ModelT", bound=BaseModel)


def extract_sql_table(model: type[ModelT]) -> list[ModelT]:
    """Extract sql tables and parse them into pydantic models.

    Settings:
        model: pydantic ModelT

    Returns:
        list of parsed pydantic ModelT
    """
    connection = IFSGConnector.get()
    return [model.model_validate(row) for row in connection.parse_rows(model)]
