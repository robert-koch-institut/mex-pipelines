import pytest

from mex.common.models import ExtractedPerson
from mex.common.types import Identifier
from mex.ff_projects.settings import FFProjectsSettings


@pytest.fixture(autouse=True)
def settings() -> FFProjectsSettings:
    """Load the settings for this pytest session."""
    return FFProjectsSettings.get()


@pytest.fixture
def extracted_person() -> ExtractedPerson:
    """Return an extracted person with static dummy values."""
    return ExtractedPerson(
        email=["fictitiousf@rki.de", "info@rki.de"],
        familyName="Fictitious",
        givenName="Frieda",
        fullName="Dr. Fictitious, Frieda",
        identifierInPrimarySource="frieda",
        hadPrimarySource=Identifier.generate(seed=40),
    )
