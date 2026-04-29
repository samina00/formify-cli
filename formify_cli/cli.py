"""CLI entry point for formify-cli."""

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_parser import load_schema, validate_schema, SchemaValidationError
from formify_cli.html_generator import generate_form, HTMLGenerationError
from formify_cli.validator import validate_form_data, ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="formify",
        description="Generate accessible HTML forms from JSON schema definitions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate sub-command
    gen = subparsers.add_parser("generate", help="Generate an HTML form from a JSON schema.")
    gen.add_argument("schema", type=Path, help="Path to the JSON schema file.")
    gen.add_argument("-o", "--output", type=Path, default=None, help="Output HTML file (default: stdout).")

    # validate sub-command
    val = subparsers.add_parser("validate", help="Validate form data against a JSON schema.")
    val.add_argument("schema", type=Path, help="Path to the JSON schema file.")
    val.add_argument("data", type=Path, help="Path to a JSON file containing form data.")

    return parser


def cmd_generate(args: argparse.Namespace) -> int:
    try:
        schema = load_schema(args.schema)
        validate_schema(schema)
        html = generate_form(schema)
    except (SchemaValidationError, HTMLGenerationError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        args.output.write_text(html, encoding="utf-8")
        print(f"Form written to {args.output}")
    else:
        print(html)
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    try:
        schema = load_schema(args.schema)
        validate_schema(schema)
        with args.data.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (SchemaValidationError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    errors = validate_form_data(schema, data)
    if errors:
        print("Validation failed:")
        for field, messages in errors.items():
            for msg in messages:
                print(f"  [{field}] {msg}")
        return 2

    print("Validation passed — all fields are valid.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "generate":
        return cmd_generate(args)
    if args.command == "validate":
        return cmd_validate(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
