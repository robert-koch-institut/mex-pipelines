from typing import Any

from pydantic import Field

from mex.common.models import BaseModel


class SumoActivity(BaseModel):
    """Model class for Sumo Activity."""

    abstract: list[dict[str, Any]]
    activity_type: list[dict[str, Any]] = Field([], alias="activityType")
    contact: list[dict[str, Any]]
    documentation: list[dict[str, Any]]
    identifier_in_primary_source: list[dict[str, Any]] = Field(
        [], alias="identifierInPrimarySource"
    )
    involved_unit: list[dict[str, Any]] = Field([], alias="involvedUnit")
    publication: list[dict[str, Any]]
    responsible_unit: list[dict[str, Any]] = Field([], alias="responsibleUnit")
    short_name: list[dict[str, Any]] = Field([], alias="shortName")
    start: list[dict[str, Any]]
    theme: list[dict[str, Any]]
    title: list[dict[str, Any]]
    website: list[dict[str, Any]]
