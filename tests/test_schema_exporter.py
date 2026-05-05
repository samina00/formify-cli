"""Tests for formify_cli.schema_exporter."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from formify_cli.schema_exporter import (
    SchemaExportError,
    export_schema,
    export_schema_as_json,
    export_schema_as_markdown,
    export_schema_as_summary,
    export_schema_to_file,
    list_export_formats,
)


@pytest.fixture()
def simple_schema() -> dict:
    return {
        "title": "Contact",
        "fields": [
            {"name": "name", "type": "text", "label": "Your Name", "required": True},
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "message", "type": "textarea", "label": "Message", "required": False},
        ],
    }


def test_list_export_formats_returns_sorted_list():
    formats = list_export_formats()
    assert isinstance(formats, list)
    assert formats == sorted(formats)


def test_list_export_formats_contains_builtins():
    formats = list_export_formats()
    assert "json" in formats
    assert "markdown" in formats
    assert "summary" in formats


def test_export_as_json_is_valid_json(simple_schema):
    result = export_schema_as_json(simple_schema)
    parsed = json.loads(result)
    assert parsed["title"] == "Contact"


def test_export_as_json_raises_for_non_dict():
    with pytest.raises(SchemaExportError):
        export_schema_as_json(["not", "a", "dict"])  # type: ignore[arg-type]


def test_export_as_markdown_contains_title(simple_schema):
    result = export_schema_as_markdown(simple_schema)
    assert "# Contact" in result


def test_export_as_markdown_contains_field_names(simple_schema):
    result = export_schema_as_markdown(simple_schema)
    assert "name" in result
    assert "email" in result


def test_export_as_markdown_shows_required_yes(simple_schema):
    result = export_schema_as_markdown(simple_schema)
    assert "Yes" in result


def test_export_as_markdown_raises_for_non_dict():
    with pytest.raises(SchemaExportError):
        export_schema_as_markdown("bad")  # type: ignore[arg-type]


def test_export_as_summary_shows_field_count(simple_schema):
    result = export_schema_as_summary(simple_schema)
    assert "Fields: 3" in result


def test_export_as_summary_shows_required_count(simple_schema):
    result = export_schema_as_summary(simple_schema)
    assert "Required: 2" in result


def test_export_schema_dispatches_json(simple_schema):
    result = export_schema(simple_schema, "json")
    assert json.loads(result)["title"] == "Contact"


def test_export_schema_dispatches_markdown(simple_schema):
    result = export_schema(simple_schema, "markdown")
    assert "##" in result


def test_export_schema_dispatches_summary(simple_schema):
    result = export_schema(simple_schema, "summary")
    assert "Form:" in result


def test_export_schema_case_insensitive(simple_schema):
    result = export_schema(simple_schema, "JSON")
    assert json.loads(result)


def test_export_schema_raises_for_unknown_format(simple_schema):
    with pytest.raises(SchemaExportError, match="Unknown export format"):
        export_schema(simple_schema, "xml")


def test_export_to_file_creates_file(simple_schema, tmp_path):
    dest = tmp_path / "out" / "schema.md"
    result = export_schema_to_file(simple_schema, "markdown", dest)
    assert result.exists()
    assert "Contact" in result.read_text()


def test_export_to_file_raises_if_exists_no_overwrite(simple_schema, tmp_path):
    dest = tmp_path / "schema.json"
    dest.write_text("{}")
    with pytest.raises(SchemaExportError, match="already exists"):
        export_schema_to_file(simple_schema, "json", dest, overwrite=False)


def test_export_to_file_overwrites_when_flag_set(simple_schema, tmp_path):
    dest = tmp_path / "schema.json"
    dest.write_text("{}")
    export_schema_to_file(simple_schema, "json", dest, overwrite=True)
    assert json.loads(dest.read_text())["title"] == "Contact"
