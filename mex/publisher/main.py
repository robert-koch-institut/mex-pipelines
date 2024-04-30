from mex.common.cli import entrypoint
from mex.common.logging import logger
from mex.pipeline import asset, run_job_in_process
from mex.settings import Settings


@asset(group_name="publisher")
def publish_merged_items() -> None:
    """Get all merged items from mex-backend and write to ndjson file."""
    logger.info("Hi world :P")


@entrypoint(Settings)
def run() -> None:
    """Run the publisher job in-process."""
    run_job_in_process("publisher")
