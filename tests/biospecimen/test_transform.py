from unittest.mock import MagicMock

from mex.biospecimen.extract import extract_biospecimen_resources
from mex.biospecimen.models.source import BiospecimenResource
from mex.biospecimen.transform import transform_biospecimen_resource_to_mex_resource
from mex.common.identity import get_provider
from mex.common.models import (
    ExtractedOrganization,
    ExtractedPerson,
    ExtractedPrimarySource,
)
from mex.common.testing import Joker
from mex.common.types import Identifier, TextLanguage


def test_transform_biospecimen_resource_to_mex_resource(
    extracted_primary_sources: dict[str, ExtractedPrimarySource],
    biospecimen_resources: BiospecimenResource,
    mex_persons: list[ExtractedPerson],
    extracted_organization_rki: ExtractedOrganization,
) -> None:
    unit_stable_target_ids = MagicMock()
    unit_stable_target_ids.get.side_effect = lambda _: Identifier.generate(seed=42)

    mex_sources = transform_biospecimen_resource_to_mex_resource(
        biospecimen_resources,
        extracted_primary_sources["biospecimen"],
        extracted_primary_sources["report-server"],
        unit_stable_target_ids,
        mex_persons,
        extracted_organization_rki,
    )
    mex_source = next(mex_sources)

    expected = {
        "accessRestriction": "https://mex.rki.de/item/access-restriction-2",
        "alternativeTitle": [{"value": "alternativer Testitel"}],
        "anonymizationPseudonymization": [
            "https://mex.rki.de/item/anonymization-pseudonymization-2"
        ],
        "contact": [mex_persons[0].stableTargetId],
        "contributingUnit": [Identifier.generate(seed=42)],
        "contributor": [Identifier.generate(seed=42)],
        "description": [{"language": TextLanguage.DE, "value": "Testbeschreibung"}],
        "documentation": [
            {"language": "de", "title": "Testdokutitel", "url": "Testdokupfad"}
        ],
        "externalPartner": [Identifier.generate(seed=42)],
        "hadPrimarySource": extracted_primary_sources["biospecimen"].stableTargetId,
        "identifier": Joker(),
        "identifierInPrimarySource": "Probe1",
        "instrumentToolOrApparatus": [{"value": "Testtool"}],
        "keyword": [
            {"language": TextLanguage.DE, "value": "Testschlagwort 1, Testschlagwort 2"}
        ],
        "loincId": ["12345-6"],
        "meshId": ["http://id.nlm.nih.gov/mesh/D123"],
        "method": [{"language": TextLanguage.EN, "value": "Testmethode"}],
        "methodDescription": [
            {"language": TextLanguage.DE, "value": "Testmethodenbeschreibung"}
        ],
        "publication": [{"url": "testverwandedoi"}],
        "publisher": [extracted_organization_rki.stableTargetId],
        "resourceTypeGeneral": ["https://mex.rki.de/item/resource-type-general-2"],
        "resourceTypeSpecific": [
            {"language": TextLanguage.DE, "value": "spezieller Testtyp"}
        ],
        "rights": [{"language": TextLanguage.DE, "value": "Testrechte"}],
        "sizeOfDataBasis": "Testanzahl",
        "spatial": [{"language": TextLanguage.DE, "value": "räumlicher Testbezug"}],
        "stableTargetId": Joker(),
        "temporal": "2021-09 bis 2021-10",
        "theme": [
            "https://mex.rki.de/item/theme-27",
            "https://mex.rki.de/item/theme-11",
            "https://mex.rki.de/item/theme-37",
        ],
        "title": [{"value": "test_titel"}],
        "unitInCharge": [Identifier.generate(seed=42)],
        # created_in_context_of is None, therefore not displayed
    }
    assert mex_source.model_dump(exclude_none=True, exclude_defaults=True) == expected

    identity_provider = get_provider()
    identity = identity_provider.assign(
        extracted_primary_sources["report-server"].stableTargetId,
        "1234567",
    )  # "1234567" is the StudienID from the test_data file

    mex_sources = transform_biospecimen_resource_to_mex_resource(
        extract_biospecimen_resources(),
        extracted_primary_sources["biospecimen"],
        extracted_primary_sources["report-server"],
        unit_stable_target_ids,
        mex_persons,
        extracted_organization_rki,
    )
    mex_source = next(mex_sources)

    expected = {
        "accessRestriction": "https://mex.rki.de/item/access-restriction-2",
        "alternativeTitle": [{"value": "alternativer Testitel"}],
        "anonymizationPseudonymization": [
            "https://mex.rki.de/item/anonymization-pseudonymization-2"
        ],
        "contact": [mex_persons[0].stableTargetId],
        "contributingUnit": [Identifier.generate(seed=42)],
        "contributor": [Identifier.generate(seed=42)],
        "description": [{"language": TextLanguage.DE, "value": "Testbeschreibung"}],
        "documentation": [
            {"language": "de", "title": "Testdokutitel", "url": "Testdokupfad"}
        ],
        "externalPartner": [Identifier.generate(seed=42)],
        "hadPrimarySource": extracted_primary_sources["biospecimen"].stableTargetId,
        "identifier": Joker(),
        "identifierInPrimarySource": "Probe1",
        "instrumentToolOrApparatus": [{"value": "Testtool"}],
        "keyword": [
            {"language": TextLanguage.DE, "value": "Testschlagwort 1, Testschlagwort 2"}
        ],
        "loincId": ["12345-6"],
        "meshId": ["http://id.nlm.nih.gov/mesh/D123"],
        "method": [{"language": TextLanguage.EN, "value": "Testmethode"}],
        "methodDescription": [
            {"language": TextLanguage.DE, "value": "Testmethodenbeschreibung"}
        ],
        "publication": [{"url": "testverwandedoi"}],
        "publisher": [extracted_organization_rki.stableTargetId],
        "resourceTypeGeneral": ["https://mex.rki.de/item/resource-type-general-2"],
        "resourceTypeSpecific": [
            {"language": TextLanguage.DE, "value": "spezieller Testtyp"}
        ],
        "rights": [{"language": TextLanguage.DE, "value": "Testrechte"}],
        "sizeOfDataBasis": "Testanzahl",
        "spatial": [{"language": TextLanguage.DE, "value": "räumlicher Testbezug"}],
        "stableTargetId": Joker(),
        "temporal": "2021-09 bis 2021-10",
        "theme": [
            "https://mex.rki.de/item/theme-27",
            "https://mex.rki.de/item/theme-11",
            "https://mex.rki.de/item/theme-37",
        ],
        "title": [{"value": "test_titel"}],
        "unitInCharge": [Identifier.generate(seed=42)],
        "wasGeneratedBy": identity.stableTargetId,
    }
    assert mex_source.model_dump(exclude_none=True, exclude_defaults=True) == expected
