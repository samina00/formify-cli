"""CLI sub-commands for schema snapshot operations."""

import argparse
import json
import sys
from pathlib import Path

from formify_cli.schema_snapshot import (
    SchemaSnapshotError,
    restore_snapshot,
    snapshots_differ,
    take_snapshot,
)


def _load_json(path: str) -> dict:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"Error reading {path}: {exc}", file=sys.stderr)
        sys.exit(1)


def _write_json(data: dict, path: str) -> None:
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def build_snapshot_parser(subparsers: argparse._SubParsersAction) -> None:  # noqa: SLF001
    p = subparsers.add_parser("snapshot", help="Take or restore a schema snapshot.")
    sub = p.add_subparsers(dest="snapshot_cmd", required=True)

    take_p = sub.add_parser("take", help="Capture current schema as a snapshot.")
    take_p.add_argument("schema", help="Path to the schema JSON file.")
    take_p.add_argument("output", help="Destination path for the snapshot JSON file.")
    take_p.add_argument("--label", default="", help="Optional human-readable label.")
    take_p.set_defaults(func=cmd_take)

    restore_p = sub.add_parser("restore", help="Restore schema from a snapshot.")
    restore_p.add_argument("snapshot", help="Path to the snapshot JSON file.")
    restore_p.add_argument("output", help="Destination path for the restored schema.")
    restore_p.set_defaults(func=cmd_restore)

    diff_p = sub.add_parser("diff", help="Check whether two snapshots differ.")
    diff_p.add_argument("snapshot_a", help="First snapshot JSON file.")
    diff_p.add_argument("snapshot_b", help="Second snapshot JSON file.")
    diff_p.set_defaults(func=cmd_diff)


def cmd_take(args: argparse.Namespace) -> None:
    schema = _load_json(args.schema)
    try:
        snap = take_snapshot(schema, label=args.label)
    except SchemaSnapshotError as exc:
        print(f"Snapshot error: {exc}", file=sys.stderr)
        sys.exit(1)
    _write_json(snap, args.output)
    print(f"Snapshot saved to {args.output} (checksum: {snap['checksum'][:12]}...)")


def cmd_restore(args: argparse.Namespace) -> None:
    snap = _load_json(args.snapshot)
    try:
        schema = restore_snapshot(snap)
    except SchemaSnapshotError as exc:
        print(f"Restore error: {exc}", file=sys.stderr)
        sys.exit(1)
    _write_json(schema, args.output)
    print(f"Schema restored to {args.output}")


def cmd_diff(args: argparse.Namespace) -> None:
    snap_a = _load_json(args.snapshot_a)
    snap_b = _load_json(args.snapshot_b)
    try:
        differ = snapshots_differ(snap_a, snap_b)
    except SchemaSnapshotError as exc:
        print(f"Diff error: {exc}", file=sys.stderr)
        sys.exit(1)
    if differ:
        print("Snapshots DIFFER.")
        sys.exit(1)
    print("Snapshots are IDENTICAL.")
