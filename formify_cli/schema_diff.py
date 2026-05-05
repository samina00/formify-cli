"""Schema diff utility: compare two JSON schemas and report structural differences."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class SchemaDiffError(Exception):
    """Raised when schema diff encounters invalid input."""


@dataclass
class DiffResult:
    added_fields: list[str] = field(default_factory=list)
    removed_fields: list[str] = field(default_factory=list)
    changed_fields: dict[str, dict[str, Any]] = field(default_factory=dict)

    @property
    def has_changes(self) -> bool:
        return bool(self.added_fields or self.removed_fields or self.changed_fields)

    def summary_line(self) -> str:
        parts = []
        if self.added_fields:
            parts.append(f"+{len(self.added_fields)} added")
        if self.removed_fields:
            parts.append(f"-{len(self.removed_fields)} removed")
        if self.changed_fields:
            parts.append(f"~{len(self.changed_fields)} changed")
        return ", ".join(parts) if parts else "No changes"


_TRACKED_KEYS = {"type", "label", "required", "options", "min_length", "max_length", "placeholder"}


def _schema_field_map(schema: dict) -> dict[str, dict]:
    """Return a dict keyed by field name from a validated schema."""
    return {f["name"]: f for f in schema.get("fields", [])}


def diff_schemas(old_schema: dict, new_schema: dict) -> DiffResult:
    """Compare two schema dicts and return a DiffResult."""
    for label, schema in (("old", old_schema), ("new", new_schema)):
        if not isinstance(schema, dict):
            raise SchemaDiffError(f"The {label} schema must be a dict.")
        if "fields" not in schema:
            raise SchemaDiffError(f"The {label} schema is missing 'fields'.")

    old_fields = _schema_field_map(old_schema)
    new_fields = _schema_field_map(new_schema)

    result = DiffResult()
    result.added_fields = [n for n in new_fields if n not in old_fields]
    result.removed_fields = [n for n in old_fields if n not in new_fields]

    for name in old_fields:
        if name not in new_fields:
            continue
        old_f = old_fields[name]
        new_f = new_fields[name]
        changes: dict[str, Any] = {}
        for key in _TRACKED_KEYS:
            old_val = old_f.get(key)
            new_val = new_f.get(key)
            if old_val != new_val:
                changes[key] = {"old": old_val, "new": new_val}
        if changes:
            result.changed_fields[name] = changes

    return result
