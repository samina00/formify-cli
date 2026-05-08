"""schema_tagger.py — Add, remove, and query tags on schema fields."""

from __future__ import annotations

import copy
from typing import Dict, List


class SchemaTaggerError(Exception):
    """Raised for schema tagging errors."""


def _check_schema(schema: object) -> None:
    if not isinstance(schema, dict):
        raise SchemaTaggerError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaTaggerError("Schema must contain a 'fields' key.")


def add_tag(schema: dict, field_name: str, tag: str) -> dict:
    """Return a new schema with *tag* added to the named field's tag list."""
    _check_schema(schema)
    tag = tag.strip()
    if not tag:
        raise SchemaTaggerError("Tag must be a non-empty string.")
    result = copy.deepcopy(schema)
    for field in result["fields"]:
        if field.get("name") == field_name:
            tags: List[str] = field.setdefault("tags", [])
            if tag not in tags:
                tags.append(tag)
            return result
    raise SchemaTaggerError(f"Field '{field_name}' not found in schema.")


def remove_tag(schema: dict, field_name: str, tag: str) -> dict:
    """Return a new schema with *tag* removed from the named field."""
    _check_schema(schema)
    result = copy.deepcopy(schema)
    for field in result["fields"]:
        if field.get("name") == field_name:
            field["tags"] = [t for t in field.get("tags", []) if t != tag]
            return result
    raise SchemaTaggerError(f"Field '{field_name}' not found in schema.")


def get_tags(schema: dict, field_name: str) -> List[str]:
    """Return the list of tags for the named field (may be empty)."""
    _check_schema(schema)
    for field in schema["fields"]:
        if field.get("name") == field_name:
            return list(field.get("tags", []))
    raise SchemaTaggerError(f"Field '{field_name}' not found in schema.")


def fields_with_tag(schema: dict, tag: str) -> List[Dict]:
    """Return a list of field dicts that carry *tag*."""
    _check_schema(schema)
    tag = tag.strip()
    if not tag:
        raise SchemaTaggerError("Tag must be a non-empty string.")
    return [
        copy.deepcopy(f)
        for f in schema["fields"]
        if tag in f.get("tags", [])
    ]


def list_all_tags(schema: dict) -> List[str]:
    """Return a sorted, deduplicated list of every tag used in the schema."""
    _check_schema(schema)
    seen: set = set()
    for field in schema["fields"]:
        seen.update(field.get("tags", []))
    return sorted(seen)
