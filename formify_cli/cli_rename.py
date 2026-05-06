"""CLI sub-command: rename a field inside a schema file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_renamer import SchemaRenamerError, rename_field, rename_fields_bulk


def _load_json(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading '{path}': {exc}", file=sys.stderr)
        sys.exit(1)


def _write_json(data: dict, path: str) -> None:
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_rename_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:  # type: ignore[type-arg]
    p = subparsers.add_parser("rename", help="Rename one or more fields in a schema.")
    p.add_argument("schema", help="Path to the input schema JSON file.")
    p.add_argument("--from", dest="old_name", help="Field name to rename (single rename).")
    p.add_argument("--to", dest="new_name", help="New field name (single rename).")
    p.add_argument(
        "--map",
        nargs="+",
        metavar="OLD=NEW",
        help="Bulk rename pairs, e.g. --map email=email_address name=full_name",
    )
    p.add_argument("--output", "-o", help="Output file path (defaults to stdout).")
    p.set_defaults(func=cmd_rename)
    return p


def cmd_rename(args: argparse.Namespace) -> None:
    schema = _load_json(args.schema)

    try:
        if args.map:
            rename_map: dict[str, str] = {}
            for pair in args.map:
                if "=" not in pair:
                    print(f"Invalid map entry (expected OLD=NEW): '{pair}'", file=sys.stderr)
                    sys.exit(1)
                old, _, new = pair.partition("=")
                rename_map[old.strip()] = new.strip()
            result = rename_fields_bulk(schema, rename_map)
        elif args.old_name and args.new_name:
            result = rename_field(schema, args.old_name, args.new_name)
        else:
            print("Provide either --from/--to or --map.", file=sys.stderr)
            sys.exit(1)
    except SchemaRenamerError as exc:
        print(f"Rename error: {exc}", file=sys.stderr)
        sys.exit(1)

    output_json = json.dumps(result, indent=2)
    if args.output:
        _write_json(result, args.output)
        print(f"Written to {args.output}")
    else:
        print(output_json)
