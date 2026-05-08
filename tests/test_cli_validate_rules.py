"""Tests for cli_validate_rules sub-command."""

import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from formify_cli.cli_validate_rules import cmd_validate_rules


@pytest.fixture
def schema_file(tmp_path):
    schema = {
        "title": "Test Form",
        "fields": [
            {"name": "username", "type": "text", "min_length": 3, "max_length": 20},
        ],
    }
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(schema))
    return str(p)


@pytest.fixture
def valid_data_file(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"username": "alice"}))
    return str(p)


@pytest.fixture
def invalid_data_file(tmp_path):
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"username": "ab"}))
    return str(p)


def _make_args(schema, data, fail_fast=False):
    return SimpleNamespace(schema=schema, data=data, fail_fast=fail_fast)


def test_cmd_validate_rules_passes_on_valid_data(schema_file, valid_data_file, capsys):
    args = _make_args(schema_file, valid_data_file)
    cmd_validate_rules(args)
    out = capsys.readouterr().out
    assert "All field rules passed" in out


def test_cmd_validate_rules_reports_failure(schema_file, invalid_data_file, capsys):
    args = _make_args(schema_file, invalid_data_file)
    cmd_validate_rules(args)
    out = capsys.readouterr().out
    assert "FAIL" in out


def test_cmd_validate_rules_fail_fast_exits_1(schema_file, invalid_data_file):
    args = _make_args(schema_file, invalid_data_file, fail_fast=True)
    with pytest.raises(SystemExit) as exc_info:
        cmd_validate_rules(args)
    assert exc_info.value.code == 1


def test_cmd_validate_rules_no_exit_without_fail_fast(schema_file, invalid_data_file):
    args = _make_args(schema_file, invalid_data_file, fail_fast=False)
    # Should not raise
    cmd_validate_rules(args)


def test_cmd_validate_rules_bad_schema_path_exits(tmp_path, valid_data_file):
    args = _make_args(str(tmp_path / "missing.json"), valid_data_file)
    with pytest.raises(SystemExit) as exc_info:
        cmd_validate_rules(args)
    assert exc_info.value.code == 1


def test_cmd_validate_rules_bad_data_path_exits(schema_file, tmp_path):
    args = _make_args(schema_file, str(tmp_path / "missing.json"))
    with pytest.raises(SystemExit) as exc_info:
        cmd_validate_rules(args)
    assert exc_info.value.code == 1


def test_cmd_validate_rules_invalid_schema_content_exits(tmp_path, valid_data_file):
    bad_schema = tmp_path / "bad.json"
    bad_schema.write_text(json.dumps("not a dict"))
    args = _make_args(str(bad_schema), valid_data_file)
    with pytest.raises(SystemExit) as exc_info:
        cmd_validate_rules(args)
    assert exc_info.value.code == 1
