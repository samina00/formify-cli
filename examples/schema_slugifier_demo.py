"""Demo script for formify_cli.schema_slugifier."""

from formify_cli.schema_slugifier import slugify, slugify_field_names, slugify_labels


SAMPLE_SCHEMA = {
    "title": "Contact Form",
    "fields": [
        {"name": "Full Name",     "type": "text",  "label": "Full Name",     "required": True},
        {"name": "Email Address", "type": "email", "label": "Email Address", "required": True},
        {"name": "Phone Number",  "type": "tel",   "label": "Phone Number",  "required": False},
        {"name": "Your Message",  "type": "textarea", "label": "Your Message", "required": False},
    ],
}


def demo_basic_slugify():
    print("=== Basic slugify ===")
    examples = [
        "Hello World",
        "Email Address!",
        "  Padded String  ",
        "Multiple   Spaces",
        "CamelCaseWord",
    ]
    for text in examples:
        print(f"  {text!r:30s} -> {slugify(text)!r}")
    print()


def demo_custom_separator():
    print("=== Custom separator ===")
    text = "Full Name"
    for sep in ["-", "_", "."]:
        print(f"  separator={sep!r}: {slugify(text, separator=sep)!r}")
    print()


def demo_slugify_field_names():
    print("=== Slugify field names ===")
    result = slugify_field_names(SAMPLE_SCHEMA)
    for field in result["fields"]:
        print(f"  name={field['name']!r}")
    print()


def demo_slugify_labels():
    print("=== Slugify labels ===")
    result = slugify_labels(SAMPLE_SCHEMA, separator="_")
    for field in result["fields"]:
        print(f"  label={field['label']!r}")
    print()


def main():
    demo_basic_slugify()
    demo_custom_separator()
    demo_slugify_field_names()
    demo_slugify_labels()


if __name__ == "__main__":
    main()
