from typing import Any

from pydantic import ConfigDict, Field

from mex.common.models import BaseModel


class SeqRepoDistribution(BaseModel):
    """Model class for Seq Repo distribution."""

    model_config = ConfigDict(extra="ignore")

    access_restriction: list[dict[str, Any]] = Field(alias="accessRestriction")
    media_type: list[dict[str, Any]] = Field(alias="mediaType")
    title: list[dict[str, Any]]
    publisher: list[dict[str, Any]]
