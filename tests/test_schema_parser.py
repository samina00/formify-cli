"""Tests for the schema_parser module."""

import json
import pytest
from pathlib import Path

from formify_cli.schema_parser import (
    load_schema,
    validate_schema,
    SchemaValidationError,
)


VALID_SCHEMA = {
    "title": "Contact Form",
    "fields": [
        {"name": "full_name", "type": "text", "label": "Full Name", "required": True},
        {"name": "email", "type": "email", "label": "Email Address"},
        {
            "name": "country",
            "type": "select",
            "label": "Country",
            "options": ["USA", "Canada", "UK"],
        },
    ],
}


def test_validate_schema_passes_for_valid_schema():
    validate_schema(VALID_SCHEMA)


def test_validate_schema_raises_if_not_dict():
    with pytest.raises(SchemaValidationError, match="must be a JSON object"):
        validate_schema(["not", "a", "dict"])


def test_validate_schema_raises_if_fields_missing():
    with pytest.raises(SchemaValidationError, match="'fields' key"):
        validate_schema({"title": "No Fields"})


def test_validate_schema_raises_if_fields_empty():
    with pytest.raises(SchemaValidationError, match="non-empty list"):
        validate_schema({"fields": []})


def test_validate_schema_raises_for_missing_required_field_keys():
    schema = {"fields": [{"name": "age", "type": "number"}]}  # missing 'label'
    with pytest.raises(SchemaValidationError, match="missing required keys"):
        validate_schema(schema)


def test_validate_schema_raises_for_unsupported_type():
    schema = {"fields": [{"name": "dob", "type": "date", "label": "Date of Birth"}]}
    with pytest.raises(SchemaValidationError, match="unsupported type"):
        validate_schema(schema)


def test_validate_schema_raises_for_select_without_options():
    schema = {"fields": [{"name": "role", "type": "select", "label": "Role"}]}
    with pytest.raises(SchemaValidationError, match="must include 'options'"):
        validate_schema(schema)


def test_load_schema_raises_for_missing_file():
    with pytest.raises(FileNotFoundError):
        load_schema("nonexistent_schema.json")


def test_load_schema_raises_for_invalid_json(tmp_path: Path):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(SchemaValidationError, match="Invalid JSON"):
        load_schema(str(bad_file))


def test_load_schema_returns_parsed_dict(tmp_path: Path):
    schema_file = tmp_path / "form.json"
    schema_file.write_text(json.dumps(VALID_SCHEMA), encoding="utf-8")
    result = load_schema(str(schema_file))
    assert result["title"] == "Contact Form"
    assert len(result["fields"]) == 3
