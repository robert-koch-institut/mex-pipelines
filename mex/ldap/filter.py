from functools import cache

from mex.common.exceptions import EmptySearchResultError
from mex.common.identity import get_provider
from mex.common.ldap.connector import LDAPConnector
from mex.common.logging import echo
from mex.common.types import Identifier


@cache
def is_person_in_identity_map_and_ldap(stable_target_id: Identifier) -> bool:
    """Check if a person is present in the identity map and in active directory.

    We first look for a person with the given stable target ID in the identity db
    and successively check if this persons' original ID is found in ldap.

    Args:
        stable_target_id: Stable target ID of the person

    Returns:
        True if person is in identity db and ldap
        False if person is not in identity db or not in ldap
    """
    ldap_connector = LDAPConnector.get()
    identity_provider = get_provider()
    identities = identity_provider.fetch(stable_target_id=stable_target_id)
    if not identities:
        echo(f"Warning: Cannot find person identity: {stable_target_id}")
        return False
    try:
        person = ldap_connector.get_person(
            objectGUID=str(identities[0].identifierInPrimarySource)
        )
    except EmptySearchResultError:
        return False
    return person is not None  # sanity check
