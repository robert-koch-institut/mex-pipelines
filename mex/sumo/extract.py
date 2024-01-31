from typing import Generator, Iterable

import numpy as np
import yaml
from pandas import ExcelFile

from mex.common.identity import get_provider
from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.actor import LDAPActor
from mex.common.ldap.models.person import LDAPPersonWithQuery
from mex.common.ldap.transform import analyse_person_string
from mex.common.models import ExtractedPrimarySource
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.sumo.models.access_platform import SumoAccessPlatform
from mex.sumo.models.activity import SumoActivity
from mex.sumo.models.cc1_data_model_nokeda import Cc1DataModelNoKeda
from mex.sumo.models.cc1_data_valuesets import Cc1DataValuesets
from mex.sumo.models.cc2_aux_mapping import Cc2AuxMapping
from mex.sumo.models.cc2_aux_model import Cc2AuxModel
from mex.sumo.models.cc2_aux_valuesets import Cc2AuxValuesets
from mex.sumo.models.cc2_feat_projection import Cc2FeatProjection
from mex.sumo.models.resource_feat_model import ResourceFeatModel
from mex.sumo.models.resource_nokeda import ResourceNokeda
from mex.sumo.settings import SumoSettings


def extract_cc1_data_valuesets() -> Generator[Cc1DataValuesets, None, None]:
    """Extract data from cc1_data_valuesets_v3.0.3.xlsx file.

    Settings:
        raw_data_path: path to directory holding sumo raw data.

    Returns:
        Generator of cc1_data_valuesets instances
    """
    settings = SumoSettings.get()
    excel_path = settings.raw_data_path / "cc1_data_valuesets_v3.0.3.xlsx"
    excel_file = ExcelFile(excel_path)
    for sheet_name in excel_file.sheet_names:
        data_valuesets = excel_file.parse(sheet_name=sheet_name)
        for _, row in data_valuesets.iterrows():
            row.replace(to_replace=np.nan, value=None, inplace=True)
            row.replace(regex=r"^\s*$", value=None, inplace=True)
            yield Cc1DataValuesets(**row, sheet_name=sheet_name)


def extract_cc1_data_model_nokeda() -> Generator[Cc1DataModelNoKeda, None, None]:
    """Extract data from cc1_data_model_NoKeda_v3.0.3.xlsx file.

    Settings:
        raw_data_path: path to directory holding sumo raw data.

    Returns:
        Generator of Cc1DataModelNoKeda instances
    """
    settings = SumoSettings.get()
    excel_path = settings.raw_data_path / "cc1_data_model_NoKeda_v3.0.3.xlsx"
    excel_file = ExcelFile(excel_path)
    sheet_name = "datamodel NoKeda"
    data_model_nokeda = excel_file.parse(sheet_name=sheet_name)
    for _, row in data_model_nokeda.iterrows():
        yield Cc1DataModelNoKeda(**row)


def extract_cc2_aux_model() -> Generator[Cc2AuxModel, None, None]:
    """Extract data from cc2_aux_model_v3.0.3.xlsx file.

    Settings:
        raw_data_path: path to directory holding sumo raw data.

    Returns:
        Generator of cc2_aux_model instances
    """
    settings = SumoSettings.get()
    excel_path = settings.raw_data_path / "cc2_aux_model_v3.0.3.xlsx"
    excel_file = ExcelFile(excel_path)
    sheet_name = "datamodel aux"
    aux_model = excel_file.parse(sheet_name=sheet_name)
    for _, row in aux_model.iterrows():
        yield Cc2AuxModel(**row)


def extract_cc2_aux_mapping(
    sumo_cc2_aux_model: Iterable[Cc2AuxModel],
) -> Generator[Cc2AuxMapping, None, None]:
    """Extract data from cc2_aux_mapping_v3.0.3.xlsx file.

    Args:
        sumo_cc2_aux_model: Cc2AuxModel variables

    Settings:
        raw_data_path: path to directory holding sumo raw data.

    Returns:
        Generator of cc2_aux_mapping instances
    """
    settings = SumoSettings.get()
    excel_path = settings.raw_data_path / "cc2_aux_mapping_v3.0.3.xlsx"
    excel_file = ExcelFile(excel_path)
    for row in sumo_cc2_aux_model:
        sheet_name = row.depends_on_nokeda_variable
        aux_mapping = excel_file.parse(sheet_name=sheet_name)
        yield Cc2AuxMapping(
            sheet_name=sheet_name,
            variable_name_column=aux_mapping[row.variable_name].tolist(),
        )


def extract_cc2_aux_valuesets() -> Generator[Cc2AuxValuesets, None, None]:
    """Extract data from cc2_aux_valuesets_v3.0.3.xlsx file.

    Settings:
        raw_data_path: path to directory holding sumo raw data.

    Returns:
        Generator of cc2_aux_valuesets instances
    """
    settings = SumoSettings.get()
    excel_path = settings.raw_data_path / "cc2_aux_valuesets_v3.0.3.xlsx"
    excel_file = ExcelFile(excel_path)
    sheet_name = "aux_cedis_groups"
    aux_valuesets = excel_file.parse(sheet_name=sheet_name)
    for _, row in aux_valuesets.iterrows():
        yield Cc2AuxValuesets(**row)


