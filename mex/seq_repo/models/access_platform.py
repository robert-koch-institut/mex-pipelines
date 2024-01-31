from typing import Any

from pydantic import ConfigDict, Field

from mex.common.models import BaseModel


class SeqRepoAccessPlatform(BaseModel):
    """Model class for Seq Repo access platform."""

    model_config = ConfigDict(extra="ignore")

    alternative_title: list[dict[str, Any]] = Field(alias="alternativeTitle")
    contact: list[dict[str, Any]]
    description: list[dict[str, Any]]
    endpoint_type: list[dict[str, Any]] = Field(alias="endpointType")
    identifier_in_primary_source: list[dict[str, Any]] = Field(
        alias="identifierInPrimarySource"
    )
    landing_page: list[dict[str, Any]] = Field(alias="landingPage")
    technical_accessibility: list[dict[str, Any]] = Field(
        alias="technicalAccessibility"
    )
    title: list[dict[str, Any]]
    unit_in_charge: list[dict[str, Any]] = Field(alias="unitInCharge")
