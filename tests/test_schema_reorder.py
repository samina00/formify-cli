"""Tests for formify_cli.schema_reorder."""

import pytest
from formify_cli.schema_reorder import (
    SchemaReorderError,
    reorder_by_list,
    reorder_alphabetically,
    reorder_by_type_priority,
    list_field_names,
)


@pytest.fixture
def sample_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "username", "type": "text", "label": "Username"},
            {"name": "age", "type": "number", "label": "Age"},
            {"name": "bio", "type": "textarea", "label": "Bio"},
            {"name": "country", "type": "select", "label": "Country"},
        ],
    }


def test_reorder_by_list_basic(sample_schema):
    result = reorder_by_list(sample_schema, ["username", "email", "age"])
    names = list_field_names(result)
    assert names[:3] == ["username", "email", "age"]


def test_reorder_by_list_appends_remaining(sample_schema):
    result = reorder_by_list(sample_schema, ["bio"])
    names = list_field_names(result)
    assert names[0] == "bio"
    assert set(names) == {"email", "username", "age", "bio", "country"}


def test_reorder_by_list_ignores_unknown_names(sample_schema):
    result = reorder_by_list(sample_schema, ["nonexistent", "age"])
    names = list_field_names(result)
    assert names[0] == "age"
    assert len(names) == 5


def test_reorder_by_list_does_not_mutate_original(sample_schema):
    original_names = list_field_names(sample_schema)
    reorder_by_list(sample_schema, ["age", "email"])
    assert list_field_names(sample_schema) == original_names


def test_reorder_by_list_raises_for_empty_order(sample_schema):
    with pytest.raises(SchemaReorderError, match="empty"):
        reorder_by_list(sample_schema, [])


def test_reorder_by_list_raises_for_non_dict():
    with pytest.raises(SchemaReorderError):
        reorder_by_list(["not", "a", "dict"], ["a"])


def test_reorder_by_list_raises_for_missing_fields_key():
    with pytest.raises(SchemaReorderError, match="fields"):
        reorder_by_list({"title": "No fields"}, ["a"])


def test_reorder_alphabetically_ascending(sample_schema):
    result = reorder_alphabetically(sample_schema)
    names = list_field_names(result)
    assert names == sorted(names)


def test_reorder_alphabetically_descending(sample_schema):
    result = reorder_alphabetically(sample_schema, reverse=True)
    names = list_field_names(result)
    assert names == sorted(names, reverse=True)


def test_reorder_alphabetically_does_not_mutate(sample_schema):
    original = list_field_names(sample_schema)
    reorder_alphabetically(sample_schema)
    assert list_field_names(sample_schema) == original


def test_reorder_by_type_priority_orders_correctly(sample_schema):
    result = reorder_by_type_priority(sample_schema)
    names = list_field_names(result)
    # email comes before number, textarea, select
    assert names.index("email") < names.index("age")
    assert names.index("age") < names.index("country")
    assert names.index("country") < names.index("bio")


def test_reorder_by_type_priority_unknown_type_last():
    schema = {
        "title": "X",
        "fields": [
            {"name": "f1", "type": "custom_widget", "label": "F1"},
            {"name": "f2", "type": "text", "label": "F2"},
        ],
    }
    result = reorder_by_type_priority(schema)
    names = list_field_names(result)
    assert names == ["f2", "f1"]


def test_reorder_by_type_priority_does_not_mutate(sample_schema):
    original = list_field_names(sample_schema)
    reorder_by_type_priority(sample_schema)
    assert list_field_names(sample_schema) == original


def test_list_field_names_returns_all(sample_schema):
    names = list_field_names(sample_schema)
    assert len(names) == 5
    assert "email" in names


def test_list_field_names_raises_for_non_dict():
    with pytest.raises(SchemaReorderError):
        list_field_names("bad")
