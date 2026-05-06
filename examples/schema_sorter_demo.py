"""Demo for formify_cli.schema_sorter — run with: python examples/schema_sorter_demo.py"""

import json

from formify_cli.schema_sorter import (
    reorder_fields,
    sort_by_label,
    sort_by_name,
    sort_by_type,
    sort_required_first,
)

SAMPLE_SCHEMA = {
    "title": "Registration Form",
    "fields": [
        {"name": "zip",      "type": "text",     "label": "ZIP Code",   "required": False},
        {"name": "email",    "type": "email",    "label": "Email",      "required": True},
        {"name": "username", "type": "text",     "label": "Username",   "required": True},
        {"name": "age",      "type": "number",   "label": "Age",        "required": False},
        {"name": "bio",      "type": "textarea", "label": "Biography",  "required": False},
    ],
}


def _field_names(schema):
    return [f["name"] for f in schema["fields"]]


def demo_sort_by_name():
    print("=== Sort by name (A→Z) ===")
    result = sort_by_name(SAMPLE_SCHEMA)
    print(" ", _field_names(result))


def demo_sort_by_type():
    print("=== Sort by type (A→Z) ===")
    result = sort_by_type(SAMPLE_SCHEMA)
    print(" ", [(f["name"], f["type"]) for f in result["fields"]])


def demo_sort_required_first():
    print("=== Required fields first ===")
    result = sort_required_first(SAMPLE_SCHEMA)
    print(" ", [(f["name"], f["required"]) for f in result["fields"]])


def demo_sort_by_label():
    print("=== Sort by label (A→Z) ===")
    result = sort_by_label(SAMPLE_SCHEMA)
    print(" ", [f["label"] for f in result["fields"]])


def demo_reorder_fields():
    print("=== Custom field order ===")
    desired = ["username", "email", "age", "zip", "bio"]
    result = reorder_fields(SAMPLE_SCHEMA, desired)
    print(" ", _field_names(result))


def main():
    demo_sort_by_name()
    demo_sort_by_type()
    demo_sort_required_first()
    demo_sort_by_label()
    demo_reorder_fields()
    print("\nOriginal schema unchanged:", _field_names(SAMPLE_SCHEMA))


if __name__ == "__main__":
    main()
