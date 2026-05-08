"""schema_field_counter.py — Count and summarise fields by various criteria."""

from __future__ import annotations

from typing import Dict, List


class SchemaFieldCounterError(Exception):
    """Raised when field counting operations fail."""


def _check_schema(schema: object) -> None:
    if not isinstance(schema, dict):
        raise SchemaFieldCounterError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaFieldCounterError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaFieldCounterError("'fields' must be a list.")


def count_by_required(schema: dict) -> Dict[str, int]:
    """Return counts split by required vs optional."""
    _check_schema(schema)
    required = sum(1 for f in schema["fields"] if f.get("required", False))
    optional = len(schema["fields"]) - required
    return {"required": required, "optional": optional}


def count_by_type(schema: dict) -> Dict[str, int]:
    """Return a mapping of field type -> count."""
    _check_schema(schema)
    counts: Dict[str, int] = {}
    for field in schema["fields"]:
        ftype = str(field.get("type", "unknown")).lower()
        counts[ftype] = counts.get(ftype, 0) + 1
    return counts


def count_with_placeholder(schema: dict) -> int:
    """Return the number of fields that have a non-empty placeholder."""
    _check_schema(schema)
    return sum(
        1 for f in schema["fields"]
        if f.get("placeholder", "").strip()
    )


def count_with_label(schema: dict) -> int:
    """Return the number of fields that have a non-empty label."""
    _check_schema(schema)
    return sum(
        1 for f in schema["fields"]
        if f.get("label", "").strip()
    )


def field_type_list(schema: dict) -> List[str]:
    """Return a sorted list of unique field types present in the schema."""
    _check_schema(schema)
    return sorted({str(f.get("type", "unknown")).lower() for f in schema["fields"]})


def summary(schema: dict) -> Dict[str, object]:
    """Return a full summary dict of field counts."""
    _check_schema(schema)
    req = count_by_required(schema)
    return {
        "total": len(schema["fields"]),
        "required": req["required"],
        "optional": req["optional"],
        "with_placeholder": count_with_placeholder(schema),
        "with_label": count_with_label(schema),
        "by_type": count_by_type(schema),
        "unique_types": field_type_list(schema),
    }
