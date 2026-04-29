"""Tests for formify_cli.field_defaults."""

import pytest

from formify_cli.field_defaults import (
    FieldDefaultsError,
    apply_defaults_to_field,
    get_defaults_for_type,
    get_placeholder_hint,
    list_supported_types,
)


# ---------------------------------------------------------------------------
# get_defaults_for_type
# ---------------------------------------------------------------------------

def test_get_defaults_returns_dict_for_known_type():
    result = get_defaults_for_type("email")
    assert isinstance(result, dict)
    assert result["autocomplete"] == "email"


def test_get_defaults_is_case_insensitive():
    assert get_defaults_for_type("EMAIL") == get_defaults_for_type("email")


def test_get_defaults_returns_copy():
    a = get_defaults_for_type("text")
    b = get_defaults_for_type("text")
    a["extra"] = "mutated"
    assert "extra" not in b


def test_get_defaults_raises_for_unknown_type():
    with pytest.raises(FieldDefaultsError, match="Unknown field type"):
        get_defaults_for_type("fancywidget")


# ---------------------------------------------------------------------------
# get_placeholder_hint
# ---------------------------------------------------------------------------

def test_placeholder_hint_for_email():
    assert get_placeholder_hint("email") == "you@example.com"


def test_placeholder_hint_for_url():
    assert get_placeholder_hint("url") == "https://example.com"


def test_placeholder_hint_returns_none_for_text():
    assert get_placeholder_hint("text") is None


def test_placeholder_hint_returns_none_for_unknown():
    assert get_placeholder_hint("fancywidget") is None


# ---------------------------------------------------------------------------
# apply_defaults_to_field
# ---------------------------------------------------------------------------

def test_apply_defaults_injects_autocomplete_for_email():
    field = {"name": "user_email", "type": "email", "label": "Email"}
    enriched = apply_defaults_to_field(field)
    assert enriched["autocomplete"] == "email"


def test_apply_defaults_does_not_overwrite_existing_key():
    field = {"name": "u", "type": "email", "autocomplete": "off"}
    enriched = apply_defaults_to_field(field)
    assert enriched["autocomplete"] == "off"


def test_apply_defaults_injects_placeholder_hint():
    field = {"name": "site", "type": "url"}
    enriched = apply_defaults_to_field(field)
    assert enriched["placeholder"] == "https://example.com"


def test_apply_defaults_does_not_overwrite_existing_placeholder():
    field = {"name": "site", "type": "url", "placeholder": "Enter URL"}
    enriched = apply_defaults_to_field(field)
    assert enriched["placeholder"] == "Enter URL"


def test_apply_defaults_falls_back_to_text_type():
    field = {"name": "bio", "type": "text"}
    enriched = apply_defaults_to_field(field)
    assert enriched["spellcheck"] == "false"


def test_apply_defaults_original_field_unchanged():
    field = {"name": "phone", "type": "tel"}
    original_keys = set(field.keys())
    apply_defaults_to_field(field)
    assert set(field.keys()) == original_keys


# ---------------------------------------------------------------------------
# list_supported_types
# ---------------------------------------------------------------------------

def test_list_supported_types_returns_sorted_list():
    types = list_supported_types()
    assert types == sorted(types)


def test_list_supported_types_includes_common_types():
    types = list_supported_types()
    for t in ("text", "email", "password", "select", "textarea"):
        assert t in types
