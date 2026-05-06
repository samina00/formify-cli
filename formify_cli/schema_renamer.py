"""Rename fields and update internal references within a schema."""

from __future__ import annotations

import copy
from typing import Dict, List


class SchemaRenamerError(Exception):
    """Raised when a rename operation cannot be completed."""


def _check_schema(schema: object) -> None:
    if not isinstance(schema, dict):
        raise SchemaRenamerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaRenamerError("Schema must contain a 'fields' key.")


def rename_field(schema: dict, old_name: str, new_name: str) -> dict:
    """Return a new schema with *old_name* field renamed to *new_name*.

    Also updates any ``depends_on`` references that point to *old_name*.
    """
    _check_schema(schema)
    if not old_name or not isinstance(old_name, str):
        raise SchemaRenamerError("old_name must be a non-empty string.")
    if not new_name or not isinstance(new_name, str):
        raise SchemaRenamerError("new_name must be a non-empty string.")

    field_names = [f["name"] for f in schema["fields"] if "name" in f]
    if old_name not in field_names:
        raise SchemaRenamerError(f"Field '{old_name}' not found in schema.")
    if new_name in field_names:
        raise SchemaRenamerError(f"Field '{new_name}' already exists in schema.")

    result = copy.deepcopy(schema)
    for field in result["fields"]:
        if field.get("name") == old_name:
            field["name"] = new_name
        # Update conditional field references
        if field.get("depends_on") == old_name:
            field["depends_on"] = new_name
    return result


def rename_fields_bulk(schema: dict, rename_map: Dict[str, str]) -> dict:
    """Rename multiple fields at once using a mapping of {old_name: new_name}.

    Renames are applied atomically — all names are validated before any change.
    """
    _check_schema(schema)
    if not isinstance(rename_map, dict) or not rename_map:
        raise SchemaRenamerError("rename_map must be a non-empty dict.")

    field_names = [f["name"] for f in schema["fields"] if "name" in f]
    for old, new in rename_map.items():
        if not old or not isinstance(old, str):
            raise SchemaRenamerError("All keys in rename_map must be non-empty strings.")
        if not new or not isinstance(new, str):
            raise SchemaRenamerError("All values in rename_map must be non-empty strings.")
        if old not in field_names:
            raise SchemaRenamerError(f"Field '{old}' not found in schema.")

    result = copy.deepcopy(schema)
    for field in result["fields"]:
        name = field.get("name")
        if name in rename_map:
            field["name"] = rename_map[name]
        dep = field.get("depends_on")
        if dep in rename_map:
            field["depends_on"] = rename_map[dep]
    return result


def list_field_names(schema: dict) -> List[str]:
    """Return a list of all field names in the schema."""
    _check_schema(schema)
    return [f["name"] for f in schema["fields"] if "name" in f]
