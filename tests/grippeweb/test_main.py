import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures("mocked_grippeweb", "mocked_wikidata")
def test_job() -> None:
    result = run_job_in_process("grippeweb")
    assert result.success
