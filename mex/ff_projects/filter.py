from collections.abc import Generator, Iterable

from mex.common.types import Identifier, MergedOrganizationalUnitIdentifier
from mex.common.utils import any_contains_any, contains_any
from mex.ff_projects.models.source import FFProjectsSource
from mex.ff_projects.settings import FFProjectsSettings
from mex.logging import log_filter


def filter_and_log_ff_projects_sources(
    sources: Iterable[FFProjectsSource],
    primary_source_id: Identifier,
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
) -> Generator[FFProjectsSource, None, None]:
    """Filter FF Projects sources and log filtered sources.

    Args:
        sources: Iterable of FFProjectSources
        primary_source_id: Identifier of primary source
        unit_stable_target_ids_by_synonym: Unit IDs grouped by synonyms

    Returns:
        Generator for filtered FF Projects sources
    """
    for source in sources:
        if filter_and_log_ff_projects_source(
            source, primary_source_id, unit_stable_target_ids_by_synonym
        ):
            yield source


def filter_and_log_ff_projects_source(
    source: FFProjectsSource,
    primary_source_id: Identifier,
    unit_stable_target_ids_by_synonym: dict[str, MergedOrganizationalUnitIdentifier],
) -> bool:
    """Filter a FFprojectSource according to settings and log filtering.

    Args:
        source: FFProjectSource
        primary_source_id: Identifier of primary source
        unit_stable_target_ids_by_synonym: Unit IDs grouped by synonyms

    Settings:
        skip_categories: Skip sources with these categories
        skip_funding: Skip sources with this funding
        skip_topics: Skip sources with these topics
        skip_years: Skip sources with these years
        skip_clients: Skip sources with these clients

    Returns:
        False if source is filtered out, else True
    """
    settings = FFProjectsSettings.get()
    identifier_in_primary_source = source.lfd_nr
    if source.kategorie in settings.skip_categories:
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"Kategorie [{source.kategorie}] in settings.skip_categories",
        )
        return False

    if source.foerderprogr in settings.skip_funding:
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"Foerderprogr. [{source.foerderprogr}] in settings.skip_funding",
        )
        return False

    if source.thema_des_projekts is None or contains_any(
        source.thema_des_projekts, settings.skip_topics
    ):
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"Thema des Projekts [{source.thema_des_projekts}] "
            "is None or in settings.skip_topics",
        )
        return False

    if source.rki_az is None:
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"RKI-AZ [{source.rki_az}] is None",
        )
        return False

    if any_contains_any(source.laufzeit_cells, settings.skip_years_strings):
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"Laufzeit von/bis [{source.laufzeit_cells}] "
            "in settings.skip_years_strings",
        )
        return False

    if source.zuwendungs_oder_auftraggeber and contains_any(
        source.zuwendungs_oder_auftraggeber, settings.skip_clients
    ):
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"Zuwendungs-/ Auftraggeber [{source.zuwendungs_oder_auftraggeber}] "
            "is None or in settings.skip_clients",
        )
        return False

    if source.lfd_nr is None:
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"lfd. Nr. [{source.lfd_nr}] is None",
        )
        return False

    if source.rki_oe not in unit_stable_target_ids_by_synonym:
        log_filter(
            identifier_in_primary_source,
            primary_source_id,
            f"RKI- OE [{source.rki_oe}] is not a valid unit",
        )
        return False

    return True
