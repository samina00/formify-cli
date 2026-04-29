"""Themed HTML rendering helpers for formify-cli."""

from formify_cli.theme import Theme, get_theme
from formify_cli.html_generator import _escape


def render_css_link(url: str) -> str:
    """Return an HTML <link> tag for an external stylesheet."""
    escaped = _escape(url)
    return f'<link rel="stylesheet" href="{escaped}">'


def apply_theme_to_field(field: dict, theme: Theme) -> dict:
    """
    Return a copy of the field dict augmented with theme CSS class hints.
    Adds 'input_class', 'label_class', and 'wrapper_class' keys.
    """
    ftype = field.get("type", "text")
    if ftype == "select":
        input_class = theme.select_class
    elif ftype == "textarea":
        input_class = theme.textarea_class
    else:
        input_class = theme.input_class

    return {
        **field,
        "input_class": input_class,
        "label_class": theme.label_class,
        "wrapper_class": theme.field_wrapper_class,
    }


def render_themed_form_open(schema: dict, theme: Theme) -> str:
    """Return the opening <form> tag with theme class and aria-label."""
    title = _escape(schema.get("title", "Form"))
    cls = _escape(theme.form_class)
    class_attr = f' class="{cls}"' if cls else ""
    return f'<form{class_attr} aria-label="{title}" novalidate>'


def render_themed_submit(label: str, theme: Theme) -> str:
    """Return a themed submit button."""
    escaped_label = _escape(label)
    cls = _escape(theme.submit_class)
    class_attr = f' class="{cls}"' if cls else ""
    return f'<button type="submit"{class_attr}>{escaped_label}</button>'


def build_themed_form(schema: dict, theme_name: str = "default") -> str:
    """Generate a complete themed HTML form from a schema dict."""
    from formify_cli.html_generator import _render_field

    theme = get_theme(theme_name)
    lines = []

    if theme.extra_css:
        lines.append(render_css_link(theme.extra_css))

    title = schema.get("title", "Form")
    lines.append(f"<h1>{_escape(title)}</h1>")
    lines.append(render_themed_form_open(schema, theme))

    for field in schema.get("fields", []):
        themed_field = apply_theme_to_field(field, theme)
        lines.append(_render_field(themed_field))

    submit_label = schema.get("submit_label", "Submit")
    lines.append(render_themed_submit(submit_label, theme))
    lines.append("</form>")

    return "\n".join(lines)
