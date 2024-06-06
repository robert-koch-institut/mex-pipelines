from collections.abc import Hashable

import pytest

from mex.common.models import ExtractedPrimarySource
from mex.common.testing import Joker
from mex.common.types import Identifier
from mex.datscha_web.models.item import DatschaWebItem
from mex.datscha_web.transform import (
    transform_datscha_web_items_to_mex_activities,
)


@pytest.fixture
def person_stable_target_ids_by_query_string() -> dict[Hashable, list[Identifier]]:
    return {
        "Coolname, Cordula/ Ausgedacht, Alwina": [
            Identifier("ID000000001111"),
            Identifier("ID000000002222"),
        ],
        None: [],
    }


@pytest.fixture
def unit_stable_target_ids_by_synonym() -> dict[str, Identifier]:
    return {
        "L1": Identifier("ID000000000033"),
        "FG99": Identifier("ID000000000044"),
        "Abteilung 2": Identifier("ID000000000055"),
    }


@pytest.fixture
def organizations_stable_target_ids_by_query_string() -> dict[str, Identifier]:
    return {
        "Mentzel Oderwald OHG mbH": Identifier("ID000000000077"),
        "FG99": Identifier("ID000000000884"),
        "Abteilung 2": Identifier("ID000000000039"),
    }


def test_transform_datscha_web_items_to_mex_activities(
    datscha_web_item: DatschaWebItem,
    person_stable_target_ids_by_query_string: dict[Hashable, list[Identifier]],
    unit_stable_target_ids_by_synonym: dict[str, Identifier],
    organizations_stable_target_ids_by_query_string: dict[str, Identifier],
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
) -> None:
    mex_sources = list(
        transform_datscha_web_items_to_mex_activities(
            [datscha_web_item],
            extracted_primary_sources["datscha-web"],
            person_stable_target_ids_by_query_string,
            unit_stable_target_ids_by_synonym,
            organizations_stable_target_ids_by_query_string,
        )
    )

    assert len(mex_sources) == 1
    assert mex_sources[0].model_dump(exclude_none=True, exclude_defaults=True) == {
        "abstract": [
            {
                "value": "Est quas tempore placeat. Nam explicabo et odit "
                "dignissimos mollitia ipsam. Ea rem molestias "
                "accusamus quaerat id repudiandae. A laudantium sint "
                "doloribus eveniet sit deleniti necessitatibus."
            }
        ],
        "activityType": ["https://mex.rki.de/item/activity-type-6"],
        "contact": [Identifier("ID000000001111"), Identifier("ID000000002222")],
        "externalAssociate": [Identifier("ID000000000077")],
        "hadPrimarySource": extracted_primary_sources["datscha-web"].stableTargetId,
        "identifier": Joker(),
        "identifierInPrimarySource": "17",
        "involvedPerson": [Identifier("ID000000001111"), Identifier("ID000000002222")],
        "involvedUnit": [Identifier("ID000000000055")],
        "responsibleUnit": [
            Identifier("ID000000000033"),
            Identifier("ID000000000044"),
        ],
        "stableTargetId": Joker(),
        "theme": ["https://mex.rki.de/item/theme-1"],
        "title": [{"value": "Consequuntur atque reiciendis voluptates minus."}],
    }


def test_transform_datscha_web_items_to_mex_activities_without_involved_persons(
    datscha_web_item_without_contributors: DatschaWebItem,
    person_stable_target_ids_by_query_string: dict[Hashable, list[Identifier]],
    unit_stable_target_ids_by_synonym: dict[str, Identifier],
    organizations_stable_target_ids_by_query_string: dict[str, Identifier],
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
) -> None:
    mex_sources = list(
        transform_datscha_web_items_to_mex_activities(
            [datscha_web_item_without_contributors],
            extracted_primary_sources["datscha-web"],
            person_stable_target_ids_by_query_string,
            unit_stable_target_ids_by_synonym,
            organizations_stable_target_ids_by_query_string,
        )
    )

    assert len(mex_sources) == 1
    assert mex_sources[0].model_dump(exclude_none=True, exclude_defaults=True) == {
        "abstract": [
            {
                "value": "Est quas tempore placeat. Nam explicabo et odit dignissimos "
                "mollitia ipsam. Ea rem molestias accusamus quaerat id "
                "repudiandae. A laudantium sint doloribus eveniet sit deleniti "
                "necessitatibus."
            }
        ],
        "activityType": ["https://mex.rki.de/item/activity-type-6"],
        "contact": [
            Identifier("ID000000000033"),
            Identifier("ID000000000044"),
        ],
        "externalAssociate": [Identifier("ID000000000077")],
        "hadPrimarySource": extracted_primary_sources["datscha-web"].stableTargetId,
        "identifier": Joker(),
        "identifierInPrimarySource": "92",
        "responsibleUnit": [
            Identifier("ID000000000033"),
            Identifier("ID000000000044"),
        ],
        "stableTargetId": Joker(),
        "theme": ["https://mex.rki.de/item/theme-1"],
        "title": [{"value": "Consequuntur atque reiciendis voluptates minus."}],
    }
