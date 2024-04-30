from typing import Any

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.wikidata.extract import search_organization_by_label
from mex.common.wikidata.models.organization import WikidataOrganization
from mex.grippeweb.connector import QUERY_BY_TABLE_NAME, GrippewebConnector


def extract_columns_by_table_and_column_name() -> dict[str, dict[str, list[Any]]]:
    """Extract sql tables and parse them into column lists by table and column name.

    Returns:
        list of columns by column names and table names
    """
    connection = GrippewebConnector.get()
    return {
        table_name: connection.parse_columns_by_column_name(table_name)
        for table_name in QUERY_BY_TABLE_NAME.keys()
    }


def extract_ldap_persons(
    grippeweb_access_platform: dict[str, Any],
    grippeweb_resource_mappings: list[dict[str, Any]],
) -> list[LDAPPerson]:
    """Extract LDAP persons for grippeweb_access_platform contacts.

    Args:
        grippeweb_access_platform: grippeweb access platform
        grippeweb_resource_mappings: list of resources default value dicts

    Returns:
        list of LDAP persons
    """
    ldap = LDAPConnector.get()

    return [
        *[
            ldap.get_person(mail=mail)
            for mapping in [*grippeweb_resource_mappings, grippeweb_access_platform]
            for mail in mapping["contact"][0]["mappingRules"][0]["forValues"]
        ],
        *[
            ldap.get_person(name=name)
            for mapping in grippeweb_resource_mappings
            for name in mapping["contributor"][0]["mappingRules"][0]["forValues"]
        ],
    ]


def extract_grippeweb_organizations(
    grippeweb_resource_mappings: list[dict[str, Any]],
) -> dict[str, WikidataOrganization]:
    """Search and extract organization from wikidata.

    Args:
        grippeweb_resource_mappings: grippeweb  resource mappings

    Returns:
        Dict with keys: mapping default values
            and values: WikidataOrganization
    """
    publisher_by_name = {}
    for resource in grippeweb_resource_mappings:
        publisher_name = str(
            resource["publisher"][0]["mappingRules"][0]["setValues"][0]
        )
        if publisher := next(search_organization_by_label(publisher_name)):
            publisher_by_name[publisher_name] = publisher
    return publisher_by_name
