"""Compute statistics and summary metrics from a form schema."""

from __future__ import annotations

from typing import Any

KNOWN_TYPES = {"text", "email", "password", "number", "tel", "url",
               "textarea", "select", "checkbox", "radio", "date"}


class SchemaStatsError(ValueError):
    """Raised when statistics cannot be computed from the given schema."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaStatsError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaStatsError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaStatsError("'fields' must be a list.")


def count_fields(schema: dict) -> int:
    """Return the total number of fields in the schema."""
    _check_schema(schema)
    return len(schema["fields"])


def count_required_fields(schema: dict) -> int:
    """Return the number of fields marked as required."""
    _check_schema(schema)
    return sum(1 for f in schema["fields"] if f.get("required") is True)


def count_by_type(schema: dict) -> dict[str, int]:
    """Return a mapping of field type -> count."""
    _check_schema(schema)
    result: dict[str, int] = {}
    for field in schema["fields"]:
        ftype = str(field.get("type", "unknown")).lower()
        result[ftype] = result.get(ftype, 0) + 1
    return result


def list_unknown_types(schema: dict) -> list[str]:
    """Return a sorted list of field types not in the known-types set."""
    _check_schema(schema)
    return sorted(
        {str(f.get("type", "")).lower()
         for f in schema["fields"]
         if str(f.get("type", "")).lower() not in KNOWN_TYPES}
    )


def list_fields_without_label(schema: dict) -> list[str]:
    """Return a list of field names that are missing a non-empty label.

    Fields without a ``name`` key are identified by their index (e.g.
    ``"<field 2>"``) so callers can locate them easily.
    """
    _check_schema(schema)
    missing: list[str] = []
    for i, field in enumerate(schema["fields"]):
        label = field.get("label", "")
        if not isinstance(label, str) or not label.strip():
            identifier = field.get("name") or f"<field {i}>"
            missing.append(str(identifier))
    return missing


def compute_stats(schema: dict) -> dict:
    """Return a full statistics dict for the schema."""
    _check_schema(schema)
    total = count_fields(schema)
    required = count_required_fields(schema)
    by_type = count_by_type(schema)
    unknown = list_unknown_types(schema)
    return {
        "title": schema.get("title", ""),
        "total_fields": total,
        "required_fields": required,
        "optional_fields": total - required,
        "types": by_type,
        "unknown_types": unknown,
    }
