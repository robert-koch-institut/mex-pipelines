import pathlib
from typing import Any

import pytest
from pytest import MonkeyPatch

from mex.common.backend_api.connector import BackendApiConnector
from mex.common.backend_api.models import MergedItemsResponse
from mex.common.models import (
    MergedConsent,
    MergedContactPoint,
    MergedItem,
    MergedPrimarySource,
)


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
                    email=["1fake@e.mail"],
                    entityType="MergedContactPoint",
                    identifier="alsofakefakefakeJA",
                ),
                MergedConsent(
                    entityType="MergedConsent",
                    identifier="anotherfakefakefakefak",
                    hasConsentStatus="https://mex.rki.de/item/consent-status-1",
                    hasDataSubject="fakefakefakefakefakefa",
                    isIndicatedAtTime="2014-05-21T19:38:51Z",
                ),
                MergedContactPoint(
                    email=["2fake@e.mail"],
                    entityType="MergedContactPoint",
                    identifier="alsofakefakefakeYO",
                ),
            ],
        )

    monkeypatch.setattr(BackendApiConnector, "request", mocked_request)


@pytest.fixture(scope="session")
def ndjson_path(tmp_path_factory) -> pathlib.Path:
    return tmp_path_factory.mktemp("test") / "publisher.ndjson"
