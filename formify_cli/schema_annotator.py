"""Annotate schema fields with metadata such as hints, examples, and descriptions."""

from __future__ import annotations

from typing import Any


class SchemaAnnotatorError(Exception):
    """Raised when annotation operations fail."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaAnnotatorError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaAnnotatorError("Schema must contain a 'fields' key.")


def annotate_field(
    field: dict,
    *,
    hint: str | None = None,
    example: str | None = None,
    description: str | None = None,
) -> dict:
    """Return a copy of *field* with annotation keys added or updated."""
    if not isinstance(field, dict):
        raise SchemaAnnotatorError("Field must be a dict.")
    updated = dict(field)
    if hint is not None:
        updated["hint"] = str(hint)
    if example is not None:
        updated["example"] = str(example)
    if description is not None:
        updated["description"] = str(description)
    return updated


def annotate_schema_field(
    schema: dict,
    field_name: str,
    *,
    hint: str | None = None,
    example: str | None = None,
    description: str | None = None,
) -> dict:
    """Return a new schema with annotations applied to the named field."""
    _check_schema(schema)
    fields = schema["fields"]
    names = [f.get("name") for f in fields]
    if field_name not in names:
        raise SchemaAnnotatorError(
            f"Field '{field_name}' not found in schema."
        )
    new_fields = [
        annotate_field(f, hint=hint, example=example, description=description)
        if f.get("name") == field_name
        else dict(f)
        for f in fields
    ]
    return {**schema, "fields": new_fields}


def strip_annotations(schema: dict) -> dict:
    """Return a new schema with all annotation keys removed from every field."""
    _check_schema(schema)
    annotation_keys = {"hint", "example", "description"}
    new_fields = [
        {k: v for k, v in f.items() if k not in annotation_keys}
        for f in schema["fields"]
    ]
    return {**schema, "fields": new_fields}


def list_annotated_fields(schema: dict) -> list[str]:
    """Return names of fields that have at least one annotation key."""
    _check_schema(schema)
    annotation_keys = {"hint", "example", "description"}
    return [
        f["name"]
        for f in schema["fields"]
        if annotation_keys & set(f.keys()) and "name" in f
    ]
