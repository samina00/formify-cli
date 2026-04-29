"""Tests for formify_cli.validator."""

import pytest
from formify_cli.validator import validate_form_data, ValidationError


SIMPLE_SCHEMA = {
    "title": "Test Form",
    "fields": [
        {"name": "username", "type": "text", "label": "Username", "required": True, "min_length": 3, "max_length": 20},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "age", "type": "number", "label": "Age", "required": False, "min": 0, "max": 120},
        {"name": "bio", "type": "textarea", "label": "Bio", "required": False, "max_length": 50},
        {
            "name": "role",
            "type": "select",
            "label": "Role",
            "required": False,
            "options": [{"value": "admin", "label": "Admin"}, {"value": "user", "label": "User"}],
        },
    ],
}


def test_valid_data_returns_no_errors():
    data = {"username": "alice", "email": "alice@example.com", "age": "30"}
    assert validate_form_data(SIMPLE_SCHEMA, data) == {}


def test_required_field_missing_returns_error():
    errors = validate_form_data(SIMPLE_SCHEMA, {"email": "a@b.com"})
    assert "username" in errors
    assert any("required" in e for e in errors["username"])


def test_invalid_email_returns_error():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "not-an-email"})
    assert "email" in errors


def test_valid_email_passes():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "alice@example.com"})
    assert "email" not in errors


def test_min_length_violation():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "ab", "email": "a@b.com"})
    assert "username" in errors
    assert any("3" in e for e in errors["username"])


def test_max_length_violation():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "a" * 21, "email": "a@b.com"})
    assert "username" in errors


def test_number_below_min():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "a@b.com", "age": "-1"})
    assert "age" in errors


def test_number_above_max():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "a@b.com", "age": "200"})
    assert "age" in errors


def test_invalid_number_string():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "a@b.com", "age": "old"})
    assert "age" in errors


def test_optional_empty_field_passes():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "a@b.com", "bio": ""})
    assert "bio" not in errors


def test_select_invalid_choice():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "a@b.com", "role": "superuser"})
    assert "role" in errors


def test_select_valid_choice():
    errors = validate_form_data(SIMPLE_SCHEMA, {"username": "alice", "email": "a@b.com", "role": "admin"})
    assert "role" not in errors


def test_multiple_errors_returned():
    errors = validate_form_data(SIMPLE_SCHEMA, {})
    assert "username" in errors
    assert "email" in errors
