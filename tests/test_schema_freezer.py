"""Tests for formify_cli.schema_freezer."""

import pytest
from types import MappingProxyType

from formify_cli.schema_freezer import (
    SchemaFreezerError,
    freeze_schema,
    is_frozen,
    safe_copy,
    thaw_schema,
)


@pytest.fixture
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "age", "type": "number", "label": "Age", "required": False},
        ],
    }


# --- freeze_schema ---

def test_freeze_schema_returns_mapping_proxy(simple_schema):
    frozen = freeze_schema(simple_schema)
    assert isinstance(frozen, MappingProxyType)


def test_freeze_schema_raises_for_non_dict():
    with pytest.raises(SchemaFreezerError, match="must be a dict"):
        freeze_schema(["not", "a", "dict"])


def test_freeze_schema_top_level_is_immutable(simple_schema):
    frozen = freeze_schema(simple_schema)
    with pytest.raises(TypeError):
        frozen["title"] = "Changed"  # type: ignore[index]


def test_freeze_schema_nested_fields_are_immutable(simple_schema):
    frozen = freeze_schema(simple_schema)
    # fields is a tuple of MappingProxyType
    assert isinstance(frozen["fields"], tuple)
    with pytest.raises(TypeError):
        frozen["fields"][0]["name"] = "hacked"  # type: ignore[index]


def test_freeze_schema_does_not_mutate_original(simple_schema):
    original_title = simple_schema["title"]
    freeze_schema(simple_schema)
    assert simple_schema["title"] == original_title
    assert isinstance(simple_schema["fields"], list)


# --- thaw_schema ---

def test_thaw_schema_returns_dict(simple_schema):
    frozen = freeze_schema(simple_schema)
    thawed = thaw_schema(frozen)
    assert isinstance(thawed, dict)


def test_thaw_schema_fields_are_list(simple_schema):
    frozen = freeze_schema(simple_schema)
    thawed = thaw_schema(frozen)
    assert isinstance(thawed["fields"], list)


def test_thaw_schema_is_mutable(simple_schema):
    frozen = freeze_schema(simple_schema)
    thawed = thaw_schema(frozen)
    thawed["title"] = "New Title"
    assert thawed["title"] == "New Title"


def test_thaw_schema_raises_for_plain_dict(simple_schema):
    with pytest.raises(SchemaFreezerError, match="MappingProxyType"):
        thaw_schema(simple_schema)  # type: ignore[arg-type]


def test_thaw_is_independent_from_frozen(simple_schema):
    frozen = freeze_schema(simple_schema)
    thawed = thaw_schema(frozen)
    thawed["fields"][0]["name"] = "changed"
    # Original frozen should still hold old value
    assert frozen["fields"][0]["name"] == "email"


# --- is_frozen ---

def test_is_frozen_true_for_frozen(simple_schema):
    assert is_frozen(freeze_schema(simple_schema)) is True


def test_is_frozen_false_for_plain_dict(simple_schema):
    assert is_frozen(simple_schema) is False


def test_is_frozen_false_for_none():
    assert is_frozen(None) is False


# --- safe_copy ---

def test_safe_copy_returns_equal_dict(simple_schema):
    copied = safe_copy(simple_schema)
    assert copied == simple_schema


def test_safe_copy_is_independent(simple_schema):
    copied = safe_copy(simple_schema)
    copied["title"] = "Mutated"
    assert simple_schema["title"] == "Test Form"


def test_safe_copy_raises_for_non_dict():
    with pytest.raises(SchemaFreezerError, match="must be a dict"):
        safe_copy("not a dict")  # type: ignore[arg-type]
