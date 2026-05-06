"""Tests for formify_cli/schema_picker.py"""

import pytest

from formify_cli.schema_picker import (
    SchemaPickerError,
    list_field_names,
    omit_fields,
    pick_fields,
)


@pytest.fixture()
def schema():
    return {
        "title": "Demo Form",
        "fields": [
            {"name": "first_name", "type": "text", "label": "First Name"},
            {"name": "last_name", "type": "text", "label": "Last Name"},
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "phone", "type": "text", "label": "Phone"},
        ],
    }


# --- pick_fields ---

def test_pick_fields_returns_only_requested(schema):
    result = pick_fields(schema, ["email", "phone"])
    assert [f["name"] for f in result["fields"]] == ["email", "phone"]


def test_pick_fields_preserves_order_of_names_arg(schema):
    result = pick_fields(schema, ["phone", "first_name"])
    assert [f["name"] for f in result["fields"]] == ["phone", "first_name"]


def test_pick_fields_ignores_unknown_names(schema):
    result = pick_fields(schema, ["email", "nonexistent"])
    assert len(result["fields"]) == 1
    assert result["fields"][0]["name"] == "email"


def test_pick_fields_preserves_title(schema):
    result = pick_fields(schema, ["email"])
    assert result["title"] == "Demo Form"


def test_pick_fields_does_not_mutate_original(schema):
    original_count = len(schema["fields"])
    pick_fields(schema, ["email"])
    assert len(schema["fields"]) == original_count


def test_pick_fields_raises_for_non_dict():
    with pytest.raises(SchemaPickerError, match="dict"):
        pick_fields(["not", "a", "dict"], ["email"])


def test_pick_fields_raises_for_missing_fields_key():
    with pytest.raises(SchemaPickerError, match="fields"):
        pick_fields({"title": "X"}, ["email"])


def test_pick_fields_raises_for_empty_names(schema):
    with pytest.raises(SchemaPickerError, match="empty"):
        pick_fields(schema, [])


def test_pick_fields_raises_for_non_list_names(schema):
    with pytest.raises(SchemaPickerError, match="list"):
        pick_fields(schema, "email")


# --- omit_fields ---

def test_omit_fields_removes_named_fields(schema):
    result = omit_fields(schema, ["phone", "last_name"])
    names = [f["name"] for f in result["fields"]]
    assert "phone" not in names
    assert "last_name" not in names
    assert "first_name" in names
    assert "email" in names


def test_omit_fields_ignores_unknown_names(schema):
    result = omit_fields(schema, ["ghost"])
    assert len(result["fields"]) == 4


def test_omit_fields_does_not_mutate_original(schema):
    original_count = len(schema["fields"])
    omit_fields(schema, ["email"])
    assert len(schema["fields"]) == original_count


def test_omit_fields_raises_for_empty_names(schema):
    with pytest.raises(SchemaPickerError, match="empty"):
        omit_fields(schema, [])


# --- list_field_names ---

def test_list_field_names_returns_sorted_names(schema):
    names = list_field_names(schema)
    assert names == sorted(names)


def test_list_field_names_contains_all_fields(schema):
    names = list_field_names(schema)
    assert set(names) == {"first_name", "last_name", "email", "phone"}


def test_list_field_names_raises_for_non_dict():
    with pytest.raises(SchemaPickerError):
        list_field_names("not a dict")
