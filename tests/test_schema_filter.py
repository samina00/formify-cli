"""Tests for formify_cli.schema_filter."""

import pytest

from formify_cli.schema_filter import (
    SchemaFilterError,
    exclude_fields,
    filter_by_name_prefix,
    filter_by_required,
    filter_by_type,
    keep_fields,
)


@pytest.fixture()
def schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "first_name", "type": "text", "label": "First Name", "required": True},
            {"name": "last_name", "type": "text", "label": "Last Name", "required": False},
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "age", "type": "number", "label": "Age", "required": False},
            {"name": "bio", "type": "textarea", "label": "Bio", "required": False},
        ],
    }


# --- filter_by_required ---

def test_filter_by_required_returns_required_fields(schema):
    result = filter_by_required(schema, required=True)
    assert all(f["required"] for f in result)
    assert {f["name"] for f in result} == {"first_name", "email"}


def test_filter_by_required_returns_optional_fields(schema):
    result = filter_by_required(schema, required=False)
    assert {f["name"] for f in result} == {"last_name", "age", "bio"}


def test_filter_by_required_raises_for_non_dict():
    with pytest.raises(SchemaFilterError, match="must be a dict"):
        filter_by_required(["not", "a", "dict"])


def test_filter_by_required_raises_for_missing_fields_key():
    with pytest.raises(SchemaFilterError, match="'fields' key"):
        filter_by_required({"title": "No fields"})


# --- filter_by_type ---

def test_filter_by_type_returns_matching_fields(schema):
    result = filter_by_type(schema, "text")
    assert {f["name"] for f in result} == {"first_name", "last_name"}


def test_filter_by_type_is_case_insensitive(schema):
    result = filter_by_type(schema, "EMAIL")
    assert len(result) == 1
    assert result[0]["name"] == "email"


def test_filter_by_type_returns_empty_for_no_match(schema):
    assert filter_by_type(schema, "select") == []


def test_filter_by_type_raises_for_empty_type(schema):
    with pytest.raises(SchemaFilterError, match="non-empty string"):
        filter_by_type(schema, "   ")


# --- filter_by_name_prefix ---

def test_filter_by_name_prefix_returns_matching(schema):
    result = filter_by_name_prefix(schema, "first")
    assert len(result) == 1
    assert result[0]["name"] == "first_name"


def test_filter_by_name_prefix_multiple_matches(schema):
    result = filter_by_name_prefix(schema, "")
    # empty prefix matches nothing — raises


def test_filter_by_name_prefix_raises_for_empty_prefix(schema):
    with pytest.raises(SchemaFilterError, match="non-empty string"):
        filter_by_name_prefix(schema, "")


# --- exclude_fields ---

def test_exclude_fields_removes_named_fields(schema):
    result = exclude_fields(schema, ["email", "age"])
    names = [f["name"] for f in result["fields"]]
    assert "email" not in names
    assert "age" not in names
    assert len(names) == 3


def test_exclude_fields_returns_copy(schema):
    result = exclude_fields(schema, ["bio"])
    assert result is not schema
    assert len(schema["fields"]) == 5  # original unchanged


def test_exclude_fields_raises_for_non_list(schema):
    with pytest.raises(SchemaFilterError, match="list of strings"):
        exclude_fields(schema, "email")


# --- keep_fields ---

def test_keep_fields_retains_only_named(schema):
    result = keep_fields(schema, ["email", "bio"])
    names = [f["name"] for f in result["fields"]]
    assert names == ["email", "bio"]


def test_keep_fields_preserves_title(schema):
    result = keep_fields(schema, ["age"])
    assert result["title"] == "Test Form"


def test_keep_fields_raises_for_non_list(schema):
    with pytest.raises(SchemaFilterError, match="list of strings"):
        keep_fields(schema, "age")
