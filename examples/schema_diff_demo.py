"""Demonstrate schema diffing between two versions of a form schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from formify_cli.schema_diff import diff_schemas


OLD_SCHEMA = {
    "title": "Contact Form v1",
    "fields": [
        {"name": "name", "type": "text", "label": "Name", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "message", "type": "textarea", "label": "Message", "required": False},
    ],
}

NEW_SCHEMA = {
    "title": "Contact Form v2",
    "fields": [
        {"name": "name", "type": "text", "label": "Full Name", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "phone", "type": "text", "label": "Phone Number", "required": False},
    ],
}


def main() -> None:
    result = diff_schemas(OLD_SCHEMA, NEW_SCHEMA)

    print("=== Schema Diff Demo ===")
    print(f"Summary: {result.summary_line()}")
    print()

    if result.added_fields:
        print(f"Added fields   : {', '.join(result.added_fields)}")

    if result.removed_fields:
        print(f"Removed fields : {', '.join(result.removed_fields)}")

    if result.changed_fields:
        print("Changed fields:")
        for field_name, changes in result.changed_fields.items():
            for key, diff in changes.items():
                print(f"  {field_name}.{key}: {diff['old']!r} -> {diff['new']!r}")

    if not result.has_changes:
        print("Schemas are identical.")


if __name__ == "__main__":
    main()
