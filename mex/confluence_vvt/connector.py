from mex.common.connector import HTTPConnector
from mex.confluence_vvt.settings import ConfluenceVvtSettings


class ConfluenceVvtConnector(HTTPConnector):
    """Connector class to create a session for all requests to confluence-vvt."""

    def _set_url(self) -> None:
        """Set url of the host."""
        settings = ConfluenceVvtSettings.get()
        self.url = settings.url

    def _set_authentication(self) -> None:
        """Authenticate to the host."""
        settings = ConfluenceVvtSettings.get()
        self.session.auth = (
            settings.username.get_secret_value(),
            settings.password.get_secret_value(),
        )
