"""schema_freezer.py — Make schemas immutable (frozen) for safe sharing."""

from __future__ import annotations

import copy
from types import MappingProxyType
from typing import Any


class SchemaFreezerError(Exception):
    """Raised when freezing or thawing fails."""


def _freeze_value(value: Any) -> Any:
    """Recursively convert dicts/lists to immutable equivalents."""
    if isinstance(value, dict):
        return MappingProxyType({k: _freeze_value(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_value(item) for item in value)
    return value


def freeze_schema(schema: dict) -> MappingProxyType:
    """Return a deeply immutable (frozen) version of *schema*.

    Args:
        schema: A validated schema dict.

    Returns:
        A :class:`types.MappingProxyType` wrapping the schema.

    Raises:
        SchemaFreezerError: If *schema* is not a dict.
    """
    if not isinstance(schema, dict):
        raise SchemaFreezerError("schema must be a dict")
    return _freeze_value(schema)  # type: ignore[return-value]


def thaw_schema(frozen: MappingProxyType) -> dict:
    """Return a deep mutable copy of a frozen schema.

    Args:
        frozen: A previously frozen schema.

    Returns:
        A plain, mutable dict.

    Raises:
        SchemaFreezerError: If *frozen* is not a MappingProxyType.
    """
    if not isinstance(frozen, MappingProxyType):
        raise SchemaFreezerError("frozen must be a MappingProxyType produced by freeze_schema")
    return _thaw_value(frozen)  # type: ignore[return-value]


def _thaw_value(value: Any) -> Any:
    """Recursively convert MappingProxyType/tuple back to dict/list."""
    if isinstance(value, MappingProxyType):
        return {k: _thaw_value(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_thaw_value(item) for item in value]
    return value


def is_frozen(schema: Any) -> bool:
    """Return True if *schema* is a frozen (MappingProxyType) schema."""
    return isinstance(schema, MappingProxyType)


def safe_copy(schema: dict) -> dict:
    """Return a deep independent copy of *schema* without freezing.

    Raises:
        SchemaFreezerError: If *schema* is not a dict.
    """
    if not isinstance(schema, dict):
        raise SchemaFreezerError("schema must be a dict")
    return copy.deepcopy(schema)
