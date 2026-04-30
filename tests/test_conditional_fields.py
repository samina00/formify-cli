"""Tests for formify_cli.conditional_fields."""

import pytest
from formify_cli.conditional_fields import (
    ConditionalFieldError,
    evaluate_condition,
    filter_visible_fields,
    has_condition,
    render_condition_attrs,
    validate_condition,
)


ALL_FIELDS = [
    {"name": "contact_method", "type": "select"},
    {"name": "email", "type": "email", "depends_on": "contact_method", "depends_value": "email"},
    {"name": "phone", "type": "text", "depends_on": "contact_method", "depends_value": "phone"},
    {"name": "message", "type": "textarea"},
]


def test_has_condition_true_when_depends_on_present():
    field = {"name": "email", "depends_on": "contact_method", "depends_value": "email"}
    assert has_condition(field) is True


def test_has_condition_false_when_no_depends_on():
    field = {"name": "message", "type": "textarea"}
    assert has_condition(field) is False


def test_validate_condition_passes_for_known_field():
    field = ALL_FIELDS[1]
    validate_condition(field, ALL_FIELDS)  # should not raise


def test_validate_condition_raises_for_unknown_dependency():
    field = {"name": "email", "depends_on": "nonexistent", "depends_value": "yes"}
    with pytest.raises(ConditionalFieldError, match="unknown field 'nonexistent'"):
        validate_condition(field, ALL_FIELDS)


def test_validate_condition_raises_if_depends_value_missing():
    field = {"name": "email", "depends_on": "contact_method"}
    with pytest.raises(ConditionalFieldError, match="missing 'depends_value'"):
        validate_condition(field, ALL_FIELDS)


def test_validate_condition_noop_for_unconditional_field():
    field = {"name": "message", "type": "textarea"}
    validate_condition(field, ALL_FIELDS)  # should not raise


def test_evaluate_condition_true_when_value_matches():
    field = {"name": "email", "depends_on": "contact_method", "depends_value": "email"}
    assert evaluate_condition(field, {"contact_method": "email"}) is True


def test_evaluate_condition_false_when_value_differs():
    field = {"name": "email", "depends_on": "contact_method", "depends_value": "email"}
    assert evaluate_condition(field, {"contact_method": "phone"}) is False


def test_evaluate_condition_true_for_unconditional_field():
    field = {"name": "message", "type": "textarea"}
    assert evaluate_condition(field, {}) is True


def test_evaluate_condition_coerces_to_string():
    field = {"name": "extra", "depends_on": "count", "depends_value": "1"}
    assert evaluate_condition(field, {"count": 1}) is True


def test_filter_visible_fields_returns_matching_and_unconditional():
    visible = filter_visible_fields(ALL_FIELDS, {"contact_method": "email"})
    names = [f["name"] for f in visible]
    assert "contact_method" in names
    assert "email" in names
    assert "message" in names
    assert "phone" not in names


def test_filter_visible_fields_empty_data_hides_conditional():
    visible = filter_visible_fields(ALL_FIELDS, {})
    names = [f["name"] for f in visible]
    assert "email" not in names
    assert "phone" not in names
    assert "contact_method" in names


def test_render_condition_attrs_returns_data_attributes():
    field = {"name": "email", "depends_on": "contact_method", "depends_value": "email"}
    attrs = render_condition_attrs(field)
    assert 'data-depends-on="contact_method"' in attrs
    assert 'data-depends-value="email"' in attrs


def test_render_condition_attrs_empty_for_unconditional_field():
    field = {"name": "message", "type": "textarea"}
    assert render_condition_attrs(field) == ""
