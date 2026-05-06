"""Demonstrates schema_clone utilities.

Run::

    python examples/schema_clone_demo.py
"""

import json

from formify_cli.schema_clone import clone_schema, prefix_field_names, rename_field

BASE_SCHEMA = {
    "title": "Registration",
    "fields": [
        {"name": "username", "type": "text", "label": "Username", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "password", "type": "password", "label": "Password", "required": True},
    ],
}


def demo_simple_clone():
    print("=== Simple Clone ===")
    cloned = clone_schema(BASE_SCHEMA)
    print(f"Original title : {BASE_SCHEMA['title']}")
    print(f"Cloned title   : {cloned['title']}")
    print(f"Same content?  : {cloned == BASE_SCHEMA}")
    print(f"Same object?   : {cloned is BASE_SCHEMA}")
    print()


def demo_clone_with_new_title():
    print("=== Clone with New Title ===")
    cloned = clone_schema(BASE_SCHEMA, new_title="Quick Sign-Up")
    print(f"New title: {cloned['title']}")
    print()


def demo_rename_field():
    print("=== Rename Field ===")
    updated = rename_field(BASE_SCHEMA, "username", "handle")
    names = [f["name"] for f in updated["fields"]]
    print(f"Field names after rename: {names}")
    original_names = [f["name"] for f in BASE_SCHEMA["fields"]]
    print(f"Original unchanged      : {original_names}")
    print()


def demo_prefix_fields():
    print("=== Prefix Field Names ===")
    prefixed = prefix_field_names(BASE_SCHEMA, "reg_")
    names = [f["name"] for f in prefixed["fields"]]
    print(f"Prefixed names: {names}")
    print()


def demo_combined():
    print("=== Combined Operations ===")
    result = clone_schema(BASE_SCHEMA, new_title="Embedded Form")
    result = prefix_field_names(result, "emb_")
    result = rename_field(result, "emb_password", "emb_secret")
    print(json.dumps(result, indent=2))
    print()


def main():
    demo_simple_clone()
    demo_clone_with_new_title()
    demo_rename_field()
    demo_prefix_fields()
    demo_combined()


if __name__ == "__main__":
    main()
