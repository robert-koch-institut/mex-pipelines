from mex.common.models import MergedConsent, MergedContactPoint, MergedPrimarySource
from mex.extractors.publisher.filter import filter_merged_items


def test_filter_merged_items() -> None:
    items = [
        MergedPrimarySource(
            entityType="MergedPrimarySource", identifier="fakefakefakeJA"
        ),
        MergedContactPoint(
            email=["1fake@e.mail"],
            entityType="MergedContactPoint",
            identifier="alsofakefakefakeJA",
        ),
        MergedConsent(
            entityType="MergedConsent",
            identifier="anotherfakefakefakefak",
            hasConsentStatus="https://mex.rki.de/item/consent-status-1",
            hasDataSubject="fakefakefakefakefakefa",
            isIndicatedAtTime="2014-05-21T19:38:51Z",
        ),
        MergedContactPoint(
            email=["2fake@e.mail"],
            entityType="MergedContactPoint",
            identifier="alsofakefakefakeYO",
        ),
    ]
    allowed_items_generator = filter_merged_items(items)
    allowed_items = list(allowed_items_generator)

    assert allowed_items == [items[1], items[3]]
