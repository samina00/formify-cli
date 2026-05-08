"""Tests for schema_validator_report module."""

import pytest
from formify_cli.schema_validator_report import (
    FieldRuleReport,
    FieldRuleResult,
    FieldRuleReportError,
    validate_field_rules,
    validate_schema_rules,
)


@pytest.fixture
def email_field():
    return {"name": "email", "type": "email", "min_length": 5, "max_length": 50}


@pytest.fixture
def simple_schema():
    return {
        "title": "Test Form",
        "fields": [
            {"name": "username", "type": "text", "min_length": 3, "max_length": 20},
            {"name": "age", "type": "number", "min_value": 0, "max_value": 120},
        ],
    }


def test_validate_field_rules_all_pass(email_field):
    report = validate_field_rules(email_field, "user@example.com", "email")
    assert report.passed


def test_validate_field_rules_min_length_fail(email_field):
    report = validate_field_rules(email_field, "a@b", "email")
    assert not report.passed
    failures = report.failures()
    assert any(r.rule == "min_length" for r in failures)


def test_validate_field_rules_max_length_fail(email_field):
    report = validate_field_rules(email_field, "a" * 60 + "@x.com", "email")
    assert not report.passed
    failures = report.failures()
    assert any(r.rule == "max_length" for r in failures)


def test_validate_field_rules_no_rules_returns_empty_report():
    field_def = {"name": "note", "type": "text"}
    report = validate_field_rules(field_def, "hello", "note")
    assert report.passed
    assert len(report.results) == 0


def test_validate_field_rules_raises_for_non_dict():
    with pytest.raises(FieldRuleReportError):
        validate_field_rules("not a dict", "value", "field")


def test_field_rule_report_summary_no_results():
    report = FieldRuleReport(results=[])
    assert report.summary_line() == "No rules evaluated."


def test_field_rule_report_summary_all_pass():
    results = [FieldRuleResult("f", "min_length", True)]
    report = FieldRuleReport(results=results)
    assert "All 1 rule(s) passed" in report.summary_line()


def test_field_rule_report_summary_with_failures():
    results = [
        FieldRuleResult("f", "min_length", False, "too short"),
        FieldRuleResult("f", "max_length", True),
    ]
    report = FieldRuleReport(results=results)
    assert "1/2" in report.summary_line()


def test_field_rule_report_as_text_contains_field_name():
    results = [FieldRuleResult("username", "min_length", False, "too short")]
    report = FieldRuleReport(results=results)
    text = report.as_text()
    assert "username" in text
    assert "FAIL" in text
    assert "too short" in text


def test_field_rule_report_as_text_pass_entry():
    results = [FieldRuleResult("username", "max_length", True)]
    report = FieldRuleReport(results=results)
    text = report.as_text()
    assert "PASS" in text


def test_validate_schema_rules_returns_report_per_field(simple_schema):
    data = {"username": "alice", "age": 25}
    reports = validate_schema_rules(simple_schema, data)
    assert "username" in reports
    assert "age" in reports


def test_validate_schema_rules_all_pass(simple_schema):
    data = {"username": "alice", "age": 25}
    reports = validate_schema_rules(simple_schema, data)
    assert all(r.passed for r in reports.values())


def test_validate_schema_rules_detects_failure(simple_schema):
    data = {"username": "ab", "age": 25}  # too short
    reports = validate_schema_rules(simple_schema, data)
    assert not reports["username"].passed


def test_validate_schema_rules_raises_for_non_dict_schema():
    with pytest.raises(FieldRuleReportError):
        validate_schema_rules("bad", {})


def test_validate_schema_rules_raises_for_non_dict_data(simple_schema):
    with pytest.raises(FieldRuleReportError):
        validate_schema_rules(simple_schema, "bad")
