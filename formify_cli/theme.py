"""Theme support for formify-cli HTML form generation."""

from dataclasses import dataclass, field
from typing import Dict, Optional


class ThemeError(Exception):
    """Raised when a theme cannot be loaded or is invalid."""


@dataclass
class Theme:
    name: str
    form_class: str = "form"
    field_wrapper_class: str = "form-group"
    label_class: str = "form-label"
    input_class: str = "form-control"
    select_class: str = "form-select"
    textarea_class: str = "form-control"
    submit_class: str = "btn btn-primary"
    error_class: str = "form-error"
    extra_css: Optional[str] = None


BUILTIN_THEMES: Dict[str, Theme] = {
    "default": Theme(
        name="default",
        form_class="form",
        field_wrapper_class="form-group",
        label_class="form-label",
        input_class="form-control",
        select_class="form-select",
        textarea_class="form-control",
        submit_class="btn btn-primary",
        error_class="form-error",
    ),
    "minimal": Theme(
        name="minimal",
        form_class="",
        field_wrapper_class="field",
        label_class="label",
        input_class="input",
        select_class="select",
        textarea_class="textarea",
        submit_class="submit",
        error_class="error",
    ),
    "bootstrap": Theme(
        name="bootstrap",
        form_class="needs-validation",
        field_wrapper_class="mb-3",
        label_class="form-label",
        input_class="form-control",
        select_class="form-select",
        textarea_class="form-control",
        submit_class="btn btn-primary",
        error_class="invalid-feedback",
        extra_css="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
    ),
}


def get_theme(name: str) -> Theme:
    """Return a Theme by name. Raises ThemeError if not found."""
    name = name.lower()
    if name not in BUILTIN_THEMES:
        available = ", ".join(BUILTIN_THEMES.keys())
        raise ThemeError(
            f"Unknown theme '{name}'. Available themes: {available}"
        )
    return BUILTIN_THEMES[name]


def list_themes() -> list:
    """Return a list of available theme names."""
    return list(BUILTIN_THEMES.keys())
