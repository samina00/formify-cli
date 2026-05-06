"""Tests for formify_cli.schema_sorter."""

import pytest

from formify_cli.schema_sorter import (
    SchemaSorterError,
    reorder_fields,
    sort_by_label,
    sort_by_name,
    sort_by_type,
    sort_required_first,
)


@pytest.fixture()
def sample_schema():
    return {
        "title": "Demo Form",
        "fields": [
            {"name": "zip", "type": "text", "label": "ZIP Code", "required": False},
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "age", "type": "number", "label": "Age", "required": False},
            {"name": "name", "type": "text", "label": "Full Name", "required": True},
        ],
    }


# --- sort_by_name ---

def test_sort_by_name_ascending(sample_schema):
    result = sort_by_name(sample_schema)
    names = [f["name"] for f in result["fields"]]
    assert names == ["age", "email", "name", "zip"]


def test_sort_by_name_descending(sample_schema):
    result = sort_by_name(sample_schema, reverse=True)
    names = [f["name"] for f in result["fields"]]
    assert names == ["zip", "name", "email", "age"]


def test_sort_by_name_does_not_mutate_original(sample_schema):
    original_names = [f["name"] for f in sample_schema["fields"]]
    sort_by_name(sample_schema)
    assert [f["name"] for f in sample_schema["fields"]] == original_names


# --- sort_by_type ---

def test_sort_by_type_groups_same_types_together(sample_schema):
    result = sort_by_type(sample_schema)
    types = [f["type"] for f in result["fields"]]
    assert types == ["email", "number", "text", "text"]


def test_sort_by_type_reverse(sample_schema):
    result = sort_by_type(sample_schema, reverse=True)
    types = [f["type"] for f in result["fields"]]
    assert types == ["text", "text", "number", "email"]


# --- sort_required_first ---

def test_sort_required_first_puts_required_at_top(sample_schema):
    result = sort_required_first(sample_schema)
    required_flags = [f["required"] for f in result["fields"]]
    assert required_flags[:2] == [True, True]
    assert required_flags[2:] == [False, False]


def test_sort_required_first_does_not_mutate_original(sample_schema):
    original = [f["name"] for f in sample_schema["fields"]]
    sort_required_first(sample_schema)
    assert [f["name"] for f in sample_schema["fields"]] == original


# --- sort_by_label ---

def test_sort_by_label_ascending(sample_schema):
    result = sort_by_label(sample_schema)
    labels = [f["label"] for f in result["fields"]]
    assert labels == ["Age", "Email", "Full Name", "ZIP Code"]


# --- reorder_fields ---

def test_reorder_fields_custom_order(sample_schema):
    result = reorder_fields(sample_schema, ["name", "email", "age", "zip"])
    names = [f["name"] for f in result["fields"]]
    assert names == ["name", "email", "age", "zip"]


def test_reorder_fields_partial_order_appends_remainder(sample_schema):
    result = reorder_fields(sample_schema, ["email", "name"])
    names = [f["name"] for f in result["fields"]]
    assert names[:2] == ["email", "name"]
    assert set(names[2:]) == {"zip", "age"}


def test_reorder_fields_unknown_names_ignored(sample_schema):
    result = reorder_fields(sample_schema, ["ghost", "email"])
    names = [f["name"] for f in result["fields"]]
    assert "email" in names
    assert "ghost" not in names


# --- error cases ---

def test_raises_for_non_dict():
    with pytest.raises(SchemaSorterError, match="must be a dict"):
        sort_by_name(["not", "a", "dict"])


def test_raises_for_missing_fields_key():
    with pytest.raises(SchemaSorterError, match="'fields' key"):
        sort_by_name({"title": "No fields here"})


def test_reorder_raises_if_order_not_list(sample_schema):
    with pytest.raises(SchemaSorterError, match="must be a list"):
        reorder_fields(sample_schema, "email,name")
