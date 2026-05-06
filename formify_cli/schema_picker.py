"""schema_picker.py — Select a subset of fields from a schema by name list."""

from __future__ import annotations

from typing import Any


class SchemaPickerError(Exception):
    """Raised when field picking fails."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaPickerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaPickerError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaPickerError("Schema 'fields' must be a list.")


def pick_fields(schema: dict, names: list[str]) -> dict:
    """Return a new schema containing only fields whose 'name' is in *names*.

    Order of the returned fields follows the order in *names*.
    Unknown names are silently ignored.
    """
    _check_schema(schema)
    if not isinstance(names, list):
        raise SchemaPickerError("names must be a list of strings.")
    if not names:
        raise SchemaPickerError("names list must not be empty.")

    field_map: dict[str, dict] = {
        f["name"]: f for f in schema["fields"] if isinstance(f, dict) and "name" in f
    }

    picked = [field_map[n] for n in names if n in field_map]

    result = {k: v for k, v in schema.items() if k != "fields"}
    result["fields"] = [dict(f) for f in picked]
    return result


def omit_fields(schema: dict, names: list[str]) -> dict:
    """Return a new schema with the named fields removed."""
    _check_schema(schema)
    if not isinstance(names, list):
        raise SchemaPickerError("names must be a list of strings.")
    if not names:
        raise SchemaPickerError("names list must not be empty.")

    exclude = set(names)
    kept = [
        dict(f)
        for f in schema["fields"]
        if isinstance(f, dict) and f.get("name") not in exclude
    ]

    result = {k: v for k, v in schema.items() if k != "fields"}
    result["fields"] = kept
    return result


def list_field_names(schema: dict) -> list[str]:
    """Return a sorted list of all field names in the schema."""
    _check_schema(schema)
    return sorted(
        f["name"]
        for f in schema["fields"]
        if isinstance(f, dict) and "name" in f
    )
