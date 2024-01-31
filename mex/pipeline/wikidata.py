from mex.common.models import ExtractedOrganization, ExtractedPrimarySource
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.common.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations,
)
from mex.pipeline import asset
from mex.sinks import load


@asset(group_name="default")
def wikidata_organization_rki() -> list[WikidataOrganization]:
    """Extract WikidataOrganization for Robert Koch-Institut."""
    return list(search_organization_by_label("Robert Koch-Institut"))


@asset(group_name="default")
def extracted_organization_rki(
    wikidata_organization_rki: list[WikidataOrganization],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> ExtractedOrganization:
    """Transforms RKI organization data to extracted organizations and load result."""
    extracted_organization_rki = list(
        transform_wikidata_organizations_to_extracted_organizations(
            wikidata_organization_rki, extracted_primary_source_wikidata
        )
    )
    load(extracted_organization_rki)
    return extracted_organization_rki[0]
