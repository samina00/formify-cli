"""High-level form builder that wires schema parsing, theming, and HTML generation."""

from __future__ import annotations

from typing import Any

from formify_cli.schema_parser import load_schema, validate_schema, SchemaValidationError
from formify_cli.html_generator import generate_form, HTMLGenerationError
from formify_cli.field_defaults import apply_defaults_to_field
from formify_cli.theme import get_theme, ThemeError
from formify_cli.theme_renderer import build_themed_form


class FormBuilderError(Exception):
    """Raised when the form builder encounters an unrecoverable error."""


def build_form(
    schema_path: str,
    *,
    theme_name: str | None = None,
    include_css_link: bool = True,
    extra_attrs: dict[str, Any] | None = None,
) -> str:
    """Load *schema_path*, apply defaults + optional theme, and return HTML.

    Parameters
    ----------
    schema_path:
        Path to a JSON schema file understood by :func:`load_schema`.
    theme_name:
        Optional built-in theme name (e.g. ``"default"``, ``"dark"``).
        When *None* the plain HTML generator is used without theming.
    include_css_link:
        When *True* and a theme is selected, prepend a ``<link>`` tag for the
        theme stylesheet.
    extra_attrs:
        Mapping of extra HTML attributes forwarded to :func:`generate_form`.
    """
    try:
        schema = load_schema(schema_path)
    except (OSError, ValueError) as exc:
        raise FormBuilderError(f"Cannot load schema '{schema_path}': {exc}") from exc

    try:
        validate_schema(schema)
    except SchemaValidationError as exc:
        raise FormBuilderError(f"Invalid schema: {exc}") from exc

    # Apply field-level defaults so generators always receive complete data.
    enriched_fields = []
    for field in schema.get("fields", []):
        enriched_fields.append(apply_defaults_to_field(dict(field)))
    schema = {**schema, "fields": enriched_fields}

    if theme_name is not None:
        try:
            theme = get_theme(theme_name)
        except ThemeError as exc:
            raise FormBuilderError(str(exc)) from exc
        return build_themed_form(
            schema,
            theme,
            include_css_link=include_css_link,
            extra_attrs=extra_attrs or {},
        )

    try:
        return generate_form(schema, extra_attrs=extra_attrs or {})
    except HTMLGenerationError as exc:
        raise FormBuilderError(f"HTML generation failed: {exc}") from exc
