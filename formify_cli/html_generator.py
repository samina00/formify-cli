"""Generates accessible HTML forms from a validated schema dict."""

from __future__ import annotations

from typing import Any

from formify_cli.field_defaults import apply_defaults_to_field


class HTMLGenerationError(Exception):
    pass


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def generate_form(schema: dict[str, Any], theme_class: str = "") -> str:
    """Return a complete HTML form string generated from *schema*."""
    if not isinstance(schema, dict):
        raise HTMLGenerationError("Schema must be a dict.")

    title = _escape(schema.get("title", "Form"))
    fields = schema.get("fields", [])

    form_class = f' class="{_escape(theme_class)}"' if theme_class else ""
    lines: list[str] = [
        f'<form aria-label="{title}"{form_class}>',
        f'  <h1>{title}</h1>',
    ]

    for field in fields:
        enriched = apply_defaults_to_field(field)
        lines.append(_render_field(enriched))

    lines += [
        '  <button type="submit">Submit</button>',
        "</form>",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _render_field(field: dict[str, Any]) -> str:
    """Render a single form field as an HTML snippet."""
    field_type = field.get("type", "text")
    name = _escape(field.get("name", ""))
    label_text = _escape(field.get("label", name))
    required = field.get("required", False)
    field_id = f"field_{name}"

    required_attr = ' required aria-required="true"' if required else ""
    label_required = ' <span aria-hidden="true">*</span>' if required else ""

    label = f'  <label for="{field_id}">{label_text}{label_required}</label>'

    if field_type == "textarea":
        rows = _escape(str(field.get("rows", "4")))
        placeholder = field.get("placeholder", "")
        ph_attr = f' placeholder="{_escape(placeholder)}"' if placeholder else ""
        tag = (
            f'  <textarea id="{field_id}" name="{name}" rows="{rows}"'
            f'{ph_attr}{required_attr}></textarea>'
        )
    elif field_type == "select":
        options_html = _render_options(field.get("options", []))
        tag = (
            f'  <select id="{field_id}" name="{name}"{required_attr}>'
            f'{options_html}</select>'
        )
    else:
        placeholder = field.get("placeholder", "")
        ph_attr = f' placeholder="{_escape(placeholder)}"' if placeholder else ""
        extra = _extra_attrs(field)
        tag = (
            f'  <input type="{_escape(field_type)}" id="{field_id}" '
            f'name="{name}"{ph_attr}{extra}{required_attr} />'
        )

    return f"{label}\n{tag}"


def _render_options(options: list[Any]) -> str:
    parts = ['<option value="">-- select --</option>']
    for opt in options:
        if isinstance(opt, dict):
            val = _escape(str(opt.get("value", "")))
            text = _escape(str(opt.get("label", val)))
        else:
            val = text = _escape(str(opt))
        parts.append(f'<option value="{val}">{text}</option>')
    return "".join(parts)


_PASSTHROUGH_ATTRS = {"autocomplete", "inputmode", "spellcheck", "min", "max", "pattern"}


def _extra_attrs(field: dict[str, Any]) -> str:
    parts: list[str] = []
    for attr in sorted(_PASSTHROUGH_ATTRS):
        if attr in field:
            parts.append(f' {attr}="{_escape(str(field[attr]))}"')
    return "".join(parts)


def _escape(text: str) -> str:
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
