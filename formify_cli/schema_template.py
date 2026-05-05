"""Schema template generator — produces starter JSON schema skeletons."""

from __future__ import annotations

from typing import Any

_BUILTIN_TEMPLATES: dict[str, dict[str, Any]] = {
    "contact": {
        "title": "Contact Form",
        "fields": [
            {"name": "name", "type": "text", "label": "Full Name", "required": True},
            {"name": "email", "type": "email", "label": "Email Address", "required": True},
            {"name": "message", "type": "textarea", "label": "Message", "required": True},
        ],
    },
    "login": {
        "title": "Login Form",
        "fields": [
            {"name": "username", "type": "text", "label": "Username", "required": True},
            {"name": "password", "type": "password", "label": "Password", "required": True},
        ],
    },
    "survey": {
        "title": "Survey Form",
        "fields": [
            {"name": "full_name", "type": "text", "label": "Full Name", "required": True},
            {"name": "rating", "type": "select", "label": "Rating", "required": True,
             "options": ["1", "2", "3", "4", "5"]},
            {"name": "comments", "type": "textarea", "label": "Comments", "required": False},
        ],
    },
    "registration": {
        "title": "Registration Form",
        "fields": [
            {"name": "first_name", "type": "text", "label": "First Name", "required": True},
            {"name": "last_name", "type": "text", "label": "Last Name", "required": True},
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "password", "type": "password", "label": "Password", "required": True},
            {"name": "agree", "type": "checkbox", "label": "I agree to the terms", "required": True},
        ],
    },
}


class SchemaTemplateError(Exception):
    """Raised when a template operation fails."""


def list_templates() -> list[str]:
    """Return sorted list of available built-in template names."""
    return sorted(_BUILTIN_TEMPLATES.keys())


def get_template(name: str) -> dict[str, Any]:
    """Return a deep copy of the named template schema.

    Args:
        name: Template name (case-insensitive).

    Raises:
        SchemaTemplateError: If the template name is unknown.
    """
    import copy

    key = name.strip().lower()
    if key not in _BUILTIN_TEMPLATES:
        available = ", ".join(list_templates())
        raise SchemaTemplateError(
            f"Unknown template '{name}'. Available templates: {available}."
        )
    return copy.deepcopy(_BUILTIN_TEMPLATES[key])


def scaffold_field(field_type: str, name: str, label: str | None = None) -> dict[str, Any]:
    """Create a minimal field dict for the given type.

    Args:
        field_type: The HTML field type (e.g. 'text', 'email').
        name: The field's name attribute.
        label: Optional label; defaults to a title-cased version of name.

    Returns:
        A field dict suitable for inclusion in a schema's 'fields' list.
    """
    if not name or not name.strip():
        raise SchemaTemplateError("Field name must not be empty.")
    if not field_type or not field_type.strip():
        raise SchemaTemplateError("Field type must not be empty.")
    return {
        "name": name.strip(),
        "type": field_type.strip().lower(),
        "label": label if label is not None else name.replace("_", " ").title(),
        "required": False,
    }
