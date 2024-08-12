from collections.abc import Generator, Hashable, Iterable

from mex.common.logging import watch
from mex.common.models import ExtractedActivity, ExtractedPrimarySource
from mex.common.types import ActivityType, Identifier, Theme
from mex.common.utils import contains_any
from mex.extractors.blueant.models.source import BlueAntSource

INTERNATIONAL_PROJECT_DEPARTMENTS = [
    "ZIG",
    "Europäische Union",
    "EU",
    "Auswärtiges Amt",
    "WHO Europe",
    "World Wildlife Fund",
]

RKI_INTERNAL_PROJECT_TYPES = [
    "Standardprojekt",
    "Standardprojekt agil",
    "Dienstleistung und Support",
    "Linienprojekt",
    "internes Projekt",
    "Organisationsprojekt",
    "Maßnahme",
]

STUDY_PROJECT_TYPES = ["Study"]


@watch
def transform_blueant_sources_to_extracted_activities(
    blueant_sources: Iterable[BlueAntSource],
    primary_source: ExtractedPrimarySource,
    person_stable_target_ids_by_employee_id: dict[Hashable, list[Identifier]],
    unit_stable_target_ids_by_synonym: dict[str, Identifier],
) -> Generator[ExtractedActivity, None, None]:
    """Transform Blue Ant sources to ExtractedActivities.

    Args:
        blueant_sources: Blue Ant sources
        primary_source: MEx primary_source for Blue Ant
        person_stable_target_ids_by_employee_id: Mapping from LDAP employeeIDs
                                                 to person stable target IDs
        unit_stable_target_ids_by_synonym: Map from unit acronyms and labels
                                           to unit stable target IDs

    Returns:
        Generator for ExtractedActivity instances
    """
    for source in blueant_sources:
        # find source type
        if contains_any(source.type_, RKI_INTERNAL_PROJECT_TYPES):
            activity_type = [ActivityType["RKI_INTERNAL_PROJECT"]]
        elif contains_any(source.department, INTERNATIONAL_PROJECT_DEPARTMENTS):
            activity_type = [ActivityType["INTERNATIONAL_PROJECT"]]
        elif contains_any(source.type_, STUDY_PROJECT_TYPES):
            activity_type = [ActivityType["STUDY"]]
        else:
            activity_type = [ActivityType["OTHER"]]

        # find responsible unit
        department = source.department.replace("(h)", "").strip()
        responsible_unit = unit_stable_target_ids_by_synonym.get(department)

        # get contact employee or fallback to unit
        contact = person_stable_target_ids_by_employee_id[
            source.projectLeaderEmployeeId
        ]
        if not contact and responsible_unit:
            contact.append(responsible_unit)

        theme = [Theme["PUBLIC_HEALTH"]]

        yield ExtractedActivity(
            start=source.start,
            end=source.end,
            activityType=activity_type,
            contact=contact,
            involvedPerson=person_stable_target_ids_by_employee_id[
                source.projectLeaderEmployeeId
            ],
            hadPrimarySource=primary_source.stableTargetId,
            responsibleUnit=responsible_unit,
            # TODO: resolve funderOrCommissioner as organization from client_names
            funderOrCommissioner=None,
            theme=theme,
            title=source.name,
            identifierInPrimarySource=source.number,
        )
