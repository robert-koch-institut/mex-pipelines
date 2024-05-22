from pathlib import Path
from typing import Any

from mex.common.cli import entrypoint
from mex.common.ldap.transform import (
    transform_ldap_actors_to_mex_contact_points,
    transform_ldap_persons_to_mex_persons,
)
from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedOrganizationalUnit,
    ExtractedPerson,
    ExtractedPrimarySource,
    ExtractedResource,
    ExtractedVariableGroup,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.common.types import (
    Email,
    MergedContactPointIdentifier,
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
)
from mex.grippeweb.extract import (
    extract_columns_by_table_and_column_name,
    extract_grippeweb_organizations,
    extract_ldap_actors,
    extract_ldap_persons,
)
from mex.grippeweb.settings import GrippewebSettings
from mex.grippeweb.transform import (
    transform_grippeweb_access_platform_to_extracted_access_platform,
    transform_grippeweb_resource_mappings_to_extracted_resources,
)
from mex.mapping.extract import extract_mapping_data
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load
from mex.sumo.transform import get_contact_merged_ids_by_emails
from mex.wikidata.transform import (
    transform_wikidata_organizations_to_extracted_organizations_with_query,
)


@asset(group_name="grippeweb", deps=["extracted_primary_source_mex"])
def extracted_primary_source_grippeweb(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return Grippeweb primary source."""
    (extracted_primary_sources_grippeweb,) = get_primary_sources_by_name(
        extracted_primary_sources, "grippeweb"
    )
    load([extracted_primary_sources_grippeweb])

    return extracted_primary_sources_grippeweb


@asset(group_name="grippeweb")
def grippeweb_columns() -> dict[str, dict[str, list[Any]]]:
    """Extract Grippeweb SQL Server columns."""
    return extract_columns_by_table_and_column_name()


@asset(group_name="grippeweb")
def grippeweb_access_platform() -> dict[str, Any]:
    """Extract Grippeweb `access_platform` default values."""
    settings = GrippewebSettings.get()
    return extract_mapping_data(
        settings.mapping_path / "access-platform.yaml", ExtractedAccessPlatform
    )


@asset(group_name="grippeweb")
def grippeweb_resource_mappings() -> list[dict[str, Any]]:
    """Extract Grippeweb resource mappings."""
    settings = GrippewebSettings.get()
    return [
        extract_mapping_data(file, ExtractedResource)
        for file in Path(settings.mapping_path).glob("resource_*.yaml")
    ]


@asset(group_name="grippeweb")
def grippeweb_variable_group() -> dict[str, Any]:
    """Extract Grippeweb `variable_group` default values."""
    settings = GrippewebSettings.get()
    return extract_mapping_data(
        settings.mapping_path / "variable-group.yaml", ExtractedVariableGroup
    )


@asset(group_name="grippeweb")
def extracted_mex_functional_units_grippeweb(
    grippeweb_resource_mappings: list[dict[str, Any]],
    extracted_primary_source_ldap: ExtractedPrimarySource,
) -> dict[Email, MergedContactPointIdentifier]:
    """Extract ldap persons for grippeweb from ldap and transform them to mex persons and load them to sinks."""  # noqa: E501
    ldap_actors = extract_ldap_actors(grippeweb_resource_mappings)
    mex_actors_resources = list(
        transform_ldap_actors_to_mex_contact_points(
            ldap_actors, extracted_primary_source_ldap
        )
    )
    load(mex_actors_resources)
    return get_contact_merged_ids_by_emails(mex_actors_resources)


@asset(group_name="grippeweb")
def extracted_mex_persons_grippeweb(
    grippeweb_resource_mappings: list[dict[str, Any]],
    grippeweb_access_platform: dict[str, Any],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
) -> list[ExtractedPerson]:
    """Extract ldap persons for grippeweb from ldap and transform them to mex persons and load them to sinks."""  # noqa: E501
    ldap_persons = extract_ldap_persons(
        grippeweb_resource_mappings, grippeweb_access_platform
    )
    mex_persons = list(
        transform_ldap_persons_to_mex_persons(
            ldap_persons, extracted_primary_source_ldap, extracted_organizational_units
        )
    )
    load(mex_persons)
    return mex_persons


@asset(group_name="grippeweb")
def grippeweb_organization_ids_by_query_string(
    grippeweb_resource_mappings: list[dict[str, Any]],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> dict[str, MergedOrganizationIdentifier]:
    """Extract organizations for grippeweb from wikidata and group them by query."""
    wikidata_organizations_by_query = extract_grippeweb_organizations(
        grippeweb_resource_mappings
    )

    extracted_organizations_by_query = (
        transform_wikidata_organizations_to_extracted_organizations_with_query(
            wikidata_organizations_by_query, extracted_primary_source_wikidata
        )
    )
    load(extracted_organizations_by_query.values())

    return {
        query: MergedOrganizationIdentifier(organization.stableTargetId)
        for query, organization in extracted_organizations_by_query.items()
    }


@asset(group_name="grippeweb")
def extracted_access_platform_grippeweb(
    grippeweb_access_platform: dict[str, Any],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_primary_source_grippeweb: ExtractedPrimarySource,
    extracted_mex_functional_units_grippeweb: dict[Email, MergedContactPointIdentifier],
) -> ExtractedAccessPlatform:
    """Transform Grippeweb values to extracted access platform and load to sinks."""
    extracted_access_platform_grippeweb = (
        transform_grippeweb_access_platform_to_extracted_access_platform(
            grippeweb_access_platform,
            unit_stable_target_ids_by_synonym,
            extracted_primary_source_grippeweb,
            extracted_mex_functional_units_grippeweb,
        )
    )
    load([extracted_access_platform_grippeweb])
    return extracted_access_platform_grippeweb


@asset(group_name="grippeweb")
def grippeweb_extracted_resources(
    grippeweb_resource_mappings: list[dict[str, Any]],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_access_platform_grippeweb: ExtractedAccessPlatform,
    extracted_primary_source_grippeweb: ExtractedPrimarySource,
    extracted_mex_persons_grippeweb: list[ExtractedPerson],
    grippeweb_organization_ids_by_query_string: dict[str, MergedOrganizationIdentifier],
    extracted_mex_functional_units_grippeweb: dict[Email, MergedContactPointIdentifier],
    # extracted_confluence_vvt_sources: list[ExtractedActivity],
) -> list[ExtractedResource]:
    """Transform Grippeweb default values to extracted resources and load to sinks."""
    extracted_resources = transform_grippeweb_resource_mappings_to_extracted_resources(
        grippeweb_resource_mappings,
        unit_stable_target_ids_by_synonym,
        extracted_access_platform_grippeweb,
        extracted_primary_source_grippeweb,
        extracted_mex_persons_grippeweb,
        grippeweb_organization_ids_by_query_string,
        extracted_mex_functional_units_grippeweb,
        # extracted_confluence_vvt_sources,
    )
    load(extracted_resources)
    return extracted_resources


@entrypoint(GrippewebSettings)
def run() -> None:
    """Run the Grippeweb extractor job in-process."""
    run_job_in_process("grippeweb")
