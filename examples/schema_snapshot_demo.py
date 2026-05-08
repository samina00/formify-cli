"""Demonstrates the schema snapshot feature."""

import copy
import json

from formify_cli.schema_snapshot import (
    list_snapshot_labels,
    restore_snapshot,
    snapshots_differ,
    take_snapshot,
)


def demo_take_and_inspect() -> None:
    print("=== Take & Inspect ===")
    schema = {
        "title": "Newsletter Signup",
        "fields": [
            {"name": "email", "type": "email", "label": "Email Address", "required": True},
            {"name": "name", "type": "text", "label": "Full Name"},
        ],
    }
    snap = take_snapshot(schema, label="v1.0")
    print(f"  Label    : {snap['label']}")
    print(f"  Timestamp: {snap['timestamp']}")
    print(f"  Checksum : {snap['checksum'][:16]}...")
    print()


def demo_restore() -> None:
    print("=== Restore ===")
    schema = {
        "title": "Feedback",
        "fields": [{"name": "msg", "type": "textarea", "label": "Message"}],
    }
    snap = take_snapshot(schema, label="original")
    restored = restore_snapshot(snap)
    print(f"  Restored title : {restored['title']}")
    print(f"  Field count    : {len(restored['fields'])}")
    print()


def demo_diff() -> None:
    print("=== Diff ===")
    schema = {
        "title": "Login",
        "fields": [{"name": "user", "type": "text", "label": "Username"}],
    }
    snap_a = take_snapshot(schema, label="before")
    modified = copy.deepcopy(schema)
    modified["fields"].append({"name": "pass", "type": "password", "label": "Password"})
    snap_b = take_snapshot(modified, label="after")
    print(f"  Same schema -> differ: {snapshots_differ(snap_a, snap_a)}")
    print(f"  Modified    -> differ: {snapshots_differ(snap_a, snap_b)}")
    print()


def demo_snapshot_history() -> None:
    print("=== Snapshot History ===")
    schema = {
        "title": "Survey",
        "fields": [{"name": "q1", "type": "text", "label": "Question 1"}],
    }
    history = [
        take_snapshot(schema, label="draft"),
        take_snapshot(schema, label="review"),
        take_snapshot(schema, label="published"),
    ]
    labels = list_snapshot_labels(history)
    print("  Labels:", labels)
    print()


def main() -> None:
    demo_take_and_inspect()
    demo_restore()
    demo_diff()
    demo_snapshot_history()


if __name__ == "__main__":
    main()
