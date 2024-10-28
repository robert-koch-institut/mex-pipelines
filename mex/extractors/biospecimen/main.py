from mex.common.cli import entrypoint
from mex.common.ldap.transform import transform_ldap_persons_to_mex_persons
from mex.common.models import (
    ExtractedActivity,
    ExtractedOrganization,
    ExtractedOrganizationalUnit,
    ExtractedPerson,
    ExtractedPrimarySource,
    ExtractedResource,
)
from mex.common.primary_source.transform import get_primary_sources_by_name
from mex.common.types import MergedOrganizationalUnitIdentifier
from mex.extractors.biospecimen.extract import (
    extract_biospecimen_contacts_by_email,
    extract_biospecimen_organizations,
    extract_biospecimen_resources,
)
from mex.extractors.biospecimen.models.source import BiospecimenResource
from mex.extractors.biospecimen.transform import (
    transform_biospecimen_resource_to_mex_resource,
)
from mex.extractors.mapping.extract import extract_mapping_data
from mex.extractors.mapping.transform import transform_mapping_data_to_model
from mex.extractors.pipeline import asset, run_job_in_process
from mex.extractors.settings import Settings
from mex.extractors.sinks import load
from mex.extractors.wikidata.extract import (
    get_merged_organization_id_by_query_with_transform_and_load,
)


@asset(group_name="biospecimen", deps=["extracted_primary_source_mex"])
def extracted_primary_source_biospecimen(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return biospecimen primary source and load them to sinks."""
    (extracted_primary_source_biospecimen,) = get_primary_sources_by_name(
        extracted_primary_sources, "biospecimen"
    )
    load([extracted_primary_source_biospecimen])
    return extracted_primary_source_biospecimen


@asset(group_name="biospecimen")
def biospecimen_resources() -> list[BiospecimenResource]:
    """Extract from biospecimen resources."""
    return list(extract_biospecimen_resources())


@asset(group_name="biospecimen")
def extracted_mex_persons(
    biospecimen_resources: list[BiospecimenResource],
    extracted_primary_source_ldap: ExtractedPrimarySource,
    extracted_organizational_units: list[ExtractedOrganizationalUnit],
) -> list[ExtractedPerson]:
    """Extract ldap persons for biospecimen from ldap and transform them to mex persons and load them to sinks."""  # noqa: E501
    ldap_persons = extract_biospecimen_contacts_by_email(biospecimen_resources)
    mex_persons = list(
        transform_ldap_persons_to_mex_persons(
            ldap_persons, extracted_primary_source_ldap, extracted_organizational_units
        )
    )
    load(mex_persons)
    return mex_persons


@asset(group_name="biospecimen")
def extracted_biospecimen_resources(
    biospecimen_resources: list[BiospecimenResource],
    extracted_primary_source_biospecimen: ExtractedPrimarySource,
    extracted_mex_persons: list[ExtractedPerson],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_organization_rki: ExtractedOrganization,
    extracted_synopse_activities: list[ExtractedActivity],
    extracted_primary_source_wikidata: ExtractedPrimarySource,
) -> list[ExtractedResource]:
    """Transform biospecimen resources to extracted resources and load them to the sinks."""  # noqa: E501
    settings = Settings.get()
    resource_mapping = transform_mapping_data_to_model(
        extract_mapping_data(settings.biospecimen.mapping_path / "resource.yaml"),
        ExtractedResource,
    )
    biospecimen_organizations = extract_biospecimen_organizations(biospecimen_resources)
    extracted_organizations = (
        get_merged_organization_id_by_query_with_transform_and_load(
            biospecimen_organizations, extracted_primary_source_wikidata
        )
    )
    mex_sources = list(
        transform_biospecimen_resource_to_mex_resource(
            biospecimen_resources,
            extracted_primary_source_biospecimen,
            unit_stable_target_ids_by_synonym,
            extracted_mex_persons,
            extracted_organization_rki,
            extracted_synopse_activities,
            resource_mapping,
            extracted_organizations,
        )
    )
    load(mex_sources)
    return mex_sources


@entrypoint(Settings)
def run() -> None:
    """Run the biospecimen extractor job in-process."""
    run_job_in_process("biospecimen")
