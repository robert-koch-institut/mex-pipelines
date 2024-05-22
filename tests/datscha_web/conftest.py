import pytest

from mex.datscha_web.settings import DatschaWebSettings


@pytest.fixture(autouse=True)
def settings() -> DatschaWebSettings:
    """Load the settings for this pytest session."""
    return DatschaWebSettings.get()
