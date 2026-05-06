"""Tests for formify_cli.schema_search."""

import pytest
from formify_cli.schema_search import (
    SchemaSearchError,
    search_by_type,
    search_by_name,
    search_by_label,
    search_required_fields,
    filter_fields,
)


@pytest.fixture()
def schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email Address", "required": True},
            {"name": "age", "type": "number", "label": "Your Age", "required": False},
            {"name": "bio", "type": "textarea", "label": "Short Bio", "required": False},
            {"name": "country", "type": "select", "label": "Country", "required": True},
        ],
    }


def test_search_by_type_returns_matching_fields(schema):
    result = search_by_type(schema, "email")
    assert len(result) == 1
    assert result[0]["name"] == "email"


def test_search_by_type_is_case_insensitive(schema):
    result = search_by_type(schema, "TEXTAREA")
    assert len(result) == 1
    assert result[0]["name"] == "bio"


def test_search_by_type_returns_empty_for_no_match(schema):
    assert search_by_type(schema, "checkbox") == []


def test_search_by_type_raises_for_empty_type(schema):
    with pytest.raises(SchemaSearchError):
        search_by_type(schema, "")


def test_search_by_type_raises_for_non_dict_schema():
    with pytest.raises(SchemaSearchError):
        search_by_type(["not", "a", "dict"], "text")


def test_search_by_name_returns_field(schema):
    result = search_by_name(schema, "age")
    assert result is not None
    assert result["type"] == "number"


def test_search_by_name_returns_none_for_missing(schema):
    assert search_by_name(schema, "nonexistent") is None


def test_search_by_name_raises_for_empty_name(schema):
    with pytest.raises(SchemaSearchError):
        search_by_name(schema, "   ")


def test_search_by_label_finds_keyword(schema):
    result = search_by_label(schema, "age")
    assert any(f["name"] == "age" for f in result)


def test_search_by_label_is_case_insensitive(schema):
    result = search_by_label(schema, "ADDRESS")
    assert len(result) == 1
    assert result[0]["name"] == "email"


def test_search_by_label_raises_for_empty_keyword(schema):
    with pytest.raises(SchemaSearchError):
        search_by_label(schema, "")


def test_search_required_fields_returns_required_only(schema):
    result = search_required_fields(schema)
    assert all(f["required"] is True for f in result)
    assert len(result) == 2


def test_search_required_fields_raises_for_missing_fields_key():
    with pytest.raises(SchemaSearchError):
        search_required_fields({"title": "No fields key"})


def test_filter_fields_single_criterion(schema):
    result = filter_fields(schema, required=True)
    assert len(result) == 2


def test_filter_fields_multiple_criteria(schema):
    result = filter_fields(schema, type="select", required=True)
    assert len(result) == 1
    assert result[0]["name"] == "country"


def test_filter_fields_no_match_returns_empty(schema):
    result = filter_fields(schema, type="file")
    assert result == []
