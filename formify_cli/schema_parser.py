"""Parse and validate JSON schema definitions for form generation."""

import json
from pathlib import Path
from typing import Any

SUPPORTED_FIELD_TYPES = {"text", "email", "number", "password", "textarea", "select", "checkbox", "radio"}

REQUIRED_FIELD_KEYS = {"name", "type", "label"}


class SchemaValidationError(Exception):
    """Raised when a JSON schema fails validation."""
    pass


def load_schema(path: str) -> dict[str, Any]:
    """Load and parse a JSON schema file.

    Args:
        path: Path to the JSON schema file.

    Returns:
        Parsed schema as a dictionary.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        SchemaValidationError: If the JSON is invalid or malformed.
    """
    schema_path = Path(path)
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")

    try:
        with schema_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise SchemaValidationError(f"Invalid JSON in schema file: {exc}") from exc

    validate_schema(data)
    return data


def validate_schema(schema: dict[str, Any]) -> None:
    """Validate the structure of a form schema.

    Args:
        schema: The schema dictionary to validate.

    Raises:
        SchemaValidationError: If the schema structure is invalid.
    """
    if not isinstance(schema, dict):
        raise SchemaValidationError("Schema must be a JSON object.")

    if "fields" not in schema:
        raise SchemaValidationError("Schema must contain a 'fields' key.")

    if not isinstance(schema["fields"], list) or len(schema["fields"]) == 0:
        raise SchemaValidationError("'fields' must be a non-empty list.")

    for idx, field in enumerate(schema["fields"]):
        _validate_field(field, idx)


def _validate_field(field: dict[str, Any], idx: int) -> None:
    """Validate a single field definition."""
    if not isinstance(field, dict):
        raise SchemaValidationError(f"Field at index {idx} must be an object.")

    missing = REQUIRED_FIELD_KEYS - field.keys()
    if missing:
        raise SchemaValidationError(
            f"Field at index {idx} is missing required keys: {missing}"
        )

    if field["type"] not in SUPPORTED_FIELD_TYPES:
        raise SchemaValidationError(
            f"Field '{field['name']}' has unsupported type '{field['type']}'. "
            f"Supported types: {SUPPORTED_FIELD_TYPES}"
        )

    if field["type"] in {"select", "radio"} and "options" not in field:
        raise SchemaValidationError(
            f"Field '{field['name']}' of type '{field['type']}' must include 'options'."
        )
