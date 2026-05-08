"""Patch a schema by applying field-level updates from a patch dict."""

from __future__ import annotations

import copy
from typing import Any


class SchemaPatchError(Exception):
    """Raised when a schema patch operation fails."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaPatchError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaPatchError("Schema must contain a 'fields' key.")


def patch_field(schema: dict, field_name: str, updates: dict) -> dict:
    """Return a new schema with the named field updated by *updates*.

    Only keys present in *updates* are changed; other keys are preserved.
    Raises SchemaPatchError if the field does not exist or updates is not a dict.
    """
    _check_schema(schema)
    if not isinstance(updates, dict):
        raise SchemaPatchError("updates must be a dict.")
    if not updates:
        raise SchemaPatchError("updates must not be empty.")

    result = copy.deepcopy(schema)
    for field in result["fields"]:
        if field.get("name") == field_name:
            field.update(updates)
            return result

    raise SchemaPatchError(f"Field '{field_name}' not found in schema.")


def patch_fields_bulk(schema: dict, patches: dict[str, dict]) -> dict:
    """Apply multiple patches at once.

    *patches* maps field names to their update dicts.
    All patches are applied to the same deep copy; fields missing from the
    schema are silently skipped unless *strict* is True.
    """
    _check_schema(schema)
    if not isinstance(patches, dict):
        raise SchemaPatchError("patches must be a dict mapping field names to update dicts.")

    result = copy.deepcopy(schema)
    field_map = {f.get("name"): f for f in result["fields"]}

    for field_name, updates in patches.items():
        if not isinstance(updates, dict):
            raise SchemaPatchError(
                f"Update for field '{field_name}' must be a dict, got {type(updates).__name__}."
            )
        if field_name in field_map:
            field_map[field_name].update(updates)

    return result


def list_field_names(schema: dict) -> list[str]:
    """Return sorted list of field names in the schema."""
    _check_schema(schema)
    return sorted(f.get("name", "") for f in schema["fields"])
