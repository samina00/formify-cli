"""Built-in validation rules for form field values."""

import re
from typing import Any


class RuleError(Exception):
    """Raised when a rule definition is invalid."""


# Registry of rule name -> callable(value, param) -> error_message | None
_RULES: dict = {}


def register_rule(name: str):
    """Decorator to register a validation rule function."""
    def decorator(fn):
        _RULES[name] = fn
        return fn
    return decorator


@register_rule("min_length")
def _rule_min_length(value: Any, param: int) -> str | None:
    if isinstance(value, str) and len(value) < param:
        return f"Must be at least {param} characters long."
    return None


@register_rule("max_length")
def _rule_max_length(value: Any, param: int) -> str | None:
    if isinstance(value, str) and len(value) > param:
        return f"Must be no more than {param} characters long."
    return None


@register_rule("pattern")
def _rule_pattern(value: Any, param: str) -> str | None:
    if isinstance(value, str) and not re.fullmatch(param, value):
        return f"Does not match required pattern: {param}."
    return None


@register_rule("min_value")
def _rule_min_value(value: Any, param) -> str | None:
    try:
        if float(value) < float(param):
            return f"Must be at least {param}."
    except (TypeError, ValueError):
        return f"Invalid numeric value."
    return None


@register_rule("max_value")
def _rule_max_value(value: Any, param) -> str | None:
    try:
        if float(value) > float(param):
            return f"Must be no more than {param}."
    except (TypeError, ValueError):
        return f"Invalid numeric value."
    return None


def list_rules() -> list[str]:
    """Return sorted list of registered rule names."""
    return sorted(_RULES.keys())


def apply_rule(rule_name: str, value: Any, param: Any) -> str | None:
    """Apply a named rule. Returns error message or None."""
    if rule_name not in _RULES:
        raise RuleError(f"Unknown rule '{rule_name}'. Available: {list_rules()}")
    return _RULES[rule_name](value, param)


def apply_all_rules(field: dict, value: Any) -> list[str]:
    """Apply all rules defined in field['rules'] dict. Returns list of errors."""
    errors = []
    rules = field.get("rules", {})
    if not isinstance(rules, dict):
        raise RuleError("Field 'rules' must be a dict mapping rule names to parameters.")
    for rule_name, param in rules.items():
        msg = apply_rule(rule_name, value, param)
        if msg:
            errors.append(msg)
    return errors
