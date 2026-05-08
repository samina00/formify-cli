"""CLI sub-command: validate-rules — run schema rule validation on form data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_validator_report import (
    FieldRuleReportError,
    validate_schema_rules,
)


def _load_json(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Error loading {path!r}: {exc}", file=sys.stderr)
        sys.exit(1)


def build_validate_rules_parser(subparsers: argparse._SubParsersAction) -> None:
    parser = subparsers.add_parser(
        "validate-rules",
        help="Validate form data against schema field rules and print a report.",
    )
    parser.add_argument("schema", help="Path to JSON schema file")
    parser.add_argument("data", help="Path to JSON form data file")
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Exit with code 1 if any rule fails",
    )
    parser.set_defaults(func=cmd_validate_rules)


def cmd_validate_rules(args: argparse.Namespace) -> None:
    schema = _load_json(args.schema)
    data = _load_json(args.data)

    try:
        reports = validate_schema_rules(schema, data)
    except FieldRuleReportError as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        sys.exit(1)

    any_failed = False
    for field_name, report in reports.items():
        if report.results:
            print(report.as_text())
        if not report.passed:
            any_failed = True

    if not any_failed:
        print("All field rules passed.")
    elif args.fail_fast:
        sys.exit(1)
