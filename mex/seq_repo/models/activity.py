from typing import Any

from pydantic import ConfigDict

from mex.common.models import BaseModel


class SeqRepoActivity(BaseModel):
    """Model class for Seq Repo activity."""

    model_config = ConfigDict(extra="ignore")

    theme: list[dict[str, Any]]
