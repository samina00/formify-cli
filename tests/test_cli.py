"""Integration tests for the formify CLI."""

import json
import pytest
from pathlib import Path
from formify_cli.cli import main


SCHEMA = {
    "title": "Contact",
    "fields": [
        {"name": "name", "type": "text", "label": "Name", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
    ],
}


@pytest.fixture()
def schema_file(tmp_path: Path) -> Path:
    p = tmp_path / "schema.json"
    p.write_text(json.dumps(SCHEMA), encoding="utf-8")
    return p


@pytest.fixture()
def valid_data_file(tmp_path: Path) -> Path:
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"name": "Alice", "email": "alice@example.com"}), encoding="utf-8")
    return p


@pytest.fixture()
def invalid_data_file(tmp_path: Path) -> Path:
    p = tmp_path / "data.json"
    p.write_text(json.dumps({"name": "", "email": "bad-email"}), encoding="utf-8")
    return p


def test_generate_exits_zero(schema_file: Path):
    assert main(["generate", str(schema_file)]) == 0


def test_generate_writes_output_file(schema_file: Path, tmp_path: Path):
    out = tmp_path / "form.html"
    assert main(["generate", str(schema_file), "-o", str(out)]) == 0
    assert out.exists()
    assert "<form" in out.read_text(encoding="utf-8")


def test_generate_missing_schema_exits_nonzero(tmp_path: Path):
    assert main(["generate", str(tmp_path / "nope.json")]) != 0


def test_validate_valid_data_exits_zero(schema_file: Path, valid_data_file: Path):
    assert main(["validate", str(schema_file), str(valid_data_file)]) == 0


def test_validate_invalid_data_exits_two(schema_file: Path, invalid_data_file: Path):
    assert main(["validate", str(schema_file), str(invalid_data_file)]) == 2


def test_validate_missing_data_file_exits_nonzero(schema_file: Path, tmp_path: Path):
    assert main(["validate", str(schema_file), str(tmp_path / "missing.json")]) != 0


def test_validate_output_contains_field_name(schema_file: Path, invalid_data_file: Path, capsys):
    main(["validate", str(schema_file), str(invalid_data_file)])
    captured = capsys.readouterr()
    assert "name" in captured.out or "email" in captured.out
