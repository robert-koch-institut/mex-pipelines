from typing import Any

import pytest

from mex.common.models import (
    ExtractedAccessPlatform,
    ExtractedPerson,
    ExtractedPrimarySource,
)
from mex.common.testing import Joker
from mex.common.types import (
    Email,
    MergedContactPointIdentifier,
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
    YearMonth,
)
from mex.grippeweb.transform import (
    transform_grippeweb_access_platform_to_extracted_access_platform,
    transform_grippeweb_resource_mappings_to_dict,
    transform_grippeweb_resource_mappings_to_extracted_resources,
)


@pytest.mark.usefixtures("mocked_grippeweb")
def test_transform_grippeweb_access_platform_to_extracted_access_platform(
    grippeweb_access_platform: dict[str, Any],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
    extracted_mex_persons_grippeweb: list[ExtractedPerson],
) -> None:

    extracted_access_platform = (
        transform_grippeweb_access_platform_to_extracted_access_platform(
            grippeweb_access_platform,
            unit_stable_target_ids_by_synonym,
            extracted_primary_sources["grippeweb"],
            extracted_mex_persons_grippeweb,
        )
    )
    expected = {
        "hadPrimarySource": extracted_primary_sources["grippeweb"].stableTargetId,
        "identifierInPrimarySource": "primary-source",
        "contact": [extracted_mex_persons_grippeweb[0].stableTargetId],
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


@pytest.mark.usefixtures("mocked_grippeweb")
def test_transform_grippeweb_resource_mappings_to_dict(
    grippeweb_resource_mappings: list[dict[str, Any]],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    grippeweb_extracted_access_platform: ExtractedAccessPlatform,
    extracted_primary_sources: list[ExtractedPrimarySource],
    extracted_mex_persons_grippeweb: list[ExtractedPerson],
    grippeweb_organization_ids_by_query_string: dict[str, MergedOrganizationIdentifier],
    extracted_mex_functional_units_grippeweb: dict[Email, MergedContactPointIdentifier],
) -> None:
    resource_dict = transform_grippeweb_resource_mappings_to_dict(
        grippeweb_resource_mappings,
        unit_stable_target_ids_by_synonym,
        grippeweb_extracted_access_platform,
        extracted_primary_sources["grippeweb"],
        extracted_mex_persons_grippeweb,
        grippeweb_organization_ids_by_query_string,
        extracted_mex_functional_units_grippeweb,
    )
    expected = {
        "hadPrimarySource": extracted_primary_sources["grippeweb"].stableTargetId,
        "identifierInPrimarySource": "grippeweb",
        "accessPlatform": [grippeweb_extracted_access_platform.stableTargetId],
        "accessRestriction": "https://mex.rki.de/item/access-restriction-2",
        "accrualPeriodicity": "https://mex.rki.de/item/frequency-15",
        "anonymizationPseudonymization": [
            "https://mex.rki.de/item/anonymization-pseudonymization-2"
        ],
        "contact": [extracted_mex_functional_units_grippeweb["contactc@rki.de"]],
        "contributingUnit": [unit_stable_target_ids_by_synonym["C1"]],
        "contributor": [extracted_mex_persons_grippeweb[0].stableTargetId],
        "created": YearMonth("2011"),
        "description": [{"value": "GrippeWeb", "language": "de"}],
        "documentation": [
            {"language": "de", "title": "RKI Website", "url": "https://www.rki.de"}
        ],
        "icd10code": ["J00-J99"],
        "keyword": [{"value": "Citizen Science", "language": "en"}],
        "language": ["https://mex.rki.de/item/language-1"],
        "meshId": ["http://id.nlm.nih.gov/mesh/D012140"],
        "method": [{"value": "Online-Befragung", "language": "de"}],
        "methodDescription": [
            {"value": "Online-Surveillanceintrument", "language": "de"}
        ],
        "publication": [
            {
                "language": "de",
                "title": "COVID-19-Raten",
                "url": "https://doi.org/10.25646/11292",
            }
        ],
        "publisher": [
            grippeweb_organization_ids_by_query_string["Robert Koch-Institut"]
        ],
        "resourceTypeGeneral": ["https://mex.rki.de/item/resource-type-general-10"],
        "resourceTypeSpecific": [
            {"value": "bevölkerungsbasierte Surveillancedaten", "language": "de"}
        ],
        "rights": [{"value": "Verfahren", "language": "de"}],
        "stateOfDataProcessing": ["https://mex.rki.de/item/data-processing-state-1"],
        "temporal": "seit 2011",
        "theme": ["https://mex.rki.de/item/theme-35"],
        "title": [{"value": "GrippeWeb", "language": "de"}],
        "unitInCharge": [unit_stable_target_ids_by_synonym["C1"]],
        "identifier": Joker(),
        "stableTargetId": Joker(),
    }
    assert (
        resource_dict["grippeweb"].model_dump(exclude_none=True, exclude_defaults=True)
        == expected
    )


@pytest.mark.usefixtures("mocked_grippeweb")
def test_transform_grippeweb_resource_mappings_to_extracted_resources(
    grippeweb_resource_mappings: list[dict[str, Any]],
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    grippeweb_extracted_access_platform: ExtractedAccessPlatform,
    extracted_primary_sources: list[ExtractedPrimarySource],
    extracted_mex_persons_grippeweb: list[ExtractedPerson],
    grippeweb_organization_ids_by_query_string: dict[str, MergedOrganizationIdentifier],
    extracted_mex_functional_units_grippeweb: dict[Email, MergedContactPointIdentifier],
) -> None:
    resource_dict = transform_grippeweb_resource_mappings_to_extracted_resources(
        grippeweb_resource_mappings,
        unit_stable_target_ids_by_synonym,
        grippeweb_extracted_access_platform,
        extracted_primary_sources["grippeweb"],
        extracted_mex_persons_grippeweb,
        grippeweb_organization_ids_by_query_string,
        extracted_mex_functional_units_grippeweb,
    )
    assert resource_dict["grippeweb-plus"].isPartOf == [
        resource_dict["grippeweb"].stableTargetId
    ]
