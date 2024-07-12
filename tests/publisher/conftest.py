import pathlib
from typing import Any

import pytest
from pytest import MonkeyPatch

from mex.common.backend_api.connector import BackendApiConnector


@pytest.fixture
def mocked_backend(monkeypatch: MonkeyPatch) -> None:
    def mocked_request(
        self: BackendApiConnector,
        method: str,
        endpoint: str | None = None,
        payload: Any = None,
        params: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        return {
            "total": 1,
            "items": [{"Test": 1, "AnotherTest": 2}, {"bla": "blub", "foo": "bar"}],
        }

    monkeypatch.setattr(BackendApiConnector, "request", mocked_request)


@pytest.fixture(scope="session")
def ndjson_path(tmp_path_factory) -> pathlib.Path:
    return tmp_path_factory.mktemp("test") / "publisher.ndjson"
