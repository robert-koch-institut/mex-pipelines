from mex.common.models import ExtractedPrimarySource
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.common.wikidata.transform import (
    transform_wikidata_organization_to_extracted_organization,
)
from mex.pipeline.wikidata import get_organization_merged_id_by_query


def test_get_organization_merged_id_by_query(
    wikidata_organization: WikidataOrganization,
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
) -> None:
    wikidata_primary_source = extracted_primary_sources["wikidata"]

    returned = get_organization_merged_id_by_query(
        {"foo": wikidata_organization}, wikidata_primary_source
    )
    assert returned == {}

    extracted_organization = transform_wikidata_organization_to_extracted_organization(
        wikidata_organization, wikidata_primary_source
    )
    returned = get_organization_merged_id_by_query(
        {"foo": wikidata_organization}, wikidata_primary_source
    )
    assert returned == {"foo": extracted_organization.stableTargetId}
