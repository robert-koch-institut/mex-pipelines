import pytest

from mex.common.identity import get_provider
from mex.common.models import ExtractedPrimarySource
from mex.pipeline import run_job_in_process


@pytest.mark.usefixtures("mocked_wikidata")
def test_job(
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
) -> None:

    identity_provider = get_provider()
    identity_provider.assign(
        extracted_primary_sources["international-projects"].stableTargetId,
        "testAAbr",
    )  # "testAAbr" is the default value from test mapping

    result = run_job_in_process("odk")
    assert result.success
