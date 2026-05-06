"""CLI sub-command: normalize a schema JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_normalizer import SchemaNormalizerError, normalize_schema, list_unknown_types


def _load_json(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading '{path}': {exc}", file=sys.stderr)
        sys.exit(1)


def build_normalize_parser(subparsers: argparse._SubParsersAction) -> argparse.ArgumentParser:  # type: ignore[type-arg]
    parser = subparsers.add_parser(
        "normalize",
        help="Normalize a schema JSON file to canonical form.",
    )
    parser.add_argument("schema", help="Path to the input schema JSON file.")
    parser.add_argument("-o", "--output", help="Write normalized schema to this file instead of stdout.")
    parser.add_argument("--warn-unknown", action="store_true", help="Print a warning for fields with unknown types.")
    return parser


def cmd_normalize(args: argparse.Namespace) -> None:
    raw = _load_json(args.schema)

    try:
        normalized = normalize_schema(raw)
    except SchemaNormalizerError as exc:
        print(f"Normalization error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.warn_unknown:
        unknown = list_unknown_types(raw)
        for name in unknown:
            print(f"Warning: field '{name}' has an unrecognized type.", file=sys.stderr)

    output_text = json.dumps(normalized, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_text, encoding="utf-8")
        print(f"Normalized schema written to '{args.output}'.")
    else:
        print(output_text)
