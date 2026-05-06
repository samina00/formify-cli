"""CLI sub-commands for schema cloning and field renaming."""

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_clone import (
    SchemaCloneError,
    clone_schema,
    prefix_field_names,
    rename_field,
)


def _load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def _write_json(data: dict, path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")


def build_clone_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa: SLF001
    p = subparsers.add_parser("clone", help="Clone or transform a schema file")
    p.add_argument("schema", help="Path to source schema JSON")
    p.add_argument("output", help="Destination path for the cloned schema JSON")
    p.add_argument("--title", help="Override the title in the cloned schema")
    p.add_argument("--rename", nargs=2, metavar=("OLD", "NEW"),
                   help="Rename a field: OLD NEW")
    p.add_argument("--prefix", metavar="PREFIX",
                   help="Prefix all field names with PREFIX")
    p.set_defaults(func=cmd_clone)


def cmd_clone(args: argparse.Namespace) -> None:
    schema = _load_json(args.schema)
    try:
        result = clone_schema(schema, new_title=args.title)
        if args.rename:
            result = rename_field(result, args.rename[0], args.rename[1])
        if args.prefix:
            result = prefix_field_names(result, args.prefix)
    except SchemaCloneError as exc:
        print(f"Clone error: {exc}", file=sys.stderr)
        sys.exit(1)

    _write_json(result, args.output)
    print(f"Schema written to {args.output}")
