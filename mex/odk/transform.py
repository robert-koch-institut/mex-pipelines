from typing import Any

from mex.common.models import ExtractedResource


def transform_odk_resources_to_mex_resources(
    odk_resource_mappings: list[dict[str, Any]]
) -> list[ExtractedResource]:
    """Transform Resources."""
    extracted_resources = []
    for resource in odk_resource_mappings:
        extracted_resources.append(
            ExtractedResource(
                identifierInPrimarySource=resource["identifierInPrimarySource"][0][
                    "mappingRules"
                ][0]["setValues"][0],
            )
        )
    return []
