from numpy import nan
from pandas import DataFrame

from mex.odk.extract import extract_odk_raw_data, get_column_dict_by_pattern


def test_extract_odk_raw_data() -> None:
    test = extract_odk_raw_data()
    expected = {
        "file_name": "test_raw_data.xlsx",
        "hint": {
            "hint": [
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                "*(-88 = don't know, -99 = refused to answer)*",
                "*(-88 = don't know, -99 = refused to answer)*",
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
                nan,
            ]
        },
        "label_choices": {
            "label::English (en)": [
                nan,
                "I AGREE with the above statements and wish to take part in the survey",
                "I do NOT AGREE to take part in the survey",
                nan,
                "Yes",
                "No",
                nan,
                "Yes",
                "No",
                "Don't know",
                "Refused to answer",
                nan,
                "Head of household",
                "Wife, husband, partner",
                "Son or daughter",
            ],
            "label::Otjiherero (hz)": [
                nan,
                "Ami ME ITAVERE komaheya nge ri kombanda mba nu otji me raisa kutja mbi nonḓero okukara norupa mongonḓononeno.",
                "Ami HI NOKUITAVERA okukara norupa mongonḓononeno.",
                nan,
                "Ii",
                "Kako",
                nan,
                "Ii",
                "Kako",
                "Ke nokutjiwa",
                "Ma panḓa okuzira",
                nan,
                "Otjiuru tjeṱunḓu",
                "Omukazendu we, omurumendu we, otjiyambura tje",
                "Omuatje we omuzandu poo omukazona",
            ],
        },
        "label_survey": {
            "label::English (en)": [
                nan,
                "Store username of interviewer.",
                "Interviewer:",
                "(*Interviewer:",
                "(*Interviewer:",
                "(*Interviewer:",
                "Introduction of study to gatekeeper",
                nan,
                "**Verbal consent**",
                nan,
                nan,
                "Are you",
                "*(Interviewer: End of Interview.)*",
                nan,
                "How many",
                "*(Interviewer: End of interview, no adult household members)*",
                "Thank you for providing this basic information.",
                "*(Interviewer: End of interview.)*",
                "Introduction of study to gatekeeper",
                nan,
                "Selection of respondent",
                "**Verbal consent**",
                "*(Interviewer: No more adult household members. End of interview.)*",
                "Are you currently 18 years old or older?",
                "Selection of respondent",
            ],
            "label::Otjiherero (hz)": [
                nan,
                "Store username of interviewer.",
                "Interviewer:",
                "(*Interviewer:",
                "(*Interviewer:",
                "(*Interviewer:",
                "Introduction of study to gatekeeper",
                nan,
                "**Omaitaverero wokotjinyo**",
                nan,
                nan,
                "Ove moyenene okunyamukura omapuriro inga?",
                "*(Interviewer: End of Interview.)*",
                "Tji wa twa kumwe",
                "Ovandu vengapi",
                "*(Interviewer:",
                "Okuhepa tjinene",
                "*(Interviewer:",
                nan,
                nan,
                "Selection of respondent",
                "**Omaitaverero wokotjinyo**",
                "*(Interviewer: No more adult household members. End of interview.)*",
                "Una ozombura 18 nokombanda?",
                nan,
            ],
        },
        "list_name": [
            nan,
            "consent",
            "consent",
            nan,
            "yes_no",
            "yes_no",
            nan,
            "region",
            "region",
            "region",
            "region",
            nan,
            "relationship_to_head",
            "relationship_to_head",
            "relationship_to_head",
        ],
        "name": [
            "start",
            "username",
            "confirmed_username",
            "region",
            "constituency",
            "household_id",
            "gatekeeper",
            nan,
            "consent_gatekeeper",
            nan,
            nan,
            "consent_basic_questions",
            "end_of_interview_1",
            "NR1",
            "NR2",
            "NR3end",
            "consent_gatekeeper_2",
            "end_of_interview_3",
            "gatekeeper",
            nan,
            "selection",
            "consent_respondent",
            "end_of_interview_2",
            "age_verification",
            "selection",
        ],
        "type": [
            "start",
            "username",
            "text",
            "select_one region",
            "select_one constituency",
            "text",
            "begin_group",
            nan,
            "select_one consent",
            nan,
            nan,
            "select_one yes_no",
            "note",
            "integer",
            "integer",
            "note",
            "select_one yes_no",
            "note",
            "end_group",
            nan,
            "begin_group",
            "select_one consent",
            "note",
            "select_one yes_no",
            "end_group",
        ],
    }
    assert test[0].model_dump(exclude_defaults=True) == expected


def test_get_column_dict_by_pattern() -> None:
    result = get_column_dict_by_pattern(
        DataFrame({"name": "a", "label1": "b", "label2": "c"}, index=[1]), "label"
    )
    assert result == {"label1": ["b"], "label2": ["c"]}
