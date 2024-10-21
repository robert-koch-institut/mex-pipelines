from mex.common.primary_source.helpers import get_extracted_primary_source_by_name
from mex.common.types import MergedPrimarySourceIdentifier
from mex.extractors.sinks import load


# Helper for primary source
def get_extracted_primary_source_id_by_name(
    name: str,
) -> MergedPrimarySourceIdentifier | None:
    """Use helper function to look up a primary source and return its stableTargetId.

    A primary source is searched by its name and loaded into the configured sink.
    Also it's stable target id is returned.

    Returns:
        ExtractedPrimarySource stableTargetId if one matching primary source is found.
        None if multiple matches / no match is found
    """
    extracted_primary_source = get_extracted_primary_source_by_name(name)

    if extracted_primary_source is None:
        return None

    load([extracted_primary_source])

    return extracted_primary_source.stableTargetId
