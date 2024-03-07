from typing import Any

from mex.common.cli import entrypoint
from mex.common.ldap.transform import (
    transform_ldap_actors_to_mex_contact_points,
    transform_ldap_persons_with_query_to_mex_persons,
)
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedActivity,
    ExtractedOrganization,
    ExtractedOrganizationalUnit,
    ExtractedPrimarySource,
    ExtractedResource,
    ExtractedVariable,
    ExtractedVariableGroup,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.common.types import (
    Email,
    MergedContactPointIdentifier,
    MergedOrganizationalUnitIdentifier,
)
from mex.common.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations,
)
from mex.mapping.extract import extract_mapping_data
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load
from mex.sumo.extract import (
    extract_cc1_data_model_nokeda,
    extract_cc1_data_valuesets,
    extract_cc2_aux_mapping,
    extract_cc2_aux_model,
    extract_cc2_aux_valuesets,
    extract_cc2_feat_projection,
    extract_ldap_contact_points_by_emails,
    extract_ldap_contact_points_by_name,
    extract_sumo_organizations,
    get_organization_merged_id_by_query,
)
from mex.sumo.filter import filter_and_log_cc2_aux_model
from mex.sumo.models.cc1_data_model_nokeda import Cc1DataModelNoKeda
from mex.sumo.models.cc2_aux_model import Cc2AuxModel
from mex.sumo.models.cc2_feat_projection import Cc2FeatProjection
from mex.sumo.settings import SumoSettings
from mex.sumo.transform import (
    get_contact_merged_ids_by_emails,
    get_contact_merged_ids_by_names,
    transform_feat_projection_variable_to_mex_variable,
    transform_feat_variable_to_mex_variable_group,
    transform_model_nokeda_variable_to_mex_variable_group,
    transform_nokeda_aux_variable_to_mex_variable,
    transform_nokeda_aux_variable_to_mex_variable_group,
    transform_nokeda_model_variable_to_mex_variable,
    transform_resource_feat_model_to_mex_resource,
    transform_resource_nokeda_to_mex_resource,
    transform_sumo_access_platform_to_mex_access_platform,
    transform_sumo_activity_to_extracted_activity,
)


