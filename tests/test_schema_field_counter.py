"""Tests for formify_cli.schema_field_counter."""

import pytest

from formify_cli.schema_field_counter import (
    SchemaFieldCounterError,
    count_by_required,
    count_by_type,
    count_with_placeholder,
    count_with_label,
    field_type_list,
    summary,
)


@pytest.fixture()
def sample_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email", "required": True, "placeholder": "you@example.com"},
            {"name": "name", "type": "text", "label": "Name", "required": True, "placeholder": ""},
            {"name": "bio", "type": "textarea", "label": "Bio", "required": False, "placeholder": "Tell us about yourself"},
            {"name": "age", "type": "number", "label": "", "required": False},
            {"name": "country", "type": "select", "label": "Country", "required": False, "placeholder": "Pick one"},
        ],
    }


def test_count_by_required_correct_split(sample_schema):
    result = count_by_required(sample_schema)
    assert result["required"] == 2
    assert result["optional"] == 3


def test_count_by_required_all_required():
    schema = {"fields": [{"name": "a", "type": "text", "required": True}, {"name": "b", "type": "text", "required": True}]}
    result = count_by_required(schema)
    assert result["required"] == 2
    assert result["optional"] == 0


def test_count_by_required_raises_for_non_dict():
    with pytest.raises(SchemaFieldCounterError):
        count_by_required(["not", "a", "dict"])


def test_count_by_required_raises_for_missing_fields_key():
    with pytest.raises(SchemaFieldCounterError):
        count_by_required({"title": "No fields"})


def test_count_by_type_groups_correctly(sample_schema):
    result = count_by_type(sample_schema)
    assert result["email"] == 1
    assert result["text"] == 1
    assert result["textarea"] == 1
    assert result["number"] == 1
    assert result["select"] == 1


def test_count_by_type_is_case_insensitive():
    schema = {"fields": [{"name": "a", "type": "TEXT"}, {"name": "b", "type": "text"}]}
    result = count_by_type(schema)
    assert result["text"] == 2


def test_count_by_type_unknown_type_for_missing_type_key():
    schema = {"fields": [{"name": "a"}, {"name": "b", "type": "text"}]}
    result = count_by_type(schema)
    assert result["unknown"] == 1
    assert result["text"] == 1


def test_count_with_placeholder(sample_schema):
    assert count_with_placeholder(sample_schema) == 3


def test_count_with_placeholder_empty_schema():
    assert count_with_placeholder({"fields": []}) == 0


def test_count_with_label(sample_schema):
    # age has empty label
    assert count_with_label(sample_schema) == 4


def test_field_type_list_returns_sorted_unique(sample_schema):
    result = field_type_list(sample_schema)
    assert result == sorted(set(result))
    assert "email" in result
    assert "textarea" in result


def test_field_type_list_no_duplicates():
    schema = {"fields": [{"name": "a", "type": "text"}, {"name": "b", "type": "text"}]}
    assert field_type_list(schema) == ["text"]


def test_summary_returns_all_keys(sample_schema):
    result = summary(sample_schema)
    for key in ("total", "required", "optional", "with_placeholder", "with_label", "by_type", "unique_types"):
        assert key in result


def test_summary_total(sample_schema):
    assert summary(sample_schema)["total"] == 5


def test_summary_raises_for_non_dict():
    with pytest.raises(SchemaFieldCounterError):
        summary("not a dict")
