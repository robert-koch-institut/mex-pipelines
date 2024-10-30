from pydantic import Field

from mex.common.settings import BaseSettings


class PublisherSettings(BaseSettings):
    """Settings submodel for the Publishing pipeline."""

    skip_merged_items: list[str] = Field(
        ["MergedPrimarySource", "MergedConsent"],
        description="Skip merged items with these types",
        validation_alias="MEX_SKIP_MERGED_ITEMS",
    )
