"""Tests for formify_cli.schema_clone."""

import pytest
from formify_cli.schema_clone import (
    SchemaCloneError,
    clone_schema,
    rename_field,
    prefix_field_names,
)


@pytest.fixture()
def simple_schema():
    return {
        "title": "Contact",
        "fields": [
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "message", "type": "textarea", "label": "Message"},
        ],
    }


# --- clone_schema ---

def test_clone_schema_returns_equal_but_independent(simple_schema):
    cloned = clone_schema(simple_schema)
    assert cloned == simple_schema
    cloned["fields"][0]["name"] = "changed"
    assert simple_schema["fields"][0]["name"] == "email"


def test_clone_schema_overrides_title(simple_schema):
    cloned = clone_schema(simple_schema, new_title="Feedback")
    assert cloned["title"] == "Feedback"
    assert simple_schema["title"] == "Contact"


def test_clone_schema_raises_for_non_dict():
    with pytest.raises(SchemaCloneError, match="must be a dict"):
        clone_schema(["not", "a", "dict"])


def test_clone_schema_raises_for_empty_new_title(simple_schema):
    with pytest.raises(SchemaCloneError, match="non-empty string"):
        clone_schema(simple_schema, new_title="   ")


def test_clone_schema_raises_for_non_string_title(simple_schema):
    with pytest.raises(SchemaCloneError):
        clone_schema(simple_schema, new_title=42)


# --- rename_field ---

def test_rename_field_changes_name(simple_schema):
    updated = rename_field(simple_schema, "email", "email_address")
    names = [f["name"] for f in updated["fields"]]
    assert "email_address" in names
    assert "email" not in names


def test_rename_field_does_not_mutate_original(simple_schema):
    rename_field(simple_schema, "email", "email_address")
    assert simple_schema["fields"][0]["name"] == "email"


def test_rename_field_raises_for_unknown_field(simple_schema):
    with pytest.raises(SchemaCloneError, match="not found"):
        rename_field(simple_schema, "nonexistent", "other")


def test_rename_field_raises_for_name_conflict(simple_schema):
    with pytest.raises(SchemaCloneError, match="already exists"):
        rename_field(simple_schema, "email", "message")


def test_rename_field_raises_for_empty_names(simple_schema):
    with pytest.raises(SchemaCloneError):
        rename_field(simple_schema, "", "new_name")


# --- prefix_field_names ---

def test_prefix_field_names_prepends_to_all(simple_schema):
    updated = prefix_field_names(simple_schema, "form1_")
    names = [f["name"] for f in updated["fields"]]
    assert names == ["form1_email", "form1_message"]


def test_prefix_field_names_does_not_mutate_original(simple_schema):
    prefix_field_names(simple_schema, "x_")
    assert simple_schema["fields"][0]["name"] == "email"


def test_prefix_field_names_raises_for_empty_prefix(simple_schema):
    with pytest.raises(SchemaCloneError, match="non-empty string"):
        prefix_field_names(simple_schema, "")


def test_prefix_field_names_raises_for_invalid_chars(simple_schema):
    with pytest.raises(SchemaCloneError, match="alphanumeric"):
        prefix_field_names(simple_schema, "bad prefix!")


def test_prefix_field_names_raises_for_non_dict():
    with pytest.raises(SchemaCloneError, match="must be a dict"):
        prefix_field_names("not a dict", "p_")
