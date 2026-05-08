"""Tests for formify_cli.schema_snapshot."""

import pytest

from formify_cli.schema_snapshot import (
    SchemaSnapshotError,
    list_snapshot_labels,
    restore_snapshot,
    snapshots_differ,
    take_snapshot,
)


@pytest.fixture
def simple_schema():
    return {
        "title": "Contact",
        "fields": [
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "message", "type": "textarea", "label": "Message"},
        ],
    }


def test_take_snapshot_returns_dict(simple_schema):
    snap = take_snapshot(simple_schema)
    assert isinstance(snap, dict)


def test_take_snapshot_contains_required_keys(simple_schema):
    snap = take_snapshot(simple_schema)
    for key in ("label", "timestamp", "checksum", "schema"):
        assert key in snap


def test_take_snapshot_stores_schema_copy(simple_schema):
    snap = take_snapshot(simple_schema)
    assert snap["schema"] == simple_schema
    assert snap["schema"] is not simple_schema


def test_take_snapshot_label_stored(simple_schema):
    snap = take_snapshot(simple_schema, label="v1")
    assert snap["label"] == "v1"


def test_take_snapshot_label_stripped(simple_schema):
    snap = take_snapshot(simple_schema, label="  v2  ")
    assert snap["label"] == "v2"


def test_take_snapshot_checksum_is_hex_string(simple_schema):
    snap = take_snapshot(simple_schema)
    assert isinstance(snap["checksum"], str)
    assert len(snap["checksum"]) == 64


def test_take_snapshot_raises_for_non_dict():
    with pytest.raises(SchemaSnapshotError):
        take_snapshot(["not", "a", "dict"])


def test_take_snapshot_raises_for_missing_fields_key():
    with pytest.raises(SchemaSnapshotError):
        take_snapshot({"title": "No fields"})


def test_take_snapshot_raises_for_non_string_label(simple_schema):
    with pytest.raises(SchemaSnapshotError):
        take_snapshot(simple_schema, label=42)


def test_restore_snapshot_returns_schema(simple_schema):
    snap = take_snapshot(simple_schema)
    restored = restore_snapshot(snap)
    assert restored == simple_schema


def test_restore_snapshot_returns_copy(simple_schema):
    snap = take_snapshot(simple_schema)
    restored = restore_snapshot(snap)
    assert restored is not snap["schema"]


def test_restore_snapshot_raises_for_non_dict():
    with pytest.raises(SchemaSnapshotError):
        restore_snapshot("not a snapshot")


def test_restore_snapshot_raises_for_missing_schema_key():
    with pytest.raises(SchemaSnapshotError):
        restore_snapshot({"label": "x", "checksum": "abc"})


def test_snapshots_differ_returns_false_for_identical(simple_schema):
    snap_a = take_snapshot(simple_schema)
    snap_b = take_snapshot(simple_schema)
    assert snapshots_differ(snap_a, snap_b) is False


def test_snapshots_differ_returns_true_after_change(simple_schema):
    snap_a = take_snapshot(simple_schema)
    modified = dict(simple_schema)
    modified["title"] = "Changed"
    snap_b = take_snapshot(modified)
    assert snapshots_differ(snap_a, snap_b) is True


def test_snapshots_differ_raises_for_invalid_snapshot(simple_schema):
    snap = take_snapshot(simple_schema)
    with pytest.raises(SchemaSnapshotError):
        snapshots_differ(snap, {"no_checksum": True})


def test_list_snapshot_labels_returns_list(simple_schema):
    snaps = [take_snapshot(simple_schema, label="a"), take_snapshot(simple_schema, label="b")]
    assert list_snapshot_labels(snaps) == ["a", "b"]


def test_list_snapshot_labels_raises_for_non_list(simple_schema):
    with pytest.raises(SchemaSnapshotError):
        list_snapshot_labels("not a list")
