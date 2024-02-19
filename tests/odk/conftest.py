import pytest

from mex.odk.settings import ODKSettings


@pytest.fixture(autouse=True)
def settings() -> ODKSettings:
    """Load the settings for this pytest session."""
    return ODKSettings.get()
