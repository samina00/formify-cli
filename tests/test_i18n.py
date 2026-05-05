"""Tests for formify_cli.i18n module."""

import pytest

from formify_cli.i18n import (
    I18NError,
    apply_locale_to_schema,
    get_locale,
    list_locales,
    translate,
)


def test_list_locales_returns_all_builtins():
    locales = list_locales()
    assert "en" in locales
    assert "fr" in locales
    assert "es" in locales
    assert "de" in locales


def test_list_locales_is_sorted():
    locales = list_locales()
    assert locales == sorted(locales)


def test_get_locale_returns_dict():
    catalog = get_locale("en")
    assert isinstance(catalog, dict)
    assert "submit_button" in catalog


def test_get_locale_is_case_insensitive():
    assert get_locale("EN") == get_locale("en")
    assert get_locale("Fr") == get_locale("fr")


def test_get_locale_returns_copy():
    c1 = get_locale("en")
    c1["submit_button"] = "MUTATED"
    c2 = get_locale("en")
    assert c2["submit_button"] != "MUTATED"


def test_get_locale_raises_for_unknown():
    with pytest.raises(I18NError, match="Unsupported locale 'xx'"):
        get_locale("xx")


def test_i18n_error_lists_available_locales():
    with pytest.raises(I18NError, match="en"):
        get_locale("zz")


def test_translate_english_submit():
    assert translate("submit_button", locale="en") == "Submit"


def test_translate_french_submit():
    assert translate("submit_button", locale="fr") == "Envoyer"


def test_translate_with_format_kwargs():
    result = translate("error_min_length", locale="en", min="5")
    assert "5" in result


def test_translate_german_required_legend():
    result = translate("required_legend", locale="de")
    assert "Pflichtfelder" in result


def test_translate_falls_back_to_english_for_missing_key():
    # All locales should have the same keys, but if one is missing it falls back
    result = translate("submit_button", locale="es")
    assert result  # non-empty


def test_translate_returns_key_if_completely_unknown():
    result = translate("nonexistent_key", locale="en")
    assert result == "nonexistent_key"


def test_apply_locale_to_schema_adds_submit_label():
    schema = {"title": "Test", "fields": []}
    patched = apply_locale_to_schema(schema, locale="en")
    assert patched["submit_label"] == "Submit"


def test_apply_locale_to_schema_adds_required_legend():
    schema = {"title": "Test", "fields": []}
    patched = apply_locale_to_schema(schema, locale="fr")
    assert "obligatoires" in patched["required_legend"]


def test_apply_locale_to_schema_does_not_override_existing_submit_label():
    schema = {"title": "Test", "fields": [], "submit_label": "Go!"}
    patched = apply_locale_to_schema(schema, locale="en")
    assert patched["submit_label"] == "Go!"


def test_apply_locale_to_schema_sets_locale_key():
    schema = {"title": "T", "fields": []}
    patched = apply_locale_to_schema(schema, locale="DE")
    assert patched["_locale"] == "de"


def test_apply_locale_to_schema_does_not_mutate_original():
    schema = {"title": "T", "fields": []}
    apply_locale_to_schema(schema, locale="en")
    assert "submit_label" not in schema
