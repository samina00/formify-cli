"""Tests for formify_cli.schema_duplicates."""

import pytest
from formify_cli.schema_duplicates import (
    SchemaDuplicatesError,
    find_duplicate_names,
    find_duplicate_labels,
    has_duplicates,
    duplicates_report,
)


@pytest.fixture
def clean_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "email", "label": "Email", "type": "email"},
            {"name": "name", "label": "Full Name", "type": "text"},
        ],
    }


@pytest.fixture
def dup_name_schema():
    return {
        "title": "Dup Form",
        "fields": [
            {"name": "email", "label": "Email", "type": "email"},
            {"name": "email", "label": "Another Email", "type": "text"},
            {"name": "name", "label": "Name", "type": "text"},
        ],
    }


@pytest.fixture
def dup_label_schema():
    return {
        "title": "Label Form",
        "fields": [
            {"name": "field1", "label": "Contact", "type": "text"},
            {"name": "field2", "label": "Contact", "type": "email"},
        ],
    }


def test_find_duplicate_names_returns_empty_for_clean(clean_schema):
    assert find_duplicate_names(clean_schema) == []


def test_find_duplicate_names_detects_dup(dup_name_schema):
    result = find_duplicate_names(dup_name_schema)
    assert "email" in result


def test_find_duplicate_names_returns_sorted(dup_name_schema):
    dup_name_schema["fields"].append({"name": "age", "label": "Age", "type": "text"})
    dup_name_schema["fields"].append({"name": "age", "label": "Age2", "type": "text"})
    result = find_duplicate_names(dup_name_schema)
    assert result == sorted(result)


def test_find_duplicate_labels_returns_empty_for_clean(clean_schema):
    assert find_duplicate_labels(clean_schema) == []


def test_find_duplicate_labels_detects_dup(dup_label_schema):
    result = find_duplicate_labels(dup_label_schema)
    assert "Contact" in result


def test_has_duplicates_false_for_clean(clean_schema):
    assert has_duplicates(clean_schema) is False


def test_has_duplicates_true_for_dup(dup_name_schema):
    assert has_duplicates(dup_name_schema) is True


def test_duplicates_report_no_issues(clean_schema):
    report = duplicates_report(clean_schema)
    assert "No duplicate field names" in report
    assert "No duplicate field labels" in report


def test_duplicates_report_lists_dup_names(dup_name_schema):
    report = duplicates_report(dup_name_schema)
    assert "email" in report


def test_duplicates_report_lists_dup_labels(dup_label_schema):
    report = duplicates_report(dup_label_schema)
    assert "Contact" in report


def test_find_duplicate_names_raises_for_non_dict():
    with pytest.raises(SchemaDuplicatesError, match="must be a dict"):
        find_duplicate_names(["not", "a", "dict"])


def test_find_duplicate_names_raises_for_missing_fields_key():
    with pytest.raises(SchemaDuplicatesError, match="'fields'"):
        find_duplicate_names({"title": "No Fields"})


def test_find_duplicate_labels_raises_for_non_list_fields():
    with pytest.raises(SchemaDuplicatesError, match="must be a list"):
        find_duplicate_labels({"fields": "not-a-list"})
