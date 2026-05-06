"""Tests for formify_cli.cli_normalize."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from formify_cli.cli_normalize import build_normalize_parser, cmd_normalize
import argparse


@pytest.fixture()
def schema_file(tmp_path: Path) -> Path:
    schema = {
        "title": "Test Form",
        "fields": [
            {"name": "username", "type": "TEXT", "label": " User "},
            {"name": "email", "type": "email", "label": "Email", "required": True},
        ],
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(schema), encoding="utf-8")
    return p


@pytest.fixture()
def bad_schema_file(tmp_path: Path) -> Path:
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"title": "No fields"}), encoding="utf-8")
    return p


def _make_args(**kwargs) -> argparse.Namespace:
    defaults = {"output": None, "warn_unknown": False}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_cmd_normalize_prints_to_stdout(schema_file: Path, capsys):
    args = _make_args(schema=str(schema_file))
    cmd_normalize(args)
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result["title"] == "Test Form"
    assert len(result["fields"]) == 2


def test_cmd_normalize_lowercases_type(schema_file: Path, capsys):
    args = _make_args(schema=str(schema_file))
    cmd_normalize(args)
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    types = [f["type"] for f in result["fields"]]
    assert all(t == t.lower() for t in types)


def test_cmd_normalize_writes_output_file(schema_file: Path, tmp_path: Path, capsys):
    out = tmp_path / "out" / "normalized.json"
    args = _make_args(schema=str(schema_file), output=str(out))
    cmd_normalize(args)
    assert out.exists()
    data = json.loads(out.read_text())
    assert "fields" in data


def test_cmd_normalize_exits_on_bad_schema(bad_schema_file: Path):
    args = _make_args(schema=str(bad_schema_file))
    with pytest.raises(SystemExit) as exc_info:
        cmd_normalize(args)
    assert exc_info.value.code == 1


def test_cmd_normalize_warn_unknown_prints_warning(tmp_path: Path, capsys):
    schema = {
        "title": "T",
        "fields": [{"name": "w", "type": "custom_widget", "label": "W"}],
    }
    p = tmp_path / "s.json"
    p.write_text(json.dumps(schema))
    args = _make_args(schema=str(p), warn_unknown=True)
    cmd_normalize(args)
    captured = capsys.readouterr()
    assert "Warning" in captured.err
    assert "w" in captured.err


def test_build_normalize_parser_registers_subcommand():
    root = argparse.ArgumentParser()
    sub = root.add_subparsers(dest="command")
    build_normalize_parser(sub)
    parsed = root.parse_args(["normalize", "schema.json"])
    assert parsed.command == "normalize"
    assert parsed.schema == "schema.json"


def test_cmd_normalize_exits_for_missing_file():
    args = _make_args(schema="/nonexistent/schema.json")
    with pytest.raises(SystemExit) as exc_info:
        cmd_normalize(args)
    assert exc_info.value.code == 1
