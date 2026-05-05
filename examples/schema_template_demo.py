"""Demonstrates schema template generation and field scaffolding."""

import json

from formify_cli.schema_template import (
    get_template,
    list_templates,
    scaffold_field,
)
from formify_cli.form_builder import build_form


def demo_list_templates() -> None:
    print("=== Available Templates ===")
    for name in list_templates():
        print(f"  - {name}")
    print()


def demo_get_template() -> None:
    print("=== Contact Template Schema ===")
    schema = get_template("contact")
    print(json.dumps(schema, indent=2))
    print()


def demo_scaffold_custom_form() -> None:
    print("=== Custom Scaffolded Schema ===")
    schema = {
        "title": "Feedback Form",
        "fields": [
            scaffold_field("text", "full_name", label="Your Name"),
            scaffold_field("email", "email"),
            scaffold_field("select", "category", label="Feedback Category"),
            scaffold_field("textarea", "feedback", label="Your Feedback"),
        ],
    }
    # Mark some fields required after scaffolding
    schema["fields"][0]["required"] = True
    schema["fields"][1]["required"] = True
    schema["fields"][2]["options"] = ["Bug", "Feature Request", "General"]

    print(json.dumps(schema, indent=2))
    print()
    return schema


def demo_build_html_from_template() -> None:
    print("=== HTML from Login Template ===")
    schema = get_template("login")
    html = build_form(schema)
    # Print just the first 300 chars to keep output tidy
    print(html[:300], "...")
    print()


def main() -> None:
    demo_list_templates()
    demo_get_template()
    custom_schema = demo_scaffold_custom_form()
    demo_build_html_from_template()
    print("Demo complete.")


if __name__ == "__main__":
    main()
