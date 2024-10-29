import pytest

from mex.common.models import MergedContactPoint, MergedPrimarySource
from mex.extractors.publisher.extract import get_merged_items


@pytest.mark.usefixtures("mocked_backend")
def test_get_merged_items_mocked() -> None:
    item_generator = get_merged_items()
    items = list(item_generator)
    assert len(items) == 2
    assert isinstance(items[0], MergedPrimarySource)
    assert items == [
        MergedPrimarySource(
            entityType="MergedPrimarySource", identifier="fakefakefakeJA"
        ),
        MergedContactPoint(
            email=["fake@e.mail"],
            entityType="MergedContactPoint",
            identifier="alsofakefakefakeJA",
        ),
    ]
