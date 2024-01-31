from typing import TYPE_CHECKING, Any, Callable, TypeVar

if TYPE_CHECKING:  # pragma: no cover
    _AssetFn = TypeVar("_AssetFn")

    def asset(**_: Any) -> Callable[[_AssetFn], _AssetFn]:
        """Create a definition for how to compute an asset."""
        ...

else:
    from dagster import asset

from mex.pipeline.base import load_job_definitions, run_job_in_process

__all__ = ("asset", "run_job_in_process", "load_job_definitions")
