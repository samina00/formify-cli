"""Utilities for generating URL/ID-safe slugs from schema field names and labels."""

import re


class SchemaSlugifierError(Exception):
    """Raised when slug generation fails."""


def slugify(text: str, separator: str = "-") -> str:
    """Convert a string to a URL/ID-safe slug.

    Args:
        text: The input string to slugify.
        separator: Character used to replace spaces and special chars.

    Returns:
        A lowercase, separator-delimited slug string.

    Raises:
        SchemaSlugifierError: If text is not a non-empty string.
    """
    if not isinstance(text, str):
        raise SchemaSlugifierError(f"Expected a string, got {type(text).__name__}.")
    if not text.strip():
        raise SchemaSlugifierError("Cannot slugify an empty or whitespace-only string.")
    if not isinstance(separator, str) or len(separator) == 0:
        raise SchemaSlugifierError("Separator must be a non-empty string.")

    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", separator, slug)
    slug = re.sub(rf"{re.escape(separator)}+", separator, slug)
    slug = slug.strip(separator)
    return slug


def slugify_field_names(schema: dict, separator: str = "-") -> dict:
    """Return a new schema where every field's 'name' is replaced with its slug.

    Args:
        schema: A validated schema dict with a 'fields' list.
        separator: Separator passed to slugify().

    Returns:
        A new schema dict with slugified field names.

    Raises:
        SchemaSlugifierError: If schema is invalid or a field name cannot be slugified.
    """
    if not isinstance(schema, dict):
        raise SchemaSlugifierError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaSlugifierError("Schema must contain a 'fields' key.")

    import copy
    new_schema = copy.deepcopy(schema)
    for field in new_schema["fields"]:
        try:
            field["name"] = slugify(field["name"], separator)
        except SchemaSlugifierError as exc:
            raise SchemaSlugifierError(
                f"Failed to slugify field name {field.get('name')!r}: {exc}"
            ) from exc
    return new_schema


def slugify_labels(schema: dict, separator: str = "-") -> dict:
    """Return a new schema where every field's 'label' is replaced with its slug.

    Useful for generating CSS class names from labels.

    Args:
        schema: A validated schema dict with a 'fields' list.
        separator: Separator passed to slugify().

    Returns:
        A new schema dict with slugified field labels.

    Raises:
        SchemaSlugifierError: If schema is invalid.
    """
    if not isinstance(schema, dict):
        raise SchemaSlugifierError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaSlugifierError("Schema must contain a 'fields' key.")

    import copy
    new_schema = copy.deepcopy(schema)
    for field in new_schema["fields"]:
        if "label" in field:
            try:
                field["label"] = slugify(field["label"], separator)
            except SchemaSlugifierError as exc:
                raise SchemaSlugifierError(
                    f"Failed to slugify label {field.get('label')!r}: {exc}"
                ) from exc
    return new_schema
