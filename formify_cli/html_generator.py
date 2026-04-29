"""HTML form generator from validated schema definitions."""

from typing import Any

FIELD_TYPE_MAP = {
    "text": "text",
    "email": "email",
    "password": "password",
    "number": "number",
    "tel": "tel",
    "url": "url",
    "textarea": "textarea",
    "select": "select",
    "checkbox": "checkbox",
    "radio": "radio",
}


class HTMLGenerationError(Exception):
    """Raised when HTML generation fails."""


def generate_form(schema: dict[str, Any]) -> str:
    """Generate an accessible HTML form string from a validated schema."""
    title = schema.get("title", "Form")
    fields = schema.get("fields", [])

    lines = [
        f'<form aria-label="{_escape(title)}" novalidate>',
        f'  <h2>{_escape(title)}</h2>',
    ]

    for field in fields:
        lines.append(_render_field(field))

    lines.append('  <button type="submit">Submit</button>')
    lines.append("</form>")

    return "\n".join(lines)


def _render_field(field: dict[str, Any]) -> str:
    field_id = _escape(field["name"])
    label_text = _escape(field.get("label", field["name"].replace("_", " ").title()))
    field_type = field.get("type", "text")
    required = field.get("required", False)
    placeholder = field.get("placeholder", "")
    options = field.get("options", [])

    if field_type not in FIELD_TYPE_MAP:
        raise HTMLGenerationError(f"Unsupported field type: '{field_type}'")

    required_attr = ' required aria-required="true"' if required else ""
    required_indicator = ' <span aria-hidden="true">*</span>' if required else ""

    label_html = f'  <label for="{field_id}">{label_text}{required_indicator}</label>'

    if field_type == "textarea":
        input_html = (
            f'  <textarea id="{field_id}" name="{field_id}"'
            f' placeholder="{_escape(placeholder)}"{required_attr}></textarea>'
        )
    elif field_type == "select":
        option_lines = [f'  <select id="{field_id}" name="{field_id}"{required_attr}>']
        option_lines.append('    <option value="">-- Select --</option>')
        for opt in options:
            opt_val = _escape(str(opt))
            option_lines.append(f'    <option value="{opt_val}">{opt_val}</option>')
        option_lines.append("  </select>")
        return "\n".join([label_html] + option_lines)
    elif field_type in ("checkbox", "radio"):
        input_html = (
            f'  <input type="{field_type}" id="{field_id}" name="{field_id}"{required_attr}>'
        )
    else:
        html_type = FIELD_TYPE_MAP[field_type]
        input_html = (
            f'  <input type="{html_type}" id="{field_id}" name="{field_id}"'
            f' placeholder="{_escape(placeholder)}"{required_attr}>'
        )

    return "\n".join([label_html, input_html])


def _escape(value: str) -> str:
    """Escape special HTML characters."""
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
