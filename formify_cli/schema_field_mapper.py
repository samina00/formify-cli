"""Map fields from one schema to another using a name mapping dictionary."""

from __future__ import annotations

import copy
from typing import Dict, List


class SchemaFieldMapperError(Exception):
    """Raised when field mapping fails."""


def _check_schema(schema: object) -> None:
    if not isinstance(schema, dict):
        raise SchemaFieldMapperError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaFieldMapperError("Schema must contain a 'fields' key.")


def map_field_names(schema: dict, mapping: Dict[str, str]) -> dict:
    """Return a new schema with field names renamed according to *mapping*.

    Keys in *mapping* are old names; values are new names.  Fields whose
    names are not present in *mapping* are left unchanged.  Any
    ``depends_on`` references that point to a renamed field are updated
    automatically.
    """
    _check_schema(schema)
    if not isinstance(mapping, dict):
        raise SchemaFieldMapperError("Mapping must be a dict.")
    if not mapping:
        raise SchemaFieldMapperError("Mapping must not be empty.")

    result = copy.deepcopy(schema)
    new_fields: List[dict] = []
    for field in result["fields"]:
        field = dict(field)
        old_name = field.get("name")
        if old_name in mapping:
            new_name = mapping[old_name]
            if not isinstance(new_name, str) or not new_name.strip():
                raise SchemaFieldMapperError(
                    f"Mapped name for '{old_name}' must be a non-empty string."
                )
            field["name"] = new_name
        # Update depends_on if it points to a renamed field
        if "depends_on" in field and field["depends_on"] in mapping:
            field["depends_on"] = mapping[field["depends_on"]]
        new_fields.append(field)
    result["fields"] = new_fields
    return result


def build_name_index(schema: dict) -> Dict[str, int]:
    """Return a dict mapping each field name to its position index."""
    _check_schema(schema)
    return {f["name"]: i for i, f in enumerate(schema["fields"]) if "name" in f}


def list_field_names(schema: dict) -> List[str]:
    """Return an ordered list of all field names in *schema*."""
    _check_schema(schema)
    return [f["name"] for f in schema["fields"] if "name" in f]
