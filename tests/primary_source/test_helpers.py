from unittest.mock import Mock

import pytest
from pytest import MonkeyPatch

from mex.common.types import MergedPrimarySourceIdentifier
from mex.extractors.primary_source import helpers
from mex.extractors.primary_source.helpers import (
    get_extracted_primary_source_id_by_name,
)


@pytest.mark.usefixtures("extracted_primary_sources")
def test_get_extracted_primary_source_id_by_name(
    monkeypatch: MonkeyPatch,
) -> None:
    """Primary source helper finds "Wikidata" and returns None for nonsense query."""
    query_wiki = "wikidata"
    query_nonsense = "this should give None"

    mocked_load = Mock()
    monkeypatch.setattr(helpers, "load", mocked_load)

    returned = get_extracted_primary_source_id_by_name(query_wiki)
    mocked_load.assert_called_once()

    assert returned == MergedPrimarySourceIdentifier("djbNGb5fLgYHFyMh3fZE2g")
    assert get_extracted_primary_source_id_by_name(query_nonsense) is None
