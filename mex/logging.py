from mex.common.logging import echo
from mex.common.types import Identifier


def log_filter(
    identifier_in_primary_source: str | None,
    primary_source_id: Identifier,
    reason: str,
) -> None:
    """Log filtered sources.

    Args:
        identifier_in_primary_source: optional identifier in the primary source
        primary_source_id: identifier of the primary source
        reason: string explaining the reason for filtering
    """
    echo(
        f"[source filtered] reason: {reason}, "
        f"had_primary_source: {primary_source_id}, "
        f"identifier_in_primary_source: {identifier_in_primary_source}"
    )
