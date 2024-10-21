from mex.common.types import MergedOrganizationIdentifier
from mex.common.wikidata.helpers import get_extracted_organization_from_wikidata
from mex.extractors.sinks import load


def get_wikidata_extracted_organization_id_by_name(
    name: str,
) -> MergedOrganizationIdentifier | None:
    """Use helper function to look up an organization and return its stableTargetId.

    An organization searched by its name on Wikidata and loaded into the configured
    sink. Also it's stable target id is returned.

    Returns:
        ExtractedOrganization stableTargetId if one matching organization is found.
        None if multiple matches / no match is found
    """
    extracted_organization = get_extracted_organization_from_wikidata(name)

    if extracted_organization is None:
        return None

    load([extracted_organization])

    return extracted_organization.stableTargetId
