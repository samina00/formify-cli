"""Tests for formify_cli.schema_diff."""

import pytest

from formify_cli.schema_diff import (
    DiffResult,
    SchemaDiffError,
    diff_schemas,
)


BASE_SCHEMA = {
    "title": "Contact",
    "fields": [
        {"name": "name", "type": "text", "label": "Name", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
    ],
}


def _clone(schema):
    import copy
    return copy.deepcopy(schema)


def test_no_changes_returns_empty_result():
    result = diff_schemas(BASE_SCHEMA, _clone(BASE_SCHEMA))
    assert not result.has_changes
    assert result.summary_line() == "No changes"


def test_added_field_detected():
    new_schema = _clone(BASE_SCHEMA)
    new_schema["fields"].append({"name": "phone", "type": "text", "label": "Phone"})
    result = diff_schemas(BASE_SCHEMA, new_schema)
    assert "phone" in result.added_fields
    assert result.has_changes


def test_removed_field_detected():
    new_schema = _clone(BASE_SCHEMA)
    new_schema["fields"] = [f for f in new_schema["fields"] if f["name"] != "email"]
    result = diff_schemas(BASE_SCHEMA, new_schema)
    assert "email" in result.removed_fields


def test_changed_field_type_detected():
    new_schema = _clone(BASE_SCHEMA)
    new_schema["fields"][0]["type"] = "textarea"
    result = diff_schemas(BASE_SCHEMA, new_schema)
    assert "name" in result.changed_fields
    assert result.changed_fields["name"]["type"] == {"old": "text", "new": "textarea"}


def test_changed_required_flag_detected():
    new_schema = _clone(BASE_SCHEMA)
    new_schema["fields"][1]["required"] = False
    result = diff_schemas(BASE_SCHEMA, new_schema)
    assert "email" in result.changed_fields
    assert "required" in result.changed_fields["email"]


def test_summary_line_reflects_all_change_types():
    new_schema = _clone(BASE_SCHEMA)
    new_schema["fields"][0]["label"] = "Full Name"
    new_schema["fields"].append({"name": "age", "type": "number", "label": "Age"})
    new_schema["fields"] = [f for f in new_schema["fields"] if f["name"] != "email"]
    result = diff_schemas(BASE_SCHEMA, new_schema)
    summary = result.summary_line()
    assert "+1 added" in summary
    assert "-1 removed" in summary
    assert "~1 changed" in summary


def test_raises_if_old_schema_not_dict():
    with pytest.raises(SchemaDiffError, match="old"):
        diff_schemas("not a dict", BASE_SCHEMA)


def test_raises_if_new_schema_missing_fields():
    with pytest.raises(SchemaDiffError, match="new"):
        diff_schemas(BASE_SCHEMA, {"title": "Oops"})


def test_unchanged_fields_not_in_changed_dict():
    result = diff_schemas(BASE_SCHEMA, _clone(BASE_SCHEMA))
    assert result.changed_fields == {}


def test_diff_result_has_changes_false_when_empty():
    result = DiffResult()
    assert not result.has_changes
