from typing import Sequence

from mex.common.types import Timestamp
from mex.models import BaseRawData


class BlueAntSource(BaseRawData):
    """Model class for Blue Ant sources."""

    client_names: list[str]
    department: str
    end: Timestamp
    name: str
    number: str
    projectLeaderEmployeeId: str | None = None
    start: Timestamp
    status: str
    type_: str

    def get_partners(self) -> Sequence[str | None]:
        """Return partners from extractor."""
        return []

    def get_start_year(self) -> Timestamp | None:
        """Return start year from extractor."""
        return self.start

    def get_end_year(self) -> Timestamp | None:
        """Return end year from extractor."""
        return self.end

    def get_units(self) -> Sequence[str | None]:
        """Return units from extractor."""
        return [self.department]

    def get_identifier_in_primary_source(self) -> str | None:
        """Return identifier in primary source from extractor."""
        return self.number
