from unittest.mock import MagicMock, Mock

import pytest
from pytest import MonkeyPatch

from mex.drop import DropApiConnector


@pytest.mark.integration
def test_list_files() -> None:
    connector = DropApiConnector.get()
    files = connector.list_files("test")
    assert files == ["default"]


def test_list_files_mocked(monkeypatch: MonkeyPatch) -> None:
    mocked_send_request = MagicMock(
        spec=DropApiConnector._send_request,
        return_value=Mock(json=MagicMock(return_value=["default"])),
    )
    monkeypatch.setattr(DropApiConnector, "_send_request", mocked_send_request)
    connector = DropApiConnector.get()
    files = connector.list_files("test")
    assert files == ["default"]
