"""Export schemas to various formats (JSON, YAML summary, Markdown docs)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SchemaExportError(Exception):
    """Raised when schema export fails."""


_SUPPORTED_FORMATS = ("json", "markdown", "summary")


def list_export_formats() -> list[str]:
    """Return sorted list of supported export formats."""
    return sorted(_SUPPORTED_FORMATS)


def export_schema_as_json(schema: dict[str, Any], indent: int = 2) -> str:
    """Serialize schema back to a formatted JSON string."""
    if not isinstance(schema, dict):
        raise SchemaExportError("Schema must be a dict.")
    return json.dumps(schema, indent=indent)


def export_schema_as_markdown(schema: dict[str, Any]) -> str:
    """Generate a Markdown documentation string from a schema."""
    if not isinstance(schema, dict):
        raise SchemaExportError("Schema must be a dict.")
    title = schema.get("title", "Untitled Form")
    fields: list[dict] = schema.get("fields", [])
    lines: list[str] = [
        f"# {title}",
        "",
        "## Fields",
        "",
        "| Name | Type | Label | Required |",
        "|------|------|-------|----------|",
    ]
    for field in fields:
        name = field.get("name", "")
        ftype = field.get("type", "text")
        label = field.get("label", name)
        required = "Yes" if field.get("required") else "No"
        lines.append(f"| {name} | {ftype} | {label} | {required} |")
    return "\n".join(lines) + "\n"


def export_schema_as_summary(schema: dict[str, Any]) -> str:
    """Return a compact plain-text summary of the schema."""
    if not isinstance(schema, dict):
        raise SchemaExportError("Schema must be a dict.")
    title = schema.get("title", "Untitled Form")
    fields: list[dict] = schema.get("fields", [])
    required_count = sum(1 for f in fields if f.get("required"))
    lines = [
        f"Form: {title}",
        f"Fields: {len(fields)}",
        f"Required: {required_count}",
    ]
    return "\n".join(lines) + "\n"


def export_schema(schema: dict[str, Any], fmt: str) -> str:
    """Dispatch export to the requested format.

    Args:
        schema: Validated schema dict.
        fmt: One of 'json', 'markdown', 'summary'.

    Returns:
        Exported content as a string.

    Raises:
        SchemaExportError: For unknown format or invalid schema.
    """
    fmt = fmt.lower()
    if fmt == "json":
        return export_schema_as_json(schema)
    if fmt == "markdown":
        return export_schema_as_markdown(schema)
    if fmt == "summary":
        return export_schema_as_summary(schema)
    raise SchemaExportError(
        f"Unknown export format '{fmt}'. Choose from: {', '.join(list_export_formats())}."
    )


def export_schema_to_file(schema: dict[str, Any], fmt: str, path: str | Path, overwrite: bool = False) -> Path:
    """Export schema to a file on disk."""
    dest = Path(path)
    if dest.exists() and not overwrite:
        raise SchemaExportError(f"File already exists: {dest}. Use overwrite=True to replace.")
    content = export_schema(schema, fmt)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    return dest
