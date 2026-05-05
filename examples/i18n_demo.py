"""Demonstrates i18n support in formify-cli.

Run:
    python examples/i18n_demo.py
"""

from __future__ import annotations

from formify_cli.i18n import apply_locale_to_schema, list_locales, translate
from formify_cli.schema_parser import load_schema
from formify_cli.html_generator import generate_form

SAMPLE_SCHEMA = {
    "title": "Contact Us",
    "fields": [
        {
            "name": "full_name",
            "type": "text",
            "label": "Full Name",
            "required": True,
        },
        {
            "name": "email",
            "type": "email",
            "label": "Email Address",
            "required": True,
        },
        {
            "name": "message",
            "type": "textarea",
            "label": "Message",
            "required": False,
        },
    ],
}


def demo_translations() -> None:
    print("=== Available locales ===")
    print(", ".join(list_locales()))
    print()

    keys_to_show = ["submit_button", "required_legend", "error_required"]
    for locale in list_locales():
        print(f"--- {locale.upper()} ---")
        for key in keys_to_show:
            print(f"  {key}: {translate(key, locale=locale)}")
    print()


def demo_schema_patching() -> None:
    print("=== Schema patching demo ===")
    for locale in list_locales():
        patched = apply_locale_to_schema(SAMPLE_SCHEMA, locale=locale)
        print(
            f"[{locale}] submit_label={patched['submit_label']!r}  "
            f"required_legend={patched['required_legend']!r}"
        )
    print()


def demo_html_generation() -> None:
    print("=== HTML generation with locale (French) ===")
    patched = apply_locale_to_schema(SAMPLE_SCHEMA, locale="fr")
    html = generate_form(patched)
    # Print just the first 400 chars for brevity
    print(html[:400])
    print("...")
    print()


def main() -> None:
    demo_translations()
    demo_schema_patching()
    demo_html_generation()


if __name__ == "__main__":
    main()
