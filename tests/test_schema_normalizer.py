"""Tests for formify_cli.schema_normalizer."""

import pytest

from formify_cli.schema_normalizer import (
    SchemaNormalizerError,
    normalize_field,
    normalize_schema,
    list_unknown_types,
)


# ---------------------------------------------------------------------------
# normalize_field
# ---------------------------------------------------------------------------

def test_normalize_field_fills_defaults():
    field = {"name": "email", "type": "email", "label": "Email"}
    result = normalize_field(field)
    assert result["required"] is False
    assert result["placeholder"] == ""
    assert result["help_text"] == ""
    assert result["options"] == []


def test_normalize_field_preserves_existing_values():
    field = {"name": "age", "type": "number", "label": "Age", "required": True, "placeholder": "25"}
    result = normalize_field(field)
    assert result["required"] is True
    assert result["placeholder"] == "25"


def test_normalize_field_lowercases_type():
    field = {"name": "q", "type": "TEXT", "label": "Q"}
    result = normalize_field(field)
    assert result["type"] == "text"


def test_normalize_field_strips_whitespace():
    field = {"name": "  user  ", "type": " text ", "label": " User "}
    result = normalize_field(field)
    assert result["name"] == "user"
    assert result["type"] == "text"
    assert result["label"] == "User"


def test_normalize_field_raises_for_non_dict():
    with pytest.raises(SchemaNormalizerError, match="must be a dict"):
        normalize_field("not a dict")


def test_normalize_field_raises_for_missing_name():
    with pytest.raises(SchemaNormalizerError, match="'name'"):
        normalize_field({"type": "text", "label": "X"})


def test_normalize_field_raises_for_missing_type():
    with pytest.raises(SchemaNormalizerError, match="'type'"):
        normalize_field({"name": "x", "label": "X"})


def test_normalize_field_raises_for_missing_label():
    with pytest.raises(SchemaNormalizerError, match="'label'"):
        normalize_field({"name": "x", "type": "text"})


def test_normalize_field_coerces_options_to_list_if_invalid():
    field = {"name": "x", "type": "select", "label": "X", "options": "bad"}
    result = normalize_field(field)
    assert result["options"] == []


# ---------------------------------------------------------------------------
# normalize_schema
# ---------------------------------------------------------------------------

def _simple_schema():
    return {
        "title": "Contact",
        "fields": [
            {"name": "name", "type": "text", "label": "Name"},
            {"name": "email", "type": "email", "label": "Email", "required": True},
        ],
    }


def test_normalize_schema_returns_dict():
    result = normalize_schema(_simple_schema())
    assert isinstance(result, dict)


def test_normalize_schema_preserves_title():
    result = normalize_schema(_simple_schema())
    assert result["title"] == "Contact"


def test_normalize_schema_defaults_title_to_empty_string():
    schema = {"fields": [{"name": "x", "type": "text", "label": "X"}]}
    result = normalize_schema(schema)
    assert result["title"] == ""


def test_normalize_schema_normalizes_all_fields():
    result = normalize_schema(_simple_schema())
    for field in result["fields"]:
        assert "required" in field
        assert "placeholder" in field


def test_normalize_schema_raises_for_non_dict():
    with pytest.raises(SchemaNormalizerError, match="must be a dict"):
        normalize_schema(["not", "a", "dict"])


def test_normalize_schema_raises_for_missing_fields():
    with pytest.raises(SchemaNormalizerError, match="'fields'"):
        normalize_schema({"title": "Oops"})


def test_normalize_schema_raises_for_empty_fields():
    with pytest.raises(SchemaNormalizerError, match="non-empty list"):
        normalize_schema({"title": "T", "fields": []})


# ---------------------------------------------------------------------------
# list_unknown_types
# ---------------------------------------------------------------------------

def test_list_unknown_types_empty_for_known_types():
    result = list_unknown_types(_simple_schema())
    assert result == []


def test_list_unknown_types_returns_unknown():
    schema = {
        "title": "T",
        "fields": [
            {"name": "x", "type": "WIDGET", "label": "X"},
            {"name": "y", "type": "text", "label": "Y"},
        ],
    }
    result = list_unknown_types(schema)
    assert result == ["x"]
