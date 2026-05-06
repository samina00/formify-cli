"""Flatten nested or grouped schema fields into a single-level field list."""

from __future__ import annotations

import copy
from typing import Any


class SchemaFlattenerError(Exception):
    """Raised when schema flattening fails."""


def flatten_schema(schema: dict[str, Any], separator: str = "_") -> dict[str, Any]:
    """Return a new schema with all group fields expanded into top-level fields.

    Fields of type 'group' must have a 'fields' key containing a list of
    sub-fields.  Each sub-field is promoted to the top level with its name
    prefixed by the group name and *separator*.

    Args:
        schema: A validated schema dict.
        separator: String used to join group name and sub-field name.

    Returns:
        A deep-copied schema dict with no group-type fields.

    Raises:
        SchemaFlattenerError: If *schema* is not a dict, lacks a 'fields' key,
            or a group field is malformed.
    """
    if not isinstance(schema, dict):
        raise SchemaFlattenerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaFlattenerError("Schema must contain a 'fields' key.")
    if not isinstance(separator, str) or not separator:
        raise SchemaFlattenerError("Separator must be a non-empty string.")

    result = copy.deepcopy(schema)
    result["fields"] = _flatten_fields(result["fields"], separator=separator)
    return result


def _flatten_fields(
    fields: list[dict[str, Any]],
    prefix: str = "",
    separator: str = "_",
) -> list[dict[str, Any]]:
    """Recursively flatten a list of fields."""
    flat: list[dict[str, Any]] = []
    for field in fields:
        if not isinstance(field, dict):
            raise SchemaFlattenerError(f"Each field must be a dict, got: {type(field).__name__}")
        if field.get("type") == "group":
            sub_fields = field.get("fields")
            if not isinstance(sub_fields, list) or not sub_fields:
                raise SchemaFlattenerError(
                    f"Group field '{field.get('name', '?')}' must have a non-empty 'fields' list."
                )
            group_prefix = (prefix + separator + field["name"]) if prefix else field["name"]
            flat.extend(_flatten_fields(sub_fields, prefix=group_prefix, separator=separator))
        else:
            promoted = copy.deepcopy(field)
            if prefix:
                promoted["name"] = prefix + separator + field.get("name", "")
            flat.append(promoted)
    return flat


def list_field_names(schema: dict[str, Any]) -> list[str]:
    """Return a sorted list of field names from a (possibly already flat) schema.

    Raises:
        SchemaFlattenerError: If *schema* is invalid.
    """
    if not isinstance(schema, dict):
        raise SchemaFlattenerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaFlattenerError("Schema must contain a 'fields' key.")
    return sorted(f["name"] for f in schema["fields"] if isinstance(f, dict) and "name" in f)
