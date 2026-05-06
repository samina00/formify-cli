"""Render HTML id/name/class attributes using slugified field identifiers."""

from formify_cli.schema_slugifier import SchemaSlugifierError, slugify


class SlugRenderError(Exception):
    """Raised when slug-based attribute rendering fails."""


def _validate_field(field: object) -> None:
    """Raise SlugRenderError if *field* is not a dict containing a 'name' key."""
    if not isinstance(field, dict):
        raise SlugRenderError("field must be a dict.")
    if "name" not in field:
        raise SlugRenderError("field must contain a 'name' key.")


def field_id(field: dict, separator: str = "-") -> str:
    """Return a slug suitable for use as an HTML id attribute.

    Args:
        field: A field dict containing at least a 'name' key.
        separator: Slug separator.

    Returns:
        A slugified id string prefixed with 'field-'.

    Raises:
        SlugRenderError: If the field is invalid or slugification fails.
    """
    _validate_field(field)
    try:
        return "field-" + slugify(field["name"], separator)
    except SchemaSlugifierError as exc:
        raise SlugRenderError(str(exc)) from exc


def field_css_class(field: dict, prefix: str = "form-field", separator: str = "-") -> str:
    """Return a CSS class string combining a prefix and the slugified field name.

    Args:
        field: A field dict with at least a 'name' key.
        prefix: A static CSS class prefix.
        separator: Slug separator.

    Returns:
        A string like 'form-field form-field--email-address'.

    Raises:
        SlugRenderError: If the field is invalid.
    """
    _validate_field(field)
    try:
        slug = slugify(field["name"], separator)
    except SchemaSlugifierError as exc:
        raise SlugRenderError(str(exc)) from exc
    return f"{prefix} {prefix}--{slug}"


def render_label_for(field: dict, separator: str = "-") -> str:
    """Return an HTML <label> tag whose 'for' attribute uses the slugified field id.

    Args:
        field: A field dict with 'name' and optionally 'label' keys.
        separator: Slug separator.

    Returns:
        An HTML label string.

    Raises:
        SlugRenderError: If the field is invalid.
    """
    fid = field_id(field, separator)
    label_text = field.get("label") or field.get("name", "")
    escaped = label_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<label for="{fid}">{escaped}</label>'
