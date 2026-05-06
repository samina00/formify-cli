"""Search and filter fields within a JSON schema definition."""

from typing import Any


class SchemaSearchError(Exception):
    """Raised when schema search operations fail."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaSearchError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaSearchError("Schema must contain a 'fields' key.")


def search_by_type(schema: dict, field_type: str) -> list[dict]:
    """Return all fields matching the given type (case-insensitive)."""
    _check_schema(schema)
    if not isinstance(field_type, str) or not field_type.strip():
        raise SchemaSearchError("field_type must be a non-empty string.")
    needle = field_type.strip().lower()
    return [
        f for f in schema["fields"]
        if isinstance(f, dict) and f.get("type", "").lower() == needle
    ]


def search_by_name(schema: dict, name: str) -> dict | None:
    """Return the first field whose 'name' matches exactly, or None."""
    _check_schema(schema)
    if not isinstance(name, str) or not name.strip():
        raise SchemaSearchError("name must be a non-empty string.")
    for field in schema["fields"]:
        if isinstance(field, dict) and field.get("name") == name.strip():
            return field
    return None


def search_by_label(schema: dict, keyword: str) -> list[dict]:
    """Return all fields whose label contains the keyword (case-insensitive)."""
    _check_schema(schema)
    if not isinstance(keyword, str) or not keyword.strip():
        raise SchemaSearchError("keyword must be a non-empty string.")
    needle = keyword.strip().lower()
    return [
        f for f in schema["fields"]
        if isinstance(f, dict) and needle in f.get("label", "").lower()
    ]


def search_required_fields(schema: dict) -> list[dict]:
    """Return all fields marked as required."""
    _check_schema(schema)
    return [
        f for f in schema["fields"]
        if isinstance(f, dict) and f.get("required") is True
    ]


def filter_fields(schema: dict, **criteria: Any) -> list[dict]:
    """Return fields matching ALL provided key=value criteria."""
    _check_schema(schema)
    results = []
    for field in schema["fields"]:
        if not isinstance(field, dict):
            continue
        if all(field.get(k) == v for k, v in criteria.items()):
            results.append(field)
    return results
