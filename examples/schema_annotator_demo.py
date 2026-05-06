"""Demonstration of schema_annotator capabilities."""

from __future__ import annotations

import json

from formify_cli.schema_annotator import (
    annotate_field,
    annotate_schema_field,
    list_annotated_fields,
    strip_annotations,
)


SAMPLE_SCHEMA = {
    "title": "Contact Form",
    "fields": [
        {"name": "name", "type": "text", "label": "Full Name", "required": True},
        {"name": "email", "type": "email", "label": "Email Address", "required": True},
        {"name": "age", "type": "number", "label": "Age"},
        {"name": "message", "type": "textarea", "label": "Message"},
    ],
}


def demo_annotate_single_field() -> None:
    print("=== Annotate a single field ===")
    field = {"name": "email", "type": "email", "label": "Email"}
    annotated = annotate_field(
        field,
        hint="We will never share your email.",
        example="user@example.com",
        description="Primary contact address",
    )
    print(json.dumps(annotated, indent=2))
    print()


def demo_annotate_schema_field() -> None:
    print("=== Annotate a field inside a schema ===")
    updated = annotate_schema_field(
        SAMPLE_SCHEMA,
        "email",
        hint="We will never share your email.",
        example="user@example.com",
    )
    updated = annotate_schema_field(
        updated,
        "message",
        description="Tell us anything you like.",
    )
    for field in updated["fields"]:
        print(f"  {field['name']}: {field}")
    print()


def demo_list_annotated() -> None:
    print("=== List annotated fields ===")
    schema = annotate_schema_field(SAMPLE_SCHEMA, "name", hint="Your full legal name")
    schema = annotate_schema_field(schema, "age", example="25")
    names = list_annotated_fields(schema)
    print(f"Annotated fields: {names}")
    print()


def demo_strip_annotations() -> None:
    print("=== Strip all annotations ===")
    schema = annotate_schema_field(SAMPLE_SCHEMA, "email", hint="hint", example="ex")
    stripped = strip_annotations(schema)
    for field in stripped["fields"]:
        assert "hint" not in field
        assert "example" not in field
    print("All annotations removed successfully.")
    print()


def main() -> None:
    demo_annotate_single_field()
    demo_annotate_schema_field()
    demo_list_annotated()
    demo_strip_annotations()


if __name__ == "__main__":
    main()
