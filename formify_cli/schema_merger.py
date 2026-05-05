"""Merge two JSON schema definitions into a single combined schema."""

from __future__ import annotations

from typing import Any


class SchemaMergerError(Exception):
    """Raised when schema merging fails."""


def merge_schemas(
    base: dict[str, Any],
    override: dict[str, Any],
    *,
    conflict: str = "override",
) -> dict[str, Any]:
    """Merge *override* schema into *base* schema and return a new schema.

    Parameters
    ----------
    base:
        The primary schema to merge into.
    override:
        The schema whose fields are merged on top of *base*.
    conflict:
        Strategy when both schemas define a field with the same name.
        ``"override"`` (default) replaces the base field with the override
        field.  ``"keep"`` retains the base field and ignores the override.
        ``"error"`` raises :class:`SchemaMergerError`.
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise SchemaMergerError("Both schemas must be dictionaries.")

    for schema, label in ((base, "base"), (override, "override")):
        if "fields" not in schema:
            raise SchemaMergerError(
                f"The {label} schema is missing the required 'fields' key."
            )
        if not isinstance(schema["fields"], list):
            raise SchemaMergerError(
                f"The {label} schema 'fields' value must be a list."
            )

    valid_strategies = {"override", "keep", "error"}
    if conflict not in valid_strategies:
        raise SchemaMergerError(
            f"Unknown conflict strategy '{conflict}'. "
            f"Choose one of: {', '.join(sorted(valid_strategies))}."
        )

    base_field_map: dict[str, dict[str, Any]] = {
        f["name"]: f for f in base["fields"] if isinstance(f, dict) and "name" in f
    }
    override_field_map: dict[str, dict[str, Any]] = {
        f["name"]: f for f in override["fields"] if isinstance(f, dict) and "name" in f
    }

    conflicts = set(base_field_map) & set(override_field_map)
    if conflicts and conflict == "error":
        names = ", ".join(sorted(conflicts))
        raise SchemaMergerError(
            f"Conflicting field names found: {names}. "
            "Resolve conflicts or choose a different strategy."
        )

    merged_fields: list[dict[str, Any]] = []

    # Keep all base fields, applying overrides where applicable.
    for name, field in base_field_map.items():
        if name in override_field_map and conflict == "override":
            merged_fields.append(dict(override_field_map[name]))
        else:
            merged_fields.append(dict(field))

    # Append fields that exist only in override.
    for name, field in override_field_map.items():
        if name not in base_field_map:
            merged_fields.append(dict(field))

    merged: dict[str, Any] = {
        **base,
        "title": override.get("title", base.get("title", "")),
        "fields": merged_fields,
    }
    return merged


def list_field_names(schema: dict[str, Any]) -> list[str]:
    """Return the ordered list of field names from *schema*."""
    if not isinstance(schema, dict) or "fields" not in schema:
        raise SchemaMergerError("Schema must be a dict with a 'fields' key.")
    return [
        f["name"]
        for f in schema["fields"]
        if isinstance(f, dict) and "name" in f
    ]
