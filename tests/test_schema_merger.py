"""Tests for formify_cli.schema_merger."""

import pytest

from formify_cli.schema_merger import (
    SchemaMergerError,
    list_field_names,
    merge_schemas,
)


@pytest.fixture()
def base_schema():
    return {
        "title": "Base Form",
        "fields": [
            {"name": "first_name", "type": "text", "label": "First Name"},
            {"name": "email", "type": "email", "label": "Email"},
        ],
    }


@pytest.fixture()
def override_schema():
    return {
        "title": "Extended Form",
        "fields": [
            {"name": "email", "type": "email", "label": "Email Address", "required": True},
            {"name": "phone", "type": "tel", "label": "Phone"},
        ],
    }


def test_merge_returns_dict(base_schema, override_schema):
    result = merge_schemas(base_schema, override_schema)
    assert isinstance(result, dict)


def test_merge_title_taken_from_override(base_schema, override_schema):
    result = merge_schemas(base_schema, override_schema)
    assert result["title"] == "Extended Form"


def test_merge_title_falls_back_to_base_when_override_lacks_title(base_schema):
    override = {"fields": [{"name": "phone", "type": "tel", "label": "Phone"}]}
    result = merge_schemas(base_schema, override)
    assert result["title"] == "Base Form"


def test_merge_override_strategy_replaces_conflicting_field(base_schema, override_schema):
    result = merge_schemas(base_schema, override_schema, conflict="override")
    email_field = next(f for f in result["fields"] if f["name"] == "email")
    assert email_field["label"] == "Email Address"
    assert email_field.get("required") is True


def test_merge_keep_strategy_retains_base_field(base_schema, override_schema):
    result = merge_schemas(base_schema, override_schema, conflict="keep")
    email_field = next(f for f in result["fields"] if f["name"] == "email")
    assert email_field["label"] == "Email"


def test_merge_error_strategy_raises_on_conflict(base_schema, override_schema):
    with pytest.raises(SchemaMergerError, match="Conflicting field names"):
        merge_schemas(base_schema, override_schema, conflict="error")


def test_merge_non_conflicting_fields_from_override_are_appended(base_schema, override_schema):
    result = merge_schemas(base_schema, override_schema)
    names = [f["name"] for f in result["fields"]]
    assert "phone" in names


def test_merge_preserves_base_only_fields(base_schema, override_schema):
    result = merge_schemas(base_schema, override_schema)
    names = [f["name"] for f in result["fields"]]
    assert "first_name" in names


def test_merge_raises_if_base_not_dict(override_schema):
    with pytest.raises(SchemaMergerError, match="dictionaries"):
        merge_schemas(["not", "a", "dict"], override_schema)


def test_merge_raises_if_fields_missing_in_base(override_schema):
    with pytest.raises(SchemaMergerError, match="base"):
        merge_schemas({"title": "No Fields"}, override_schema)


def test_merge_raises_for_invalid_conflict_strategy(base_schema, override_schema):
    with pytest.raises(SchemaMergerError, match="Unknown conflict strategy"):
        merge_schemas(base_schema, override_schema, conflict="merge_all")


def test_merge_does_not_mutate_base(base_schema, override_schema):
    original_fields = [dict(f) for f in base_schema["fields"]]
    merge_schemas(base_schema, override_schema)
    assert base_schema["fields"] == original_fields


def test_list_field_names_returns_ordered_names(base_schema):
    names = list_field_names(base_schema)
    assert names == ["first_name", "email"]


def test_list_field_names_raises_for_invalid_schema():
    with pytest.raises(SchemaMergerError):
        list_field_names({"title": "Missing fields"})
