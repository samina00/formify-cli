"""Schema field sorter — reorder fields in a schema by various criteria."""

from __future__ import annotations

import copy
from typing import List


class SchemaSorterError(Exception):
    """Raised when sorting cannot be performed."""


def _check_schema(schema: object) -> None:
    if not isinstance(schema, dict):
        raise SchemaSorterError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaSorterError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaSorterError("'fields' must be a list.")


def sort_by_name(schema: dict, reverse: bool = False) -> dict:
    """Return a new schema with fields sorted alphabetically by 'name'."""
    _check_schema(schema)
    result = copy.deepcopy(schema)
    result["fields"] = sorted(
        result["fields"],
        key=lambda f: f.get("name", "").lower(),
        reverse=reverse,
    )
    return result


def sort_by_type(schema: dict, reverse: bool = False) -> dict:
    """Return a new schema with fields sorted alphabetically by 'type'."""
    _check_schema(schema)
    result = copy.deepcopy(schema)
    result["fields"] = sorted(
        result["fields"],
        key=lambda f: f.get("type", "").lower(),
        reverse=reverse,
    )
    return result


def sort_required_first(schema: dict) -> dict:
    """Return a new schema with required fields listed before optional ones."""
    _check_schema(schema)
    result = copy.deepcopy(schema)
    result["fields"] = sorted(
        result["fields"],
        key=lambda f: (0 if f.get("required") else 1),
    )
    return result


def sort_by_label(schema: dict, reverse: bool = False) -> dict:
    """Return a new schema with fields sorted alphabetically by 'label'."""
    _check_schema(schema)
    result = copy.deepcopy(schema)
    result["fields"] = sorted(
        result["fields"],
        key=lambda f: f.get("label", "").lower(),
        reverse=reverse,
    )
    return result


def reorder_fields(schema: dict, order: List[str]) -> dict:
    """Return a new schema with fields reordered to match the given name list.

    Fields not present in *order* are appended at the end in their original
    relative order.  Names in *order* that don't match any field are ignored.
    """
    _check_schema(schema)
    if not isinstance(order, list):
        raise SchemaSorterError("'order' must be a list of field name strings.")
    result = copy.deepcopy(schema)
    field_map = {f["name"]: f for f in result["fields"] if "name" in f}
    ordered = [field_map[name] for name in order if name in field_map]
    ordered_names = set(order)
    remainder = [f for f in result["fields"] if f.get("name") not in ordered_names]
    result["fields"] = ordered + remainder
    return result
