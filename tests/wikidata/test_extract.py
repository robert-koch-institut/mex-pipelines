from mex.common.models import ExtractedPrimarySource
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.wikidata.extract import (
    get_merged_organization_id_by_query_with_transform_and_load,
)


def test_get_organization_merged_id_by_query_with_transform_and_load(
    wikidata_organization: WikidataOrganization,
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
) -> None:
    wikidata_primary_source = extracted_primary_sources["wikidata"]

    returned = get_merged_organization_id_by_query_with_transform_and_load(
        {"foo": wikidata_organization}, wikidata_primary_source
    )
    assert returned == {"foo": "ga6xh6pgMwgq7DC7r6Wjqg"}
