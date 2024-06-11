import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures(
    "mocked_drop_for_voxco",
)
def test_job() -> None:
    result = run_job_in_process("voxco")
    assert result.success
