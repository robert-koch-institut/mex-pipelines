import pytest

from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures(
    "mocked_blueant",
    "mocked_confluence_vvt",
    "mocked_datscha_web",
    "mocked_drop",
    "mocked_grippeweb",
    "mocked_ifsg",
    "mocked_ldap",
    "mocked_rdmo",
    "mocked_wikidata",
)
def test_job() -> None:
    result = run_job_in_process("all_extractors")
    assert result.success
