"""Conditional field visibility logic for formify-cli.

Supports simple show/hide rules based on other field values.
"""

from typing import Any


class ConditionalFieldError(Exception):
    """Raised when a conditional field rule is invalid."""


DEPENDS_ON_KEY = "depends_on"
DEPENDS_VALUE_KEY = "depends_value"


def has_condition(field: dict) -> bool:
    """Return True if the field defines a conditional visibility rule."""
    return DEPENDS_ON_KEY in field


def validate_condition(field: dict, all_fields: list[dict]) -> None:
    """Raise ConditionalFieldError if the condition references an unknown field."""
    if not has_condition(field):
        return

    depends_on = field[DEPENDS_ON_KEY]
    known_names = {f.get("name") for f in all_fields}

    if depends_on not in known_names:
        raise ConditionalFieldError(
            f"Field '{field.get('name')}' depends_on unknown field '{depends_on}'. "
            f"Known fields: {sorted(known_names)}"
        )

    if DEPENDS_VALUE_KEY not in field:
        raise ConditionalFieldError(
            f"Field '{field.get('name')}' has depends_on but is missing '{DEPENDS_VALUE_KEY}'."
        )


def evaluate_condition(field: dict, form_data: dict[str, Any]) -> bool:
    """Return True if the field should be shown given current form_data.

    Fields without conditions are always visible.
    """
    if not has_condition(field):
        return True

    depends_on = field[DEPENDS_ON_KEY]
    depends_value = field[DEPENDS_VALUE_KEY]
    actual_value = form_data.get(depends_on)

    return str(actual_value) == str(depends_value)


def filter_visible_fields(fields: list[dict], form_data: dict[str, Any]) -> list[dict]:
    """Return only the fields that should be visible for the given form_data."""
    return [f for f in fields if evaluate_condition(f, form_data)]


def render_condition_attrs(field: dict) -> str:
    """Return HTML data attributes encoding the condition, for JS-driven UIs."""
    if not has_condition(field):
        return ""

    depends_on = field[DEPENDS_ON_KEY]
    depends_value = field[DEPENDS_VALUE_KEY]
    return f'data-depends-on="{depends_on}" data-depends-value="{depends_value}"'
