from typing import Any

from pydantic import Field

from mex.common.models import BaseModel


class ResourceNokeda(BaseModel):
    """Model class for Sumo resource nokeda entities."""

    access_restriction: list[dict[str, Any]] = Field([], alias="accessRestriction")
    accrual_periodicity: list[dict[str, Any]] = Field([], alias="accrualPeriodicity")
    contact: list[dict[str, Any]]
    contributing_unit: list[dict[str, Any]] = Field([], alias="contributingUnit")
    description: list[dict[str, Any]]
    documentation: list[dict[str, Any]]
    keyword: list[dict[str, Any]]
    mesh_id: list[dict[str, Any]] = Field([], alias="meshId")
    publication: list[dict[str, Any]]
    publisher: list[dict[str, Any]]
    resource_type_general: list[dict[str, Any]] = Field([], alias="resourceTypeGeneral")
    resource_type_specific: list[dict[str, Any]] = Field(
        [], alias="resourceTypeSpecific"
    )
    rights: list[dict[str, Any]]
    spatial: list[dict[str, Any]]
    state_of_data_processing: list[dict[str, Any]] = Field(
        [], alias="stateOfDataProcessing"
    )
    theme: list[dict[str, Any]]
    title: list[dict[str, Any]]
    unit_in_charge: list[dict[str, Any]] = Field([], alias="unitInCharge")
