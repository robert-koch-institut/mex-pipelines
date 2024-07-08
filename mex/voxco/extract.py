from typing import Any

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.drop import DropApiConnector
from mex.voxco.model import VoxcoVariable


def extract_voxco_variables() -> dict[str, list[VoxcoVariable]]:
    """Extract voxco variables by loading data from mex-drop source json file.

    Returns:
        lists of voxco variables by json file name
    """
    connector = DropApiConnector.get()
    files = connector.list_files("voxco")
    data = {
        file_name: connector.get_file("voxco", file_name)
        for file_name in files
        if "test_" not in file_name
    }
    return {
        file_name: [VoxcoVariable.model_validate(item) for item in file_rows["value"]]
        for file_name, file_rows in data.items()
    }


def extract_voxco_organizations(
    voxco_resource_mappings: list[dict[str, Any]],
) -> dict[str, WikidataOrganization]:
    """Search and extract voxco organization from wikidata.

    Args:
        voxco_resource_mappings: voxco resource mappings

    Returns:
        Dict with organization label and WikidataOrganization
    """
    voxco_resource_organizations = {}
    external_partners = [
        mapping["externalPartner"][0]["mappingRules"][0]["forValues"][0]
        for mapping in voxco_resource_mappings
        if mapping.get("externalPartner")
    ]
    for external_partner in external_partners:
        if external_partner and (org := search_organization_by_label(external_partner)):
            voxco_resource_organizations[external_partner] = org
    return voxco_resource_organizations


def extract_ldap_persons_voxco(
    voxco_resource_mappings: list[dict[str, Any]],
) -> list[LDAPPerson]:
    """Extract LDAP persons for voxco.

    Args:
        voxco_resource_mappings: list of resources default value dictss

    Returns:
        list of LDAP persons
    """
    ldap = LDAPConnector.get()
    return [
        ldap.get_person(mail=mapping["contact"][0]["mappingRules"][0]["forValues"][1])
        for mapping in voxco_resource_mappings
    ]
