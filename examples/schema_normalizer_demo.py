"""Demo script for formify_cli.schema_normalizer."""

from __future__ import annotations

import json

from formify_cli.schema_normalizer import (
    normalize_schema,
    list_unknown_types,
)


_RAW_SCHEMA = {
    "title": "  Registration Form  ",
    "fields": [
        {"name": "username", "type": "TEXT", "label": " Username "},
        {"name": "email", "type": "Email", "label": "Email Address", "required": 1},
        {"name": "age", "type": "number", "label": "Age", "placeholder": "18"},
        {"name": "bio", "type": "TEXTAREA", "label": "Bio", "help_text": "Tell us about yourself."},
        {"name": "widget", "type": "custom_widget", "label": "Widget"},
    ],
}


def demo_normalize() -> None:
    print("=== Raw schema ===")
    print(json.dumps(_RAW_SCHEMA, indent=2))

    normalized = normalize_schema(_RAW_SCHEMA)
    print("\n=== Normalized schema ===")
    print(json.dumps(normalized, indent=2))


def demo_unknown_types() -> None:
    unknown = list_unknown_types(_RAW_SCHEMA)
    if unknown:
        print(f"\n=== Fields with unknown types ===")
        for name in unknown:
            print(f"  - {name}")
    else:
        print("\nAll field types are recognized.")


def main() -> None:
    demo_normalize()
    demo_unknown_types()


if __name__ == "__main__":
    main()
