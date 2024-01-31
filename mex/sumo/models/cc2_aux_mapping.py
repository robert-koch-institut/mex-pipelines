from mex.sumo.models.base import SumoBaseModel


class Cc2AuxMapping(SumoBaseModel):
    """Model class for aux_mapping."""

    sheet_name: str
    variable_name_column: list[str]
