# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- configure open-code synchronization workflow
- add mapping connector

### Changes

- update cruft template to latest version
- update to pytest 8 and other minor/patch bumps

### Deprecated

### Removed

### Fixed

### Security

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
- ifsg resource tranformation
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
