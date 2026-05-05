"""Helpers that wire i18n translations into HTML form rendering."""

from __future__ import annotations

from html import escape
from typing import Optional

from formify_cli.i18n import get_locale, translate


def render_required_legend(locale: str = "en") -> str:
    """Return an HTML <p> element with the required-fields legend."""
    text = translate("required_legend", locale=locale)
    return f'<p class="required-legend">{escape(text)}</p>'


def render_submit_button(locale: str = "en", css_class: str = "btn-submit") -> str:
    """Return a localised submit <button> element."""
    label = translate("submit_button", locale=locale)
    cls = escape(css_class)
    return f'<button type="submit" class="{cls}">{escape(label)}</button>'


def render_required_marker(locale: str = "en") -> str:
    """Return an accessible required-field marker span."""
    marker = translate("required_marker", locale=locale)
    return (
        f'<span class="required-marker" aria-hidden="true">{escape(marker)}</span>'
    )


def render_field_label(
    field: dict,
    locale: str = "en",
    *,
    for_id: Optional[str] = None,
) -> str:
    """Return an HTML <label> for *field*, with an optional required marker.

    If *for_id* is given it is used as the ``for`` attribute; otherwise the
    field ``name`` is used.
    """
    label_text = escape(field.get("label", field.get("name", "")))
    target_id = escape(for_id or field.get("name", ""))
    required = field.get("required", False)

    marker = render_required_marker(locale) if required else ""
    return f'<label for="{target_id}">{label_text}{marker}</label>'


def localize_schema_messages(schema: dict, locale: str = "en") -> dict:
    """Return a copy of *schema* with i18n submit_label and required_legend.

    Existing values are preserved (not overwritten).
    """
    catalog = get_locale(locale)
    patched = dict(schema)
    patched.setdefault("submit_label", catalog["submit_button"])
    patched.setdefault("required_legend", catalog["required_legend"])
    patched["_locale"] = locale.lower().strip()
    return patched


def build_error_messages(errors: dict[str, str], locale: str = "en") -> str:
    """Render a <ul> of validation error messages.

    *errors* maps field names to raw error keys or already-formatted strings.
    """
    if not errors:
        return ""
    items = ""
    for field_name, message in errors.items():
        safe_name = escape(field_name)
        safe_msg = escape(message)
        items += (
            f'<li><strong>{safe_name}</strong>: {safe_msg}</li>\n'
        )
    return f'<ul class="form-errors" role="alert">\n{items}</ul>'
