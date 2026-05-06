"""Tests for formify_cli.schema_grouper."""

import pytest
from formify_cli.schema_grouper import (
    SchemaGrouperError,
    group_by_key,
    list_group_names,
    fields_in_group,
    ungroup_schema,
)


@pytest.fixture()
def grouped_schema():
    return {
        "title": "Registration",
        "fields": [
            {"name": "first_name", "type": "text", "label": "First Name", "group": "personal"},
            {"name": "last_name", "type": "text", "label": "Last Name", "group": "personal"},
            {"name": "email", "type": "email", "label": "Email", "group": "contact"},
            {"name": "notes", "type": "textarea", "label": "Notes"},
        ],
    }


def test_group_by_key_returns_dict(grouped_schema):
    result = group_by_key(grouped_schema, "group")
    assert isinstance(result, dict)


def test_group_by_key_correct_groups(grouped_schema):
    result = group_by_key(grouped_schema, "group")
    assert set(result.keys()) == {"personal", "contact", ""}


def test_group_by_key_personal_has_two_fields(grouped_schema):
    result = group_by_key(grouped_schema, "group")
    assert len(result["personal"]) == 2


def test_group_by_key_missing_key_goes_to_empty_string(grouped_schema):
    result = group_by_key(grouped_schema, "group")
    names = [f["name"] for f in result[""]]
    assert names == ["notes"]


def test_group_by_key_raises_for_non_dict():
    with pytest.raises(SchemaGrouperError, match="dict"):
        group_by_key(["not", "a", "dict"], "group")


def test_group_by_key_raises_for_missing_fields_key():
    with pytest.raises(SchemaGrouperError, match="fields"):
        group_by_key({"title": "x"}, "group")


def test_group_by_key_raises_for_empty_key(grouped_schema):
    with pytest.raises(SchemaGrouperError):
        group_by_key(grouped_schema, "")


def test_list_group_names_returns_sorted(grouped_schema):
    names = list_group_names(grouped_schema, "group")
    assert names == sorted(names)


def test_list_group_names_contains_all_groups(grouped_schema):
    names = list_group_names(grouped_schema, "group")
    assert "personal" in names
    assert "contact" in names


def test_fields_in_group_returns_correct_fields(grouped_schema):
    fields = fields_in_group(grouped_schema, "group", "personal")
    assert len(fields) == 2
    assert all(f["group"] == "personal" for f in fields)


def test_fields_in_group_returns_empty_for_unknown_group(grouped_schema):
    fields = fields_in_group(grouped_schema, "group", "nonexistent")
    assert fields == []


def test_fields_in_group_returns_copy(grouped_schema):
    fields = fields_in_group(grouped_schema, "group", "personal")
    fields[0]["name"] = "mutated"
    original = grouped_schema["fields"][0]["name"]
    assert original == "first_name"


def test_ungroup_schema_removes_key(grouped_schema):
    result = ungroup_schema(grouped_schema, "group")
    for field in result["fields"]:
        assert "group" not in field


def test_ungroup_schema_does_not_mutate_original(grouped_schema):
    ungroup_schema(grouped_schema, "group")
    assert "group" in grouped_schema["fields"][0]


def test_ungroup_schema_preserves_other_keys(grouped_schema):
    result = ungroup_schema(grouped_schema, "group")
    names = [f["name"] for f in result["fields"]]
    assert "first_name" in names


def test_ungroup_schema_raises_for_empty_key(grouped_schema):
    with pytest.raises(SchemaGrouperError):
        ungroup_schema(grouped_schema, "")
