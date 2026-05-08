"""Tests for formify_cli.schema_field_mapper."""

import pytest

from formify_cli.schema_field_mapper import (
    SchemaFieldMapperError,
    build_name_index,
    list_field_names,
    map_field_names,
)


@pytest.fixture()
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "first_name", "type": "text", "label": "First Name", "required": True},
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "city", "type": "text", "label": "City", "required": False},
        ],
    }


@pytest.fixture()
def depends_schema():
    return {
        "title": "Conditional Form",
        "fields": [
            {"name": "has_dog", "type": "checkbox", "label": "Has dog?"},
            {"name": "dog_name", "type": "text", "label": "Dog name",
             "depends_on": "has_dog", "depends_value": True},
        ],
    }


def test_map_field_names_renames_field(simple_schema):
    result = map_field_names(simple_schema, {"first_name": "given_name"})
    names = [f["name"] for f in result["fields"]]
    assert "given_name" in names
    assert "first_name" not in names


def test_map_field_names_leaves_unmapped_fields_unchanged(simple_schema):
    result = map_field_names(simple_schema, {"email": "email_address"})
    names = [f["name"] for f in result["fields"]]
    assert "first_name" in names
    assert "city" in names


def test_map_field_names_does_not_mutate_original(simple_schema):
    original_names = [f["name"] for f in simple_schema["fields"]]
    map_field_names(simple_schema, {"first_name": "given_name"})
    assert [f["name"] for f in simple_schema["fields"]] == original_names


def test_map_field_names_updates_depends_on(depends_schema):
    result = map_field_names(depends_schema, {"has_dog": "owns_dog"})
    dog_name_field = next(f for f in result["fields"] if f["name"] == "dog_name")
    assert dog_name_field["depends_on"] == "owns_dog"


def test_map_field_names_raises_for_non_dict_schema():
    with pytest.raises(SchemaFieldMapperError, match="must be a dict"):
        map_field_names(["not", "a", "dict"], {"a": "b"})


def test_map_field_names_raises_for_missing_fields_key():
    with pytest.raises(SchemaFieldMapperError, match="'fields'"):
        map_field_names({"title": "No fields"}, {"a": "b"})


def test_map_field_names_raises_for_empty_mapping(simple_schema):
    with pytest.raises(SchemaFieldMapperError, match="empty"):
        map_field_names(simple_schema, {})


def test_map_field_names_raises_for_blank_new_name(simple_schema):
    with pytest.raises(SchemaFieldMapperError, match="non-empty string"):
        map_field_names(simple_schema, {"email": "   "})


def test_map_field_names_raises_for_non_dict_mapping(simple_schema):
    with pytest.raises(SchemaFieldMapperError, match="Mapping must be a dict"):
        map_field_names(simple_schema, ["email", "mail"])


def test_build_name_index_returns_correct_positions(simple_schema):
    index = build_name_index(simple_schema)
    assert index == {"first_name": 0, "email": 1, "city": 2}


def test_build_name_index_raises_for_non_dict():
    with pytest.raises(SchemaFieldMapperError):
        build_name_index("bad")


def test_list_field_names_returns_ordered_list(simple_schema):
    assert list_field_names(simple_schema) == ["first_name", "email", "city"]


def test_list_field_names_raises_for_missing_fields_key():
    with pytest.raises(SchemaFieldMapperError):
        list_field_names({"title": "oops"})
