from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from mex.common.types import MergedOrganizationIdentifier, MergedPrimarySourceIdentifier
from mex.helpers import helpers
from mex.helpers.helpers import (
    get_extracted_primary_source_id_by_name,
    get_wikidata_extracted_organization_id_by_name,
)


@pytest.mark.usefixtures("extracted_primary_sources")
def test_get_extracted_primary_source_id_by_name(
    monkeypatch: MonkeyPatch,
) -> None:
    query_wiki = "wikidata"
    query_nonsense = "this shlould give None"

    mocked_load = Mock()
    monkeypatch.setattr(helpers, "load", mocked_load)

    returned = get_extracted_primary_source_id_by_name(query_wiki)
    mocked_load.assert_called_once()

    assert returned == MergedPrimarySourceIdentifier("djbNGb5fLgYHFyMh3fZE2g")
    assert get_extracted_primary_source_id_by_name(query_nonsense) is None


@pytest.mark.usefixtures("mocked_wikidata")
def test_get_wikidata_extracted_organization_id_by_name(
    monkeypatch: MonkeyPatch,
) -> None:
    query_wiki = "wikidata"
    query_nonsense = "this shlould give None"

    mocked_load = Mock()
    monkeypatch.setattr(helpers, "load", mocked_load)

    returned = get_wikidata_extracted_organization_id_by_name(query_wiki)
    mocked_load.assert_called_once()

    assert returned == MergedOrganizationIdentifier("ga6xh6pgMwgq7DC7r6Wjqg")
    assert get_wikidata_extracted_organization_id_by_name(query_nonsense) is None
