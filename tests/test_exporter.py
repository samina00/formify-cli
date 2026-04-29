"""Tests for formify_cli.exporter module."""

import pytest
from pathlib import Path

from formify_cli.exporter import (
    ExportError,
    export_html,
    export_to_stdout,
    get_output_path,
)

SAMPLE_HTML = "<html><body><form></form></body></html>"


def test_export_html_creates_file(tmp_path):
    out = tmp_path / "form.html"
    result = export_html(SAMPLE_HTML, str(out))
    assert result == out.resolve()
    assert out.read_text(encoding="utf-8") == SAMPLE_HTML


def test_export_html_creates_parent_dirs(tmp_path):
    out = tmp_path / "nested" / "deep" / "form.html"
    export_html(SAMPLE_HTML, str(out))
    assert out.exists()


def test_export_html_raises_if_file_exists_no_overwrite(tmp_path):
    out = tmp_path / "form.html"
    out.write_text("old content", encoding="utf-8")
    with pytest.raises(ExportError, match="already exists"):
        export_html(SAMPLE_HTML, str(out), overwrite=False)


def test_export_html_overwrites_when_flag_set(tmp_path):
    out = tmp_path / "form.html"
    out.write_text("old content", encoding="utf-8")
    export_html(SAMPLE_HTML, str(out), overwrite=True)
    assert out.read_text(encoding="utf-8") == SAMPLE_HTML


def test_export_html_raises_for_empty_content(tmp_path):
    out = tmp_path / "form.html"
    with pytest.raises(ExportError, match="empty"):
        export_html("", str(out))


def test_export_html_raises_for_whitespace_only_content(tmp_path):
    out = tmp_path / "form.html"
    with pytest.raises(ExportError, match="empty"):
        export_html("   \n  ", str(out))


def test_export_to_stdout_prints(capsys):
    export_to_stdout(SAMPLE_HTML)
    captured = capsys.readouterr()
    assert SAMPLE_HTML in captured.out


def test_export_to_stdout_raises_for_empty():
    with pytest.raises(ExportError, match="empty"):
        export_to_stdout("")


def test_get_output_path_default_dir():
    result = get_output_path("examples/contact_form.json")
    assert result == Path(".") / "contact_form.html"


def test_get_output_path_custom_dir():
    result = get_output_path("schemas/signup.json", output_dir="dist")
    assert result == Path("dist") / "signup.html"


def test_get_output_path_returns_path_object():
    result = get_output_path("form.json")
    assert isinstance(result, Path)
