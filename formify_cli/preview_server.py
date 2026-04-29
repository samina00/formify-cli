"""Local preview server for generated HTML forms."""

from __future__ import annotations

import http.server
import os
import threading
import webbrowser
from pathlib import Path
from typing import Optional


class PreviewError(Exception):
    """Raised when the preview server encounters an error."""


class _SingleFileHandler(http.server.BaseHTTPRequestHandler):
    """Minimal HTTP handler that serves a single HTML file."""

    html_content: bytes = b""

    def do_GET(self) -> None:  # noqa: N802
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.html_content)))
        self.end_headers()
        self.wfile.write(self.html_content)

    def log_message(self, fmt: str, *args: object) -> None:  # pragma: no cover
        """Suppress default request logging."""


def _make_handler(html: str) -> type[_SingleFileHandler]:
    """Return a handler class pre-loaded with *html* content."""
    content = html.encode("utf-8")

    class Handler(_SingleFileHandler):
        html_content = content

    return Handler


def start_preview(
    html: str,
    port: int = 8080,
    open_browser: bool = True,
    *,
    block: bool = True,
) -> Optional[http.server.HTTPServer]:
    """Start a local HTTP server to preview *html*.

    Parameters
    ----------
    html:
        The rendered HTML string to serve.
    port:
        TCP port to listen on (default 8080).
    open_browser:
        If *True*, open the default web browser automatically.
    block:
        If *True* (default), block until the server is stopped with Ctrl-C.
        If *False*, start the server in a daemon thread and return the server
        object so tests can shut it down programmatically.
    """
    if not html or not html.strip():
        raise PreviewError("Cannot preview empty HTML content.")

    handler_cls = _make_handler(html)

    try:
        server = http.server.HTTPServer(("127.0.0.1", port), handler_cls)
    except OSError as exc:
        raise PreviewError(f"Could not bind to port {port}: {exc}") from exc

    url = f"http://127.0.0.1:{port}/"

    if open_browser:
        webbrowser.open(url)  # pragma: no cover

    if block:  # pragma: no cover
        print(f"Serving form preview at {url}  (Ctrl-C to stop)")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            server.server_close()
        return None

    # Non-blocking path used by tests / programmatic callers
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server
