"""Provides default attributes and placeholder hints for common field types."""

from typing import Any


class FieldDefaultsError(Exception):
    pass


# Default HTML attributes per field type
_TYPE_DEFAULTS: dict[str, dict[str, Any]] = {
    "text": {"autocomplete": "off", "spellcheck": "false"},
    "email": {"autocomplete": "email", "inputmode": "email"},
    "tel": {"autocomplete": "tel", "inputmode": "tel"},
    "number": {"inputmode": "numeric"},
    "password": {"autocomplete": "current-password"},
    "url": {"inputmode": "url", "autocomplete": "url"},
    "textarea": {"rows": "4", "spellcheck": "true"},
    "select": {},
    "checkbox": {},
    "radio": {},
    "date": {},
    "time": {},
}

# Suggested placeholder text per field type
_TYPE_PLACEHOLDERS: dict[str, str] = {
    "email": "you@example.com",
    "tel": "+1 555 000 0000",
    "url": "https://example.com",
    "number": "0",
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
}


def get_defaults_for_type(field_type: str) -> dict[str, Any]:
    """Return a copy of default HTML attributes for the given field type."""
    field_type = field_type.lower()
    if field_type not in _TYPE_DEFAULTS:
        raise FieldDefaultsError(
            f"Unknown field type '{field_type}'. "
            f"Supported types: {', '.join(sorted(_TYPE_DEFAULTS))}"
        )
    return dict(_TYPE_DEFAULTS[field_type])


def get_placeholder_hint(field_type: str) -> str | None:
    """Return a suggested placeholder string for the given field type, or None."""
    return _TYPE_PLACEHOLDERS.get(field_type.lower())


def apply_defaults_to_field(field: dict[str, Any]) -> dict[str, Any]:
    """Return a new field dict enriched with type-based defaults.

    Existing keys in *field* are never overwritten.
    """
    field_type = field.get("type", "text")
    defaults = get_defaults_for_type(field_type)

    enriched = dict(defaults)
    enriched.update(field)  # field values win over defaults

    # Inject placeholder hint only when none is already set
    if "placeholder" not in enriched:
        hint = get_placeholder_hint(field_type)
        if hint:
            enriched["placeholder"] = hint

    return enriched


def list_supported_types() -> list[str]:
    """Return a sorted list of all supported field types."""
    return sorted(_TYPE_DEFAULTS.keys())
