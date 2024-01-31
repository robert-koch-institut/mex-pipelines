from typing import Any

from pydantic import Field

from mex.common.models import BaseModel


# TODO: use mex.ops.mapping.schema.GenericField or
#       generate_mapping_schema_for_mex_class(BaseAccessPlatform) here
class SumoAccessPlatform(BaseModel):
    """Model class for Sumo Access Platform."""

    contact: list[dict[str, Any]]
    identifier_in_primary_source: list[dict[str, Any]] = Field(
        [], alias="identifierInPrimarySource"
    )
    technical_accessibility: list[dict[str, Any]] = Field(
        [], alias="technicalAccessibility"
    )
    title: list[dict[str, Any]]
    unit_in_charge: list[dict[str, Any]] = Field([], alias="unitInCharge")
