"""cli_freeze.py — CLI sub-commands for freezing/thawing schemas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_freezer import SchemaFreezerError, freeze_schema, is_frozen, thaw_schema


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


def build_freeze_parser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore[type-arg]
    p = subparsers.add_parser("freeze", help="Freeze a schema (report immutability status).")
    p.add_argument("schema", help="Path to the JSON schema file.")
    p.add_argument("-o", "--output", help="Write thawed/plain copy to this path.")
    p.set_defaults(func=cmd_freeze)


def cmd_freeze(args: argparse.Namespace) -> None:
    schema = _load_json(args.schema)
    try:
        frozen = freeze_schema(schema)
    except SchemaFreezerError as exc:
        print(f"freeze error: {exc}", file=sys.stderr)
        sys.exit(1)

    field_count = len(frozen.get("fields", ()))
    print(f"Schema '{frozen.get('title', '(untitled)')}' frozen successfully.")
    print(f"  Fields : {field_count}")
    print(f"  Frozen : {is_frozen(frozen)}")

    if args.output:
        # Thaw before writing so the output is plain JSON-serialisable dict
        plain = thaw_schema(frozen)
        _write_json(plain, args.output)
        print(f"  Written: {args.output}")
