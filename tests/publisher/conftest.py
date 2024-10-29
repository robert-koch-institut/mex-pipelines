import pathlib
from typing import Any

import pytest
from pytest import MonkeyPatch

from mex.common.backend_api.connector import BackendApiConnector
from mex.common.backend_api.models import MergedItemsResponse
from mex.common.models import MergedContactPoint, MergedItem, MergedPrimarySource


@pytest.fixture
def mocked_backend(monkeypatch: MonkeyPatch) -> None:
    def mocked_request(
        self: BackendApiConnector,
        method: str,
        endpoint: str | None = None,
        payload: Any = None,
        params: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> MergedItem:
        return MergedItemsResponse(
            total=1,
            items=[
                MergedPrimarySource(
                    entityType="MergedPrimarySource", identifier="fakefakefakeJA"
                ),
                MergedContactPoint(
                    email=["fake@e.mail"],
                    entityType="MergedContactPoint",
                    identifier="alsofakefakefakeJA",
                ),
            ],
        )

    monkeypatch.setattr(BackendApiConnector, "request", mocked_request)


@pytest.fixture(scope="session")
def ndjson_path(tmp_path_factory) -> pathlib.Path:
    return tmp_path_factory.mktemp("test") / "publisher.ndjson"
