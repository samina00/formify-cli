"""Tests for formify_cli.schema_version."""

import pytest

from formify_cli.schema_version import (
    SchemaVersionError,
    bump_version,
    compare_versions,
    get_schema_version,
    parse_version,
    set_schema_version,
)


# ---------------------------------------------------------------------------
# parse_version
# ---------------------------------------------------------------------------

def test_parse_version_returns_tuple():
    assert parse_version("1.2.3") == (1, 2, 3)


def test_parse_version_zeros():
    assert parse_version("0.0.0") == (0, 0, 0)


def test_parse_version_strips_whitespace():
    assert parse_version("  2.10.4  ") == (2, 10, 4)


def test_parse_version_raises_for_non_string():
    with pytest.raises(SchemaVersionError, match="string"):
        parse_version(123)


def test_parse_version_raises_for_bad_format():
    with pytest.raises(SchemaVersionError, match="Invalid version"):
        parse_version("1.2")


def test_parse_version_raises_for_alpha():
    with pytest.raises(SchemaVersionError):
        parse_version("1.2.x")


# ---------------------------------------------------------------------------
# bump_version
# ---------------------------------------------------------------------------

def test_bump_patch():
    assert bump_version("1.2.3") == "1.2.4"


def test_bump_minor_resets_patch():
    assert bump_version("1.2.3", "minor") == "1.3.0"


def test_bump_major_resets_minor_and_patch():
    assert bump_version("1.2.3", "major") == "2.0.0"


def test_bump_is_case_insensitive():
    assert bump_version("0.0.1", "PATCH") == "0.0.2"


def test_bump_raises_for_unknown_part():
    with pytest.raises(SchemaVersionError, match="Unknown version part"):
        bump_version("1.0.0", "build")


# ---------------------------------------------------------------------------
# compare_versions
# ---------------------------------------------------------------------------

def test_compare_equal_versions():
    assert compare_versions("1.0.0", "1.0.0") == 0


def test_compare_v1_less_than_v2():
    assert compare_versions("1.0.0", "2.0.0") == -1


def test_compare_v1_greater_than_v2():
    assert compare_versions("1.2.0", "1.1.9") == 1


def test_compare_patch_difference():
    assert compare_versions("0.0.1", "0.0.2") == -1


# ---------------------------------------------------------------------------
# get_schema_version / set_schema_version
# ---------------------------------------------------------------------------

def test_get_schema_version_present():
    schema = {"title": "Test", "version": "2.3.1", "fields": []}
    assert get_schema_version(schema) == "2.3.1"


def test_get_schema_version_defaults_to_0_1_0():
    schema = {"title": "Test", "fields": []}
    assert get_schema_version(schema) == "0.1.0"


def test_get_schema_version_raises_for_non_dict():
    with pytest.raises(SchemaVersionError):
        get_schema_version(["not", "a", "dict"])


def test_set_schema_version_returns_updated_copy():
    schema = {"title": "Test", "fields": []}
    updated = set_schema_version(schema, "3.0.0")
    assert updated["version"] == "3.0.0"


def test_set_schema_version_does_not_mutate_original():
    schema = {"title": "Test", "fields": []}
    set_schema_version(schema, "1.0.0")
    assert "version" not in schema


def test_set_schema_version_raises_for_invalid_version():
    schema = {"title": "Test", "fields": []}
    with pytest.raises(SchemaVersionError):
        set_schema_version(schema, "not-a-version")


def test_set_schema_version_raises_for_non_dict():
    with pytest.raises(SchemaVersionError):
        set_schema_version("oops", "1.0.0")
