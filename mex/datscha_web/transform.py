from collections.abc import Generator, Hashable, Iterable

from mex.common.logging import watch
from mex.common.models import (
    ExtractedActivity,
    ExtractedPrimarySource,
)
from mex.common.types import Identifier
from mex.datscha_web.models.item import DatschaWebItem


@watch
def transform_datscha_web_items_to_mex_activities(
    datscha_web_items: Iterable[DatschaWebItem],
    primary_source: ExtractedPrimarySource,
    person_stable_target_ids_by_query_string: dict[Hashable, list[Identifier]],
    unit_stable_target_ids_by_synonym: dict[str, Identifier],
    organizations_stable_target_ids_by_query_string: dict[str, Identifier],
) -> Generator[ExtractedActivity, None, None]:
    """Transform datscha-web items to extracted activities.

    Args:
        datscha_web_items: Datscha-web items
        primary_source: MEx primary_source for datscha-web
        person_stable_target_ids_by_query_string: Mapping from author query
                                                  to person stable target IDs
        unit_stable_target_ids_by_synonym: Mapping from unit acronyms and labels
                                           to unit stable target IDs
        organizations_stable_target_ids_by_query_string: Mapping from org queries
                                                         to org stable target IDs

    Returns:
        Generator for ExtractedSources
    """
    for datscha_web_item in datscha_web_items:
        # lookup units
        involved_unit = (
            unit_stable_target_ids_by_synonym.get(unit_name)
            if (unit_name := datscha_web_item.zentrale_stelle_fuer_die_verarbeitung)
            else None
        )
        responsible_unit = [
            unit_id
            for unit_name in (
                datscha_web_item.liegenschaften_oder_organisationseinheiten_loz
            )
            if (unit_id := unit_stable_target_ids_by_synonym.get(unit_name))
        ]
        # lookup actors
        involved_person = person_stable_target_ids_by_query_string[
            datscha_web_item.auskunftsperson
        ]
        if involved_person:
            contact = involved_person
        else:
            contact = responsible_unit

        external_associate = []
        for partner in datscha_web_item.get_partners():
            if partner:
                if associate := organizations_stable_target_ids_by_query_string.get(
                    partner
                ):
                    external_associate.append(associate)

        yield ExtractedActivity(
            abstract=datscha_web_item.kurzbeschreibung,
            activityType="https://mex.rki.de/item/activity-type-6",
            contact=contact,
            externalAssociate=external_associate,
            hadPrimarySource=primary_source.stableTargetId,
            identifierInPrimarySource=str(datscha_web_item.item_id),
            involvedPerson=involved_person,
            involvedUnit=involved_unit,
            responsibleUnit=responsible_unit,
            theme="https://mex.rki.de/item/theme-1",
            title=datscha_web_item.bezeichnung_der_verarbeitungstaetigkeit,
        )