def extract_cc2_feat_projection() -> Generator[Cc2FeatProjection, None, None]:
    """Extract data from cc2_feat_projection_v3.0.3.xlsx file.

    Settings:
        raw_data_path: path to directory holding sumo raw data.

    Returns:
        Generator of cc2_feat_projection instances
    """
    settings = SumoSettings.get()
    excel_path = settings.raw_data_path / "cc2_feat_projection_v3.0.3.xlsx"
    excel_file = ExcelFile(excel_path)
    sheet_name = "feat_syndrome"
    aux_valuesets = excel_file.parse(sheet_name=sheet_name)
    for _, row in aux_valuesets.iterrows():
        yield Cc2FeatProjection(**row)


def extract_sumo_access_platform() -> SumoAccessPlatform:
    """Extract Access Platform by loading `access-platform.yaml` from `mapping_path`.

    Settings:
        mapping_path: path to directory holding sumo mapping.

    Returns:
        Sumo Access Platform
    """
    settings = SumoSettings.get()
    with open(
        settings.mapping_path / "access-platform.yaml", "r", encoding="utf-8"
    ) as f:
        access_platform_info = yaml.safe_load(f)

    return SumoAccessPlatform.model_validate(access_platform_info)


def extract_sumo_activity() -> SumoActivity:
    """Extract Sumo Activity by loading `activity.yaml` from `mapping_path`.

    Settings:
        mapping_path: path to directory holding sumo mapping.

    Returns:
        Sumo Activity
    """
    settings = SumoSettings.get()
    with open(settings.mapping_path / "activity.yaml", "r", encoding="utf-8") as f:
        activity = yaml.safe_load(f)

    return SumoActivity.model_validate(activity)


def extract_sumo_resources_nokeda() -> ResourceNokeda:
    """Extract Resource by loading data from mapping/sumo/resource_nokeda.yaml.

    Settings:
        mapping_path: path to directory holding sumo mapping.

    Returns:
        Resource Nokeda
    """
    settings = SumoSettings.get()
    with open(
        settings.mapping_path / "resource_nokeda.yaml", "r", encoding="utf-8"
    ) as f:
        resource_nokeda = yaml.safe_load(f)

    return ResourceNokeda.model_validate(resource_nokeda)


def extract_sumo_resources_feat() -> ResourceFeatModel:
    """Extract ResourceFeatModel from mapping/sumo/resource_feat-model.yaml.

    Settings:
        mapping_path: path to directory holding sumo mapping.

    Returns:
        Resource Feat Model
    """
    settings = SumoSettings.get()
    with open(
        settings.mapping_path / "resource_feat-model.yaml",
        "r",
        encoding="utf-8",
    ) as f:
        resource_feat_model = yaml.safe_load(f)

    return ResourceFeatModel.model_validate(resource_feat_model)


def extract_ldap_contact_points_by_emails(
    extracted_resources: Iterable[ResourceNokeda | ResourceFeatModel],
) -> Generator[LDAPActor, None, None]:
    """Extract contact points from ldap for email in resource contacts.

    Args:
        extracted_resources: iterable of sumo resources

    Returns:
        Iterable of ldap actors
    """
    connector = LDAPConnector.get()

    emails = {
        r.contact[0]["mappingRules"][0]["forValues"][0] for r in extracted_resources
    }
    return (
        actor for email in emails for actor in connector.get_functional_accounts(email)
    )


def extract_ldap_contact_points_by_name(
    sumo_access_platform: SumoAccessPlatform,
) -> Generator[LDAPPersonWithQuery, None, None]:
    """Extract contact points from ldap for contact name in Sumo access platform.

    Args:
        sumo_access_platform: SUMO extracted access platform

    Returns:
        Iterable of ldap persons with query
    """
    connector = LDAPConnector.get()
    names = sumo_access_platform.contact[0]["mappingRules"][0]["forValues"]
    split_names = [
        split_name for name in names for split_name in analyse_person_string(name)
    ]
    for split_name in split_names:
        persons = list(
            connector.get_persons(
                surname=split_name.surname, given_name=split_name.given_name
            )
        )
        if len(persons) == 1 and persons[0].objectGUID:
            yield LDAPPersonWithQuery(person=persons[0], query=names)


def extract_sumo_organizations(
    sumo_sumo_resource_nokeda: ResourceNokeda,
) -> dict[str, WikidataOrganization]:
    """Search and extract sumo organization from wikidata.

    Args:
        sumo_sumo_resource_nokeda: sumo resource nokeda

    Returns:
        Dict with organization label and WikidataOrganization
    """
    sumo_resource_organizations = {}
    publisher = sumo_sumo_resource_nokeda.publisher[0]["mappingRules"][0]["forValues"][
        0
    ]
    for label in [publisher]:
        if (
            label
            and (orgs := list(search_organization_by_label(label)))
            and len(orgs) == 1
        ):
            sumo_resource_organizations[label] = orgs[0]
    return sumo_resource_organizations


def get_organization_merged_id_by_query(
    sumo_organizations: dict[str, WikidataOrganization],
    wikidata_primary_source: ExtractedPrimarySource,
) -> dict[str, str]:
    """Return a mapping from organizations to their stable target ID.

    There may be multiple entries per unit mapping to the same stable target ID.

    Args:
        sumo_organizations: Iterable of extracted organizations
        wikidata_primary_source: Primary source item for wikidata

    Returns:
        Dict with organization label and stable target ID
    """
    identity_provider = get_provider()
    organization_stable_target_id_by_query = {}
    for query, wikidata_organization in sumo_organizations.items():
        identities = identity_provider.fetch(
            had_primary_source=wikidata_primary_source.stableTargetId,
            identifier_in_primary_source=wikidata_organization.identifier,
        )
        if identities:
            organization_stable_target_id_by_query[query] = str(
                identities[0].stableTargetId
            )

    return organization_stable_target_id_by_query
