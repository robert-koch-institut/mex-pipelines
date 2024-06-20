from typing import Any

from mex.common.models import (
    ExtractedOrganization,
    ExtractedPerson,
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.types import (
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
)


def transform_voxco_resource_mappings_to_extracted_resources(
    voxco_resource_mappings: list[dict[str, Any]],
    organization_stable_target_id_by_query_voxco: dict[
        str, MergedOrganizationIdentifier
    ],
    extracted_mex_persons_voxco: list[ExtractedPerson],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_organization_rki: ExtractedOrganization,
    extracted_primary_source_voxco: ExtractedPrimarySource,
    # TODO: (MX-1583) international-projects,
) -> dict[str, ExtractedResource]:
    """Transform grippe web values to extracted resources.

    Args:
        voxco_resource_mappings: voxco  resource mappings
        organization_stable_target_id_by_query_voxco:
            extracted voxco organizations dict
        extracted_mex_persons_voxco: extracted voxco mex persons
        unit_stable_target_ids_by_synonym: merged organizational units by name
        extracted_organization_rki: extracted rki organization
        extracted_primary_source_voxco: extracted voxco primary source

    Returns:
        dict extracted voxco resource by identifier in primary source
    """
    resource_dict = {}
    mex_persons_stable_target_id_by_email = {
        person.email[0]: person.stableTargetId for person in extracted_mex_persons_voxco
    }
    for resource in voxco_resource_mappings:

        access_restriction = resource["accessRestriction"][0]["mappingRules"][0][
            "setValues"
        ]
        anonymization_pseudonymization = resource["anonymizationPseudonymization"][0][
            "mappingRules"
        ][0]["setValues"]
        contact = mex_persons_stable_target_id_by_email[
            resource["contact"][0]["mappingRules"][0]["forValues"][1]
        ]
        description = resource["description"][0]["mappingRules"][0]["setValues"] or None
        external_partner = organization_stable_target_id_by_query_voxco.get(
            resource["contact"][0]["mappingRules"][0]["forValues"][0]
        )
        identifier_in_primary_source = resource["identifierInPrimarySource"][0][
            "mappingRules"
        ][0]["setValues"][0]

        keyword = resource["keyword"][0]["mappingRules"][0]["setValues"]
        language = resource["language"][0]["mappingRules"][0]["setValues"]
        mesh_id = resource["meshId"][0]["mappingRules"][0]["setValues"]
        method = resource["method"][0]["mappingRules"][0]["setValues"]
        publisher = extracted_organization_rki.stableTargetId

        resource_type_general = resource["resourceTypeGeneral"][0]["mappingRules"][0][
            "setValues"
        ]
        quality_information = resource["qualityInformation"][0]["mappingRules"][0][
            "setValues"
        ]
        rights = resource["rights"][0]["mappingRules"][0]["setValues"]
        spatial = resource["spatial"][0]["mappingRules"][0]["setValues"]
        theme = resource["theme"][0]["mappingRules"][0]["setValues"]
        title = resource["title"][0]["mappingRules"][0]["setValues"]
        unit_in_charge = unit_stable_target_ids_by_synonym[
            resource["unitInCharge"][0]["mappingRules"][0]["forValues"][0]
        ]

        resource_dict[identifier_in_primary_source] = ExtractedResource(
            accessRestriction=access_restriction,
            anonymizationPseudonymization=anonymization_pseudonymization,
            contact=contact,
            description=description,
            externalPartner=external_partner,
            hadPrimarySource=extracted_primary_source_voxco.stableTargetId,
            identifierInPrimarySource=identifier_in_primary_source,
            keyword=keyword,
            language=language,
            meshId=mesh_id,
            method=method,
            publisher=publisher,
            resourceTypeGeneral=resource_type_general,
            qualityInformation=quality_information,
            rights=rights,
            spatial=spatial,
            theme=theme,
            title=title,
            unitInCharge=unit_in_charge,
            # TODO: (blocked by MX-1583) wasGeneratedBy = was_generated_by
        )
    return resource_dict
