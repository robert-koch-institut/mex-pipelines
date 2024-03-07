from typing import Any, Generator

from mex.common.ldap.models.person import LDAPPersonWithQuery
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedDistribution,
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.types import Identifier, OrganizationalUnitID, PersonID
from mex.seq_repo.model import SeqRepoSource


def transform_seq_repo_activities_to_extracted_activities(
    seq_repo_sources: dict[str, SeqRepoSource],
    seq_repo_activity: dict[str, Any],
    seq_repo_source_project_coordinators: list[LDAPPersonWithQuery],
    unit_merged_ids_by_synonyms: dict[str, OrganizationalUnitID],
    project_coordinators_merged_ids_by_query_string: dict[str, list[PersonID]],
    extracted_primary_source: ExtractedPrimarySource,
) -> Generator[ExtractedActivity, None, None]:
    """Transform seq-repo activity to ExtractedActivity.

    Args:
        seq_repo_sources: Seq Repo extracted sources
        seq_repo_activity: Seq Repo extracted activity for default values from mapping
        seq_repo_source_project_coordinators: Seq Repo sources project coordinators
                                            ldap query results
        unit_merged_ids_by_synonyms: Unit merged ids by synonyms
        project_coordinators_merged_ids_by_query_string: Sources project coordinators
                                                        merged ids
        extracted_primary_source: Extracted primary source

    Returns:
        Generator for ExtractedActivity
    """
    theme = seq_repo_activity["theme"][0]["mappingRules"][0]["setValues"]
    for _, source in seq_repo_sources.items():
        project_coordinators_ids = []
        responsible_units = []
        for pc in source.project_coordinators:
            person_merged_id = project_coordinators_merged_ids_by_query_string.get(pc)
            if person_merged_id:
                project_coordinators_ids.append(person_merged_id[0])

            for query in seq_repo_source_project_coordinators:
                query_ldap: LDAPPersonWithQuery = query
                if (
                    query_ldap.person.sAMAccountName
                    and query_ldap.person.departmentNumber
                ):
                    if query_ldap.person.sAMAccountName.lower() == pc.lower():
                        unit = unit_merged_ids_by_synonyms.get(
                            query_ldap.person.departmentNumber
                        )
                        if unit:
                            responsible_units.append(unit)
        if not responsible_units or not project_coordinators_ids:
            continue

        yield ExtractedActivity(
            contact=project_coordinators_ids,
            hadPrimarySource=extracted_primary_source.stableTargetId,
            identifierInPrimarySource=source.project_id,
            involvedPerson=project_coordinators_ids,
            responsibleUnit=responsible_units,
            theme=theme,
            title=source.project_name,
        )


def transform_seq_repo_distribution_to_extracted_distribution(
    seq_repo_sources: dict[str, SeqRepoSource],
    seq_repo_distribution: dict[str, Any],
    mex_access_platform: ExtractedAccessPlatform,
    extracted_primary_source: ExtractedPrimarySource,
) -> Generator[ExtractedDistribution, None, None]:
    """Transform seq-repo distribution to ExtractedDistribution.

    Args:
        seq_repo_sources: Seq Repo extracted sources
        seq_repo_distribution: Seq Repo extracted distribution
        mex_access_platform: Extracted access platform
        extracted_primary_source: Extracted primary source

    Returns:
        Generator for ExtractedDistribution
    """
    access_restriction = seq_repo_distribution["accessRestriction"][0]["mappingRules"][
        0
    ]["setValues"]
    media_type = seq_repo_distribution["mediaType"][0]["mappingRules"][0]["setValues"]
    title = seq_repo_distribution["title"][0]["mappingRules"][0]["setValues"]

    for identifier_in_primary_source, source in seq_repo_sources.items():
        yield ExtractedDistribution(
            accessService=mex_access_platform.stableTargetId,
            accessRestriction=access_restriction,
            hadPrimarySource=extracted_primary_source.stableTargetId,
            identifierInPrimarySource=identifier_in_primary_source,
            issued=source.sequencing_date,
            mediaType=media_type,
            publisher=[
                Identifier.generate()
            ],  # TODO: publisher -> resolve with wikidata
            title=title,
        )


