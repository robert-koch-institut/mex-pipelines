from mex.common.cli import entrypoint
from mex.common.public_api.extract import extract_mex_person_items
from mex.common.sinks.purge import purge_items
from mex.ldap.filter import is_person_in_identity_map_and_ldap
from mex.pipeline import asset, run_job_in_process
from mex.settings import Settings


@asset(group_name="sync_persons")
def sync_ldap_persons() -> None:
    """Verify all persons represented in MEx are still present in LDAP."""
    mex_persons_not_in_ldap = (
        person
        for person in extract_mex_person_items()
        if not is_person_in_identity_map_and_ldap(person.businessId)
    )
    purge_items(mex_persons_not_in_ldap)


@entrypoint(Settings)
def run() -> None:
    """Run the sync persons job in-process."""
    run_job_in_process("sync_persons")
