"""Tests for formify_cli.preview_server."""

from __future__ import annotations

import urllib.request

import pytest

from formify_cli.preview_server import PreviewError, _make_handler, start_preview


MINIMAL_HTML = "<html><body><form><input></form></body></html>"


# ---------------------------------------------------------------------------
# _make_handler
# ---------------------------------------------------------------------------

def test_make_handler_stores_content():
    handler_cls = _make_handler(MINIMAL_HTML)
    assert handler_cls.html_content == MINIMAL_HTML.encode("utf-8")


def test_make_handler_different_instances_are_independent():
    h1 = _make_handler("<p>one</p>")
    h2 = _make_handler("<p>two</p>")
    assert h1.html_content != h2.html_content


# ---------------------------------------------------------------------------
# start_preview — error cases
# ---------------------------------------------------------------------------

def test_start_preview_raises_for_empty_html():
    with pytest.raises(PreviewError, match="empty"):
        start_preview("", block=False)


def test_start_preview_raises_for_whitespace_only_html():
    with pytest.raises(PreviewError, match="empty"):
        start_preview("   \n  ", block=False)


def test_start_preview_raises_on_port_conflict():
    """Binding twice to the same port should raise PreviewError."""
    server = start_preview(MINIMAL_HTML, port=19871, open_browser=False, block=False)
    assert server is not None
    try:
        with pytest.raises(PreviewError, match="port"):
            start_preview(MINIMAL_HTML, port=19871, open_browser=False, block=False)
    finally:
        server.shutdown()
        server.server_close()


# ---------------------------------------------------------------------------
# start_preview — happy path (non-blocking)
# ---------------------------------------------------------------------------

def test_start_preview_returns_server_object():
    server = start_preview(MINIMAL_HTML, port=19872, open_browser=False, block=False)
    assert server is not None
    server.shutdown()
    server.server_close()


def test_start_preview_serves_html_over_http():
    server = start_preview(MINIMAL_HTML, port=19873, open_browser=False, block=False)
    assert server is not None
    try:
        with urllib.request.urlopen("http://127.0.0.1:19873/") as resp:
            body = resp.read().decode("utf-8")
        assert "<form>" in body
    finally:
        server.shutdown()
        server.server_close()


def test_start_preview_content_type_header():
    server = start_preview(MINIMAL_HTML, port=19874, open_browser=False, block=False)
    assert server is not None
    try:
        with urllib.request.urlopen("http://127.0.0.1:19874/") as resp:
            content_type = resp.headers.get("Content-Type", "")
        assert "text/html" in content_type
    finally:
        server.shutdown()
        server.server_close()


def test_start_preview_serves_exact_html():
    html = "<html><body><h1>My Form</h1></body></html>"
    server = start_preview(html, port=19875, open_browser=False, block=False)
    assert server is not None
    try:
        with urllib.request.urlopen("http://127.0.0.1:19875/") as resp:
            body = resp.read().decode("utf-8")
        assert body == html
    finally:
        server.shutdown()
        server.server_close()
