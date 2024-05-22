from typing import Any

from mex.common.models import (
    ExtractedPrimarySource,
)
from mex.common.testing import Joker
from mex.common.types import (
    Email,
    MergedContactPointIdentifier,
    MergedOrganizationalUnitIdentifier,
)
from mex.grippeweb.transform import (
    transform_grippeweb_access_platform_to_extracted_access_platform,
)


def test_transform_grippeweb_access_platform_to_extracted_access_platform(
    grippeweb_access_platform: dict[str, Any],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
    extracted_mex_functional_units_grippeweb: dict[Email, MergedContactPointIdentifier],
) -> None:

    extracted_access_platform = (
        transform_grippeweb_access_platform_to_extracted_access_platform(
            grippeweb_access_platform,
            unit_stable_target_ids_by_synonym,
            extracted_primary_sources["grippeweb"],
            extracted_mex_functional_units_grippeweb,
        )
    )
    expected = {
        "hadPrimarySource": extracted_primary_sources["grippeweb"].stableTargetId,
        "identifierInPrimarySource": "primary-source",
        "contact": [extracted_mex_functional_units_grippeweb["c1@email.de"]],
        "technicalAccessibility": "https://mex.rki.de/item/technical-accessibility-1",
        "title": [{"value": "primary-source", "language": "en"}],
        "unitInCharge": [unit_stable_target_ids_by_synonym["C1"]],
        "identifier": Joker(),
        "stableTargetId": Joker(),
    }
    assert (
        extracted_access_platform.model_dump(exclude_none=True, exclude_defaults=True)
        == expected
    )
