"""Tests for formify_cli.schema_slugifier."""

import pytest
from formify_cli.schema_slugifier import (
    SchemaSlugifierError,
    slugify,
    slugify_field_names,
    slugify_labels,
)


# ---------------------------------------------------------------------------
# slugify
# ---------------------------------------------------------------------------

def test_slugify_basic_string():
    assert slugify("Hello World") == "hello-world"


def test_slugify_with_underscore_separator():
    assert slugify("First Name", separator="_") == "first_name"


def test_slugify_removes_special_chars():
    assert slugify("Email Address!") == "email-address"


def test_slugify_collapses_multiple_spaces():
    assert slugify("a   b") == "a-b"


def test_slugify_strips_leading_trailing_separators():
    assert slugify("  hello  ") == "hello"


def test_slugify_already_lowercase():
    assert slugify("username") == "username"


def test_slugify_raises_for_non_string():
    with pytest.raises(SchemaSlugifierError, match="Expected a string"):
        slugify(123)


def test_slugify_raises_for_empty_string():
    with pytest.raises(SchemaSlugifierError, match="empty or whitespace"):
        slugify("   ")


def test_slugify_raises_for_empty_separator():
    with pytest.raises(SchemaSlugifierError, match="Separator"):
        slugify("hello", separator="")


# ---------------------------------------------------------------------------
# slugify_field_names
# ---------------------------------------------------------------------------

@pytest.fixture
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "Full Name", "type": "text", "label": "Full Name"},
            {"name": "Email Address", "type": "email", "label": "Email"},
        ],
    }


def test_slugify_field_names_returns_new_schema(simple_schema):
    result = slugify_field_names(simple_schema)
    assert result is not simple_schema


def test_slugify_field_names_converts_names(simple_schema):
    result = slugify_field_names(simple_schema)
    names = [f["name"] for f in result["fields"]]
    assert names == ["full-name", "email-address"]


def test_slugify_field_names_does_not_mutate_original(simple_schema):
    slugify_field_names(simple_schema)
    assert simple_schema["fields"][0]["name"] == "Full Name"


def test_slugify_field_names_raises_for_non_dict():
    with pytest.raises(SchemaSlugifierError, match="must be a dict"):
        slugify_field_names(["not", "a", "dict"])


def test_slugify_field_names_raises_for_missing_fields_key():
    with pytest.raises(SchemaSlugifierError, match="'fields' key"):
        slugify_field_names({"title": "No Fields"})


# ---------------------------------------------------------------------------
# slugify_labels
# ---------------------------------------------------------------------------

def test_slugify_labels_converts_labels(simple_schema):
    result = slugify_labels(simple_schema)
    labels = [f["label"] for f in result["fields"]]
    assert labels == ["full-name", "email"]


def test_slugify_labels_does_not_mutate_original(simple_schema):
    slugify_labels(simple_schema)
    assert simple_schema["fields"][0]["label"] == "Full Name"


def test_slugify_labels_skips_fields_without_label():
    schema = {
        "title": "T",
        "fields": [{"name": "x", "type": "text"}],
    }
    result = slugify_labels(schema)
    assert "label" not in result["fields"][0]


def test_slugify_labels_raises_for_non_dict():
    with pytest.raises(SchemaSlugifierError, match="must be a dict"):
        slugify_labels("bad")


def test_slugify_labels_uses_custom_separator(simple_schema):
    result = slugify_labels(simple_schema, separator="_")
    assert result["fields"][0]["label"] == "full_name"
