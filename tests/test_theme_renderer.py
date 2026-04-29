"""Tests for formify_cli.theme_renderer module."""

import pytest
from formify_cli.theme import get_theme
from formify_cli.theme_renderer import (
    render_css_link,
    apply_theme_to_field,
    render_themed_form_open,
    render_themed_submit,
    build_themed_form,
)


SIMPLE_SCHEMA = {
    "title": "Contact",
    "submit_label": "Send",
    "fields": [
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "message", "type": "textarea", "label": "Message"},
    ],
}


def test_render_css_link_returns_link_tag():
    html = render_css_link("https://example.com/style.css")
    assert html.startswith('<link rel="stylesheet"')
    assert "https://example.com/style.css" in html


def test_render_css_link_escapes_url():
    html = render_css_link("https://example.com/style.css?v=1&amp;x=2")
    assert "<script>" not in html


def test_apply_theme_to_field_adds_class_keys():
    theme = get_theme("default")
    result = apply_theme_to_field({"name": "x", "type": "text"}, theme)
    assert "input_class" in result
    assert "label_class" in result
    assert "wrapper_class" in result


def test_apply_theme_select_uses_select_class():
    theme = get_theme("bootstrap")
    result = apply_theme_to_field({"name": "x", "type": "select"}, theme)
    assert result["input_class"] == theme.select_class


def test_apply_theme_textarea_uses_textarea_class():
    theme = get_theme("default")
    result = apply_theme_to_field({"name": "x", "type": "textarea"}, theme)
    assert result["input_class"] == theme.textarea_class


def test_render_themed_form_open_includes_aria_label():
    theme = get_theme("default")
    html = render_themed_form_open(SIMPLE_SCHEMA, theme)
    assert 'aria-label="Contact"' in html


def test_render_themed_form_open_includes_class():
    theme = get_theme("bootstrap")
    html = render_themed_form_open(SIMPLE_SCHEMA, theme)
    assert 'class="needs-validation"' in html


def test_render_themed_form_open_minimal_no_class_attr():
    theme = get_theme("minimal")
    html = render_themed_form_open(SIMPLE_SCHEMA, theme)
    assert 'class=' not in html


def test_render_themed_submit_contains_label():
    theme = get_theme("default")
    html = render_themed_submit("Go!", theme)
    assert "Go!" in html
    assert 'type="submit"' in html


def test_render_themed_submit_includes_class():
    theme = get_theme("bootstrap")
    html = render_themed_submit("Submit", theme)
    assert 'class="btn btn-primary"' in html


def test_build_themed_form_contains_title():
    html = build_themed_form(SIMPLE_SCHEMA, "default")
    assert "<h1>Contact</h1>" in html


def test_build_themed_form_contains_form_tags():
    html = build_themed_form(SIMPLE_SCHEMA, "default")
    assert "<form" in html
    assert "</form>" in html


def test_build_themed_form_bootstrap_includes_css_link():
    html = build_themed_form(SIMPLE_SCHEMA, "bootstrap")
    assert '<link rel="stylesheet"' in html
    assert "bootstrap" in html


def test_build_themed_form_default_no_css_link():
    html = build_themed_form(SIMPLE_SCHEMA, "default")
    assert '<link rel="stylesheet"' not in html
