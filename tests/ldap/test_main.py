import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures("mocked_ldap", "mocked_public_api")
def test_job() -> None:
    result = run_job_in_process("sync_persons")
    assert result.success
