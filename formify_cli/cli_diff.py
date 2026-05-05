"""CLI sub-command: diff two schema files and report structural changes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_diff import SchemaDiffError, diff_schemas


def _load_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(2)


def build_diff_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa: SLF001
    """Register the 'diff' sub-command on an existing subparsers object."""
    parser = subparsers.add_parser(
        "diff",
        help="Compare two schema files and show structural differences.",
    )
    parser.add_argument("old_schema", help="Path to the original schema JSON file.")
    parser.add_argument("new_schema", help="Path to the updated schema JSON file.")
    parser.add_argument(
        "--json",
        dest="output_json",
        action="store_true",
        help="Output the diff as JSON.",
    )
    parser.set_defaults(func=cmd_diff)


def cmd_diff(args: argparse.Namespace) -> None:
    """Execute the diff sub-command."""
    old = _load_json(args.old_schema)
    new = _load_json(args.new_schema)

    try:
        result = diff_schemas(old, new)
    except SchemaDiffError as exc:
        print(f"Diff error: {exc}", file=sys.stderr)
        sys.exit(1)

    if getattr(args, "output_json", False):
        import json as _json
        payload = {
            "added": result.added_fields,
            "removed": result.removed_fields,
            "changed": result.changed_fields,
        }
        print(_json.dumps(payload, indent=2))
        sys.exit(0 if not result.has_changes else 1)

    print(f"Summary: {result.summary_line()}")
    if result.added_fields:
        print("Added:   " + ", ".join(result.added_fields))
    if result.removed_fields:
        print("Removed: " + ", ".join(result.removed_fields))
    for field_name, changes in result.changed_fields.items():
        for key, diff in changes.items():
            print(f"Changed: {field_name}.{key}: {diff['old']!r} -> {diff['new']!r}")

    sys.exit(0 if not result.has_changes else 1)
