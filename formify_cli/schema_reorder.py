"""Reorder fields within a schema by explicit list, alphabetically, or by type priority."""

from __future__ import annotations

import copy
from typing import Dict, List, Any


class SchemaReorderError(Exception):
    """Raised when schema reordering fails."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaReorderError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaReorderError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaReorderError("'fields' must be a list.")


def reorder_by_list(schema: Dict, order: List[str]) -> Dict:
    """Return a new schema with fields reordered according to *order*.

    Fields not mentioned in *order* are appended at the end in their
    original relative order.
    """
    _check_schema(schema)
    if not order:
        raise SchemaReorderError("order list must not be empty.")

    fields = copy.deepcopy(schema["fields"])
    field_map = {f["name"]: f for f in fields if "name" in f}

    reordered: List[Dict] = []
    seen: set = set()
    for name in order:
        if name in field_map:
            reordered.append(field_map[name])
            seen.add(name)

    for field in fields:
        if field.get("name") not in seen:
            reordered.append(field)

    result = copy.deepcopy(schema)
    result["fields"] = reordered
    return result


def reorder_alphabetically(schema: Dict, reverse: bool = False) -> Dict:
    """Return a new schema with fields sorted alphabetically by name."""
    _check_schema(schema)
    fields = copy.deepcopy(schema["fields"])
    sorted_fields = sorted(fields, key=lambda f: f.get("name", ""), reverse=reverse)
    result = copy.deepcopy(schema)
    result["fields"] = sorted_fields
    return result


_TYPE_PRIORITY: Dict[str, int] = {
    "text": 0,
    "email": 1,
    "password": 2,
    "number": 3,
    "tel": 4,
    "url": 5,
    "select": 6,
    "textarea": 7,
    "checkbox": 8,
    "radio": 9,
}


def reorder_by_type_priority(schema: Dict) -> Dict:
    """Return a new schema with fields ordered by built-in type priority.

    Unknown types are placed after all known types.
    """
    _check_schema(schema)
    fields = copy.deepcopy(schema["fields"])
    sorted_fields = sorted(
        fields,
        key=lambda f: _TYPE_PRIORITY.get(f.get("type", "").lower(), 999),
    )
    result = copy.deepcopy(schema)
    result["fields"] = sorted_fields
    return result


def list_field_names(schema: Dict) -> List[str]:
    """Return ordered list of field names from the schema."""
    _check_schema(schema)
    return [f["name"] for f in schema["fields"] if "name" in f]
