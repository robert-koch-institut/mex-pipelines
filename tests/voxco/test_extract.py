import pytest

from mex.voxco.extract import extract_voxco_variables


@pytest.mark.usefixtures(
    "mocked_drop_for_voxco",
)
def test_extract_voxco_variables() -> None:
    sources = extract_voxco_variables()
    expected = {
        "Id": 50614,
        "DataType": "Text",
        "Type": "Discrete",
        "QuestionText": "Monat",
        "Choices": [
            "@{Code=1; Text=Januar; Image=; HasOpenEnd=False; Visible=True; Default=False}",
            "@{Code=1; Text=Februar; Image=; HasOpenEnd=False; Visible=True; Default=False}",
        ],
    }
    assert sources["one"][0].model_dump() == expected
