"""Tests for formify_cli.schema_annotator."""

import pytest

from formify_cli.schema_annotator import (
    SchemaAnnotatorError,
    annotate_field,
    annotate_schema_field,
    list_annotated_fields,
    strip_annotations,
)


@pytest.fixture()
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "age", "type": "number", "label": "Age"},
        ],
    }


# --- annotate_field ---

def test_annotate_field_adds_hint():
    field = {"name": "email", "type": "email"}
    result = annotate_field(field, hint="Enter your email")
    assert result["hint"] == "Enter your email"


def test_annotate_field_adds_example():
    field = {"name": "email", "type": "email"}
    result = annotate_field(field, example="user@example.com")
    assert result["example"] == "user@example.com"


def test_annotate_field_adds_description():
    field = {"name": "age", "type": "number"}
    result = annotate_field(field, description="Your current age")
    assert result["description"] == "Your current age"


def test_annotate_field_does_not_mutate_original():
    field = {"name": "email", "type": "email"}
    annotate_field(field, hint="hint")
    assert "hint" not in field


def test_annotate_field_raises_for_non_dict():
    with pytest.raises(SchemaAnnotatorError, match="Field must be a dict"):
        annotate_field(["not", "a", "dict"], hint="x")


def test_annotate_field_skips_none_values():
    field = {"name": "x", "type": "text"}
    result = annotate_field(field)
    assert "hint" not in result
    assert "example" not in result
    assert "description" not in result


# --- annotate_schema_field ---

def test_annotate_schema_field_updates_correct_field(simple_schema):
    result = annotate_schema_field(simple_schema, "email", hint="Your email")
    email_field = next(f for f in result["fields"] if f["name"] == "email")
    assert email_field["hint"] == "Your email"


def test_annotate_schema_field_does_not_affect_other_fields(simple_schema):
    result = annotate_schema_field(simple_schema, "email", hint="hint")
    age_field = next(f for f in result["fields"] if f["name"] == "age")
    assert "hint" not in age_field


def test_annotate_schema_field_raises_for_unknown_field(simple_schema):
    with pytest.raises(SchemaAnnotatorError, match="not found"):
        annotate_schema_field(simple_schema, "nonexistent", hint="x")


def test_annotate_schema_field_raises_for_non_dict():
    with pytest.raises(SchemaAnnotatorError):
        annotate_schema_field(["bad"], "email", hint="x")


def test_annotate_schema_field_raises_for_missing_fields_key():
    with pytest.raises(SchemaAnnotatorError):
        annotate_schema_field({"title": "No fields"}, "email", hint="x")


# --- strip_annotations ---

def test_strip_annotations_removes_hint():
    schema = {"title": "T", "fields": [{"name": "x", "type": "text", "hint": "h"}]}
    result = strip_annotations(schema)
    assert "hint" not in result["fields"][0]


def test_strip_annotations_removes_all_annotation_keys():
    schema = {
        "title": "T",
        "fields": [{"name": "x", "type": "text", "hint": "h", "example": "e", "description": "d"}],
    }
    result = strip_annotations(schema)
    field = result["fields"][0]
    assert "hint" not in field
    assert "example" not in field
    assert "description" not in field


def test_strip_annotations_preserves_other_keys():
    schema = {"title": "T", "fields": [{"name": "x", "type": "text", "hint": "h"}]}
    result = strip_annotations(schema)
    assert result["fields"][0]["name"] == "x"
    assert result["fields"][0]["type"] == "text"


def test_strip_annotations_does_not_mutate_original():
    schema = {"title": "T", "fields": [{"name": "x", "type": "text", "hint": "h"}]}
    strip_annotations(schema)
    assert schema["fields"][0]["hint"] == "h"


# --- list_annotated_fields ---

def test_list_annotated_fields_returns_names_with_annotations():
    schema = {
        "title": "T",
        "fields": [
            {"name": "a", "type": "text", "hint": "h"},
            {"name": "b", "type": "text"},
        ],
    }
    assert list_annotated_fields(schema) == ["a"]


def test_list_annotated_fields_returns_empty_when_none_annotated(simple_schema):
    assert list_annotated_fields(simple_schema) == []


def test_list_annotated_fields_raises_for_non_dict():
    with pytest.raises(SchemaAnnotatorError):
        list_annotated_fields("not a dict")
