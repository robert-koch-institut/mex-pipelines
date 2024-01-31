import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures("mocked_ldap", "mocked_rdmo")
def test_job() -> None:
    result = run_job_in_process("rdmo")
    assert result.success
