from mex.pipeline import run_job_in_process


def test_job() -> None:
    result = run_job_in_process("publisher")
    assert result.success
