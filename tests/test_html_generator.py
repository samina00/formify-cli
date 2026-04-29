"""Tests for the HTML form generator module."""

import pytest

from formify_cli.html_generator import HTMLGenerationError, generate_form, _escape


MINIMAL_SCHEMA = {
    "title": "Contact",
    "fields": [
        {"name": "email", "type": "email", "label": "Email", "required": True},
    ],
}


def test_generate_form_contains_form_tag():
    html = generate_form(MINIMAL_SCHEMA)
    assert "<form" in html
    assert "</form>" in html


def test_generate_form_includes_title_as_heading():
    html = generate_form(MINIMAL_SCHEMA)
    assert "<h2>Contact</h2>" in html


def test_generate_form_aria_label_on_form():
    html = generate_form(MINIMAL_SCHEMA)
    assert 'aria-label="Contact"' in html


def test_generate_form_renders_input_field():
    html = generate_form(MINIMAL_SCHEMA)
    assert 'type="email"' in html
    assert 'name="email"' in html
    assert 'id="email"' in html


def test_generate_form_required_field_has_required_attr():
    html = generate_form(MINIMAL_SCHEMA)
    assert "required" in html
    assert 'aria-required="true"' in html


def test_generate_form_optional_field_has_no_required_attr():
    schema = {
        "title": "Test",
        "fields": [{"name": "bio", "type": "textarea", "required": False}],
    }
    html = generate_form(schema)
    assert "required" not in html


def test_generate_form_renders_textarea():
    schema = {
        "title": "Test",
        "fields": [{"name": "message", "type": "textarea"}],
    }
    html = generate_form(schema)
    assert "<textarea" in html
    assert "</textarea>" in html


def test_generate_form_renders_select_with_options():
    schema = {
        "title": "Test",
        "fields": [
            {"name": "country", "type": "select", "options": ["US", "UK", "CA"]}
        ],
    }
    html = generate_form(schema)
    assert "<select" in html
    assert "<option value=\"US\">US</option>" in html
    assert "-- Select --" in html


def test_generate_form_renders_submit_button():
    html = generate_form(MINIMAL_SCHEMA)
    assert '<button type="submit">Submit</button>' in html


def test_generate_form_label_for_matches_input_id():
    html = generate_form(MINIMAL_SCHEMA)
    assert 'for="email"' in html
    assert 'id="email"' in html


def test_generate_form_raises_for_unsupported_type():
    schema = {
        "title": "Bad",
        "fields": [{"name": "file", "type": "file"}],
    }
    with pytest.raises(HTMLGenerationError, match="Unsupported field type"):
        generate_form(schema)


def test_escape_special_characters():
    assert _escape('<script>') == "&lt;script&gt;"
    assert _escape('Say "hi"') == "Say &quot;hi&quot;"
    assert _escape("it's") == "it&#39;s"
    assert _escape("a & b") == "a &amp; b"
