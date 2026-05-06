"""Tests for formify_cli.schema_stats."""

import pytest
from formify_cli.schema_stats import (
    SchemaStatsError,
    count_fields,
    count_required_fields,
    count_by_type,
    list_unknown_types,
    compute_stats,
)


@pytest.fixture
def sample_schema():
    return {
        "title": "Contact Form",
        "fields": [
            {"name": "name", "type": "text", "label": "Name", "required": True},
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "age", "type": "number", "label": "Age", "required": False},
            {"name": "bio", "type": "textarea", "label": "Bio"},
            {"name": "role", "type": "select", "label": "Role", "required": True},
        ],
    }


def test_count_fields_returns_correct_total(sample_schema):
    assert count_fields(sample_schema) == 5


def test_count_fields_raises_for_non_dict():
    with pytest.raises(SchemaStatsError, match="must be a dict"):
        count_fields(["not", "a", "dict"])


def test_count_fields_raises_for_missing_fields_key():
    with pytest.raises(SchemaStatsError, match="'fields' key"):
        count_fields({"title": "No fields"})


def test_count_required_fields(sample_schema):
    assert count_required_fields(sample_schema) == 3


def test_count_required_fields_none_required():
    schema = {"fields": [{"name": "x", "type": "text"}, {"name": "y", "type": "email"}]}
    assert count_required_fields(schema) == 0


def test_count_by_type_returns_correct_mapping(sample_schema):
    result = count_by_type(sample_schema)
    assert result["text"] == 1
    assert result["email"] == 1
    assert result["number"] == 1
    assert result["textarea"] == 1
    assert result["select"] == 1


def test_count_by_type_is_case_insensitive():
    schema = {"fields": [{"name": "a", "type": "TEXT"}, {"name": "b", "type": "text"}]}
    result = count_by_type(schema)
    assert result["text"] == 2


def test_list_unknown_types_returns_empty_for_known(sample_schema):
    assert list_unknown_types(sample_schema) == []


def test_list_unknown_types_detects_custom_type():
    schema = {"fields": [{"name": "x", "type": "rating"}, {"name": "y", "type": "text"}]}
    result = list_unknown_types(schema)
    assert result == ["rating"]


def test_list_unknown_types_is_sorted():
    schema = {"fields": [{"name": "a", "type": "zebra"}, {"name": "b", "type": "apple"}]}
    assert list_unknown_types(schema) == ["apple", "zebra"]


def test_compute_stats_returns_full_dict(sample_schema):
    stats = compute_stats(sample_schema)
    assert stats["title"] == "Contact Form"
    assert stats["total_fields"] == 5
    assert stats["required_fields"] == 3
    assert stats["optional_fields"] == 2
    assert isinstance(stats["types"], dict)
    assert stats["unknown_types"] == []


def test_compute_stats_raises_for_non_dict():
    with pytest.raises(SchemaStatsError):
        compute_stats("not a schema")


def test_compute_stats_title_defaults_to_empty_string():
    schema = {"fields": [{"name": "x", "type": "text"}]}
    stats = compute_stats(schema)
    assert stats["title"] == ""
