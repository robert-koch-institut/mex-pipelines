from pathlib import Path

from mex.common.models import MergedContactPoint, MergedPrimarySource
from mex.common.settings import BaseSettings
from mex.extractors.publisher.load import write_merged_items


def test_write_merged_items(ndjson_path: Path) -> None:
    content = [
        MergedPrimarySource(
            entityType="MergedPrimarySource", identifier="fakefakefakeJA"
        ),
        MergedContactPoint(
            email=["fake@e.mail"],
            entityType="MergedContactPoint",
            identifier="alsofakefakefakeJA",
        ),
    ]
    write_merged_items(content)

    settings = BaseSettings.get()
    ndjson_path = settings.work_dir / "publisher.ndjson"
    assert (
        ndjson_path.read_text(encoding="utf-8")
        == '{"version": null, "alternativeTitle": [], "contact": [], "description": [], "documentation": [], "locatedAt": [], "title": [], "unitInCharge": [], "entityType": "MergedPrimarySource", "identifier": "fakefakefakeJA"}\n{"email": ["fake@e.mail"], "entityType": "MergedContactPoint", "identifier": "alsofakefakefakeJA"}\n'
    )
