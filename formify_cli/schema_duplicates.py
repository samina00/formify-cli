"""Detect and report duplicate field names in a schema."""

from collections import Counter
from typing import Dict, List, Any


class SchemaDuplicatesError(Exception):
    """Raised when schema structure is invalid for duplicate detection."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaDuplicatesError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaDuplicatesError("Schema must contain a 'fields' key.")
    if not isinstance(schema["fields"], list):
        raise SchemaDuplicatesError("'fields' must be a list.")


def find_duplicate_names(schema: Dict) -> List[str]:
    """Return a sorted list of field names that appear more than once."""
    _check_schema(schema)
    names = [f.get("name", "") for f in schema["fields"] if isinstance(f, dict)]
    counts = Counter(names)
    return sorted(name for name, count in counts.items() if count > 1 and name)


def find_duplicate_labels(schema: Dict) -> List[str]:
    """Return a sorted list of field labels that appear more than once."""
    _check_schema(schema)
    labels = [f.get("label", "") for f in schema["fields"] if isinstance(f, dict)]
    counts = Counter(labels)
    return sorted(label for label, count in counts.items() if count > 1 and label)


def has_duplicates(schema: Dict) -> bool:
    """Return True if any field names are duplicated."""
    return len(find_duplicate_names(schema)) > 0


def duplicates_report(schema: Dict) -> str:
    """Return a human-readable report of duplicate field names and labels."""
    _check_schema(schema)
    dup_names = find_duplicate_names(schema)
    dup_labels = find_duplicate_labels(schema)
    lines = []
    if dup_names:
        lines.append("Duplicate field names: " + ", ".join(dup_names))
    else:
        lines.append("No duplicate field names found.")
    if dup_labels:
        lines.append("Duplicate field labels: " + ", ".join(dup_labels))
    else:
        lines.append("No duplicate field labels found.")
    return "\n".join(lines)
