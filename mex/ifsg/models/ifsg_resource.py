from typing import Any

from pydantic import Field

from mex.common.models import BaseModel


class IFSGResource(BaseModel):
    """Model class for ifsg resource entities."""

    access_restriction: list[dict[str, Any]] = Field([], alias="accessRestriction")
    accrual_periodicity: list[dict[str, Any]] = Field([], alias="accrualPeriodicity")
    alternative_title: list[dict[str, Any]] = Field([], alias="alternativeTitle")
    contact: list[dict[str, Any]]
    description: list[dict[str, Any]] = Field([])
    identifier_in_primary_source: list[dict[str, Any]] = Field(
        [], alias="identifierInPrimarySource"
    )
    instrument_tool_or_apparatus: list[dict[str, Any]] = Field(
        [], alias="instrumentToolOrApparatus"
    )
    is_part_of: list[dict[str, Any]] = Field([], alias="isPartOf")
    keyword: list[dict[str, Any]]
    language: list[dict[str, Any]]
    publication: list[dict[str, Any]]
    resource_type_general: list[dict[str, Any]] = Field([], alias="resourceTypeGeneral")
    resource_type_specific: list[dict[str, Any]] = Field(
        [], alias="resourceTypeSpecific"
    )
    rights: list[dict[str, Any]]
    spatial: list[dict[str, Any]]
    theme: list[dict[str, Any]]
    title: list[dict[str, Any]]
    unit_in_charge: list[dict[str, Any]] = Field([], alias="unitInCharge")
