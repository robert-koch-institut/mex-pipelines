from typing import Generator, Iterable

from mex.common.models import ExtractedPrimarySource
from mex.logging import log_filter
from mex.synopse.models.study_overview import SynopseStudyOverview
from mex.synopse.models.variable import SynopseVariable


def filter_and_log_variables(
    synopse_variables: Iterable[SynopseVariable],
    synopse_overviews: Iterable[SynopseStudyOverview],
    extracted_primary_source: ExtractedPrimarySource,
) -> Generator[SynopseVariable, None, None]:
    """Filter out and log variables which are not in datensatzuebersicht.

    Args:
        synopse_variables: iterable of synopse variables
        synopse_overviews: iterable of synopse overviews
        extracted_primary_source: primary source for report server platform

    Returns:
        Generator for filtered synopse variables
    """
    variables_in_datensatzuebersicht = {s.synopse_id for s in synopse_overviews}
    for variable in synopse_variables:
        if variable.synopse_id in variables_in_datensatzuebersicht:
            yield variable
        else:
            log_filter(
                variable.synopse_id,
                extracted_primary_source.stableTargetId,
                "Variable not in datensatzuebersicht, cannot assign resource.",
            )
