from mex.common.cli import entrypoint
from mex.common.models import (
    ExtractedPrimarySource,
)
from mex.common.primary_source.transform import (
    get_primary_sources_by_name,
)
from mex.grippeweb.extract import (
    extract_sql_table,
)
from mex.grippeweb.settings import GrippewebSettings
from mex.ifsg.models.meta_catalogue2item import MetaCatalogue2Item
from mex.pipeline import asset, run_job_in_process
from mex.sinks import load


@asset(group_name="grippeweb", deps=["extracted_primary_source_mex"])
def extracted_primary_sources_grippeweb(
    extracted_primary_sources: list[ExtractedPrimarySource],
) -> ExtractedPrimarySource:
    """Load and return grippeweb primary source."""
    (extracted_primary_sources_grippeweb,) = get_primary_sources_by_name(
        extracted_primary_sources, "grippeweb"
    )
    load([extracted_primary_sources_grippeweb])

    return extracted_primary_sources_grippeweb


@asset(group_name="grippeweb")
def grippeweb_tables() -> list[MetaCatalogue2Item]:
    """Extract `Catalogue2Item` table."""
    return extract_sql_table(MetaCatalogue2Item)


@entrypoint(GrippewebSettings)
def run() -> None:
    """Run the IFSG extractor job in-process."""
    run_job_in_process("grippeweb")
