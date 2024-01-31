from typing import TypeVar

import yaml
from pydantic import BaseModel

from mex.ifsg.connector import IFSGConnector
from mex.ifsg.models.ifsg_resource import IFSGResource
from mex.ifsg.models.ifsg_variable_group import IFSGVariableGroup
from mex.ifsg.settings import IFSGSettings

ModelT = TypeVar("ModelT", bound=BaseModel)


def extract_resource_disease() -> IFSGResource:
    """Extract resource_disease by loading `resource_disease.yaml` from `mapping_path`.

    Settings:
        mapping_path: path to directory holding ifsg mapping.

    Returns:
        resource_disease
    """
    settings = IFSGSettings.get()
    with open(
        settings.mapping_path / "resource_disease.yaml", "r", encoding="utf-8"
    ) as f:
        resource_disease = yaml.safe_load(f)
    return IFSGResource.model_validate(resource_disease)


def extract_resource_parent() -> IFSGResource:
    """Extract resource_parent by loading `resource_parent.yaml` from `mapping_path`.

    Settings:
        mapping_path: path to directory holding ifsg mapping.

    Returns:
        resource_parent
    """
    settings = IFSGSettings.get()
    with open(
        settings.mapping_path / "resource_parent.yaml", "r", encoding="utf-8"
    ) as f:
        resource_parent = yaml.safe_load(f)
    return IFSGResource.model_validate(resource_parent)


def extract_resource_state() -> IFSGResource:
    """Extract resource_state by loading `resource_state.yaml` from `mapping_path`.

    Settings:
        mapping_path: path to directory holding ifsg mapping.

    Returns:
        resource_state
    """
    settings = IFSGSettings.get()
    with open(
        settings.mapping_path / "resource_state.yaml", "r", encoding="utf-8"
    ) as f:
        resource_state = yaml.safe_load(f)
    return IFSGResource.model_validate(resource_state)


def extract_ifsg_variable_group() -> IFSGVariableGroup:
    """Extract IFSGVariableGroup by loading `variable-group.yaml` from `mapping_path`.

    Settings:
        mapping_path: path to directory holding ifsg mapping.

    Returns:
        IFSGVariableGroup
    """
    settings = IFSGSettings.get()
    with open(
        settings.mapping_path / "variable-group.yaml", "r", encoding="utf-8"
    ) as f:
        ifsg_variable_group = yaml.safe_load(f)
    return IFSGVariableGroup.model_validate(ifsg_variable_group)


def extract_sql_table(model: type[ModelT]) -> list[ModelT]:
    """Extract sql tables and parse them into pydantic models.

    Settings:
        model: pydantic ModelT

    Returns:
        list of parsed pydantic ModelT
    """
    connection = IFSGConnector.get()
    return [model.model_validate(row) for row in connection.parse_rows(model)]
