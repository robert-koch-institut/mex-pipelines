# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changes

### Deprecated

### Removed

### Fixed

### Security

## [0.23.0] - 2024-12-18

### Changes

- extractors now use wikidata helper function
- BREAKING: rename artificial provider function `extracted_data` to `extracted_items`
- prefer concrete unions over base classes for merged and extracted item typing
- update mex-common to 0.45.0 and mex-model to 3.4.0

### Fixed

- fix coverage and linting issues

## [0.22.0] - 2024-12-10

### Changes

- wrap up ifsg model v3 update
- wrap up seq-repo model v3 update

## [0.21.0] - 2024-11-19

### Added

- convenience / helper functions for wikidata and primary source

### Changes

- make datscha ignore organizations with name "None"
- update mex-common to 0.41 and mex-model to 3.2

### Fixed

- fix a bunch of linting errors and remove ignored ruff codes

## [0.20.0] - 2024-11-11

### Added

- increase minimum valid artificial data count to two times the number of entity types

### Changes

- improve publishing pipeline: logging, Backend connector, allow-list

### Removed

- remove `matched` setting for the artificial extractor, since that was not implemented
- stop configuring entity-type weights for artificial data, since that broke determinism
- removed unused `-c` alias for the count setting of the artificial extractor
- deprecated mapping commit hashes in README

## [0.19.0] - 2024-10-29

### Added

- setting for configuring extractors to skip in dagster

### Changes

- BREAKING: refactor package structure from `mex.foo` to `mex.extractors.foo`
- BREAKING: Mapping extractors now returns Mapping models instead of nested dictionaries
- model v3 update: artificial, international-projects, seq-repo, synopse, blueant, sumo,
  biospecimen, odk, datscha-web, confluence-vvt, grippeweb, voxco, ifsg

### Fixed

- fix bug in seq-repo that caused exponential run-time and incorrect resource keywords
- fix artificial data generation for Integers, Loinc, and BibliographicResources
- make confluence-vvt ignore ill templated pages
- make ifsg identifierInPrimarySource unique to avoid stableTargetId collisions

## [0.18.0] - 2024-08-07

### Added

- transform voxco resources and variables

### Changes

- combine seq-repo distribution and resource extraction in one asset
- duplicate seq-repo activities are filtered out
- make dependent extractors explicitly depend on each other
  (grippeweb on confluence-vvt, biospecimen on synopse, odk on international-projects)
- add publisher pipeline to pull all merged items from backend and write them to ndjson
- BREAKING: integrate extractor specific settings in main extractor settings class.
  Environment variables change from `EXTRACTOR_PARAMETER` to `MEX_EXTRACTOR__PARAMETER`,
  access from `ExtractorSettings.parameter` to `settings.extractor.parameter`.
- update mex-common to 0.32.0

### Removed

- remove mypy ignores for arg-type and call-arg
- remove unused ldap module with is_person_in_identity_map_and_ldap function

### Fixed

- fix confluence_vvt: use interne Vorgangsnummer as identifierInPrimarySource
- remaining issues in voxco extractor

## [0.17.1] - 2024-06-14

### Fixed

- hotfix pydantic version

## [0.17.0] - 2024-06-14

### Added

- entrypoint `all-extractors`: run all extractors
- transform grippeweb resources
- wikidata aux extractor into seq-repo
- function `get_merged_organization_id_by_query_with_transform_and_load` to
  wikidata.extract module
- extract voxco data

### Changes

- update mex-common to 0.27.1
- move `mex.pipeline` documentation to `__init__` to have it in sphinx
- consolidate mocked drop connector into one general mock

### Removed

- remove unused organization_stable_target_id_by_query_sumo asset

### Fixed

- first test does not receive isolated settings but potentially production settings
- mex-drop api connector trailing slash in send request

## [0.16.0] - 2024-05-16

### Added

- add settings attributes `drop_api_key` and `drop_api_url`
- drop api connector for listing and loading files from the drop api
- add basic docker configuration with dockerfile, ignore and compose
- implement odk transform functions
- grippeweb extract and transform
- dagster schedules for non-default groups, configurable via setting `schedule`

### Changes

- update cruft template with new linters
- utilize new, more precise Identifier subclasses
- make pyodbc a soft dependency (only pipelines that use it may fail)
- switch from poetry to pdm
- move MSSQL Server authentication to general settings
- receive one or None organization from wikidata aux extractor
- adjust Timestamp usage to TemporalEntity
- move quotation marks (") filtering to mex-common from requested wikidata label

### Deprecated

- get seq-repo data via mex-drop connector (was: file)

### Removed

- remove sync-persons pipeline, stopgap mx-1572
- remove `public` as a valid sink option

### Fixed

- fix some docstring indents and typings
- ifsg extractor

## [0.15.0] - 2024-02-27

### Added

- configure open-code synchronization workflow
- add mapping connector and integrate into ifsg, seq-repo and sumo
- add odk extraction assets
- LDAP and Organigram integration for seq-repo

### Changes

- update cruft template to latest version
- update to pytest 8 and other minor/patch bumps

## [0.15.0] - 2024-01-31

### Added

- `CHANGELOG.md` documenting notable changes to this project
- a template for pull requests
- ifsg connector and entry point
- Transform seq-repo sources to ExtractedData models
- dependency: dagster-postgres
- documentation workflow to Makefile, mex.bat and as github action
- README.md for mesh data
- ifsg raw data extraction
- ifsg resource transformation
- add IFSG Variable and VariableGroup transformation
- add wikidata dagster assets
- integrate wikidata and organigram into the ifsg extractor

### Changes

- update dependencies
- split synopse extractor into multiple dagster assets
- handle new entityType attribute in merged and extracted models
- split confluence-vvt extractor into multiple dagster assets
- split-up workflow jobs
- harmonize boilerplate
- clean-up tests, raw-data and code for open-sourcing
- split sumo extractor into multiple dagster assets

### Fixed

- materialize only required assets from default asset group
- convert dagster-webserver to main dependency
- update variable filter according to mapping changes
- update resource_disease title according to mapping changes
- cover none values in data with different filtering
- fix valueset extraction

## [0.14.1] - 2023-12-20

First release in changelog
