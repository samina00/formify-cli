"""Tests for formify_cli.schema_trimmer."""

import pytest

from formify_cli.schema_trimmer import (
    SchemaTrimmerError,
    trim_empty_labels,
    trim_unknown_types,
    trim_keys,
    trim_schema,
)


@pytest.fixture
def base_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "name", "type": "text", "label": "Name", "required": False},
            {"name": "ghost", "type": "text", "label": ""},
            {"name": "weird", "type": "fancywidget", "label": "Weird"},
        ],
    }


def test_trim_empty_labels_removes_blank_label(base_schema):
    result = trim_empty_labels(base_schema)
    names = [f["name"] for f in result["fields"]]
    assert "ghost" not in names


def test_trim_empty_labels_keeps_valid_labels(base_schema):
    result = trim_empty_labels(base_schema)
    names = [f["name"] for f in result["fields"]]
    assert "email" in names
    assert "name" in names


def test_trim_empty_labels_does_not_mutate_original(base_schema):
    original_len = len(base_schema["fields"])
    trim_empty_labels(base_schema)
    assert len(base_schema["fields"]) == original_len


def test_trim_empty_labels_raises_for_non_dict():
    with pytest.raises(SchemaTrimmerError, match="must be a dict"):
        trim_empty_labels(["not", "a", "dict"])


def test_trim_empty_labels_raises_for_missing_fields_key():
    with pytest.raises(SchemaTrimmerError, match="'fields' key"):
        trim_empty_labels({"title": "No fields here"})


def test_trim_unknown_types_removes_unknown(base_schema):
    result = trim_unknown_types(base_schema)
    names = [f["name"] for f in result["fields"]]
    assert "weird" not in names


def test_trim_unknown_types_keeps_known(base_schema):
    result = trim_unknown_types(base_schema)
    names = [f["name"] for f in result["fields"]]
    assert "email" in names
    assert "name" in names


def test_trim_unknown_types_custom_known_types():
    schema = {
        "title": "T",
        "fields": [
            {"name": "a", "type": "custom", "label": "A"},
            {"name": "b", "type": "text", "label": "B"},
        ],
    }
    result = trim_unknown_types(schema, known_types=["custom"])
    names = [f["name"] for f in result["fields"]]
    assert "a" in names
    assert "b" not in names


def test_trim_unknown_types_is_case_insensitive():
    schema = {
        "title": "T",
        "fields": [{"name": "x", "type": "EMAIL", "label": "X"}],
    }
    result = trim_unknown_types(schema)
    assert len(result["fields"]) == 1


def test_trim_keys_removes_unknown_keys():
    schema = {
        "title": "T",
        "fields": [{"name": "x", "type": "text", "label": "X", "_internal": True}],
    }
    result = trim_keys(schema)
    assert "_internal" not in result["fields"][0]


def test_trim_keys_keeps_allowed_keys():
    schema = {
        "title": "T",
        "fields": [{"name": "x", "type": "text", "label": "X", "required": True}],
    }
    result = trim_keys(schema)
    field = result["fields"][0]
    assert "name" in field and "type" in field and "required" in field


def test_trim_schema_applies_all_passes(base_schema):
    result = trim_schema(base_schema)
    names = [f["name"] for f in result["fields"]]
    assert "ghost" not in names
    assert "weird" not in names
    assert "email" in names


def test_trim_schema_preserves_title(base_schema):
    result = trim_schema(base_schema)
    assert result["title"] == "Test Form"
