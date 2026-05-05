"""Tests for rule_renderer module."""

import pytest
from formify_cli.rule_renderer import (
    rules_to_html_attrs,
    render_rule_attrs,
    describe_rules,
    render_rule_hint,
)


def test_rules_to_html_attrs_min_length():
    field = {"rules": {"min_length": 5}}
    attrs = rules_to_html_attrs(field)
    assert attrs == {"minlength": "5"}


def test_rules_to_html_attrs_max_length():
    field = {"rules": {"max_length": 100}}
    attrs = rules_to_html_attrs(field)
    assert attrs == {"maxlength": "100"}


def test_rules_to_html_attrs_pattern():
    field = {"rules": {"pattern": "[a-z]+"}}
    attrs = rules_to_html_attrs(field)
    assert attrs == {"pattern": "[a-z]+"}


def test_rules_to_html_attrs_min_max_value():
    field = {"rules": {"min_value": 1, "max_value": 10}}
    attrs = rules_to_html_attrs(field)
    assert attrs["min"] == "1"
    assert attrs["max"] == "10"


def test_rules_to_html_attrs_unknown_rule_ignored():
    field = {"rules": {"unknown_rule": 42}}
    attrs = rules_to_html_attrs(field)
    assert attrs == {}


def test_rules_to_html_attrs_empty_rules():
    field = {"rules": {}}
    assert rules_to_html_attrs(field) == {}


def test_rules_to_html_attrs_no_rules_key():
    field = {}
    assert rules_to_html_attrs(field) == {}


def test_rules_to_html_attrs_invalid_type_returns_empty():
    field = {"rules": "not-a-dict"}
    assert rules_to_html_attrs(field) == {}


def test_render_rule_attrs_returns_string():
    field = {"rules": {"min_length": 3}}
    result = render_rule_attrs(field)
    assert 'minlength="3"' in result


def test_render_rule_attrs_empty_when_no_rules():
    field = {}
    assert render_rule_attrs(field) == ""


def test_render_rule_attrs_starts_with_space_when_present():
    field = {"rules": {"max_length": 50}}
    result = render_rule_attrs(field)
    assert result.startswith(" ")


def test_describe_rules_min_length():
    field = {"rules": {"min_length": 8}}
    descs = describe_rules(field)
    assert any("8" in d for d in descs)


def test_describe_rules_multiple():
    field = {"rules": {"min_length": 2, "max_length": 20}}
    descs = describe_rules(field)
    assert len(descs) == 2


def test_describe_rules_empty():
    field = {}
    assert describe_rules(field) == []


def test_render_rule_hint_returns_span():
    field = {"rules": {"min_length": 5}}
    html = render_rule_hint(field, "name-hint")
    assert '<span' in html
    assert 'id="name-hint"' in html
    assert 'field-hint' in html


def test_render_rule_hint_empty_when_no_rules():
    field = {}
    assert render_rule_hint(field, "x-hint") == ""
