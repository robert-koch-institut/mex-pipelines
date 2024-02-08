from typing import Any, Generator

from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedDistribution,
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.types import Identifier
from mex.seq_repo.models.source import SeqRepoSource


def transform_seq_repo_activities_to_extracted_activities(
    seq_repo_sources: dict[str, SeqRepoSource],
    seq_repo_activity: dict[str, Any],
    extracted_primary_source: ExtractedPrimarySource,
) -> Generator[ExtractedActivity, None, None]:
    """Transform seq-repo activity to ExtractedActivity.

    Args:
        seq_repo_sources: Seq Repo extracted sources
        seq_repo_activity: Seq Repo extracted activity for default values from mapping
        extracted_primary_source: Extracted primary source

    Returns:
        Generator for ExtractedActivity
    """
    theme = seq_repo_activity["theme"][0]["mappingRules"][0]["setValues"]
    for _, source in seq_repo_sources.items():
        yield ExtractedActivity(
            contact=[
                Identifier.generate()
            ],  # TODO: resolve 'source.project-coordinators' with ldap
            hadPrimarySource=extracted_primary_source.stableTargetId,
            identifierInPrimarySource=source.project_id,
            involvedPerson=[],  # TODO: resolve 'source.project-coordinators' with ldap
            responsibleUnit=[
                Identifier.generate()
            ],  # TODO: resolve 'source.project-coordinators' with ldap
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
    accrual_periodicity = seq_repo_resource["accrualPeriodicity"][0]["mappingRules"][0][
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
        activity = seq_repo_activities[source.project_id]

        yield ExtractedResource(
            accessRestriction=access_restriction,
            accrualPeriodicity=accrual_periodicity,
            anonymizationPseudonymization=anonymization_pseudonymization,
            contact=[
                Identifier.generate()
            ],  # TODO: source.project_coordinators -> ldap
            contributingUnit=[],  # TODO: source.customer_org_unit_id -> organigram
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
            unitInCharge=[
                Identifier.generate()
            ],  # TODO: source.project_coordinators -> ldap, organigram
            wasGeneratedBy=activity.stableTargetId,
        )


def transform_seq_repo_access_platform_to_extracted_access_platform(
    seq_repo_access_platform: dict[str, Any],
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

    return ExtractedAccessPlatform(
        alternativeTitle=alternative_title,
        contact=[],  # TODO: resolve with organigram
        description=description,
        endpointType=endpoint_type,
        hadPrimarySource=extracted_primary_source.stableTargetId,
        identifierInPrimarySource=identifier_in_primary_source,
        landingPage=landing_page,
        technicalAccessibility=technical_accessibility,
        title=title,
        unitInCharge=[],  # TODO: resolve with organigram
    )
