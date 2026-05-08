"""schema_trimmer.py — Remove unused or empty fields from a schema."""

from __future__ import annotations

import copy
from typing import Any


class SchemaTrimmerError(Exception):
    """Raised when trimming cannot be performed."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaTrimmerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaTrimmerError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaTrimmerError("'fields' must be a list.")


def trim_empty_labels(schema: dict) -> dict:
    """Remove fields whose 'label' is an empty string or whitespace-only."""
    _check_schema(schema)
    result = copy.deepcopy(schema)
    result["fields"] = [
        f for f in result["fields"]
        if f.get("label", "x").strip() != ""
    ]
    return result


def trim_unknown_types(schema: dict, known_types: list[str] | None = None) -> dict:
    """Remove fields whose 'type' is not in the known types list."""
    _check_schema(schema)
    if known_types is None:
        known_types = ["text", "email", "password", "number", "textarea",
                       "select", "checkbox", "radio", "date", "tel", "url"]
    normalised = [t.lower() for t in known_types]
    result = copy.deepcopy(schema)
    result["fields"] = [
        f for f in result["fields"]
        if f.get("type", "").lower() in normalised
    ]
    return result


def trim_keys(schema: dict, allowed_keys: list[str] | None = None) -> dict:
    """Strip unrecognised keys from every field dict."""
    _check_schema(schema)
    if allowed_keys is None:
        allowed_keys = [
            "name", "type", "label", "required", "placeholder",
            "options", "depends_on", "depends_value", "min_length",
            "max_length", "pattern", "hint", "example", "description",
        ]
    allowed_set = set(allowed_keys)
    result = copy.deepcopy(schema)
    result["fields"] = [
        {k: v for k, v in field.items() if k in allowed_set}
        for field in result["fields"]
    ]
    return result


def trim_schema(schema: dict, known_types: list[str] | None = None,
                allowed_keys: list[str] | None = None) -> dict:
    """Apply all trimming passes in sequence and return a clean schema copy."""
    schema = trim_empty_labels(schema)
    schema = trim_unknown_types(schema, known_types)
    schema = trim_keys(schema, allowed_keys)
    return schema
