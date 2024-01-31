from uuid import UUID

import pytest
from pytest import LogCaptureFixture, MonkeyPatch

from mex.common.exceptions import EmptySearchResultError
from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPerson
from mex.common.models import ExtractedPerson
from mex.common.types import Identifier
from mex.ldap.filter import is_person_in_identity_map_and_ldap


@pytest.mark.usefixtures("mocked_ldap")
def test_is_person_in_identity_map_and_ldap_mocked(
    monkeypatch: MonkeyPatch, caplog: LogCaptureFixture
) -> None:
    person_found_in_both = ExtractedPerson(
        identifierInPrimarySource=str(UUID(int=1, version=4)),
        hadPrimarySource=Identifier.generate(seed=1000),
        fullName=["Betty Both"],
    )
    person_in_db_but_not_in_ldap = ExtractedPerson(
        identifierInPrimarySource=str(UUID(int=2, version=4)),
        hadPrimarySource=Identifier.generate(seed=1000),
        fullName=["Dami Db"],
    )
    # NOTE: using `construct()` prevents identity allocation
    person_in_ldap_but_not_in_db = ExtractedPerson.model_construct(
        identifierInPrimarySource=str(UUID(int=3, version=4)),
        stableTargetId=Identifier.generate(seed=1003),
        hadPrimarySource=Identifier.generate(seed=1000),
        fullName=["Lok Ldap"],
    )
    person_missing_in_both = ExtractedPerson.model_construct(
        identifierInPrimarySource=str(UUID(int=4, version=4)),
        stableTargetId=Identifier.generate(seed=1004),
        hadPrimarySource=Identifier.generate(seed=1000),
        fullName=["Miguel Missing"],
    )

    def get_person(self: LDAPConnector, objectGUID: str) -> LDAPPerson:  # noqa: N803
        if objectGUID in (
            person_found_in_both.identifierInPrimarySource,
            person_in_ldap_but_not_in_db.identifierInPrimarySource,
        ):
            return LDAPPerson(
                objectGUID=objectGUID,
                employeeID="N/A",
                sn="N/A",
                givenName=["N/A"],
            )
        raise EmptySearchResultError

    monkeypatch.setattr(LDAPConnector, "get_person", get_person)

    assert (
        is_person_in_identity_map_and_ldap(person_found_in_both.stableTargetId) is True
    )
    assert (
        is_person_in_identity_map_and_ldap(person_in_db_but_not_in_ldap.stableTargetId)
        is False
    )
    assert (
        is_person_in_identity_map_and_ldap(person_in_ldap_but_not_in_db.stableTargetId)
        is False
    )
    assert (
        f"Cannot find person identity: {person_in_ldap_but_not_in_db.stableTargetId}"
        in caplog.text
    )
    assert (
        is_person_in_identity_map_and_ldap(person_missing_in_both.stableTargetId)
        is False
    )
