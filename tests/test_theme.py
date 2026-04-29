"""Tests for formify_cli.theme module."""

import pytest
from formify_cli.theme import (
    Theme,
    ThemeError,
    BUILTIN_THEMES,
    get_theme,
    list_themes,
)


def test_list_themes_returns_all_builtins():
    themes = list_themes()
    assert "default" in themes
    assert "minimal" in themes
    assert "bootstrap" in themes


def test_get_theme_returns_theme_object():
    theme = get_theme("default")
    assert isinstance(theme, Theme)
    assert theme.name == "default"


def test_get_theme_case_insensitive():
    theme = get_theme("Bootstrap")
    assert theme.name == "bootstrap"


def test_get_theme_raises_for_unknown_theme():
    with pytest.raises(ThemeError, match="Unknown theme 'neon'"):
        get_theme("neon")


def test_theme_error_message_lists_available_themes():
    with pytest.raises(ThemeError, match="default"):
        get_theme("nonexistent")


def test_default_theme_has_expected_classes():
    theme = get_theme("default")
    assert theme.form_class == "form"
    assert theme.input_class == "form-control"
    assert theme.submit_class == "btn btn-primary"


def test_minimal_theme_has_minimal_classes():
    theme = get_theme("minimal")
    assert theme.form_class == ""
    assert theme.input_class == "input"
    assert theme.field_wrapper_class == "field"


def test_bootstrap_theme_has_extra_css():
    theme = get_theme("bootstrap")
    assert theme.extra_css is not None
    assert "bootstrap" in theme.extra_css


def test_default_theme_has_no_extra_css():
    theme = get_theme("default")
    assert theme.extra_css is None


def test_builtin_themes_dict_contains_three_entries():
    assert len(BUILTIN_THEMES) == 3


def test_theme_dataclass_fields_are_strings():
    theme = get_theme("minimal")
    assert isinstance(theme.label_class, str)
    assert isinstance(theme.error_class, str)
    assert isinstance(theme.textarea_class, str)
