"""Tests for formify_cli.schema_flattener."""

import pytest

from formify_cli.schema_flattener import (
    SchemaFlattenerError,
    flatten_schema,
    list_field_names,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def simple_schema():
    return {
        "title": "Flat Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "age", "type": "number", "label": "Age"},
        ],
    }


@pytest.fixture()
def grouped_schema():
    return {
        "title": "Grouped Form",
        "fields": [
            {"name": "username", "type": "text", "label": "Username"},
            {
                "name": "address",
                "type": "group",
                "fields": [
                    {"name": "street", "type": "text", "label": "Street"},
                    {"name": "city", "type": "text", "label": "City"},
                ],
            },
        ],
    }


# ---------------------------------------------------------------------------
# flatten_schema
# ---------------------------------------------------------------------------

def test_flatten_schema_raises_for_non_dict():
    with pytest.raises(SchemaFlattenerError, match="must be a dict"):
        flatten_schema(["not", "a", "dict"])


def test_flatten_schema_raises_for_missing_fields_key():
    with pytest.raises(SchemaFlattenerError, match="'fields' key"):
        flatten_schema({"title": "No fields"})


def test_flatten_schema_raises_for_empty_separator():
    with pytest.raises(SchemaFlattenerError, match="Separator"):
        flatten_schema({"title": "X", "fields": []}, separator="")


def test_flatten_schema_passthrough_for_flat_schema(simple_schema):
    result = flatten_schema(simple_schema)
    assert len(result["fields"]) == 2
    assert result["fields"][0]["name"] == "email"


def test_flatten_schema_expands_group(grouped_schema):
    result = flatten_schema(grouped_schema)
    names = [f["name"] for f in result["fields"]]
    assert "username" in names
    assert "address_street" in names
    assert "address_city" in names
    assert "address" not in names


def test_flatten_schema_no_group_type_remains(grouped_schema):
    result = flatten_schema(grouped_schema)
    types = [f["type"] for f in result["fields"]]
    assert "group" not in types


def test_flatten_schema_returns_independent_copy(simple_schema):
    result = flatten_schema(simple_schema)
    result["fields"][0]["name"] = "mutated"
    assert simple_schema["fields"][0]["name"] == "email"


def test_flatten_schema_custom_separator(grouped_schema):
    result = flatten_schema(grouped_schema, separator=".")
    names = [f["name"] for f in result["fields"]]
    assert "address.street" in names
    assert "address.city" in names


def test_flatten_schema_raises_for_malformed_group():
    bad = {
        "title": "Bad",
        "fields": [{"name": "grp", "type": "group", "fields": []}],
    }
    with pytest.raises(SchemaFlattenerError, match="non-empty 'fields' list"):
        flatten_schema(bad)


def test_flatten_schema_preserves_title(grouped_schema):
    result = flatten_schema(grouped_schema)
    assert result["title"] == "Grouped Form"


# ---------------------------------------------------------------------------
# list_field_names
# ---------------------------------------------------------------------------

def test_list_field_names_returns_sorted(simple_schema):
    names = list_field_names(simple_schema)
    assert names == sorted(names)


def test_list_field_names_raises_for_non_dict():
    with pytest.raises(SchemaFlattenerError):
        list_field_names("oops")


def test_list_field_names_raises_for_missing_fields():
    with pytest.raises(SchemaFlattenerError):
        list_field_names({"title": "X"})


def test_list_field_names_correct_values(simple_schema):
    assert list_field_names(simple_schema) == ["age", "email"]
