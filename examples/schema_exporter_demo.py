"""Demo for formify_cli.schema_exporter — export schemas to multiple formats."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from formify_cli.schema_exporter import (
    export_schema,
    export_schema_to_file,
    list_export_formats,
)

SAMPLE_SCHEMA = {
    "title": "Event Registration",
    "fields": [
        {"name": "full_name", "type": "text", "label": "Full Name", "required": True},
        {"name": "email", "type": "email", "label": "Email Address", "required": True},
        {"name": "ticket_type", "type": "select", "label": "Ticket Type", "required": True,
         "options": ["General", "VIP", "Student"]},
        {"name": "dietary", "type": "text", "label": "Dietary Requirements", "required": False},
    ],
}


def demo_list_formats() -> None:
    print("=== Supported Export Formats ===")
    for fmt in list_export_formats():
        print(f"  - {fmt}")
    print()


def demo_json_export() -> None:
    print("=== JSON Export ===")
    result = export_schema(SAMPLE_SCHEMA, "json")
    parsed = json.loads(result)
    print(f"Exported {len(parsed['fields'])} fields for form: {parsed['title']}")
    print()


def demo_markdown_export() -> None:
    print("=== Markdown Export ===")
    result = export_schema(SAMPLE_SCHEMA, "markdown")
    print(result)


def demo_summary_export() -> None:
    print("=== Summary Export ===")
    result = export_schema(SAMPLE_SCHEMA, "summary")
    print(result)


def demo_file_export(output_dir: Path) -> None:
    print("=== Export to Files ===")
    for fmt, ext in [("json", "json"), ("markdown", "md"), ("summary", "txt")]:
        dest = output_dir / f"event_registration.{ext}"
        path = export_schema_to_file(SAMPLE_SCHEMA, fmt, dest, overwrite=True)
        print(f"  Written [{fmt}]: {path}")
    print()


def main() -> None:
    demo_list_formats()
    demo_json_export()
    demo_markdown_export()
    demo_summary_export()
    output_dir = Path("/tmp/formify_export_demo")
    output_dir.mkdir(parents=True, exist_ok=True)
    demo_file_export(output_dir)
    print("Demo complete.")


if __name__ == "__main__":
    main()
