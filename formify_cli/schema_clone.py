"""Deep clone and rename utilities for form schemas."""

import copy
import re
from typing import Optional


class SchemaCloneError(Exception):
    """Raised when schema cloning fails."""


def clone_schema(schema: dict, new_title: Optional[str] = None) -> dict:
    """Return a deep copy of *schema*, optionally overriding its title.

    Args:
        schema: A validated schema dict.
        new_title: If provided, replaces the ``title`` key in the clone.

    Returns:
        A completely independent deep copy of the schema.

    Raises:
        SchemaCloneError: If *schema* is not a dict.
    """
    if not isinstance(schema, dict):
        raise SchemaCloneError("schema must be a dict")
    cloned = copy.deepcopy(schema)
    if new_title is not None:
        if not isinstance(new_title, str) or not new_title.strip():
            raise SchemaCloneError("new_title must be a non-empty string")
        cloned["title"] = new_title
    return cloned


def rename_field(schema: dict, old_name: str, new_name: str) -> dict:
    """Return a new schema with a field renamed from *old_name* to *new_name*.

    Args:
        schema: A validated schema dict.
        old_name: Current ``name`` value of the field to rename.
        new_name: Replacement ``name`` value.

    Returns:
        A deep copy of the schema with the field renamed.

    Raises:
        SchemaCloneError: If the field is not found or *new_name* conflicts.
    """
    if not isinstance(schema, dict):
        raise SchemaCloneError("schema must be a dict")
    if not old_name or not new_name:
        raise SchemaCloneError("old_name and new_name must be non-empty strings")
    cloned = copy.deepcopy(schema)
    fields = cloned.get("fields", [])
    names = [f.get("name") for f in fields]
    if old_name not in names:
        raise SchemaCloneError(f"field '{old_name}' not found in schema")
    if new_name in names:
        raise SchemaCloneError(f"field '{new_name}' already exists in schema")
    for field in fields:
        if field.get("name") == old_name:
            field["name"] = new_name
            break
    return cloned


def prefix_field_names(schema: dict, prefix: str) -> dict:
    """Return a new schema where every field name is prefixed with *prefix*.

    Args:
        schema: A validated schema dict.
        prefix: String to prepend to each field name.

    Returns:
        A deep copy of the schema with all field names prefixed.

    Raises:
        SchemaCloneError: If *prefix* is empty or *schema* is invalid.
    """
    if not isinstance(schema, dict):
        raise SchemaCloneError("schema must be a dict")
    if not isinstance(prefix, str) or not prefix:
        raise SchemaCloneError("prefix must be a non-empty string")
    if not re.match(r'^[A-Za-z0-9_-]+$', prefix):
        raise SchemaCloneError("prefix must contain only alphanumeric characters, hyphens, or underscores")
    cloned = copy.deepcopy(schema)
    for field in cloned.get("fields", []):
        if "name" in field:
            field["name"] = f"{prefix}{field['name']}"
    return cloned
