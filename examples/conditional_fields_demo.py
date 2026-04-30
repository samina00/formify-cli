"""Demonstrates conditional field evaluation and HTML attribute rendering.

Run with:
    python examples/conditional_fields_demo.py
"""

from formify_cli.conditional_fields import (
    evaluate_condition,
    filter_visible_fields,
    render_condition_attrs,
    validate_condition,
)


SCHEMA_FIELDS = [
    {"name": "contact_method", "type": "select", "label": "Preferred Contact"},
    {
        "name": "email",
        "type": "email",
        "label": "Email Address",
        "depends_on": "contact_method",
        "depends_value": "email",
    },
    {
        "name": "phone",
        "type": "text",
        "label": "Phone Number",
        "depends_on": "contact_method",
        "depends_value": "phone",
    },
    {"name": "message", "type": "textarea", "label": "Message"},
]


def main() -> None:
    print("=== Conditional Fields Demo ===\n")

    print("Validating conditions against schema...")
    for field in SCHEMA_FIELDS:
        validate_condition(field, SCHEMA_FIELDS)
    print("All conditions valid.\n")

    scenarios = [
        {"contact_method": "email"},
        {"contact_method": "phone"},
        {},
    ]

    for data in scenarios:
        print(f"Form data: {data}")
        visible = filter_visible_fields(SCHEMA_FIELDS, data)
        print(f"  Visible fields: {[f['name'] for f in visible]}")

    print("\nHTML data attributes for conditional fields:")
    for field in SCHEMA_FIELDS:
        attrs = render_condition_attrs(field)
        if attrs:
            print(f"  <input name='{field['name']}' {attrs}>")
        else:
            print(f"  <input name='{field['name']}'> (always visible)")


if __name__ == "__main__":
    main()
