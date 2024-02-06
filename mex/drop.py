from typing import cast
from urllib.parse import urljoin

from mex.common.connector import HTTPConnector
from mex.settings import Settings


class DropApiConnector(HTTPConnector):
    """Connector class to handle interaction with the Drop API."""

    API_VERSION = "v0"

    def _check_availability(self) -> None:
        """Send a GET request to verify the API is available."""
        self.request("GET", "../_system/check")

    def _set_authentication(self) -> None:
        """Set the drop API key to all session headers."""
        settings = Settings.get()
        self.session.headers["X-API-Key"] = settings.drop_api_key.get_secret_value()

    def _set_url(self) -> None:
        """Set the drop api url with the version path."""
        settings = Settings.get()
        self.url = urljoin(str(settings.drop_api_url), self.API_VERSION)

    def list_files(self, x_system: str) -> list[str]:
        """Get available files for the x_system."""
        return cast(
            list[str],
            self.request(
                method="GET",
                endpoint=f"/{x_system}/",
            ),
        )
