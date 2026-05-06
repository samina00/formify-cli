"""cli_pick.py — CLI sub-commands for picking/omitting schema fields."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_picker import SchemaPickerError, omit_fields, pick_fields


def _load_json(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def _write_output(data: dict, output: str | None) -> None:
    text = json.dumps(data, indent=2)
    if output:
        Path(output).write_text(text, encoding="utf-8")
        print(f"Written to {output}")
    else:
        print(text)


def build_pick_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:
    p = subparsers.add_parser(
        "pick",
        help="Select or omit specific fields from a schema.",
    )
    p.add_argument("schema", help="Path to the JSON schema file.")
    p.add_argument(
        "--fields",
        nargs="+",
        metavar="NAME",
        help="Field names to keep (pick mode).",
    )
    p.add_argument(
        "--omit",
        nargs="+",
        metavar="NAME",
        help="Field names to remove (omit mode).",
    )
    p.add_argument("-o", "--output", help="Write result to this file instead of stdout.")
    p.set_defaults(func=cmd_pick)
    return p


def cmd_pick(args: argparse.Namespace) -> None:
    schema = _load_json(args.schema)

    if args.fields and args.omit:
        print("Error: --fields and --omit are mutually exclusive.", file=sys.stderr)
        sys.exit(1)

    if not args.fields and not args.omit:
        print("Error: provide --fields or --omit.", file=sys.stderr)
        sys.exit(1)

    try:
        if args.fields:
            result = pick_fields(schema, args.fields)
        else:
            result = omit_fields(schema, args.omit)
    except SchemaPickerError as exc:
        print(f"Pick error: {exc}", file=sys.stderr)
        sys.exit(1)

    _write_output(result, args.output)
