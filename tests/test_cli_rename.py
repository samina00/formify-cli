"""Tests for formify_cli.cli_rename."""

import json
import argparse
import pytest
from pathlib import Path

from formify_cli.cli_rename import build_rename_parser, cmd_rename


@pytest.fixture()
def schema_file(tmp_path):
    schema = {
        "title": "Demo",
        "fields": [
            {"name": "email", "type": "email", "label": "Email", "required": True},
            {"name": "name", "type": "text", "label": "Name", "required": False},
        ],
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(schema))
    return str(p)


@pytest.fixture()
def output_path(tmp_path):
    return str(tmp_path / "out.json")


def _make_args(**kwargs):
    defaults = {"old_name": None, "new_name": None, "map": None, "output": None}
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def test_rename_single_writes_output_file(schema_file, output_path):
    args = _make_args(schema=schema_file, old_name="email", new_name="email_address", output=output_path)
    cmd_rename(args)
    data = json.loads(Path(output_path).read_text())
    names = [f["name"] for f in data["fields"]]
    assert "email_address" in names
    assert "email" not in names


def test_rename_single_prints_to_stdout(schema_file, capsys):
    args = _make_args(schema=schema_file, old_name="email", new_name="email_address")
    cmd_rename(args)
    out = capsys.readouterr().out
    data = json.loads(out)
    names = [f["name"] for f in data["fields"]]
    assert "email_address" in names


def test_rename_bulk_via_map(schema_file, output_path):
    args = _make_args(schema=schema_file, map=["email=email_address", "name=full_name"], output=output_path)
    cmd_rename(args)
    data = json.loads(Path(output_path).read_text())
    names = [f["name"] for f in data["fields"]]
    assert "email_address" in names
    assert "full_name" in names


def test_rename_exits_on_unknown_field(schema_file):
    args = _make_args(schema=schema_file, old_name="ghost", new_name="phantom")
    with pytest.raises(SystemExit) as exc_info:
        cmd_rename(args)
    assert exc_info.value.code == 1


def test_rename_exits_when_no_args_given(schema_file):
    args = _make_args(schema=schema_file)
    with pytest.raises(SystemExit) as exc_info:
        cmd_rename(args)
    assert exc_info.value.code == 1


def test_rename_exits_on_bad_map_entry(schema_file):
    args = _make_args(schema=schema_file, map=["email_no_equals"])
    with pytest.raises(SystemExit) as exc_info:
        cmd_rename(args)
    assert exc_info.value.code == 1


def test_build_rename_parser_registers_subcommand():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()
    build_rename_parser(subs)
    args = parser.parse_args(["rename", "schema.json", "--from", "a", "--to", "b"])
    assert args.old_name == "a"
    assert args.new_name == "b"
