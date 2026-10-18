"""Serves the companion site on the local machine."""

import functools
import http.server
from pathlib import Path


class SiteServer:
    """Serves the site folder on 127.0.0.1.

    Attributes:
        port: The port to listen on.
    """

    def __init__(self, port: int = 8765):
        """Sets the port.

        Args:
            port (int): The port.
        """
        self.port = port

    def run(self) -> None:
        """Serves until interrupted."""
        folder = Path(__file__).parent / 'site'
        handler = functools.partial(
            http.server.SimpleHTTPRequestHandler,
            directory=str(folder),
        )
        server = http.server.ThreadingHTTPServer(
            ('127.0.0.1', self.port), handler
        )
        print(f'http://127.0.0.1:{self.port}')
        server.serve_forever()


def main() -> None:
    """Starts the server."""
    SiteServer().run()
