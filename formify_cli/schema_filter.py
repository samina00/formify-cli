"""Filter schema fields by various criteria."""

from __future__ import annotations

from typing import Any


class SchemaFilterError(Exception):
    """Raised when schema filtering fails."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaFilterError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaFilterError("Schema must contain a 'fields' key.")


def filter_by_required(schema: dict, *, required: bool = True) -> list[dict]:
    """Return fields whose 'required' flag matches the given value."""
    _check_schema(schema)
    return [
        f for f in schema["fields"]
        if bool(f.get("required", False)) == required
    ]


def filter_by_type(schema: dict, field_type: str) -> list[dict]:
    """Return fields whose type matches *field_type* (case-insensitive)."""
    _check_schema(schema)
    if not field_type or not field_type.strip():
        raise SchemaFilterError("field_type must be a non-empty string.")
    needle = field_type.strip().lower()
    return [f for f in schema["fields"] if f.get("type", "").lower() == needle]


def filter_by_name_prefix(schema: dict, prefix: str) -> list[dict]:
    """Return fields whose 'name' starts with *prefix*."""
    _check_schema(schema)
    if not isinstance(prefix, str) or not prefix:
        raise SchemaFilterError("prefix must be a non-empty string.")
    return [f for f in schema["fields"] if f.get("name", "").startswith(prefix)]


def exclude_fields(schema: dict, names: list[str]) -> dict:
    """Return a shallow copy of *schema* with named fields removed."""
    _check_schema(schema)
    if not isinstance(names, list):
        raise SchemaFilterError("names must be a list of strings.")
    name_set = set(names)
    filtered = [f for f in schema["fields"] if f.get("name") not in name_set]
    return {**schema, "fields": filtered}


def keep_fields(schema: dict, names: list[str]) -> dict:
    """Return a shallow copy of *schema* containing only the named fields."""
    _check_schema(schema)
    if not isinstance(names, list):
        raise SchemaFilterError("names must be a list of strings.")
    name_set = set(names)
    filtered = [f for f in schema["fields"] if f.get("name") in name_set]
    return {**schema, "fields": filtered}
