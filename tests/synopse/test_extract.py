import pytest

from mex.synopse.extract import (
    extract_projects,
    extract_study_data,
    extract_study_overviews,
    extract_synopse_project_contributors,
    extract_variables,
)
from mex.synopse.models.project import SynopseProject


def test_extract_variables() -> None:
    expected_first_variable = {
        "auspraegungen": "-95",
        "datentyp": "Zahl",
        "originalfrage": None,
        "studie": "BBCCDD1",
        "studie_id": 1122999,
        "synopse_id": "503",
        "text_dt": "Eingangsfrage wn/kA",
        "thema_und_fragebogenausschnitt": "Krankheiten (1101)",
        "unterthema": "Lorem (110116)",
        "val_instrument": None,
        "varlabel": "Lorem Symptome: Halsschmerzen (1. Tag)",
        "varname": "KLMNO_F4",
    }
    expected_second_variable = {
        "auspraegungen": "-98",
        "datentyp": "Zahl",
        "originalfrage": None,
        "studie": "BBCCDD1",
        "studie_id": 1122999,
        "synopse_id": "503",
        "text_dt": "Weiß nicht",
        "thema_und_fragebogenausschnitt": "Krankheiten (1101)",
        "unterthema": "Lorem (110116)",
        "val_instrument": None,
        "varlabel": "Lorem Symptome: Halsschmerzen (1. Tag)",
        "varname": "KLMNO_F4",
    }
    variables = list(extract_variables())
    assert len(variables) == 16
    assert variables[0].model_dump() == expected_first_variable
    assert variables[4].model_dump() == expected_second_variable


def test_extract_study_data() -> None:
    expected_study_data = {
        "beschreibung": "BBCCDD Basiserhebung, Kohorte",
        "dateiformat": "sas,stata",
        "dokumentation": r'"Z:\Lorem\Ipsum\DATA\BBCCDD\Dokumentation',
        "ds_typ_id": 15,
        "erstellungs_datum": "2013",
        "lizenz": None,
        "plattform": "Reportserver",
        "plattform_adresse": "BBCCDD-Basis Variablennamen - XYZ-Reports",
        "rechte": None,
        "schlagworte_themen": "BBCCDD Basiserhebung, Kohorte",
        "studie": "BBCCDD",
        "studien_id": "1234567",
        "titel_datenset": "BBCCDD",
        "version": "V26",
        "zugangsbeschraenkung": "restriktiv",
    }
    study_data = list(extract_study_data())
    assert len(study_data) == 6
    assert study_data[0].model_dump() == expected_study_data


def test_extract_projects() -> None:
    expected_project = {
        "akronym_des_studientitels": "BBCCDD1",
        "beschreibung_der_studie": "Mit der BBCCDD-Basiserhebung hat das Robert "
        "Koch-Institut umfassende Daten zur Gesundheit der "
        "in Deutschland lebenden Lorems gesammelt. Das "
        "Studienprogramm umfasste neben Befragungen auch "
        "Ipsumalysen.",
        "kontakt": ["fg@example.com"],
        "project_studientitel": "Studie zu Lorem und Ipsum",
        "studien_id": "1122999",
        "studienart_studientyp": "Monitoring-Studie",
        "verantwortliche_oe": "CHLD",
    }
    projects = list(extract_projects())
    assert len(projects) == 4
    assert projects[0].model_dump(exclude_none=True) == expected_project


@pytest.mark.usefixtures("mocked_ldap")
def test_extract_synopse_project_contributors(synopse_project: SynopseProject) -> None:
    persons = list(
        extract_synopse_project_contributors([synopse_project, synopse_project])
    )
    assert len(persons) == 1
    assert persons[0].person.displayName == "Resolved, Roland"


def test_extract_study_overviews() -> None:
    expected_overview = {
        "ds_typ_id": 15,
        "studien_id": "1234567",
        "synopse_id": "405",
        "titel_datenset": "BBCCDD",
    }
    overviews = list(extract_study_overviews())
    assert len(overviews) == 9
    assert overviews[0].model_dump() == expected_overview
