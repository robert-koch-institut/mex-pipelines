import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures(
    "mocked_ldap",
    "mocked_blueant",
)
def test_job() -> None:
    result = run_job_in_process("blueant")
    assert result.success
