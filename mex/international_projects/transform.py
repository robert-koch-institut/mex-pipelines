from collections import defaultdict
from collections.abc import Generator, Hashable, Iterable

from mex.common.logging import watch
from mex.common.models import ExtractedActivity, ExtractedPrimarySource
from mex.common.types import (
    ActivityType,
    Link,
    MergedOrganizationalUnitIdentifier,
    MergedOrganizationIdentifier,
    MergedPersonIdentifier,
    Theme,
)
from mex.international_projects.models.source import InternationalProjectsSource

THEME_BY_ACTIVITY_OR_TOPIC = {
    "Other": Theme["PUBLIC_HEALTH"],
    "Crisis management": Theme["PUBLIC_HEALTH"],
    "Capacity building including trainings": Theme["PUBLIC_HEALTH"],
    "Conducting research": Theme["RESEARCH"],
    "Supporting global governance structures and processes": Theme["PUBLIC_HEALTH"],
    "Public health systems": Theme["PUBLIC_HEALTH"],
    "Non-communicable diseases": Theme["NON_COMMUNICABLE_DISEASE"],
    "Laboratory diagnostics": Theme["LABORATORY"],
    "One Health": Theme["ONE_HEALTH"],
    "Surveillance (infectious diseases)": Theme["PUBLIC_HEALTH"],
    "Vaccines/vaccinations": Theme["PUBLIC_HEALTH"],
}
ACTIVITY_TYPES_BY_FUNDING_TYPE = defaultdict(
    lambda: [ActivityType["INTERNATIONAL_PROJECT"]],
    {
        "Third party funded": [
            ActivityType["INTERNATIONAL_PROJECT"],
            ActivityType["THIRD_PARTY_FUNDED_PROJECT"],
        ],
        "RKI funded": [
            ActivityType["INTERNATIONAL_PROJECT"],
            ActivityType["RKI_INTERNAL_PROJECT"],
        ],
    },
)


def transform_international_projects_source_to_extracted_activity(
    source: InternationalProjectsSource,
    extracted_primary_source: ExtractedPrimarySource,
    person_stable_target_ids_by_query_string: dict[
        Hashable, list[MergedPersonIdentifier]
    ],
    unit_stable_target_id_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    funding_sources_stable_target_id_by_query: dict[str, MergedOrganizationIdentifier],
    partner_organizations_stable_target_id_by_query: dict[
        str, MergedOrganizationIdentifier
    ],
) -> ExtractedActivity | None:
    """Transform international projects source to extracted activity.

    Args:
        source: international projects sources
        extracted_primary_source: Extracted primary_source for FF Projects
        person_stable_target_ids_by_query_string: Mapping from author query
                                                  to person stable target ID
        unit_stable_target_id_by_synonym: Mapping from unit acronyms and labels
                                          to unit stable target ID
        funding_sources_stable_target_id_by_query: Mapping from funding sources
                                                   to organization stable target ID
        partner_organizations_stable_target_id_by_query: Mapping from partner orgs to
                                                         their stable target ID

    Returns:
        ExtractedActivity or None if it was filtered out
    """
    if not source.full_project_name and not source.project_abbreviation:
        return None

    project_leads = person_stable_target_ids_by_query_string.get(
        source.project_lead_person, []
    )
    project_lead_rki_unit = unit_stable_target_id_by_synonym.get(
        source.project_lead_rki_unit
    )

    if not project_lead_rki_unit:
        return None

    additional_rki_units = (
        unit_stable_target_id_by_synonym.get(source.additional_rki_units)
        if source.additional_rki_units
        else None
    )

    all_funder_or_commissioner: list[MergedOrganizationIdentifier] = []
    if source.funding_source:
        all_funder_or_commissioner.extend(
            wfc
            for fc in source.funding_source
            if (wfc := funding_sources_stable_target_id_by_query.get(fc))
        )

    all_partner_organizations: list[MergedOrganizationIdentifier] = []
    if source.partner_organization:
        all_partner_organizations.extend(
            wfc
            for fc in source.partner_organization
            if (wfc := partner_organizations_stable_target_id_by_query.get(fc))
        )

    return ExtractedActivity(
        title=source.full_project_name,
        activityType=ACTIVITY_TYPES_BY_FUNDING_TYPE.get(source.funding_type),
        alternativeTitle=source.project_abbreviation,
        contact=[*project_leads, project_lead_rki_unit],
        involvedPerson=project_leads,
        involvedUnit=additional_rki_units,
        start=source.start_date,
        end=source.end_date,
        responsibleUnit=project_lead_rki_unit,
        identifierInPrimarySource=source.rki_internal_project_number
        or source.project_abbreviation,
        funderOrCommissioner=all_funder_or_commissioner,
        externalAssociate=all_partner_organizations,
        hadPrimarySource=extracted_primary_source.stableTargetId,
        fundingProgram=source.funding_program if source.funding_program else [],
        shortName=source.project_abbreviation,
        theme=get_theme_for_activity_or_topic(
            source.activity1, source.activity2, source.topic1, source.topic2
        ),
        website=(
            []
            if source.website in ("", "does not exist yet")
            else [Link(url=source.website)]
        ),
    )


