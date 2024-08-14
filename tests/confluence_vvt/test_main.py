import pytest

from mex.extractors.pipeline import run_job_in_process


@pytest.mark.usefixtures(
    "mocked_confluence_vvt",
    "mocked_ldap",
)
def test_job() -> None:
    result = run_job_in_process("confluence_vvt")
    assert result.success
