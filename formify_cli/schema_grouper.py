"""Group schema fields into logical sections by a shared key."""

from typing import Dict, List, Any


class SchemaGrouperError(Exception):
    """Raised when grouping operations fail."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaGrouperError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaGrouperError("Schema must have a 'fields' key.")


def group_by_key(schema: Dict, key: str) -> Dict[str, List[Dict]]:
    """Group fields by the value of a given key (e.g. 'group', 'section').

    Fields that do not have the key are placed under the special group ''.
    Returns a dict mapping group name -> list of field dicts.
    """
    if not key or not isinstance(key, str):
        raise SchemaGrouperError("key must be a non-empty string.")
    _check_schema(schema)

    groups: Dict[str, List[Dict]] = {}
    for field in schema["fields"]:
        group_name = field.get(key, "")
        groups.setdefault(group_name, []).append(dict(field))
    return groups


def list_group_names(schema: Dict, key: str) -> List[str]:
    """Return sorted list of unique group values for *key* across all fields."""
    groups = group_by_key(schema, key)
    return sorted(groups.keys())


def fields_in_group(schema: Dict, key: str, group_name: str) -> List[Dict]:
    """Return fields whose *key* equals *group_name*.

    An empty *group_name* matches fields that lack the key entirely.
    """
    groups = group_by_key(schema, key)
    return groups.get(group_name, [])


def ungroup_schema(schema: Dict, key: str) -> Dict:
    """Return a copy of *schema* with *key* stripped from every field."""
    _check_schema(schema)
    if not key or not isinstance(key, str):
        raise SchemaGrouperError("key must be a non-empty string.")
    cleaned_fields = [
        {k: v for k, v in field.items() if k != key}
        for field in schema["fields"]
    ]
    result = dict(schema)
    result["fields"] = cleaned_fields
    return result
