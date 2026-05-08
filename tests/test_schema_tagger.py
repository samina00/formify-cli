"""Tests for formify_cli.schema_tagger."""

import pytest
from formify_cli.schema_tagger import (
    SchemaTaggerError,
    add_tag,
    remove_tag,
    get_tags,
    fields_with_tag,
    list_all_tags,
)


@pytest.fixture()
def schema():
    return {
        "title": "Demo",
        "fields": [
            {"name": "email", "type": "email", "label": "Email", "tags": ["pii", "contact"]},
            {"name": "age", "type": "number", "label": "Age"},
            {"name": "newsletter", "type": "checkbox", "label": "Subscribe", "tags": ["contact"]},
        ],
    }


# --- add_tag ---

def test_add_tag_adds_new_tag(schema):
    result = add_tag(schema, "age", "analytics")
    assert "analytics" in result["fields"][1]["tags"]


def test_add_tag_does_not_duplicate(schema):
    result = add_tag(schema, "email", "pii")
    assert result["fields"][0]["tags"].count("pii") == 1


def test_add_tag_does_not_mutate_original(schema):
    add_tag(schema, "age", "new")
    assert "tags" not in schema["fields"][1]


def test_add_tag_raises_for_unknown_field(schema):
    with pytest.raises(SchemaTaggerError, match="not found"):
        add_tag(schema, "ghost", "x")


def test_add_tag_raises_for_empty_tag(schema):
    with pytest.raises(SchemaTaggerError, match="non-empty"):
        add_tag(schema, "email", "   ")


def test_add_tag_raises_for_non_dict_schema():
    with pytest.raises(SchemaTaggerError, match="must be a dict"):
        add_tag(["not", "a", "dict"], "email", "tag")


# --- remove_tag ---

def test_remove_tag_removes_existing_tag(schema):
    result = remove_tag(schema, "email", "pii")
    assert "pii" not in result["fields"][0]["tags"]


def test_remove_tag_noop_for_missing_tag(schema):
    result = remove_tag(schema, "email", "nonexistent")
    assert result["fields"][0]["tags"] == ["pii", "contact"]


def test_remove_tag_does_not_mutate_original(schema):
    remove_tag(schema, "email", "pii")
    assert "pii" in schema["fields"][0]["tags"]


def test_remove_tag_raises_for_unknown_field(schema):
    with pytest.raises(SchemaTaggerError, match="not found"):
        remove_tag(schema, "missing", "pii")


# --- get_tags ---

def test_get_tags_returns_list(schema):
    assert get_tags(schema, "email") == ["pii", "contact"]


def test_get_tags_returns_empty_list_when_no_tags(schema):
    assert get_tags(schema, "age") == []


def test_get_tags_raises_for_unknown_field(schema):
    with pytest.raises(SchemaTaggerError, match="not found"):
        get_tags(schema, "unknown")


# --- fields_with_tag ---

def test_fields_with_tag_returns_matching_fields(schema):
    result = fields_with_tag(schema, "contact")
    names = [f["name"] for f in result]
    assert names == ["email", "newsletter"]


def test_fields_with_tag_returns_empty_for_no_match(schema):
    assert fields_with_tag(schema, "unknown-tag") == []


def test_fields_with_tag_raises_for_empty_tag(schema):
    with pytest.raises(SchemaTaggerError, match="non-empty"):
        fields_with_tag(schema, "")


# --- list_all_tags ---

def test_list_all_tags_returns_sorted_unique(schema):
    assert list_all_tags(schema) == ["contact", "pii"]


def test_list_all_tags_returns_empty_for_untagged_schema():
    s = {"title": "T", "fields": [{"name": "x", "type": "text", "label": "X"}]}
    assert list_all_tags(s) == []


def test_list_all_tags_raises_for_missing_fields_key():
    with pytest.raises(SchemaTaggerError, match="'fields' key"):
        list_all_tags({"title": "oops"})
