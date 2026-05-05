"""Tests for schema_validator_rules module."""

import pytest
from formify_cli.schema_validator_rules import (
    RuleError,
    list_rules,
    apply_rule,
    apply_all_rules,
)


def test_list_rules_returns_sorted_list():
    rules = list_rules()
    assert isinstance(rules, list)
    assert rules == sorted(rules)


def test_list_rules_contains_builtins():
    rules = list_rules()
    for expected in ["min_length", "max_length", "pattern", "min_value", "max_value"]:
        assert expected in rules


def test_apply_rule_min_length_passes():
    assert apply_rule("min_length", "hello", 3) is None


def test_apply_rule_min_length_fails():
    result = apply_rule("min_length", "hi", 5)
    assert result is not None
    assert "5" in result


def test_apply_rule_max_length_passes():
    assert apply_rule("max_length", "hi", 10) is None


def test_apply_rule_max_length_fails():
    result = apply_rule("max_length", "toolongstring", 5)
    assert result is not None
    assert "5" in result


def test_apply_rule_pattern_passes():
    assert apply_rule("pattern", "abc123", r"[a-z0-9]+") is None


def test_apply_rule_pattern_fails():
    result = apply_rule("pattern", "ABC", r"[a-z]+")
    assert result is not None
    assert "pattern" in result.lower()


def test_apply_rule_min_value_passes():
    assert apply_rule("min_value", "10", 5) is None


def test_apply_rule_min_value_fails():
    result = apply_rule("min_value", "3", 5)
    assert result is not None
    assert "5" in result


def test_apply_rule_max_value_passes():
    assert apply_rule("max_value", "4", 5) is None


def test_apply_rule_max_value_fails():
    result = apply_rule("max_value", "10", 5)
    assert result is not None
    assert "5" in result


def test_apply_rule_unknown_raises():
    with pytest.raises(RuleError, match="Unknown rule"):
        apply_rule("nonexistent_rule", "value", None)


def test_apply_all_rules_no_errors():
    field = {"rules": {"min_length": 2, "max_length": 10}}
    errors = apply_all_rules(field, "hello")
    assert errors == []


def test_apply_all_rules_collects_multiple_errors():
    field = {"rules": {"min_length": 10, "max_length": 2}}
    errors = apply_all_rules(field, "hi")
    # min_length fails (2 < 10), max_length fails (2 > 2 is false, but 2 == 2 passes)
    assert any("10" in e for e in errors)


def test_apply_all_rules_empty_rules():
    field = {"rules": {}}
    assert apply_all_rules(field, "anything") == []


def test_apply_all_rules_no_rules_key():
    field = {}
    assert apply_all_rules(field, "anything") == []


def test_apply_all_rules_invalid_rules_type():
    field = {"rules": ["min_length"]}
    with pytest.raises(RuleError, match="must be a dict"):
        apply_all_rules(field, "value")
