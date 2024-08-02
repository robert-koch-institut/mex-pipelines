from unittest.mock import Mock

from pytest import MonkeyPatch

from mex.common.models import ExtractedPrimarySource
from mex.common.types import MergedOrganizationIdentifier
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.wikidata import convenience
from mex.wikidata.convenience import (
    get_merged_organization_id_by_query_with_extract_transform_and_load,
)


def test_get_merged_organization_id_by_query_with_extract_transform_and_load(
    wikidata_organization: WikidataOrganization,
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
    monkeypatch: MonkeyPatch,
) -> None:

    query_string = "wikidata"
    wikidata_primary_source = extracted_primary_sources[query_string]

    mocked_load = Mock()
    monkeypatch.setattr(convenience, "load", mocked_load)

    returned = get_merged_organization_id_by_query_with_extract_transform_and_load(
        query_string, wikidata_primary_source
    )
    mocked_load.assert_called_once()

    assert returned == MergedOrganizationIdentifier("ga6xh6pgMwgq7DC7r6Wjqg")