@watch
def transform_international_projects_sources_to_extracted_activities(
    international_projects_sources: Iterable[InternationalProjectsSource],
    extracted_primary_source: ExtractedPrimarySource,
    person_stable_target_ids_by_query_string: dict[
        Hashable, list[MergedPersonIdentifier]
    ],
    unit_stable_target_id_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
    funding_sources_stable_target_id_by_query: dict[str, MergedOrganizationIdentifier],
    partner_organizations_stable_target_id_by_query: dict[
        str, MergedOrganizationIdentifier
    ],
) -> Generator[ExtractedActivity, None, None]:
    """Transform international projects sources to extracted activity.

    Args:
        international_projects_sources: international projects sources
        extracted_primary_source: Extracted primary_source for FF Projects
        person_stable_target_ids_by_query_string: Mapping from author query
                                                  to person stable target ID
        unit_stable_target_id_by_synonym: Mapping from unit acronyms and labels
                                          to unit stable target ID
        funding_sources_stable_target_id_by_query: Mapping from funding sources
                                                   to organization stable target ID
        partner_organizations_stable_target_id_by_query: Mapping from partner orgs to
                                                         their stable target ID

    Returns:
        Generator for ExtractedActivity instances
    """
    for source in international_projects_sources:
        if activity := transform_international_projects_source_to_extracted_activity(
            source,
            extracted_primary_source,
            person_stable_target_ids_by_query_string,
            unit_stable_target_id_by_synonym,
            funding_sources_stable_target_id_by_query,
            partner_organizations_stable_target_id_by_query,
        ):
            yield activity


def get_theme_for_activity_or_topic(
    activity1: str | None, activity2: str | None, topic1: str | None, topic2: str | None
) -> list[Theme]:
    """Get theme identifier for activities and topics.

    Args:
        activity1: activity 1
        activity2: activity 1
        topic1: topic 1
        topic2: topic 2

    Returns:
        Sorted list of Theme
    """
    theme = set()

    if not activity1 and activity2 and topic1 and topic2:
        return [THEME_BY_ACTIVITY_OR_TOPIC["Other"]]
    if activity1:
        if a1 := THEME_BY_ACTIVITY_OR_TOPIC.get(activity1):
            theme.add(a1)
    if activity2:
        if a2 := THEME_BY_ACTIVITY_OR_TOPIC.get(activity2):
            theme.add(a2)
    if topic1:
        if t1 := THEME_BY_ACTIVITY_OR_TOPIC.get(topic1):
            theme.add(t1)
    if topic2:
        if t2 := THEME_BY_ACTIVITY_OR_TOPIC.get(topic2):
            theme.add(t2)

    return sorted(list(theme), key=lambda x: x.name)
