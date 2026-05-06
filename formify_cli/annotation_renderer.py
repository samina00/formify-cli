"""Render field annotation metadata (hint, example, description) as HTML."""

from __future__ import annotations

import html


class AnnotationRenderError(Exception):
    """Raised when annotation rendering fails."""


def render_hint(field: dict, *, id_prefix: str = "hint") -> str:
    """Return a <span> hint element for the field, or empty string if none."""
    hint = field.get("hint", "").strip()
    if not hint:
        return ""
    name = field.get("name", "field")
    span_id = f"{id_prefix}-{html.escape(name)}"
    return f'<span id="{span_id}" class="field-hint">{html.escape(hint)}</span>'


def render_example(field: dict) -> str:
    """Return a <span> example element for the field, or empty string if none."""
    example = field.get("example", "").strip()
    if not example:
        return ""
    escaped = html.escape(example)
    return f'<span class="field-example">Example: {escaped}</span>'


def render_description(field: dict) -> str:
    """Return a <p> description element for the field, or empty string if none."""
    description = field.get("description", "").strip()
    if not description:
        return ""
    return f'<p class="field-description">{html.escape(description)}</p>'


def render_annotations_block(field: dict) -> str:
    """Render all annotation elements for a field as a combined HTML block."""
    if not isinstance(field, dict):
        raise AnnotationRenderError("Field must be a dict.")
    parts = [
        render_description(field),
        render_hint(field),
        render_example(field),
    ]
    return "".join(p for p in parts if p)


def aria_describedby_attr(field: dict, *, id_prefix: str = "hint") -> str:
    """Return aria-describedby attribute string if a hint is present, else empty."""
    hint = field.get("hint", "").strip()
    if not hint:
        return ""
    name = field.get("name", "field")
    span_id = f"{id_prefix}-{html.escape(name)}"
    return f'aria-describedby="{span_id}"'
