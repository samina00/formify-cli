"""Integration-style tests for cli_clone sub-commands."""

import json
import sys
from pathlib import Path

import pytest

from formify_cli.cli_clone import build_clone_parser, cmd_clone
import argparse


@pytest.fixture()
def schema_file(tmp_path):
    data = {
        "title": "Original",
        "fields": [
            {"name": "first", "type": "text", "label": "First"},
            {"name": "last", "type": "text", "label": "Last"},
        ],
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(data))
    return str(p)


@pytest.fixture()
def output_path(tmp_path):
    return str(tmp_path / "out" / "cloned.json")


def _run(schema_file, output_path, extra=None):
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()
    build_clone_parser(subs)
    argv = ["clone", schema_file, output_path] + (extra or [])
    args = parser.parse_args(argv)
    args.func(args)
    return json.loads(Path(output_path).read_text())


def test_clone_creates_output_file(schema_file, output_path):
    result = _run(schema_file, output_path)
    assert Path(output_path).exists()
    assert result["title"] == "Original"


def test_clone_with_title_override(schema_file, output_path):
    result = _run(schema_file, output_path, ["--title", "Renamed"])
    assert result["title"] == "Renamed"


def test_clone_with_rename(schema_file, output_path):
    result = _run(schema_file, output_path, ["--rename", "first", "given_name"])
    names = [f["name"] for f in result["fields"]]
    assert "given_name" in names
    assert "first" not in names


def test_clone_with_prefix(schema_file, output_path):
    result = _run(schema_file, output_path, ["--prefix", "p_"])
    names = [f["name"] for f in result["fields"]]
    assert all(n.startswith("p_") for n in names)


def test_clone_bad_rename_exits_nonzero(schema_file, output_path):
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()
    build_clone_parser(subs)
    args = parser.parse_args(["clone", schema_file, output_path, "--rename", "nonexistent", "x"])
    with pytest.raises(SystemExit) as exc_info:
        args.func(args)
    assert exc_info.value.code != 0


def test_clone_bad_prefix_exits_nonzero(schema_file, output_path):
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()
    build_clone_parser(subs)
    args = parser.parse_args(["clone", schema_file, output_path, "--prefix", "bad prefix!"])
    with pytest.raises(SystemExit) as exc_info:
        args.func(args)
    assert exc_info.value.code != 0


def test_clone_creates_parent_directories(schema_file, tmp_path):
    deep_out = str(tmp_path / "a" / "b" / "c" / "out.json")
    result = _run(schema_file, deep_out)
    assert Path(deep_out).exists()
