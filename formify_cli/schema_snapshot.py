"""Schema snapshot: capture, compare, and restore schema states."""

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any


class SchemaSnapshotError(Exception):
    """Raised when a snapshot operation fails."""


def _check_schema(schema: Any) -> None:
    if not isinstance(schema, dict):
        raise SchemaSnapshotError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaSnapshotError("Schema must contain a 'fields' key.")


def take_snapshot(schema: dict, label: str = "") -> dict:
    """Return a snapshot dict containing a deep copy of the schema plus metadata."""
    _check_schema(schema)
    if not isinstance(label, str):
        raise SchemaSnapshotError("Label must be a string.")
    payload = copy.deepcopy(schema)
    serialised = json.dumps(payload, sort_keys=True)
    checksum = hashlib.sha256(serialised.encode()).hexdigest()
    return {
        "label": label.strip(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checksum": checksum,
        "schema": payload,
    }


def restore_snapshot(snapshot: dict) -> dict:
    """Return a deep copy of the schema stored inside *snapshot*."""
    if not isinstance(snapshot, dict):
        raise SchemaSnapshotError("Snapshot must be a dict.")
    if "schema" not in snapshot:
        raise SchemaSnapshotError("Snapshot is missing the 'schema' key.")
    schema = snapshot["schema"]
    _check_schema(schema)
    return copy.deepcopy(schema)


def snapshots_differ(snap_a: dict, snap_b: dict) -> bool:
    """Return True when the two snapshots contain different schemas."""
    for snap in (snap_a, snap_b):
        if not isinstance(snap, dict) or "checksum" not in snap:
            raise SchemaSnapshotError(
                "Both arguments must be valid snapshot dicts with a 'checksum' key."
            )
    return snap_a["checksum"] != snap_b["checksum"]


def list_snapshot_labels(snapshots: list) -> list:
    """Return the labels from a list of snapshots (empty string when unlabelled)."""
    if not isinstance(snapshots, list):
        raise SchemaSnapshotError("snapshots must be a list.")
    return [s.get("label", "") for s in snapshots]
