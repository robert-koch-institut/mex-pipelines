import json
from collections.abc import Generator

from mex.common.ldap.connector import LDAPConnector
from mex.common.ldap.models.person import LDAPPersonWithQuery
from mex.common.logging import watch
from mex.seq_repo.model import (
    SeqRepoSource,
)
from mex.seq_repo.settings import SeqRepoSettings


def extract_sources() -> Generator[SeqRepoSource, None, None]:
    """Extract Seq Repo sources by loading data from source json file.

    Settings:
        default_json_file_path: Path to the seq-repo json file,
                                absolute or relative to `assets_dir`

    Returns:
        Generator for Seq Repo resources
    """
    settings = SeqRepoSettings.get()
    with open(settings.default_json_file_path, encoding="utf-8") as file:
        data = json.load(file)
        for item in data:
            yield SeqRepoSource.model_validate(item)


@watch
def extract_source_project_coordinator(
    seq_repo_sources: dict[str, SeqRepoSource],
) -> Generator[LDAPPersonWithQuery, None, None]:
    """Extract LDAP persons with their query string for source project coordinators.

    Args:
        seq_repo_sources: Seq Repo sources

    Returns:
        Generator for LDAP persons with query
    """
    ldap = LDAPConnector.get()
    seen = set()
    for value in seq_repo_sources.values():
        names = value.project_coordinators
        for name in names:
            if not name:
                continue
            if name in seen:
                continue
            seen.add(name)
            persons = list(ldap.get_persons(mail=f"{name}@rki.de"))
            if len(persons) == 1 and persons[0].objectGUID:
                yield LDAPPersonWithQuery(person=persons[0], query=name)
