"""Tests for formify_cli.form_builder."""

from __future__ import annotations

import json
import pathlib

import pytest

from formify_cli.form_builder import build_form, FormBuilderError


MINIMAL_SCHEMA = {
    "title": "Sign Up",
    "fields": [
        {"name": "username", "type": "text", "label": "Username", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
    ],
}


@pytest.fixture()
def schema_file(tmp_path: pathlib.Path) -> str:
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(MINIMAL_SCHEMA))
    return str(p)


@pytest.fixture()
def bad_schema_file(tmp_path: pathlib.Path) -> str:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"title": "Oops"}))
    return str(p)


def test_build_form_returns_html_string(schema_file: str) -> None:
    html = build_form(schema_file)
    assert isinstance(html, str)
    assert "<form" in html


def test_build_form_contains_title(schema_file: str) -> None:
    html = build_form(schema_file)
    assert "Sign Up" in html


def test_build_form_contains_field_labels(schema_file: str) -> None:
    html = build_form(schema_file)
    assert "Username" in html
    assert "Email" in html


def test_build_form_raises_for_missing_file() -> None:
    with pytest.raises(FormBuilderError, match="Cannot load schema"):
        build_form("/nonexistent/path/schema.json")


def test_build_form_raises_for_invalid_schema(bad_schema_file: str) -> None:
    with pytest.raises(FormBuilderError, match="Invalid schema"):
        build_form(bad_schema_file)


def test_build_form_with_valid_theme(schema_file: str) -> None:
    html = build_form(schema_file, theme_name="default")
    assert "<form" in html


def test_build_form_with_theme_includes_css_link(schema_file: str) -> None:
    html = build_form(schema_file, theme_name="default", include_css_link=True)
    assert "<link" in html


def test_build_form_with_theme_no_css_link(schema_file: str) -> None:
    html = build_form(schema_file, theme_name="default", include_css_link=False)
    assert "<link" not in html


def test_build_form_raises_for_unknown_theme(schema_file: str) -> None:
    with pytest.raises(FormBuilderError):
        build_form(schema_file, theme_name="nonexistent_theme_xyz")


def test_build_form_extra_attrs_forwarded(schema_file: str) -> None:
    html = build_form(schema_file, extra_attrs={"data-testid": "my-form"})
    assert "data-testid" in html
