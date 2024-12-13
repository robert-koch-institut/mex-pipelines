import math
from collections.abc import Generator
from urllib.parse import urljoin

from mex.common.connector import HTTPConnector
from mex.extractors.open_data.models.source import (
    ZenodoParentRecordSource,
    ZenodoRecordVersion,
)
from mex.extractors.settings import Settings


class OpenDataConnector(HTTPConnector):
    """Connector class to handle requesting the Zenodo API."""

    def _set_url(self) -> None:
        """Set url of the host."""
        settings = Settings.get()
        self.url = settings.open_data.url

    def get_parent_sources(self) -> Generator[ZenodoParentRecordSource, None, None]:
        """Load parent sources by querying the Zenodo API.

        Gets the parent sources (~ latest version) of all the sources of the
        Zenodo communitiy "robertkochinstitut".

        Returns:
            Generator for Zenodo parent sources
        """
        communities = "robertkochinstitut"

        base_url = urljoin(
            self.url,
            f"communities/{communities}/",
        )

        total_records = self.session.get(urljoin(base_url, "records?size=1")).json()[
            "hits"
        ]["total"]

        limit = 100
        amount_pages = math.ceil(total_records / limit)

        for page in range(1, amount_pages + 1):
            response = self.session.get(
                urljoin(
                    base_url,
                    f"records?size={limit}&page={page}",
                )
            )
            response.raise_for_status()

            for item in response.json()["hits"]["hits"]:
                yield ZenodoParentRecordSource.model_validate(item)

    def get_record_versions(
        self, record_id: int
    ) -> Generator[ZenodoRecordVersion, None, None]:
        """Load versions of different records by querying the Zenodo API.

        For a specific parent source get all the versions of this source.
        The Zenodo API doesn't work by giving it the parent source id ("conceptrecid")
        but call it with the id ("id") of any version of that parent source and then
        'ask' for the versions in general.

        Args:
            record_id: id of any record version

        Returns:
            Generator for Zenodo record versions
        """
        base_url = urljoin(
            self.url,
            f"records/{record_id}/",
        )

        total_records = self.session.get(urljoin(base_url, "versions?size=1")).json()[
            "hits"
        ]["total"]

        limit = 100
        amount_pages = math.ceil(total_records / limit)

        for page in range(1, amount_pages + 1):
            response = self.session.get(
                urljoin(
                    base_url,
                    f"versions?size={limit}&page={page}",
                )
            )
            response.raise_for_status()

            for item in response.json()["hits"]["hits"]:
                yield ZenodoRecordVersion.model_validate(item)

    def get_oldest_record_versions(self, record_id: int) -> ZenodoRecordVersion:
        """Load oldest (first) version of a record by querying the Zenodo API.

        Args:
            record_id: id of any record version

        Returns:
            Zenodo record version (oldest)
        """
        base_url = urljoin(
            self.url,
            f"records/{record_id}/",
        )

        oldest_record = self.session.get(
            urljoin(base_url, "versions?size=1&sort=oldest")
        ).json()

        oldest_record.raise_for_status()

        item = oldest_record.json()["hits"]["hits"][0]

        return ZenodoRecordVersion.model_validate(item)

    def get_totals(self, record_id: int | None) -> int:
        """Get totals."""
        base_url = urljoin(
            self.url,
            f"records/{record_id}/",
        )

        return int(
            self.session.get(urljoin(base_url, "versions?size=1")).json()["hits"][
                "total"
            ]
        )
