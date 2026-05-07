"""Tests for formify_cli.cli_freeze."""

import json
import sys
from pathlib import Path

import pytest

from formify_cli.cli_freeze import cmd_freeze


@pytest.fixture
def schema_file(tmp_path):
    schema = {
        "title": "Login Form",
        "fields": [
            {"name": "user", "type": "text", "label": "User", "required": True},
            {"name": "pass", "type": "password", "label": "Password", "required": True},
        ],
    }
    p = tmp_path / "login.json"
    p.write_text(json.dumps(schema))
    return str(p)


@pytest.fixture
def output_path(tmp_path):
    return str(tmp_path / "out" / "frozen_copy.json")


def _make_args(schema, output=None):
    class Args:
        pass
    a = Args()
    a.schema = schema
    a.output = output
    return a


def test_cmd_freeze_prints_title(schema_file, capsys):
    cmd_freeze(_make_args(schema_file))
    out = capsys.readouterr().out
    assert "Login Form" in out


def test_cmd_freeze_prints_field_count(schema_file, capsys):
    cmd_freeze(_make_args(schema_file))
    out = capsys.readouterr().out
    assert "2" in out


def test_cmd_freeze_prints_frozen_true(schema_file, capsys):
    cmd_freeze(_make_args(schema_file))
    out = capsys.readouterr().out
    assert "True" in out


def test_cmd_freeze_writes_output_file(schema_file, output_path):
    cmd_freeze(_make_args(schema_file, output=output_path))
    assert Path(output_path).exists()


def test_cmd_freeze_output_is_valid_json(schema_file, output_path):
    cmd_freeze(_make_args(schema_file, output=output_path))
    data = json.loads(Path(output_path).read_text())
    assert data["title"] == "Login Form"


def test_cmd_freeze_output_fields_is_list(schema_file, output_path):
    cmd_freeze(_make_args(schema_file, output=output_path))
    data = json.loads(Path(output_path).read_text())
    assert isinstance(data["fields"], list)


def test_cmd_freeze_creates_parent_dirs(schema_file, tmp_path):
    nested = str(tmp_path / "a" / "b" / "c" / "out.json")
    cmd_freeze(_make_args(schema_file, output=nested))
    assert Path(nested).exists()


def test_cmd_freeze_exits_on_bad_file(tmp_path):
    with pytest.raises(SystemExit):
        cmd_freeze(_make_args(str(tmp_path / "missing.json")))
