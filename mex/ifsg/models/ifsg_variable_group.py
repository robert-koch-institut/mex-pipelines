from typing import Any

from mex.common.models import BaseModel


class IFSGVariableGroup(BaseModel):
    """Model class for ifsg variable group entities."""

    label: list[dict[str, Any]]
