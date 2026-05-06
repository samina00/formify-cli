"""Tests for formify_cli/cli_pick.py"""

import json
import sys
from pathlib import Path

import pytest

from formify_cli.cli_pick import build_pick_parser, cmd_pick
import argparse


@pytest.fixture()
def schema_file(tmp_path):
    schema = {
        "title": "Test Form",
        "fields": [
            {"name": "username", "type": "text", "label": "Username"},
            {"name": "email", "type": "email", "label": "Email"},
            {"name": "age", "type": "number", "label": "Age"},
        ],
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(schema), encoding="utf-8")
    return str(p)


@pytest.fixture()
def output_path(tmp_path):
    return str(tmp_path / "out.json")


def _make_args(**kwargs):
    defaults = {"schema": None, "fields": None, "omit": None, "output": None}
    defaults.update(kwargs)
    ns = argparse.Namespace(**defaults)
    ns.func = cmd_pick
    return ns


def test_pick_writes_output_file(schema_file, output_path):
    args = _make_args(schema=schema_file, fields=["email"], output=output_path)
    cmd_pick(args)
    data = json.loads(Path(output_path).read_text())
    assert len(data["fields"]) == 1
    assert data["fields"][0]["name"] == "email"


def test_pick_prints_to_stdout(schema_file, capsys):
    args = _make_args(schema=schema_file, fields=["username", "age"])
    cmd_pick(args)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert {f["name"] for f in data["fields"]} == {"username", "age"}


def test_omit_removes_field(schema_file, output_path):
    args = _make_args(schema=schema_file, omit=["age"], output=output_path)
    cmd_pick(args)
    data = json.loads(Path(output_path).read_text())
    names = [f["name"] for f in data["fields"]]
    assert "age" not in names
    assert "username" in names


def test_mutually_exclusive_flags_exits(schema_file):
    args = _make_args(schema=schema_file, fields=["email"], omit=["age"])
    with pytest.raises(SystemExit) as exc_info:
        cmd_pick(args)
    assert exc_info.value.code == 1


def test_no_flags_exits(schema_file):
    args = _make_args(schema=schema_file)
    with pytest.raises(SystemExit) as exc_info:
        cmd_pick(args)
    assert exc_info.value.code == 1


def test_bad_schema_path_exits(tmp_path):
    args = _make_args(schema=str(tmp_path / "missing.json"), fields=["email"])
    with pytest.raises(SystemExit) as exc_info:
        cmd_pick(args)
    assert exc_info.value.code == 1


def test_build_pick_parser_registers_subcommand():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()
    build_pick_parser(subs)
    args = parser.parse_args(["pick", "schema.json", "--fields", "email"])
    assert args.fields == ["email"]


def test_pick_preserves_title(schema_file, output_path):
    args = _make_args(schema=schema_file, fields=["email"], output=output_path)
    cmd_pick(args)
    data = json.loads(Path(output_path).read_text())
    assert data["title"] == "Test Form"
