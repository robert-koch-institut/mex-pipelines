from typing import Any

from pydantic import Field

from mex.common.models import BaseModel


class ResourceFeatModel(BaseModel):
    """Model class for Sumo resource feat  model entities."""

    access_restriction: list[dict[str, Any]] = Field([], alias="accessRestriction")
    accrual_periodicity: list[dict[str, Any]] = Field([], alias="accrualPeriodicity")
    contact: list[dict[str, Any]]
    contributing_unit: list[dict[str, Any]] = Field([], alias="contributingUnit")
    keyword: list[dict[str, Any]]
    mesh_id: list[dict[str, Any]] = Field([], alias="meshId")
    resource_type_general: list[dict[str, Any]] = Field([], alias="resourceTypeGeneral")
    theme: list[dict[str, Any]]
    title: list[dict[str, Any]]
    unit_in_charge: list[dict[str, Any]] = Field([], alias="unitInCharge")
