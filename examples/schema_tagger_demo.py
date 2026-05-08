"""Demonstrates schema_tagger: add/remove tags, query by tag, list all tags."""

from formify_cli.schema_tagger import (
    add_tag,
    remove_tag,
    get_tags,
    fields_with_tag,
    list_all_tags,
)

SCHEMA = {
    "title": "User Profile",
    "fields": [
        {"name": "email", "type": "email", "label": "Email Address", "required": True},
        {"name": "full_name", "type": "text", "label": "Full Name", "required": True},
        {"name": "age", "type": "number", "label": "Age"},
        {"name": "newsletter", "type": "checkbox", "label": "Subscribe to newsletter"},
    ],
}


def demo_add_tags() -> None:
    print("=== Add Tags ===")
    s = add_tag(SCHEMA, "email", "pii")
    s = add_tag(s, "email", "contact")
    s = add_tag(s, "full_name", "pii")
    s = add_tag(s, "newsletter", "contact")
    print("email tags   :", get_tags(s, "email"))
    print("full_name tags:", get_tags(s, "full_name"))
    print("age tags     :", get_tags(s, "age"))
    print()
    return s


def demo_remove_tag(schema: dict) -> None:
    print("=== Remove Tag ===")
    s = remove_tag(schema, "email", "contact")
    print("email tags after removing 'contact':", get_tags(s, "email"))
    print()


def demo_fields_with_tag(schema: dict) -> None:
    print("=== Fields with tag 'pii' ===")
    pii_fields = fields_with_tag(schema, "pii")
    for f in pii_fields:
        print(" -", f["name"], "|", f["label"])
    print()


def demo_list_all_tags(schema: dict) -> None:
    print("=== All Tags in Schema ===")
    tags = list_all_tags(schema)
    print("Tags:", tags)
    print()


def main() -> None:
    tagged = demo_add_tags()
    demo_remove_tag(tagged)
    demo_fields_with_tag(tagged)
    demo_list_all_tags(tagged)


if __name__ == "__main__":
    main()
