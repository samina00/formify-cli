"""Demonstration of schema_reorder utilities."""

from formify_cli.schema_reorder import (
    reorder_by_list,
    reorder_alphabetically,
    reorder_by_type_priority,
    list_field_names,
)


SAMPLE_SCHEMA = {
    "title": "Registration Form",
    "fields": [
        {"name": "bio", "type": "textarea", "label": "Bio"},
        {"name": "email", "type": "email", "label": "Email Address", "required": True},
        {"name": "username", "type": "text", "label": "Username", "required": True},
        {"name": "age", "type": "number", "label": "Age"},
        {"name": "country", "type": "select", "label": "Country"},
        {"name": "newsletter", "type": "checkbox", "label": "Subscribe to newsletter"},
    ],
}


def _print_order(schema, title: str) -> None:
    print(f"\n--- {title} ---")
    for name in list_field_names(schema):
        print(f"  {name}")


def demo_reorder_by_explicit_list() -> None:
    desired_order = ["username", "email", "age", "country"]
    result = reorder_by_list(SAMPLE_SCHEMA, desired_order)
    _print_order(result, "Explicit order: username → email → age → country (rest appended)")


def demo_reorder_alphabetically() -> None:
    asc = reorder_alphabetically(SAMPLE_SCHEMA)
    _print_order(asc, "Alphabetical ascending")

    desc = reorder_alphabetically(SAMPLE_SCHEMA, reverse=True)
    _print_order(desc, "Alphabetical descending")


def demo_reorder_by_type_priority() -> None:
    result = reorder_by_type_priority(SAMPLE_SCHEMA)
    _print_order(result, "By built-in type priority (text/email first, checkbox last)")


def demo_immutability() -> None:
    original_order = list_field_names(SAMPLE_SCHEMA)
    reorder_by_list(SAMPLE_SCHEMA, ["newsletter"])
    reorder_alphabetically(SAMPLE_SCHEMA)
    reorder_by_type_priority(SAMPLE_SCHEMA)
    assert list_field_names(SAMPLE_SCHEMA) == original_order
    print("\n--- Immutability check passed: original schema unchanged ---")


def main() -> None:
    print("=== schema_reorder demo ===")
    demo_reorder_by_explicit_list()
    demo_reorder_alphabetically()
    demo_reorder_by_type_priority()
    demo_immutability()


if __name__ == "__main__":
    main()
