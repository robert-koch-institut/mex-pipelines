# MEx extractors

ETL pipelines for the RKI Metadata Exchange.

[![cookiecutter](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/cookiecutter.yml/badge.svg)](https://github.com/robert-koch-institut/mex-template)
[![cve-scan](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/cve-scan.yml/badge.svg)](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/cve-scan.yml)
[![documentation](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/documentation.yml/badge.svg)](https://robert-koch-institut.github.io/mex-extractors)
[![linting](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/linting.yml/badge.svg)](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/linting.yml)
[![open-code](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/open-code.yml/badge.svg)](https://gitlab.opencode.de/robert-koch-institut/mex/mex-extractors)
[![testing](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/testing.yml/badge.svg)](https://github.com/robert-koch-institut/mex-extractors/actions/workflows/testing.yml)

## project

The Metadata Exchange (MEx) project is committed to improve the retrieval of RKI
research data and projects. How? By focusing on metadata: instead of providing the
actual research data directly, the MEx metadata catalog captures descriptive information
about research data and activities. On this basis, we want to make the data FAIR[^1] so
that it can be shared with others.

Via MEx, metadata will be made findable, accessible and shareable, as well as available
for further research. The goal is to get an overview of what research data is available,
understand its context, and know what needs to be considered for subsequent use.

RKI cooperated with D4L data4life gGmbH for a pilot phase where the vision of a
FAIR metadata catalog was explored and concepts and prototypes were developed.
The partnership has ended with the successful conclusion of the pilot phase.

After an internal launch, the metadata will also be made publicly available and thus be
available to external researchers as well as the interested (professional) public to
find research data from the RKI.

For further details, please consult our
[project page](https://www.rki.de/DE/Content/Forsch/MEx/MEx_node.html).

[^1]: FAIR is referencing the so-called
[FAIR data principles](https://www.go-fair.org/fair-principles/) – guidelines to make
data Findable, Accessible, Interoperable and Reusable.

## package

The `mex-extractors` package implements a variety of ETL pipelines to **extract**
metadata from primary data sources using a range of different technologies and
protocols. Then, we **transform** the metadata into a standardized format using models
provided by `mex-common`. The last step in this process is to **load** the harmonized
metadata into a sink (file output, API upload, etc).

## license

This package is licensed under the [MIT license](/LICENSE). All other software
components of the MEx project are open-sourced under the same license as well.

## development

### installation

- on unix, consider using pyenv https://github.com/pyenv/pyenv
  - get pyenv `curl https://pyenv.run | bash`
  - install 3.11 `pyenv install 3.11`
  - switch version `pyenv global 3.11`
  - run `make install`
- on windows, consider using pyenv-win https://pyenv-win.github.io/pyenv-win/
  - follow https://pyenv-win.github.io/pyenv-win/#quick-start
  - install 3.11 `pyenv install 3.11`
  - switch version `pyenv global 3.11`
  - run `.\mex.bat install`

### linting and testing

- run all linters with `pdm lint`
- run only unit tests with `pdm unit`
- run unit and integration tests with `pdm test`

### updating dependencies

- update boilerplate files with `cruft update`
- update global requirements in `requirements.txt` manually
- update git hooks with `pre-commit autoupdate`
- update package dependencies using `pdm update-all`
- update github actions in `.github/workflows/*.yml` manually

### creating release

- run `pdm release RULE` to release a new version where RULE determines which part of
  the version to update and is one of `major`, `minor`, `patch`.

### container workflow

- build image with `make image`
- run directly using docker `make run`
- start with docker compose `make start`

## commands

- run `pdm run {command} --help` to print instructions
- run `pdm run {command} --debug` for interactive debugging

### dagster

- `pdm run dagster dev` to launch a local dagster UI

### all extractors

- `pdm run all-extractors` executes all extractors
- execute only in local or dev environment

### artificial extractor

- `pdm run artificial` creates deterministic artificial sample data
- execute only in local or dev environment

### biospecimen extractor

- `pdm run biospecimen` extracts sources from the Biospecimen excel files
- based on biospecimen to MEx mapping commit e629af3

### blueant extractor

- `pdm run blueant` extracts sources from the Blue Ant project management software
- based on blueant to MEx mapping commit e629af3

### confluence-vvt extractor

- `pdm run confluence-vvt` extracts sources from the VVT confluence page
- based on confluence-vvt to MEx mapping commit bbaf91e

### datscha-web extractor

- `pdm run datscha-web` extracts sources from the datscha web app
- based on datscha-web to MEx mapping commit e629af3

### ff-projects extractor

- `pdm run ff-projects` extracts sources from the FF Projects excel file
- based on ff-projects to MEx mapping commit a913b9e

### ifsg extractor

- `pdm run ifsg` extracts sources from the ifsg data base
- based on ifsg to MEx mapping commit f0e54cd

### international-projects extractor

- `pdm run international-projects` extracts sources from the international projects excel
- based on international-projects to MEx mapping version a913b9e

### grippeweb extractor

- `pdm run grippeweb` extracts grippeweb metadata from grippeweb database
- based on grippeweb to MEx mapping commit eb88773

### odk extractor

- `pdm run odk` extracts ODK survey data from excel files
- based on odk to MEx mapping commit 6696577

### organigram extractor

- `pdm run organigram` extracts organizational units from JSON file
- based on organigram to MEx mapping commit a913b9e

### rdmo extractor

- `pdm run rdmo` extracts sources from RDMO using its REST API
- based on rdmo to MEx mapping commit e629af3

### seq-repo extractor

- `pdm run seq-repo` extracts sources from seq-repo JSON file
- based on seq-repo to MEx mapping commit f2814f9

### sumo extractor

- `pdm run sumo` extract sumo data from xlsx files
- based on sumo to MEx mapping commit f5e2b5f

### synopse extractor

- `pdm run synopse` extracts synopse data from report-server exports
- based on synopse to MEx mapping commit 6472329