def transform_seq_repo_resource_to_extracted_resource(
    seq_repo_sources: dict[str, SeqRepoSource],
    seq_repo_distributions: dict[str, ExtractedDistribution],
    seq_repo_activities: dict[str, ExtractedActivity],
    seq_repo_resource: dict[str, Any],
    seq_repo_source_project_coordinators: list[LDAPPersonWithQuery],
    unit_merged_ids_by_synonyms: dict[str, OrganizationalUnitID],
    project_coordinators_merged_ids_by_query_string: dict[str, list[PersonID]],
    extracted_primary_source: ExtractedPrimarySource,
) -> Generator[ExtractedResource, None, None]:
    """Transform seq-repo resource to ExtractedResource.

    Args:
        seq_repo_sources: Seq Repo extracted sources
        seq_repo_distributions: Seq Repo extracted distribution
        seq_repo_activities: Seq Repo extracted activity for default values from mapping
        seq_repo_resource: Seq Repo extracted resource
        extracted_primary_source: Extracted primary source

    Returns:
        Generator for ExtractedResource
    """
    access_restriction = seq_repo_resource["accessRestriction"][0]["mappingRules"][0][
        "setValues"
    ]
    accrual_periodicity = seq_repo_resource["contributingUnit"][0]["mappingRules"][0][
        "setValues"
    ]
    anonymization_pseudonymization = seq_repo_resource["anonymizationPseudonymization"][
        0
    ]["mappingRules"][0]["setValues"]
    method = seq_repo_resource["method"][0]["mappingRules"][0]["setValues"]

    resource_type_general = seq_repo_resource["resourceTypeGeneral"][0]["mappingRules"][
        0
    ]["setValues"]
    resource_type_specific = seq_repo_resource["resourceTypeSpecific"][0][
        "mappingRules"
    ][0]["setValues"]
    rights = seq_repo_resource["rights"][0]["mappingRules"][0]["setValues"]
    state_of_data_processing = seq_repo_resource["stateOfDataProcessing"][0][
        "mappingRules"
    ][0]["setValues"]
    theme = seq_repo_resource["theme"][0]["mappingRules"][0]["setValues"]

    for identifier_in_primary_source, source in seq_repo_sources.items():
        distribution = seq_repo_distributions[identifier_in_primary_source]
        activity = seq_repo_activities.get(source.project_id)

        project_coordinators_ids = []
        units_in_charge = []
        for pc in source.project_coordinators:
            person_merged_id = project_coordinators_merged_ids_by_query_string.get(pc)
            if person_merged_id:
                project_coordinators_ids.append(person_merged_id[0])

            for query in seq_repo_source_project_coordinators:
                query_ldap: LDAPPersonWithQuery = query
                if (
                    query_ldap.person.sAMAccountName
                    and query_ldap.person.departmentNumber
                ):
                    if query_ldap.person.sAMAccountName.lower() == pc.lower():
                        unit = unit_merged_ids_by_synonyms.get(
                            query_ldap.person.departmentNumber
                        )
                        if unit:
                            units_in_charge.append(unit)
        if not units_in_charge or not project_coordinators_ids:
            continue

        contributing_unit = unit_merged_ids_by_synonyms.get(source.customer_org_unit_id)

        yield ExtractedResource(
            accessRestriction=access_restriction,
            accrualPeriodicity=accrual_periodicity,
            anonymizationPseudonymization=anonymization_pseudonymization,
            contact=project_coordinators_ids,
            contributingUnit=contributing_unit or [],
            created=source.sequencing_date,
            distribution=distribution.stableTargetId,
            hadPrimarySource=extracted_primary_source.stableTargetId,
            identifierInPrimarySource=identifier_in_primary_source,
            instrumentToolOrApparatus=source.sequencing_platform,
            keyword=source.species,
            method=method,
            publisher=[],  # TODO: publisher -> wikidata
            resourceTypeGeneral=resource_type_general,
            resourceTypeSpecific=resource_type_specific,
            rights=rights,
            stateOfDataProcessing=state_of_data_processing,
            theme=theme,
            title=f"{source.project_name} sample {source.customer_sample_name}",
            unitInCharge=units_in_charge,
            wasGeneratedBy=activity.stableTargetId if activity else None,
        )


def transform_seq_repo_access_platform_to_extracted_access_platform(
    seq_repo_access_platform: dict[str, Any],
    unit_merged_ids_by_synonyms: dict[str, OrganizationalUnitID],
    extracted_primary_source: ExtractedPrimarySource,
) -> ExtractedAccessPlatform:
    """Transform seq-repo access platform to ExtractedAccessPlatform.

    Args:
        seq_repo_access_platform: Seq Repo extracted access platform
        extracted_primary_source: Extracted primary source

    Returns:
        ExtractedAccessPlatform
    """
    alternative_title = seq_repo_access_platform["alternativeTitle"][0]["mappingRules"][
        0
    ]["setValues"]

    description = seq_repo_access_platform["description"][0]["mappingRules"][0][
        "setValues"
    ]
    endpoint_type = seq_repo_access_platform["endpointType"][0]["mappingRules"][0][
        "setValues"
    ]
    identifier_in_primary_source = seq_repo_access_platform[
        "identifierInPrimarySource"
    ][0]["mappingRules"][0]["setValues"]
    landing_page = seq_repo_access_platform["landingPage"][0]["mappingRules"][0][
        "setValues"
    ]

    technical_accessibility = seq_repo_access_platform["technicalAccessibility"][0][
        "mappingRules"
    ][0]["setValues"]
    title = seq_repo_access_platform["title"][0]["mappingRules"][0]["setValues"]

    contacts = seq_repo_access_platform["contact"][0]["mappingRules"][0]["forValues"]

    resolved_organigram = []
    for contact in contacts:
        resolved_organigram.append(unit_merged_ids_by_synonyms.get(contact))

    return ExtractedAccessPlatform(
        alternativeTitle=alternative_title,
        contact=resolved_organigram,
        description=description,
        endpointType=endpoint_type,
        hadPrimarySource=extracted_primary_source.stableTargetId,
        identifierInPrimarySource=identifier_in_primary_source,
        landingPage=landing_page,
        technicalAccessibility=technical_accessibility,
        title=title,
        unitInCharge=resolved_organigram,
    )

    # TODO: update docs everywhere in transform.py
    # TODO: run tests on transform, fix tests
