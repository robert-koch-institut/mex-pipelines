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


@pytest.mark.integration
def test_get_file() -> None:
    connector = DropApiConnector.get()
    content = connector.get_file("test", "default")
    assert content == {"foo": "bar", "list": [1, 2, "foo"], "nested": {"foo": "bar"}}


def test_get_file_mocked(monkeypatch: MonkeyPatch) -> None:
    mocked_send_request = MagicMock(
        spec=DropApiConnector._send_request,
        return_value=Mock(json=MagicMock(return_value={"foo": "bar"})),
    )
    monkeypatch.setattr(DropApiConnector, "_send_request", mocked_send_request)
    connector = DropApiConnector.get()
    content = connector.get_file("test", "default")
    assert content == {"foo": "bar"}