@asset(group_name="sumo", deps=["extracted_primary_source_mex"])
def extracted_primary_source_sumo(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return SUMO primary source."""
    (extracted_primary_sumo,) = get_primary_sources_by_name(
        extracted_primary_sources, "nokeda"
    )
    load([extracted_primary_sumo])
    return extracted_primary_sumo


@asset(group_name="sumo")
def transformed_sumo_access_platform(
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_primary_source_sumo: ExtractedPrimarySource,
) -> None:
    """Transform and load SUMO access platform and related LDAP actors."""
    settings = SumoSettings.get()
    sumo_access_platform = extract_mapping_data(
        settings.mapping_path / "access-platform.yaml",
        ExtractedAccessPlatform,
    )
    ldap_contact_points_access_platform = extract_ldap_contact_points_by_name(
        sumo_access_platform
    )
    mex_actors_access_platform = list(
        transform_ldap_persons_with_query_to_mex_persons(
            ldap_contact_points_access_platform,
            extracted_primary_source_ldap,
            extracted_organizational_units,
        )
    )
    load(mex_actors_access_platform)

    contact_merged_ids_by_name = get_contact_merged_ids_by_names(
        mex_actors_access_platform
    )
    transformed_access_platform = transform_sumo_access_platform_to_mex_access_platform(
        sumo_access_platform,
        unit_stable_target_ids_by_synonym,
        contact_merged_ids_by_name,
        extracted_primary_source_sumo,
    )
    load([transformed_access_platform])


@asset(group_name="sumo")
def contact_merged_ids_by_emails_sumo(
    extracted_resources_nokeda_sumo: dict[str, Any],
    extracted_resources_feat_sumo: dict[str, Any],
    extracted_primary_source_ldap: ExtractedPrimarySource,
) -> dict[Email, MergedContactPointIdentifier]:
    """Load contacts related to resources and return them by their e-mail addresses."""
    ldap_contact_points_resources = list(
        extract_ldap_contact_points_by_emails(
            [extracted_resources_nokeda_sumo, extracted_resources_feat_sumo]
        )
    )
    mex_actors_resources = list(
        transform_ldap_actors_to_mex_contact_points(
            ldap_contact_points_resources, extracted_primary_source_ldap
        )
    )
    load(mex_actors_resources)
    return get_contact_merged_ids_by_emails(mex_actors_resources)


@asset(group_name="sumo")
def transformed_activity_sumo(
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    contact_merged_ids_by_emails_sumo: dict[Email, MergedContactPointIdentifier],
    extracted_primary_source_sumo: ExtractedPrimarySource,
) -> ExtractedActivity:
    """Extract, transform and load SUMO activity."""
    settings = SumoSettings.get()
    sumo_activity = extract_mapping_data(
        settings.mapping_path / "activity.yaml", ExtractedActivity
    )
    transformed_activity = transform_sumo_activity_to_extracted_activity(
        sumo_activity,
        unit_stable_target_ids_by_synonym,
        contact_merged_ids_by_emails_sumo,
        extracted_primary_source_sumo,
    )
    load([transformed_activity])
    return transformed_activity


@asset(group_name="sumo")
def extracted_resources_nokeda_sumo() -> dict[str, Any]:
    """Extract Nokeda Resource from SUMO."""
    settings = SumoSettings.get()
    return extract_mapping_data(
        settings.mapping_path / "resource_nokeda.yaml", ExtractedResource
    )


@asset(group_name="sumo")
def extracted_resources_feat_sumo() -> dict[str, Any]:
    """Extract Resource feat from SUMO."""
    settings = SumoSettings.get()
    return extract_mapping_data(
        settings.mapping_path / "resource_feat-model.yaml",
        ExtractedResource,
    )


@asset(group_name="sumo")
def extracted_cc1_data_model_nokeda_sumo() -> list[Cc1DataModelNoKeda]:
    """Extract Cc1 data model from SUMO."""
    return list(extract_cc1_data_model_nokeda())


@asset(group_name="sumo")
def extracted_cc2_aux_model_sumo(
    extracted_primary_source_sumo: ExtractedPrimarySource,
) -> list[Cc2AuxModel]:
    """Extract Cc2 auxiliary model from SUMO."""
    sumo_cc2_aux_model = list(extract_cc2_aux_model())
    return list(
        filter_and_log_cc2_aux_model(sumo_cc2_aux_model, extracted_primary_source_sumo)
    )


@asset(group_name="sumo")
def extracted_cc2_feat_projection() -> list[Cc2FeatProjection]:
    """Extract Cc2 features from SUMO data."""
    return list(extract_cc2_feat_projection())


@asset(group_name="sumo")
def organization_stable_target_id_by_query_sumo(
    extracted_resources_nokeda_sumo: dict[str, Any],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> dict[str, str]:
    """Extract and load SUMO organizations and return them by stable target ids."""
    sumo_organizations = extract_sumo_organizations(extracted_resources_nokeda_sumo)
    mex_extracted_organizations = list(
        transform_wikidata_organizations_to_extracted_organizations(
            sumo_organizations.values(), extracted_primary_source_wikidata
        )
    )
    load(mex_extracted_organizations)
    return get_organization_merged_id_by_query(
        sumo_organizations, extracted_primary_source_wikidata
    )


@asset(group_name="sumo")
def transformed_resource_nokeda_sumo(
    extracted_resources_nokeda_sumo: dict[str, Any],
    extracted_primary_source_sumo: ExtractedPrimarySource,
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    contact_merged_ids_by_emails_sumo: dict[Email, MergedContactPointIdentifier],
    extracted_organization_rki: ExtractedOrganization,
    transformed_activity_sumo: ExtractedActivity,
) -> ExtractedResource:
    """Transform and load extracted Nokeda Resource from SUMO."""
    mex_resource_nokeda = transform_resource_nokeda_to_mex_resource(
        extracted_resources_nokeda_sumo,
        extracted_primary_source_sumo,
        unit_stable_target_ids_by_synonym,
        contact_merged_ids_by_emails_sumo,
        extracted_organization_rki,
        transformed_activity_sumo,
    )
    load([mex_resource_nokeda])
    return mex_resource_nokeda


@asset(group_name="sumo")
def transformed_resource_feat_sumo(
    extracted_resources_feat_sumo: dict[str, Any],
    extracted_primary_source_sumo: ExtractedPrimarySource,
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    contact_merged_ids_by_emails_sumo: dict[Email, MergedContactPointIdentifier],
    transformed_resource_nokeda_sumo: ExtractedResource,
    transformed_activity_sumo: ExtractedActivity,
) -> ExtractedResource:
    """Transform and load extracted SUMO Resource feat."""
    mex_resource_feat = transform_resource_feat_model_to_mex_resource(
        extracted_resources_feat_sumo,
        extracted_primary_source_sumo,
        unit_stable_target_ids_by_synonym,
        contact_merged_ids_by_emails_sumo,
        transformed_resource_nokeda_sumo,
        transformed_activity_sumo,
    )
    load([mex_resource_feat])
    return mex_resource_feat


@asset(group_name="sumo")
def transformed_nokeda_aux_variable_group(
    extracted_cc2_aux_model_sumo: list[Cc2AuxModel],
    extracted_primary_source_sumo: ExtractedPrimarySource,
    transformed_resource_nokeda_sumo: ExtractedResource,
) -> list[ExtractedVariableGroup]:
    """Transform Nokeda auxiliary variables to MeX variable groups and load them."""
    mex_variable_groups_nokeda_aux = list(
        transform_nokeda_aux_variable_to_mex_variable_group(
            extracted_cc2_aux_model_sumo,
            extracted_primary_source_sumo,
            transformed_resource_nokeda_sumo,
        )
    )
    load(mex_variable_groups_nokeda_aux)
    return mex_variable_groups_nokeda_aux


@asset(group_name="sumo")
def transformed_nokeda_variable_group(
    extracted_cc1_data_model_nokeda_sumo: list[Cc1DataModelNoKeda],
    extracted_primary_source_sumo: ExtractedPrimarySource,
    transformed_resource_nokeda_sumo: ExtractedResource,
) -> list[ExtractedVariableGroup]:
    """Transform Nokeda variables to MeX variable groups and load them."""
    mex_variable_groups_model_nokeda = list(
        transform_model_nokeda_variable_to_mex_variable_group(
            extracted_cc1_data_model_nokeda_sumo,
            extracted_primary_source_sumo,
            transformed_resource_nokeda_sumo,
        )
    )
    load(mex_variable_groups_model_nokeda)
    return mex_variable_groups_model_nokeda


@asset(group_name="sumo")
def transformed_sumo_feat_variable_group(
    extracted_cc2_feat_projection: list[Cc2FeatProjection],
    extracted_primary_source_sumo: ExtractedPrimarySource,
    transformed_resource_nokeda_sumo: ExtractedResource,
) -> list[ExtractedVariableGroup]:
    """Transform SUMO Resource feat to MEx variable groups and load them."""
    mex_variable_groups_feat = list(
        transform_feat_variable_to_mex_variable_group(
            extracted_cc2_feat_projection,
            extracted_primary_source_sumo,
            transformed_resource_nokeda_sumo,
        )
    )
    load(mex_variable_groups_feat)
    return mex_variable_groups_feat


@asset(group_name="sumo")
def transformed_nokeda_model_variables(
    extracted_cc1_data_model_nokeda_sumo: list[Cc1DataModelNoKeda],
    transformed_nokeda_variable_group: list[ExtractedVariableGroup],
    transformed_resource_nokeda_sumo: ExtractedResource,
    extracted_primary_source_sumo: ExtractedPrimarySource,
) -> list[ExtractedVariable]:
    """Transform Nokeda variables to extracted variables and load them."""
    sumo_cc1_data_valuesets = extract_cc1_data_valuesets()
    transformed_nokeda_model_variable = list(
        transform_nokeda_model_variable_to_mex_variable(
            extracted_cc1_data_model_nokeda_sumo,
            sumo_cc1_data_valuesets,
            transformed_nokeda_variable_group,
            transformed_resource_nokeda_sumo,
            extracted_primary_source_sumo,
        )
    )
    load(transformed_nokeda_model_variable)
    return transformed_nokeda_model_variable


@asset(group_name="sumo")
def transformed_nokeda_aux_variables(
    extracted_cc2_aux_model_sumo: list[Cc2AuxModel],
    transformed_nokeda_aux_variable_group: list[ExtractedVariableGroup],
    transformed_resource_nokeda_sumo: ExtractedResource,
    extracted_primary_source_sumo: ExtractedPrimarySource,
) -> list[ExtractedVariable]:
    """Transform Nokeda aux variables to extracted variables and load them."""
    sumo_cc2_aux_mapping = extract_cc2_aux_mapping(extracted_cc2_aux_model_sumo)
    sumo_cc2_aux_valuesets = extract_cc2_aux_valuesets()

    transformed_nokeda_aux_variables = list(
        transform_nokeda_aux_variable_to_mex_variable(
            extracted_cc2_aux_model_sumo,
            sumo_cc2_aux_mapping,
            sumo_cc2_aux_valuesets,
            transformed_nokeda_aux_variable_group,
            transformed_resource_nokeda_sumo,
            extracted_primary_source_sumo,
        )
    )
    load(transformed_nokeda_aux_variables)
    return transformed_nokeda_aux_variables


@asset(group_name="sumo")
def transformed_sumo_feat_projection_variables(
    extracted_cc2_feat_projection: list[Cc2FeatProjection],
    transformed_sumo_feat_variable_group: list[ExtractedVariableGroup],
    transformed_resource_feat_sumo: ExtractedResource,
    extracted_primary_source_sumo: ExtractedPrimarySource,
) -> list[ExtractedVariable]:
    """Transform SUMO feat projection variables to extracted variables and load them."""
    transformed_feat_projection_variable = list(
        transform_feat_projection_variable_to_mex_variable(
            extracted_cc2_feat_projection,
            transformed_sumo_feat_variable_group,
            transformed_resource_feat_sumo,
            extracted_primary_source_sumo,
        )
    )
    load(transformed_feat_projection_variable)
    return transformed_feat_projection_variable


@entrypoint(SumoSettings)
def run() -> None:
    """Run the sumo extractor job in-process."""
    run_job_in_process("sumo")
