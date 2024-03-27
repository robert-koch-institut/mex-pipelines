from typing import Any

from mex.grippeweb.connector import QUERY_BY_TABLE_NAME, GrippewebConnector


def extract_columns_by_table_and_column_name() -> dict[str, dict[str, list[Any]]]:
    """Extract sql tables and parse them into column lists by table and column name.

    Returns:
        list of columns by column names and table names
    """
    connection = GrippewebConnector.get()
    return {
        table_name: connection.parse_columns_by_column_name(table_name)
        for table_name in QUERY_BY_TABLE_NAME.keys()
    }
