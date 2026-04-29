"""Field-level validation logic for form submissions against a schema."""

from typing import Any


class ValidationError(Exception):
    """Raised when form data fails validation."""

    def __init__(self, errors: dict[str, list[str]]) -> None:
        self.errors = errors
        super().__init__(f"Validation failed: {errors}")


def validate_form_data(schema: dict, data: dict[str, Any]) -> dict[str, list[str]]:
    """Validate submitted form data against the schema.

    Returns a dict mapping field names to lists of error messages.
    An empty dict means all fields passed validation.
    """
    errors: dict[str, list[str]] = {}

    for field in schema.get("fields", []):
        name = field["name"]
        field_errors = _validate_field_value(field, data.get(name))
        if field_errors:
            errors[name] = field_errors

    return errors


def _validate_field_value(field: dict, value: Any) -> list[str]:
    """Return a list of validation error messages for a single field value."""
    errors: list[str] = []
    field_type = field.get("type", "text")
    required = field.get("required", False)
    is_empty = value is None or str(value).strip() == ""

    if required and is_empty:
        errors.append(f"'{field['name']}' is required.")
        return errors  # no further checks if value is absent

    if is_empty:
        return errors

    str_value = str(value).strip()

    if field_type == "email":
        if "@" not in str_value or "." not in str_value.split("@")[-1]:
            errors.append("Enter a valid email address.")

    if field_type in ("text", "textarea", "email"):
        min_length = field.get("min_length")
        max_length = field.get("max_length")
        if min_length is not None and len(str_value) < min_length:
            errors.append(f"Must be at least {min_length} characters.")
        if max_length is not None and len(str_value) > max_length:
            errors.append(f"Must be at most {max_length} characters.")

    if field_type == "number":
        try:
            num = float(str_value)
        except ValueError:
            errors.append("Enter a valid number.")
        else:
            min_val = field.get("min")
            max_val = field.get("max")
            if min_val is not None and num < min_val:
                errors.append(f"Must be at least {min_val}.")
            if max_val is not None and num > max_val:
                errors.append(f"Must be at most {max_val}.")

    if field_type == "select":
        options = [opt["value"] for opt in field.get("options", [])]
        if str_value not in options:
            errors.append(f"'{str_value}' is not a valid choice.")

    return errors
