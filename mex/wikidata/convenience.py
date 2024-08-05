from mex.common.models import ExtractedPrimarySource
from mex.common.types import MergedOrganizationIdentifier
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.transform import (
    transform_wikidata_organization_to_extracted_organization,
)
from mex.sinks import load

_ORGANIZATION_BY_QUERY_CACHE: dict[str, MergedOrganizationIdentifier] = {}


def get_merged_organization_id_by_query_with_extract_transform_and_load(
    query_string: str,
    wikidata_primary_source: ExtractedPrimarySource,
) -> MergedOrganizationIdentifier | None:
    """Looks up and loads a WikidataOrganization and returns its stableTargetId.

    An organization is searched for in wikidata, transformed into an
    ExtractedOrganization and loaded into the configured sink.
    Also it's stable target id is returned.

    Returns:
        Extracted WikidataOrganization stableTargetId if one matching organization
        is found in Wikidata lookup.
        None if multiple matches / no organization is found
    """
    try:
        return _ORGANIZATION_BY_QUERY_CACHE[query_string]
    except KeyError:
        pass

    found_organization = search_organization_by_label(query_string)

    if found_organization is None:
        return None

    extracted_organization = transform_wikidata_organization_to_extracted_organization(
        found_organization, wikidata_primary_source
    )

    if extracted_organization is None:
        return None

    load([extracted_organization])

    _ORGANIZATION_BY_QUERY_CACHE[query_string] = extracted_organization.stableTargetId

    return extracted_organization.stableTargetId
