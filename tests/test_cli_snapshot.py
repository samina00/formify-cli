"""Tests for formify_cli.cli_snapshot."""

import json
import sys
from pathlib import Path

import pytest

from formify_cli.cli_snapshot import cmd_diff, cmd_restore, cmd_take
from formify_cli.schema_snapshot import take_snapshot


@pytest.fixture
def schema_file(tmp_path):
    schema = {
        "title": "Signup",
        "fields": [
            {"name": "username", "type": "text", "label": "Username"},
        ],
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(schema))
    return str(p)


@pytest.fixture
def snapshot_file(tmp_path, schema_file):
    schema = json.loads(Path(schema_file).read_text())
    snap = take_snapshot(schema, label="initial")
    p = tmp_path / "snap.json"
    p.write_text(json.dumps(snap))
    return str(p)


@pytest.fixture
def output_path(tmp_path):
    return str(tmp_path / "output.json")


class _Args:
    pass


def _make_take_args(schema, output, label=""):
    a = _Args()
    a.schema = schema
    a.output = output
    a.label = label
    return a


def _make_restore_args(snapshot, output):
    a = _Args()
    a.snapshot = snapshot
    a.output = output
    return a


def _make_diff_args(snap_a, snap_b):
    a = _Args()
    a.snapshot_a = snap_a
    a.snapshot_b = snap_b
    return a


def test_cmd_take_creates_output_file(schema_file, output_path):
    cmd_take(_make_take_args(schema_file, output_path))
    assert Path(output_path).exists()


def test_cmd_take_output_contains_checksum(schema_file, output_path):
    cmd_take(_make_take_args(schema_file, output_path))
    data = json.loads(Path(output_path).read_text())
    assert "checksum" in data
    assert len(data["checksum"]) == 64


def test_cmd_take_stores_label(schema_file, output_path):
    cmd_take(_make_take_args(schema_file, output_path, label="release-1"))
    data = json.loads(Path(output_path).read_text())
    assert data["label"] == "release-1"


def test_cmd_restore_creates_schema_file(snapshot_file, output_path):
    cmd_restore(_make_restore_args(snapshot_file, output_path))
    assert Path(output_path).exists()


def test_cmd_restore_schema_has_fields(snapshot_file, output_path):
    cmd_restore(_make_restore_args(snapshot_file, output_path))
    schema = json.loads(Path(output_path).read_text())
    assert "fields" in schema


def test_cmd_diff_identical_exits_zero(snapshot_file, capsys):
    args = _make_diff_args(snapshot_file, snapshot_file)
    cmd_diff(args)  # should not raise
    out = capsys.readouterr().out
    assert "IDENTICAL" in out


def test_cmd_diff_different_exits_one(tmp_path, schema_file, snapshot_file):
    schema2 = {
        "title": "Other",
        "fields": [{"name": "x", "type": "text", "label": "X"}],
    }
    snap2 = take_snapshot(schema2)
    p2 = tmp_path / "snap2.json"
    p2.write_text(json.dumps(snap2))
    args = _make_diff_args(snapshot_file, str(p2))
    with pytest.raises(SystemExit) as exc_info:
        cmd_diff(args)
    assert exc_info.value.code == 1
