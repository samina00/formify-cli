"""Tests for formify_cli.schema_patch."""

import pytest

from formify_cli.schema_patch import (
    SchemaPatchError,
    list_field_names,
    patch_field,
    patch_fields_bulk,
)


@pytest.fixture()
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "age", "type": "number", "label": "Age", "required": False},
            {"name": "bio", "type": "textarea", "label": "Bio", "required": False},
        ],
    }


# --- patch_field ---

def test_patch_field_updates_label(simple_schema):
    result = patch_field(simple_schema, "email", {"label": "E-mail Address"})
    patched = next(f for f in result["fields"] if f["name"] == "email")
    assert patched["label"] == "E-mail Address"


def test_patch_field_does_not_mutate_original(simple_schema):
    patch_field(simple_schema, "email", {"label": "Changed"})
    original = next(f for f in simple_schema["fields"] if f["name"] == "email")
    assert original["label"] == "Email"


def test_patch_field_adds_new_key(simple_schema):
    result = patch_field(simple_schema, "age", {"placeholder": "Your age"})
    patched = next(f for f in result["fields"] if f["name"] == "age")
    assert patched["placeholder"] == "Your age"


def test_patch_field_raises_for_unknown_field(simple_schema):
    with pytest.raises(SchemaPatchError, match="'missing_field' not found"):
        patch_field(simple_schema, "missing_field", {"label": "X"})


def test_patch_field_raises_for_non_dict_schema():
    with pytest.raises(SchemaPatchError, match="must be a dict"):
        patch_field(["not", "a", "dict"], "email", {"label": "X"})


def test_patch_field_raises_for_missing_fields_key():
    with pytest.raises(SchemaPatchError, match="'fields' key"):
        patch_field({"title": "No fields"}, "email", {"label": "X"})


def test_patch_field_raises_for_non_dict_updates(simple_schema):
    with pytest.raises(SchemaPatchError, match="updates must be a dict"):
        patch_field(simple_schema, "email", ["label", "X"])


def test_patch_field_raises_for_empty_updates(simple_schema):
    with pytest.raises(SchemaPatchError, match="must not be empty"):
        patch_field(simple_schema, "email", {})


# --- patch_fields_bulk ---

def test_patch_fields_bulk_applies_multiple(simple_schema):
    result = patch_fields_bulk(
        simple_schema,
        {"email": {"label": "E-mail"}, "age": {"required": True}},
    )
    email = next(f for f in result["fields"] if f["name"] == "email")
    age = next(f for f in result["fields"] if f["name"] == "age")
    assert email["label"] == "E-mail"
    assert age["required"] is True


def test_patch_fields_bulk_skips_unknown_fields(simple_schema):
    result = patch_fields_bulk(simple_schema, {"nonexistent": {"label": "X"}})
    assert list_field_names(result) == list_field_names(simple_schema)


def test_patch_fields_bulk_does_not_mutate_original(simple_schema):
    patch_fields_bulk(simple_schema, {"bio": {"label": "Biography"}})
    original = next(f for f in simple_schema["fields"] if f["name"] == "bio")
    assert original["label"] == "Bio"


def test_patch_fields_bulk_raises_for_non_dict_patches(simple_schema):
    with pytest.raises(SchemaPatchError, match="patches must be a dict"):
        patch_fields_bulk(simple_schema, "bad")


def test_patch_fields_bulk_raises_if_update_value_not_dict(simple_schema):
    with pytest.raises(SchemaPatchError, match="must be a dict"):
        patch_fields_bulk(simple_schema, {"email": "not-a-dict"})


# --- list_field_names ---

def test_list_field_names_returns_sorted(simple_schema):
    assert list_field_names(simple_schema) == ["age", "bio", "email"]


def test_list_field_names_raises_for_non_dict():
    with pytest.raises(SchemaPatchError):
        list_field_names("bad")
