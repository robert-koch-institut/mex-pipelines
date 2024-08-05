from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from mex.common.models import ExtractedPrimarySource
from mex.common.types import MergedOrganizationIdentifier
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.common.wikidata.transform import (
    transform_wikidata_organization_to_extracted_organization,
)
from mex.wikidata import convenience
from mex.wikidata.convenience import (
    get_merged_organization_id_by_query_with_extract_transform_and_load,
)


@pytest.mark.usefixtures(
    "mocked_wikidata",
)
def test_get_merged_organization_id_by_query_with_extract_transform_and_load(
    wikidata_organization: WikidataOrganization,
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
    monkeypatch: MonkeyPatch,
) -> None:

    query_string = "Robert Koch-Institut"
    wikidata_primary_source = extracted_primary_sources["wikidata"]
    extracted_wikidata_organization = (
        transform_wikidata_organization_to_extracted_organization(
            wikidata_organization, wikidata_primary_source
        )
    )

    mocked_load = Mock()
    monkeypatch.setattr(convenience, "load", mocked_load)

    returned = get_merged_organization_id_by_query_with_extract_transform_and_load(
        query_string, wikidata_primary_source
    )
    mocked_load.assert_called_once_with([extracted_wikidata_organization])

    assert returned == MergedOrganizationIdentifier("ga6xh6pgMwgq7DC7r6Wjqg")

    # transformation returns no organization
    mocked_transform_wikidata_organization_to_extracted_organization = Mock(
        return_value=None
    )
    monkeypatch.setattr(
        convenience,
        "transform_wikidata_organization_to_extracted_organization",
        mocked_transform_wikidata_organization_to_extracted_organization,
    )
    returned = get_merged_organization_id_by_query_with_extract_transform_and_load(
        query_string, wikidata_primary_source
    )
    assert returned is None
    mocked_load.assert_called_once()
    mocked_transform_wikidata_organization_to_extracted_organization.assert_called_once_with(
        wikidata_organization, wikidata_primary_source
    )

    # search returns no organization
    mocked_search_organization_by_label = Mock(return_value=None)
    monkeypatch.setattr(
        convenience, "search_organization_by_label", mocked_search_organization_by_label
    )
    returned = get_merged_organization_id_by_query_with_extract_transform_and_load(
        query_string, wikidata_primary_source
    )
    assert returned is None
    mocked_load.assert_called_once()
    mocked_transform_wikidata_organization_to_extracted_organization.assert_called_once()
    mocked_search_organization_by_label.assert_called_once_with(query_string)
