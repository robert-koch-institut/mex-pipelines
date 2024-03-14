.PHONY: all test setup hooks install linter pytest wheel docs
all: install test
test: linter pytest

LATEST = $(shell git describe --tags $(shell git rev-list --tags --max-count=1))
PWD = $(shell pwd)

setup:
	# install meta requirements system-wide
	@ echo installing requirements; \
	python -m pip --quiet --disable-pip-version-check install --force-reinstall -r requirements.txt; \

hooks:
	# install pre-commit hooks when not in CI
	@ if [ -z "$$CI" ]; then \
		pre-commit install; \
	fi; \

install: setup hooks
	# install packages from lock file in local virtual environment
	@ echo installing package; \
	poetry install --no-interaction --sync; \

linter:
	# run the linter hooks from pre-commit on all files
	@ echo linting all files; \
	pre-commit run --all-files; \

pytest:
	# run the pytest test suite with all unit tests
	@ echo running unit tests; \
	poetry run pytest -m "not integration"; \

wheel:
	# build the python package
	@ echo building wheel; \
	poetry build --no-interaction --format wheel; \

image:
	# build the docker image
	@ echo building docker image mex-extractors:${LATEST}; \
	export DOCKER_BUILDKIT=1; \
	docker build \
		--tag rki/mex-extractors:${LATEST} \
		--tag rki/mex-extractors:latest .; \

docker: image
	# run the extractors using docker
	@ echo running docker container mex-extractors:${LATEST}; \
	mkdir --parents --mode 777 work; \
	docker run \
		--env MEX_WORK_DIR=/work \
		--volume ${PWD}/work:/work \
		rki/mex-extractors:${LATEST}; \

dagster: image
	# start dagster using docker compose
	@ echo running dagster for mex-extractors:${LATEST}; \
	export DOCKER_BUILDKIT=1; \
	export COMPOSE_DOCKER_CLI_BUILD=1; \
	docker compose up --remove-orphans; \

docs:
	# use sphinx to auto-generate html docs from code
	@ echo generating api docs; \
	poetry run sphinx-apidoc -f -o docs/source mex; \
	poetry run sphinx-build -aE -b dirhtml docs docs/dist; \
