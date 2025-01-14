from unittest.mock import MagicMock, Mock

import pytest
import requests
from pytest import MonkeyPatch
from requests import HTTPError

from mex.extractors.confluence_vvt.connector import ConfluenceVvtConnector
from mex.extractors.confluence_vvt.extract import fetch_all_vvt_pages_ids


@pytest.fixture
def mocked_confluence_vvt_session(monkeypatch: MonkeyPatch) -> MagicMock:
    """Mock the ConfluenceVvt session with a MagicMock session and return that."""
    mocked_session = MagicMock(spec=requests.Session)
    mocked_session.request = MagicMock(
        return_value=Mock(spec=requests.Response, status_code=200)
    )

    mocked_session.headers = {}

    def set_mocked_session(self: ConfluenceVvtConnector) -> None:
        self.session = mocked_session

    monkeypatch.setattr(ConfluenceVvtConnector, "_set_session", set_mocked_session)
    return mocked_session


@pytest.mark.integration
def test_initialization() -> None:
    connector = ConfluenceVvtConnector.get()
    try:
        connector._check_availability()
    except HTTPError:
        pytest.fail("HTTPError : Connector initialization failed.")


def test_initialization_mocked_auth_fail(
    mocked_confluence_vvt_session: requests.Session,
) -> None:
    error_message = {
        "statusCode": 401,
        "data": {
            "authorized": False,
            "valid": True,
            "allowedInReadOnlyMode": True,
            "errors": [],
            "successful": False,
        },
        "message": "No parent or not permitted to view content with id : ContentId{id=007}",
        "reason": "Not Found",
    }
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 401
    mocked_response.json = MagicMock(return_value=error_message)
    mocked_confluence_vvt_session.request = MagicMock(return_value=mocked_response)

    connector = ConfluenceVvtConnector.get()

    response = connector.request("GET", "localhost")

    assert response["statusCode"] == 401


def test_initialization_mocked_server_error(
    mocked_confluence_vvt_session: requests.Session,
) -> None:
    error_message = {
        "statusCode": 500,
        "message": "Internal Server Error",
    }
    mocked_response = Mock(spec=requests.Response)
    mocked_response.status_code = 500
    mocked_response.json = MagicMock(return_value=error_message)
    mocked_confluence_vvt_session.request = MagicMock(return_value=mocked_response)

    connector = ConfluenceVvtConnector.get()

    response = connector.request("GET", "localhost")

    assert response["statusCode"] == 500


