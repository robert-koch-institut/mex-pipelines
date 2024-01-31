import pytest
from faker import Faker

from mex.artificial.main import factories, faker, identities
from mex.artificial.settings import ArtificialSettings


@pytest.fixture(autouse=True)
def settings() -> ArtificialSettings:
    """Load the settings for this pytest session."""
    return ArtificialSettings.get()


@pytest.fixture(autouse=True)
def reduce_output(settings: ArtificialSettings) -> None:
    """Automatically reduce the chattiness for text fields and item count for tests."""
    settings.chattiness = 5
    settings.count = 15


@pytest.fixture(name="faker")
def init_faker(settings: ArtificialSettings) -> Faker:
    """Return a fully configured faker instance."""
    Faker.seed(settings.seed)
    faker_instance = faker()
    identity_map = identities(faker_instance)
    return factories(faker_instance, identity_map)
