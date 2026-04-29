"""Demonstrate field_defaults enrichment on a sample schema."""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from formify_cli.field_defaults import apply_defaults_to_field, list_supported_types
from formify_cli.schema_parser import load_schema


def main() -> None:
    schema_path = pathlib.Path(__file__).parent / "contact_form.json"
    schema = load_schema(str(schema_path))

    print("=" * 60)
    print(f"Form: {schema.get('title', 'Untitled')}")
    print("=" * 60)

    for field in schema.get("fields", []):
        enriched = apply_defaults_to_field(field)
        print(f"\nField: {enriched.get('name')} (type={enriched.get('type', 'text')})")
        extras = {
            k: v
            for k, v in enriched.items()
            if k not in field
        }
        if extras:
            print(f"  Injected defaults: {json.dumps(extras, indent=4)}")
        else:
            print("  No defaults injected (all keys already present).")

    print("\n" + "=" * 60)
    print("Supported field types:", ", ".join(list_supported_types()))


if __name__ == "__main__":
    main()
