from typing import Any

from pydantic import ConfigDict, Field

from mex.common.models import BaseModel


class SeqRepoResource(BaseModel):
    """Model class for Seq Repo resource."""

    model_config = ConfigDict(extra="ignore")

    access_restriction: list[dict[str, Any]] = Field(alias="accessRestriction")
    accrual_periodicity: list[dict[str, Any]] = Field(alias="accrualPeriodicity")
    anonymization_pseudonymization: list[dict[str, Any]] = Field(
        alias="anonymizationPseudonymization"
    )
    method: list[dict[str, Any]]
    resource_type_general: list[dict[str, Any]] = Field(alias="resourceTypeGeneral")
    resource_type_specific: list[dict[str, Any]] = Field(alias="resourceTypeSpecific")
    rights: list[dict[str, Any]]
    state_of_data_processing: list[dict[str, Any]] = Field(
        alias="stateOfDataProcessing"
    )
    publisher: list[dict[str, Any]]
    theme: list[dict[str, Any]]
