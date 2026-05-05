"""Tests for formify_cli.schema_template."""

import pytest

from formify_cli.schema_template import (
    SchemaTemplateError,
    get_template,
    list_templates,
    scaffold_field,
)


# ---------------------------------------------------------------------------
# list_templates
# ---------------------------------------------------------------------------

def test_list_templates_returns_all_builtins():
    templates = list_templates()
    assert "contact" in templates
    assert "login" in templates
    assert "survey" in templates
    assert "registration" in templates


def test_list_templates_is_sorted():
    templates = list_templates()
    assert templates == sorted(templates)


def test_list_templates_returns_list_of_strings():
    templates = list_templates()
    assert isinstance(templates, list)
    assert all(isinstance(t, str) for t in templates)


# ---------------------------------------------------------------------------
# get_template
# ---------------------------------------------------------------------------

def test_get_template_returns_dict_with_title_and_fields():
    schema = get_template("contact")
    assert "title" in schema
    assert "fields" in schema
    assert isinstance(schema["fields"], list)


def test_get_template_is_case_insensitive():
    schema_lower = get_template("login")
    schema_upper = get_template("LOGIN")
    assert schema_lower == schema_upper


def test_get_template_returns_copy():
    schema_a = get_template("contact")
    schema_b = get_template("contact")
    schema_a["fields"].clear()
    assert len(schema_b["fields"]) > 0


def test_get_template_raises_for_unknown_template():
    with pytest.raises(SchemaTemplateError, match="Unknown template"):
        get_template("nonexistent_form")


def test_get_template_error_message_lists_available():
    with pytest.raises(SchemaTemplateError) as exc_info:
        get_template("ghost")
    assert "contact" in str(exc_info.value)


def test_get_template_survey_has_select_field():
    schema = get_template("survey")
    types = [f["type"] for f in schema["fields"]]
    assert "select" in types


def test_get_template_registration_has_checkbox():
    schema = get_template("registration")
    types = [f["type"] for f in schema["fields"]]
    assert "checkbox" in types


# ---------------------------------------------------------------------------
# scaffold_field
# ---------------------------------------------------------------------------

def test_scaffold_field_returns_dict_with_required_keys():
    field = scaffold_field("text", "first_name")
    assert "name" in field
    assert "type" in field
    assert "label" in field
    assert "required" in field


def test_scaffold_field_default_label_is_title_cased():
    field = scaffold_field("text", "first_name")
    assert field["label"] == "First Name"


def test_scaffold_field_custom_label_respected():
    field = scaffold_field("email", "email_addr", label="Your Email")
    assert field["label"] == "Your Email"


def test_scaffold_field_type_is_lowercased():
    field = scaffold_field("EMAIL", "contact_email")
    assert field["type"] == "email"


def test_scaffold_field_required_defaults_to_false():
    field = scaffold_field("text", "bio")
    assert field["required"] is False


def test_scaffold_field_raises_for_empty_name():
    with pytest.raises(SchemaTemplateError, match="name"):
        scaffold_field("text", "")


def test_scaffold_field_raises_for_empty_type():
    with pytest.raises(SchemaTemplateError, match="type"):
        scaffold_field("", "username")
