"""Demo for formify_cli.schema_grouper."""

from formify_cli.schema_grouper import (
    group_by_key,
    list_group_names,
    fields_in_group,
    ungroup_schema,
)

SCHEMA = {
    "title": "Conference Registration",
    "fields": [
        {"name": "first_name", "type": "text", "label": "First Name", "section": "personal"},
        {"name": "last_name", "type": "text", "label": "Last Name", "section": "personal"},
        {"name": "email", "type": "email", "label": "Email", "section": "contact"},
        {"name": "phone", "type": "tel", "label": "Phone", "section": "contact"},
        {"name": "dietary", "type": "select", "label": "Dietary Requirements"},
    ],
}


def demo_group_by_section():
    print("=== Group by 'section' ===")
    groups = group_by_key(SCHEMA, "section")
    for group_name, fields in groups.items():
        label = group_name if group_name else "(ungrouped)"
        print(f"  [{label}]")
        for f in fields:
            print(f"    - {f['name']} ({f['type']})")
    print()


def demo_list_group_names():
    print("=== List group names ===")
    names = list_group_names(SCHEMA, "section")
    for n in names:
        print(f"  {n!r}")
    print()


def demo_fields_in_group():
    print("=== Fields in 'contact' group ===")
    fields = fields_in_group(SCHEMA, "section", "contact")
    for f in fields:
        print(f"  {f['label']} -> {f['name']}")
    print()


def demo_ungroup():
    print("=== Ungroup (strip 'section' key) ===")
    clean = ungroup_schema(SCHEMA, "section")
    for f in clean["fields"]:
        print(f"  {f}")
    print()


def main():
    demo_group_by_section()
    demo_list_group_names()
    demo_fields_in_group()
    demo_ungroup()


if __name__ == "__main__":
    main()
