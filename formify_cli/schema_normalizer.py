"""Normalize schema fields to a canonical, consistent structure."""

from __future__ import annotations

from typing import Any


class SchemaNormalizerError(Exception):
    """Raised when normalization fails."""


_FIELD_DEFAULTS: dict[str, Any] = {
    "required": False,
    "placeholder": "",
    "help_text": "",
    "options": [],
}

_KNOWN_TYPES = {"text", "email", "password", "number", "textarea", "select", "checkbox", "radio", "date", "url", "tel"}


def normalize_field(field: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *field* with all optional keys filled in with defaults."""
    if not isinstance(field, dict):
        raise SchemaNormalizerError("Each field must be a dict.")
    if "name" not in field:
        raise SchemaNormalizerError("Field is missing required key 'name'.")
    if "type" not in field:
        raise SchemaNormalizerError(f"Field '{field.get('name')}' is missing required key 'type'.")
    if "label" not in field:
        raise SchemaNormalizerError(f"Field '{field['name']}' is missing required key 'label'.")

    normalized = {**_FIELD_DEFAULTS, **field}
    normalized["type"] = normalized["type"].strip().lower()
    normalized["name"] = normalized["name"].strip()
    normalized["label"] = normalized["label"].strip()
    normalized["required"] = bool(normalized["required"])
    if not isinstance(normalized["options"], list):
        normalized["options"] = []
    return normalized


def normalize_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Return a fully normalized copy of *schema*."""
    if not isinstance(schema, dict):
        raise SchemaNormalizerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaNormalizerError("Schema is missing required key 'fields'.")
    if not isinstance(schema["fields"], list) or len(schema["fields"]) == 0:
        raise SchemaNormalizerError("Schema 'fields' must be a non-empty list.")

    normalized_fields = [normalize_field(f) for f in schema["fields"]]
    return {
        "title": schema.get("title", "").strip(),
        "fields": normalized_fields,
    }


def list_unknown_types(schema: dict[str, Any]) -> list[str]:
    """Return field names whose type is not in the known set (after normalization)."""
    normalized = normalize_schema(schema)
    return [
        f["name"]
        for f in normalized["fields"]
        if f["type"] not in _KNOWN_TYPES
    ]
