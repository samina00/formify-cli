"""Example script: generate a form from a schema and preview it in the browser.

Usage::

    python examples/preview_example.py
    python examples/preview_example.py --port 9000 --no-browser
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running from the repo root without installing the package.
sys.path.insert(0, str(Path(__file__).parent.parent))

from formify_cli.html_generator import generate_form
from formify_cli.preview_server import PreviewError, start_preview
from formify_cli.schema_parser import load_schema, validate_schema
from formify_cli.theme import get_theme
from formify_cli.theme_renderer import build_themed_form


DEFAULT_SCHEMA = Path(__file__).parent / "contact_form.json"
DEFAULT_PORT = 8080


def main() -> None:
    parser = argparse.ArgumentParser(description="Preview a form schema in the browser.")
    parser.add_argument(
        "schema",
        nargs="?",
        default=str(DEFAULT_SCHEMA),
        help="Path to a JSON schema file (default: examples/contact_form.json)",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to listen on")
    parser.add_argument(
        "--theme",
        default="default",
        help="Built-in theme name (default: 'default')",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Do not open the browser automatically",
    )
    args = parser.parse_args()

    schema = load_schema(args.schema)
    validate_schema(schema)

    theme = get_theme(args.theme)
    html = build_themed_form(schema, theme)

    print(f"Schema : {args.schema}")
    print(f"Theme  : {args.theme}")
    print(f"Port   : {args.port}")

    try:
        start_preview(
            html,
            port=args.port,
            open_browser=not args.no_browser,
            block=True,
        )
    except PreviewError as exc:
        print(f"Preview error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
