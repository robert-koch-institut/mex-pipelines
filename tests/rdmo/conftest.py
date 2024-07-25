import pytest

from mex.common.models import ExtractedPerson
from mex.common.types import Identifier


@pytest.fixture
def extracted_person() -> ExtractedPerson:
    """Return an extracted person with static dummy values."""
    return ExtractedPerson(
        email="ausgedachta@rki.de",
        familyName="Ausgedacht",
        givenName="Arnold",
        fullName="Arnold Ausgedacht",
        hadPrimarySource=Identifier.generate(seed=43),
        identifierInPrimarySource="arnold",
    )
