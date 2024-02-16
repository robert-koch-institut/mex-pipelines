import pytest

from mex.common.types import AssetsPath
from mex.odk.settings import ODKSettings


@pytest.fixture(autouse=True)
def settings() -> ODKSettings:
    """Load the settings for this pytest session."""
    return ODKSettings.get()


@pytest.fixture(autouse=True)
def set_mapping_path(settings: ODKSettings) -> None:
    """Redirect mapping_path to test_mapping folder."""
    settings.mapping_path = AssetsPath("mappings/__final__/test_mapping")