@pytest.mark.integration
def test_get_page_by_id() -> None:
    connector = ConfluenceVvtConnector.get()
    page_data = connector.get_page_by_id("89780861")
    assert len(page_data.model_dump()) == 3
    assert page_data.model_dump()["id"] == 89780861
    assert (
        page_data.model_dump()["title"]
        == "Accessing and increasing vaccine readiness in Sub-Saharan Africa (VRSA) – Work Package 1"  # noqa: RUF001
    )
    assert page_data.model_dump()["tables"][0] == {
        "rows": [
            {
                "cells": [
                    {"text": "Interne Vorgangsnummer (Datenschutz)"},
                    {
                        "text": "Zuständige/r DatenschutzkoordinatorIn für die Abteilung(Achtung: entspricht nicht der/dem DSB!)"
                    },
                    {
                        "text": "(Funktionsbezeichnung der/des zuständigen DatenschutzkoordinatorIn hier einfügen)"
                    },
                    {
                        "text": "War eine Datenschutzfolgenabschätzung notwendig? ja/nein"
                    },
                ]
            },
            {
                "cells": [
                    {"texts": ["DS-2023-177"]},
                    {"texts": ["J. Wolf"]},
                    {"texts": None},
                    {"texts": None},
                ]
            },
            {
                "cells": [
                    {
                        "text": "Ausführliche Beschreibung des Verfahrens / der Verarbeitung / der Studie"
                    }
                ]
            },
            {
                "cells": [
                    {
                        "texts": [
                            'Dieser Antrag beschreibt das Work package 1 (VRSA-WP1) als Teil einer größeren Studie mit dem Titel "Vaccine Readiness in Sub-Saharan Africa" (VRSA). VRSA-WP1 besteht aus einer externen Evaluierung von Guineas erweitertem Impfprogramm (expanded programme on immunization, EPI).',
                            "Frühere Untersuchungen in Guinea haben gezeigt, dass das Erreichen der WHO-Ziele für die Durchimpfungsrate mit erheblichen Herausforderungen verbunden ist. In den letzten Jahren war das Land immer wieder von Epidemien betroffen, und die Versorgung, insbesondere in ländlichen Gebieten, ist nach wie vor schwierig. Zur Bekämpfung von durch Impfung vermeidbaren Krankheiten ist ein funktionierendes Grundimmunisierungsprogramm unerlässlich. Ziel des Projekts ist es, die bisherige Grundimmunisierung Guineas zu bewerten, die Bereitschaft des Gesundheitssystems zur Einführung neuer Impfstoffe zu beurteilen und einen Fahrplan zur Stärkung der Grundimmunisierung und zur Verbesserung der Durchimpfungsrate, der Zugänglichkeit und der Akzeptanz von Impfstoffen zu entwickeln. VRSA wird somit die übergreifende Strategie des Gesundheitsministeriums unterstützen, die Kinder- und Säuglingssterblichkeit durch eine Verringerung der Zahl der durch Impfung vermeidbaren Krankheiten zu senken.",
                            "Studiendesign: Die Methodik für die Durchführung dieser externen Evaluierung des EPI basiert auf einem Leitfaden der WHO aus dem Jahr 2017 und wird mit einem mixed-methods-Ansatz durchgeführt. Die Bewertung wird aus einem Desk Review, Interviews mit Schlüsselinformanten, die am Impfprogramm und der Impfstrategie Guineas beteiligt sind, Befragungen von Leitern (wie unten definiert) von ausgewählten Gesundheitseinrichtungen und einer Sekundärdatenanalyse von Routinedaten bestehen, um die dokumentierten und wahrgenommenen Bedürfnisse im Zusammenhang mit der EPI des Landes zu untersuchen.",
                            "Desk Review: In einem ersten Schritt werden wir vorhandene Dokumente durchsehen, um den aktuellen Stand des Impfprogramms innerhalb des Gesundheitssystems von Guinea zu bewerten, Trends bei der Durchimpfungsrate im Laufe der Zeit zu untersuchen, Schlüsselinformanten zu identifizieren und die Entwicklung von Themenleitfäden für die Interviews mit Schlüsselinformanten (key informant interviews, KIIs) zu unterstützen. Die Literaturrecherche umfasst eine strukturierte Suche nach wissenschaftlichen Veröffentlichungen und eine zusätzliche Suche nach grauer Literatur, einschließlich Berichten von Gebern und Organisationen, Programmberichten, Fortschrittsberichten, Regierungsdokumenten von relevanten Ministerien und anderen relevanten Dokumenten. Alle Dokumente wurden aus öffentlich zugänglichen Quellen zusammengetragen oder von der veröffentlichenden Organisation selbst zur Verfügung gestellt. Soweit im Rahmen des Desk Review personenbezogenen Daten verarbeitet werden (z.B. Name und Position), werden die datenschutzrechtlichen Vorgaben wie nachfolgend beschrieben eingehalten.",
                            "Befragung von Schlüsselinformanten (key informant interview, KII): Der Desk Review wird durch halbstrukturierte Interviews mit Schlüsselinformanten (KII) ergänzt, die zusätzliche Einblicke in den aktuellen Stand des Immunisierungsprogramms ermöglichen und zusätzliche Bedürfnisse und Lücken im System aufzeigen. Die KII werden darüber hinaus eine empirische Grundlage für eine detaillierte Bewertung des EPI liefern, die auf den Erfahrungen, dem Wissen und dem Verständnis der Schlüsselinformanten über das EPI beruht, die im Desk Review möglicherweise nicht erfasst werden. Die ersten Schlüsselinformanten werden durch den Desk Review und den Input der Partner ermittelt, während weitere Informanten durch eine Schneeballtechnik ermittelt werden können. An den KIIs werden Akteure auf nationaler, subnationaler und lokaler Ebene teilnehmen, die verschiedene Fachbereiche des Gesundheitssystems repräsentieren. Ein Themenleitfaden für die Interviews basiert auf dem Desk Review und den WHO-Leitlinien für die Durchführung von EPI-Evaluationen. Weitere Einzelheiten zur Rekrutierung sind in Abschnitt 3 und Abschnitt 7 beschrieben. Eine Liste der Variablen, die im Themenleitfaden enthalten sind, ist in Abschnitt 4.1 aufgeführt. Alle Interviews werden von dem in Abschnitt 1.2 genannten Projektpartner und/oder von den in diesem Dokument aufgeführten RKI-Mitarbeitern durchgeführt.",
                            "Erhebungen in Gesundheitseinrichtungen (Health Facility Surveys): Der quantitative Aspekt dieser Bewertung wird durch eine Datenerhebung in Gesundheitseinrichtungen abgedeckt. Wir werden Daten in Form eines standardisierten Fragebogens bei den Leitern der untersuchten Gesundheitseinrichtungen erheben. Die Leiter werden ausschließlich durch das CEA-PCMT über die zuständige Präfekturdirektion für Gesundheit (DPS) rekrutiert. Das heißt, dass das DPS zunächst um Erlaubnis für die Umfrage in den Gesundheitseinrichtungen gebeten wird und die DPS-Leitung dann den Kontakt zu der Gesundheitseinrichtung, bzw. dessen Leitung herstellt. E-Mail-Adressen, Telefonnummern oder sonstige Kontaktdaten der Leiter werden dem RKI und dem CEA-PCMT in keiner Form zur Verfügung gestellt. Im Rahmen der Umfrage werden die Faktoren und Hindernisse für die Durchführung von Impfungen im Gesundheitssystem ermittelt, die Zugänglichkeit und Verfügbarkeit von Routineimpfungen bewertet und Daten zur Durchimpfungsrate und zur Akzeptanz von Impfungen in der Bevölkerung erhoben. Sie werden auch Informationen über die Verfügbarkeit von Ressourcen, Personal, Ausrüstung und Fachwissen liefern. Eine Liste der in die Erhebung einbezogenen Variablen ist in Abschnitt 4.1 aufgeführt.",
                            "Sekundäre Daten: Vorhandene Routinedaten, die durch das Gesundheitsinformationsmanagementsystem Guineas, durch Demografie- und Gesundheitserhebungen (DHS) und durch das Institut für Gesundheitsmetrik und -evaluierung (IHME) generiert werden, werden genutzt, um den aktuellen Stand des Impfprogramms zu verstehen sowie Lücken, Trends und Diskrepanzen zwischen offiziellen Aufzeichnungen und Sekundärdaten zu identifizieren. Sekundärdaten erhält das RKI immer nur in einem bereits anonymisierten Format, das auf der Ebene der Gesundheitseinrichtung oder höher aggregiert ist. Das RKI ist zu keinem Zeitpunkt für die Erhebung der Sekundärdaten verantwortlich und ist nicht Eigentümer dieser Daten. Sekundärdaten werden grundsätzlich als öffentliche Daten betrachtet. Die Sekundärdatensätze werden nie ohne vorherige Genehmigung des Gesundheitsministeriums oder einer anderen Organisation, die die Kontrolle über den Datensatz hat, veröffentlicht. Die Ergebnisse der Sekundäranalyse werden immer in einem aggregierten Format veröffentlicht. Sekundärdaten werden in dieser Anwendung aufgrund der oben genannten Überlegungen nicht weiter beschrieben, da es sich um öffentliche aggregierte Daten handelt, die außerhalb des RKI verwaltet werden.",
                            "Datenanalyse: Die Daten aus dem Desk review werden in einer Excel-Tabelle zusammengefasst. Transkriptionen und Übersetzungen von Interviews mit Schlüsselinformanten werden mit einer intern vorab genehmigten Analysesoftware (NVIVO oder MAXQDA) ausgewertet. Alle analysierten Daten werden in einem pseudonymisierten Format gespeichert. Die Sekundärdaten werden mit der Statistiksoftware R analysiert. Die Audioaufnahmen und Transkripte werden gemäß guter wissenschaftlicher Praxis 10 Jahre lang aufbewahrt.",
                            "Die Daten aus der Befragung der Gesundheitseinrichtungen werden in einem anonymisierten Format an das RKI übermittelt und mit der intern vorab genehmigten Analysesoftware R, Stata und Python ausgewertet.",
                            "Verbreitung: Die Ergebnisse der Studie werden für weitere vertiefende Untersuchungen des EPI genutzt. Die Daten aus VRSA-WP1 werden auch in Form eines Berichts und einer PowerPoint-Präsentation während eines Workshops mit Interessengruppen vorgestellt. Die Ergebnisse werden außerdem in wissenschaftlichen Zeitschriften veröffentlicht. Alle Daten und Ergebnisse werden in einem aggregierten Format veröffentlicht.",
                        ]
                    }
                ]
            },
            {
                "cells": [
                    {"text": "Verantwortliche(r) StudienleiterIn"},
                    {"text": "OE"},
                    {"text": "Abt."},
                    {"text": "Tel."},
                ]
            },
            {
                "cells": [
                    {"texts": ["El Bcheraoui, Charbel;", "El-BcheraouiC@rki.de"]},
                    {"texts": ["ZIG2"]},
                    {"texts": ["ZIG"]},
                    {"texts": ["+49 30 18754 5067"]},
                ]
            },
            {
                "cells": [
                    {"text": "ggfs. Vertreter der / des Verantwortlichen"},
                    {"text": "OE"},
                    {"text": None},
                    {"text": "Tel."},
                ]
            },
            {
                "cells": [
                    {"texts": ["Al-Awlaqi, Sameh,", "Al-AwlaqiS@rki.de"]},
                    {"texts": ["ZIG2"]},
                    {"texts": ["ZIG"]},
                    {"texts": ["+49 30 18754 5154"]},
                ]
            },
            {
                "cells": [
                    {"text": "Mitarbeitende"},
                    {"text": "OE"},
                    {"text": None},
                    {"text": "Tel."},
                ]
            },
            {
                "cells": [
                    {
                        "texts": [
                            "Heide Weishaar",
                            "Pozo-Martin, Francisco",
                            "Geurts, Brogan",
                            "Feddern, Lukas",
                            "Greis, Alina",
                            "Al-Waziza, Raof",
                            "Röbl, Klara",
                        ]
                    },
                    {"texts": ["ZIG2", "ZIG2", "ZIG2", "ZIG2", "ZIG2", "ZIG2", "ABT3"]},
                    {"texts": ["ZIG", "ZIG", "ZIG", "ZIG", "ZIG", "ZIG", "FG32"]},
                    {
                        "texts": [
                            "+49 30 18754 5115",
                            "+49 30 18754 3685",
                            "+49 30 18754 5163",
                            "+49 30 18754 2876",
                            "+49 30 18754 5294",
                            "+49 30 18754 2391",
                            "+49 30 18754 5282",
                        ]
                    },
                ]
            },
            {
                "cells": [
                    {
                        "text": "ggfs. gemeinsam Verantwortliche(r) nach Art. 26 DSGVO (Nennung der Behörde/des Unternehmens inkl. vollständige Adresse UND der Kontaktdaten des dortigen Studienleiters / der dortigen Studienleiterin)"
                    },
                    {"text": "Tel."},
                ]
            },
            {"cells": [{"texts": None}, {"texts": None}]},
            {
                "cells": [
                    {
                        "text": "ggfs. Name des /der DSB des gemeinsam Verantwortlichen nach Art. 26 DSGVO (inkl. der Kontaktdaten)"
                    }
                ]
            },
            {
                "cells": [
                    {
                        "texts": [
                            "Centre d'Excellence Africain pour la Prévention et le Contrôle des Maladies Transmissibles of the Université Gamal Abdel Nasser (CEA-PMCT),",
                            "Commune de Dixinn, Rue 254, BP: 1017, Conakry, Guinea,",
                            "Prof. Alexandre Delamou, Associate Professor, head of CEA-PCMT",
                            "Tel: +224628594765",
                            "E: adelamou@cea-pcmt.org",
                        ]
                    }
                ]
            },
            {"cells": [{"text": "ggfs. Auftragsverarbeiter nach Art. 28 DSGVO"}]},
            {"cells": [{"texts": None}]},
            {
                "cells": [
                    {
                        "text": "ggfs. Name des /der DSB des Auftragsverarbeiters nach Art. 28 DSGVO (inkl. der Kontaktdaten)"
                    }
                ]
            },
            {"cells": [{"texts": None}]},
        ]
    }

    all_pages_ids = list(fetch_all_vvt_pages_ids())
    assert len(all_pages_ids) >= 196


nested_dict = {
    "heading_value_pair_row_1": [
        {"heading": "Interne nummer", "value": "DS-1234"},
        {"heading": "heading cell1", "value": "Bear. Wolf"},
    ],
    "heading_value_pair_row_2": [
        {"heading": "second row heading cell 1", "value": "second row value cell 1"},
        {"heading": "second row heading cell 2", "value": "second row value cell 2"},
        {"heading": "second row heading cell 3", "value": "second row value cell 3"},
    ],
    "heading_value_pair_row_3": [
        {
            "heading": "second row heading only cell",
            "value": "second row value only cell",
        },
    ],
}
