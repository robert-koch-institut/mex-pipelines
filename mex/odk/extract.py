from pathlib import Path

from pandas import DataFrame, ExcelFile

from mex.odk.model import ODKData
from mex.odk.settings import ODKSettings


def extract_odk_raw_data() -> list[ODKData]:
    """Extract odk raw data by loading data from MS-Excel file.

    Settings:
        raw_data_path: Path to the odk raw data,
                       absolute or relative to `assets_dir`

    Returns:
        list of ODK data.
    """
    settings = ODKSettings.get()
    raw_data = []
    for file in Path(settings.raw_data_path).glob("*.xlsx"):

        xls = ExcelFile(file)

        choices_sheet = xls.parse(
            sheet_name="choices", na_values=["", " "], keep_default_na=False
        )
        label_choices = get_column_dict_by_pattern(choices_sheet, "label")
        list_name = choices_sheet["list_name"].to_list()

        survey_sheet = xls.parse(
            sheet_name="survey", na_values=["", " "], keep_default_na=False
        )
        label_survey = get_column_dict_by_pattern(survey_sheet, "label")
        survey_type = survey_sheet["type"].to_list()
        name = survey_sheet["name"].to_list()
        hint = get_column_dict_by_pattern(survey_sheet, "hint")
        raw_data.append(
            ODKData(
                file_name=file.name,
                hint=hint,
                label_survey=label_survey,
                label_choices=label_choices,
                list_name=list_name,
                name=name,
                type=survey_type,
            )
        )
    return raw_data


def get_column_dict_by_pattern(
    sheet: DataFrame, pattern: str
) -> dict[str, list[str | float]]:
    """Get a dict of columns by matchting pattern.

    Args:
        sheet: sheet to extract columns from
        pattern: pattern to match column names

    Returns:
    dictionary of mathing columns by column names
    """
    col_list = [col for col in sheet.columns if pattern in col]
    return {col: sheet[col].to_list() for col in col_list}
