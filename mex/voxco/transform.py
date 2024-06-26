from typing import Any

from mex.common.models import (
    ExtractedOrganization,
    ExtractedPerson,
    ExtractedPrimarySource,
    ExtractedResource,
    ExtractedVariable,
)
from mex.common.types import (
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
)
from mex.voxco.model import VoxcoVariable


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
    """Transform voxco resource mappings to extracted resources.

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
        if anonymization_pseudonymization_top_level := resource.get(
            "anonymizationPseudonymization"
        ):
            anonymization_pseudonymization = anonymization_pseudonymization_top_level[
                0
            ]["mappingRules"][0]["setValues"]
        else:
            anonymization_pseudonymization = None
        contact = mex_persons_stable_target_id_by_email[
            resource["contact"][0]["mappingRules"][0]["forValues"][1]
        ]
        if description_top_level := resource.get("description"):
            description = description_top_level[0]["mappingRules"][0]["setValues"]
        else:
            description = None
        external_partner = organization_stable_target_id_by_query_voxco.get(
            resource["contact"][0]["mappingRules"][0]["forValues"][0]
        )
        identifier_in_primary_source = resource["identifierInPrimarySource"][0][
            "mappingRules"
        ][0]["setValues"][0]
        if keyword_top_level := resource.get("keyword"):
            keyword = keyword_top_level[0]["mappingRules"][0]["setValues"]
        else:
            keyword = None
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


def transform_voxco_variable_mappings_to_extracted_variables(
    extracted_voxco_resources: dict[str, ExtractedResource],
    voxco_variables: dict[str, list[VoxcoVariable]],
    extracted_primary_source_voxco: ExtractedPrimarySource,
) -> list[ExtractedVariable]:
    """Transform voxco variable mappings to extracted variables.

    Args:
        extracted_voxco_resources: extracted voxco resources
        voxco_variables: list of voxco variables by associated resource
        extracted_primary_source_voxco: extracted voxco primary source

    Returns:
        list of extracted variables
    """
    return [
        ExtractedVariable(
            hadPrimarySource=extracted_primary_source_voxco.stableTargetId,
            identifierInPrimarySource=str(variable.Id),
            description=variable.Type,
            label=variable.QuestionText,
            usedIn=resource.stableTargetId,
            valueSet=[
                choice.split("Text=")[1].split(";")[0] for choice in variable.Choices
            ],
        )
        for resource in extracted_voxco_resources.values()
        for variable in voxco_variables[
            f"resource_{resource.identifierInPrimarySource}"
        ]
    ]
