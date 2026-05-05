"""Tests for formify_cli.form_validator_report."""

import pytest

from formify_cli.form_validator_report import (
    ReportError,
    ValidationReport,
    build_report,
)


SAMPLE_SCHEMA = {
    "title": "Contact",
    "fields": [
        {"name": "name", "type": "text", "label": "Name", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "message", "type": "textarea", "label": "Message", "required": False},
    ],
}


def test_build_report_all_valid():
    report = build_report(SAMPLE_SCHEMA, {})
    assert report.total_fields == 3
    assert report.passed_fields == 3
    assert report.failed_fields == 0
    assert report.is_valid is True


def test_build_report_with_errors():
    errors = {"email": ["Invalid email format."]}
    report = build_report(SAMPLE_SCHEMA, errors)
    assert report.failed_fields == 1
    assert report.passed_fields == 2
    assert report.is_valid is False


def test_build_report_multiple_errors():
    errors = {
        "name": ["This field is required."],
        "email": ["Invalid email format.", "Too short."],
    }
    report = build_report(SAMPLE_SCHEMA, errors)
    assert report.failed_fields == 2
    assert len(report.errors["email"]) == 2


def test_build_report_ignores_empty_error_lists():
    errors = {"name": [], "email": ["Bad email."]}
    report = build_report(SAMPLE_SCHEMA, errors)
    assert "name" not in report.errors
    assert "email" in report.errors
    assert report.failed_fields == 1


def test_build_report_raises_for_invalid_schema():
    with pytest.raises(ReportError, match="schema must be a dict"):
        build_report("not a dict", {})


def test_build_report_raises_for_missing_fields_key():
    with pytest.raises(ReportError, match="'fields' key"):
        build_report({"title": "No fields"}, {})


def test_build_report_raises_for_invalid_errors_type():
    with pytest.raises(ReportError, match="validation_errors must be a dict"):
        build_report(SAMPLE_SCHEMA, ["error"])


def test_summary_line_passed():
    report = ValidationReport(total_fields=3, passed_fields=3, failed_fields=0)
    assert "PASSED" in report.summary_line()
    assert "3/3" in report.summary_line()


def test_summary_line_failed():
    report = ValidationReport(
        total_fields=3,
        passed_fields=2,
        failed_fields=1,
        errors={"email": ["Invalid."]},
    )
    assert "FAILED" in report.summary_line()
    assert "2/3" in report.summary_line()


def test_as_text_no_errors():
    report = build_report(SAMPLE_SCHEMA, {})
    text = report.as_text()
    assert "PASSED" in text
    assert "Errors" not in text


def test_as_text_with_errors():
    errors = {"email": ["Invalid email format."]}
    report = build_report(SAMPLE_SCHEMA, errors)
    text = report.as_text()
    assert "FAILED" in text
    assert "[email]" in text
    assert "Invalid email format." in text
