from mex.common.models import ExtractedPrimarySource
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.pipeline.wikidata import get_organization_merged_id_by_query


def test_get_organization_merged_id_by_query(
    wikidata_organization: WikidataOrganization,
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
) -> None:

    returned = get_organization_merged_id_by_query(
        {"foo": wikidata_organization}, extracted_primary_sources["wikidata"]
    )
    assert returned == {"foo": 123}
