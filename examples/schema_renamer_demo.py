"""Demonstration of the schema_renamer module."""

from __future__ import annotations

from formify_cli.schema_renamer import (
    rename_field,
    rename_fields_bulk,
    list_field_names,
)


SAMPLE_SCHEMA = {
    "title": "Contact Form",
    "fields": [
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "name", "type": "text", "label": "Full Name", "required": True},
        {"name": "country", "type": "select", "label": "Country", "depends_on": "name"},
        {"name": "message", "type": "textarea", "label": "Message", "required": False},
    ],
}


def demo_single_rename() -> None:
    print("=== Single Field Rename ===")
    print("Before:", list_field_names(SAMPLE_SCHEMA))
    result = rename_field(SAMPLE_SCHEMA, "email", "email_address")
    print("After: ", list_field_names(result))
    print()


def demo_depends_on_update() -> None:
    print("=== depends_on Reference Update ===")
    result = rename_field(SAMPLE_SCHEMA, "name", "full_name")
    country = next(f for f in result["fields"] if f["name"] == "country")
    print(f"country.depends_on updated to: '{country['depends_on']}'")
    print()


def demo_bulk_rename() -> None:
    print("=== Bulk Rename ===")
    rename_map = {
        "email": "email_address",
        "name": "full_name",
        "message": "body",
    }
    result = rename_fields_bulk(SAMPLE_SCHEMA, rename_map)
    print("Before:", list_field_names(SAMPLE_SCHEMA))
    print("After: ", list_field_names(result))
    print()


def demo_immutability() -> None:
    print("=== Original Schema Is Unchanged ===")
    rename_field(SAMPLE_SCHEMA, "email", "email_address")
    print("Original still has:", list_field_names(SAMPLE_SCHEMA))
    print()


def main() -> None:
    demo_single_rename()
    demo_depends_on_update()
    demo_bulk_rename()
    demo_immutability()


if __name__ == "__main__":
    main()
