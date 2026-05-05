"""Tests for formify_cli.schema_lint."""

import pytest

from formify_cli.schema_lint import SchemaLintError, LintResult, lint_schema


_VALID_SCHEMA = {
    "title": "Contact",
    "fields": [
        {"name": "full_name", "type": "text", "label": "Full Name"},
        {"name": "email", "type": "email", "label": "Email"},
    ],
}


def test_lint_clean_schema_has_no_issues():
    result = lint_schema(_VALID_SCHEMA)
    assert not result.has_issues


def test_lint_raises_for_non_dict():
    with pytest.raises(SchemaLintError):
        lint_schema(["not", "a", "dict"])


def test_lint_raises_for_missing_fields_key():
    with pytest.raises(SchemaLintError):
        lint_schema({"title": "Oops"})


def test_lint_warns_on_unknown_type():
    schema = {"title": "T", "fields": [{"name": "x", "type": "fancywidget", "label": "X"}]}
    result = lint_schema(schema)
    assert any("unknown field type" in w for w in result.warnings)


def test_lint_warns_on_missing_label():
    schema = {"title": "T", "fields": [{"name": "x", "type": "text", "label": ""}]}
    result = lint_schema(schema)
    assert any("label" in w for w in result.warnings)


def test_lint_warns_on_missing_name():
    schema = {"title": "T", "fields": [{"type": "text", "label": "Field"}]}
    result = lint_schema(schema)
    assert any("missing 'name'" in w for w in result.warnings)


def test_lint_warns_on_duplicate_names():
    schema = {
        "title": "T",
        "fields": [
            {"name": "dup", "type": "text", "label": "A"},
            {"name": "dup", "type": "text", "label": "B"},
        ],
    }
    result = lint_schema(schema)
    assert any("Duplicate" in w for w in result.warnings)


def test_lint_hints_missing_title():
    schema = {"fields": [{"name": "x", "type": "text", "label": "X"}]}
    result = lint_schema(schema)
    assert any("title" in h for h in result.hints)


def test_lint_hints_placeholder_for_email():
    schema = {"title": "T", "fields": [{"name": "em", "type": "email", "label": "Email"}]}
    result = lint_schema(schema)
    assert any("placeholder" in h for h in result.hints)


def test_lint_warns_select_without_options():
    schema = {"title": "T", "fields": [{"name": "s", "type": "select", "label": "Pick"}]}
    result = lint_schema(schema)
    assert any("options" in w for w in result.warnings)


def test_summary_line_no_issues():
    r = LintResult()
    assert r.summary_line() == "No issues found."


def test_summary_line_with_issues():
    r = LintResult(warnings=["w1"], hints=["h1"])
    assert "1 warning" in r.summary_line()
    assert "1 hint" in r.summary_line()


def test_as_text_contains_labels():
    r = LintResult(warnings=["bad thing"], hints=["try this"])
    text = r.as_text()
    assert "[WARN]" in text
    assert "[HINT]" in text
    assert "bad thing" in text
    assert "try this" in text
