"""Tests for formify_cli.schema_renamer."""

import pytest
from formify_cli.schema_renamer import (
    SchemaRenamerError,
    rename_field,
    rename_fields_bulk,
    list_field_names,
)


@pytest.fixture()
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "name", "type": "text", "label": "Name"},
            {"name": "country", "type": "select", "label": "Country", "depends_on": "name"},
        ],
    }


def test_rename_field_returns_new_schema(simple_schema):
    result = rename_field(simple_schema, "email", "email_address")
    names = list_field_names(result)
    assert "email_address" in names
    assert "email" not in names


def test_rename_field_does_not_mutate_original(simple_schema):
    rename_field(simple_schema, "email", "email_address")
    assert list_field_names(simple_schema) == ["email", "name", "country"]


def test_rename_field_updates_depends_on(simple_schema):
    result = rename_field(simple_schema, "name", "full_name")
    country = next(f for f in result["fields"] if f["name"] == "country")
    assert country["depends_on"] == "full_name"


def test_rename_field_raises_for_unknown_old_name(simple_schema):
    with pytest.raises(SchemaRenamerError, match="not found"):
        rename_field(simple_schema, "nonexistent", "new_name")


def test_rename_field_raises_if_new_name_already_exists(simple_schema):
    with pytest.raises(SchemaRenamerError, match="already exists"):
        rename_field(simple_schema, "email", "name")


def test_rename_field_raises_for_non_dict():
    with pytest.raises(SchemaRenamerError, match="must be a dict"):
        rename_field(["not", "a", "dict"], "email", "x")


def test_rename_field_raises_for_missing_fields_key():
    with pytest.raises(SchemaRenamerError, match="'fields'"):
        rename_field({"title": "No fields"}, "email", "x")


def test_rename_field_raises_for_empty_old_name(simple_schema):
    with pytest.raises(SchemaRenamerError, match="non-empty string"):
        rename_field(simple_schema, "", "new_name")


def test_rename_field_raises_for_empty_new_name(simple_schema):
    with pytest.raises(SchemaRenamerError, match="non-empty string"):
        rename_field(simple_schema, "email", "")


def test_rename_fields_bulk_renames_multiple(simple_schema):
    result = rename_fields_bulk(simple_schema, {"email": "email_address", "name": "full_name"})
    names = list_field_names(result)
    assert "email_address" in names
    assert "full_name" in names
    assert "email" not in names
    assert "name" not in names


def test_rename_fields_bulk_updates_depends_on(simple_schema):
    result = rename_fields_bulk(simple_schema, {"name": "full_name"})
    country = next(f for f in result["fields"] if f["name"] == "country")
    assert country["depends_on"] == "full_name"


def test_rename_fields_bulk_raises_for_empty_map(simple_schema):
    with pytest.raises(SchemaRenamerError, match="non-empty dict"):
        rename_fields_bulk(simple_schema, {})


def test_rename_fields_bulk_raises_for_unknown_field(simple_schema):
    with pytest.raises(SchemaRenamerError, match="not found"):
        rename_fields_bulk(simple_schema, {"ghost": "phantom"})


def test_list_field_names_returns_all(simple_schema):
    assert list_field_names(simple_schema) == ["email", "name", "country"]


def test_list_field_names_raises_for_non_dict():
    with pytest.raises(SchemaRenamerError):
        list_field_names("not a dict")
