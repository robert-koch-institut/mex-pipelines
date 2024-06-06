import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures(
    "mocked_drop_for_seqrepo",
    "mocked_ldap",
    "mocked_wikidata",
)
def test_job() -> None:
    result = run_job_in_process("seq_repo")
    assert result.success
