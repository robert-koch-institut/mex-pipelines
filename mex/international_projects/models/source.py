from collections.abc import Sequence

from pydantic import ConfigDict

from mex.common.types import Timestamp
from mex.models import BaseRawData


class InternationalProjectsSource(BaseRawData):
    """Model class for international projects source entities."""

    model_config = ConfigDict(str_min_length=0)

    funding_type: str
    project_lead_person: str
    end_date: Timestamp | None = None
    partner_organization: list[str] = []
    funding_source: list[str] = []
    funding_program: str
    rki_internal_project_number: str
    additional_rki_units: str
    project_lead_rki_unit: str
    project_abbreviation: str
    start_date: Timestamp | None = None
    activity1: str
    activity2: str
    topic1: str
    topic2: str
    full_project_name: str
    website: str

    def get_partners(self) -> Sequence[str | None]:
        """Return partners from extractor."""
        return self.partner_organization

    def get_start_year(self) -> Timestamp | None:
        """Return start year from extractor."""
        return self.start_date

    def get_end_year(self) -> Timestamp | None:
        """Return end year from extractor."""
        return self.end_date

    def get_units(self) -> Sequence[str | None]:
        """Return units from extractor."""
        return [self.project_lead_rki_unit]

    def get_identifier_in_primary_source(self) -> str | None:
        """Return identifier in primary source from extractor."""
        return self.rki_internal_project_number
