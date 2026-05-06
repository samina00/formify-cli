"""Schema versioning utilities for formify-cli.

Provides functions to read, bump, and compare schema version strings.
"""

from __future__ import annotations

import re
from typing import Tuple

__all__ = [
    "SchemaVersionError",
    "parse_version",
    "bump_version",
    "compare_versions",
    "get_schema_version",
    "set_schema_version",
]

_VERSION_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


class SchemaVersionError(Exception):
    """Raised when a schema version string is invalid or an operation fails."""


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse a semver string 'MAJOR.MINOR.PATCH' into a tuple of ints.

    Raises SchemaVersionError for non-conforming strings.
    """
    if not isinstance(version, str):
        raise SchemaVersionError(f"Version must be a string, got {type(version).__name__}.")
    match = _VERSION_RE.match(version.strip())
    if not match:
        raise SchemaVersionError(
            f"Invalid version string '{version}'. Expected format MAJOR.MINOR.PATCH."
        )
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def bump_version(version: str, part: str = "patch") -> str:
    """Return a new version string with the specified part incremented.

    *part* must be one of 'major', 'minor', or 'patch'.
    Bumping 'major' resets minor and patch to 0.
    Bumping 'minor' resets patch to 0.
    """
    part = part.lower()
    if part not in ("major", "minor", "patch"):
        raise SchemaVersionError(
            f"Unknown version part '{part}'. Choose from: major, minor, patch."
        )
    major, minor, patch = parse_version(version)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def compare_versions(v1: str, v2: str) -> int:
    """Compare two version strings.

    Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2.
    """
    t1 = parse_version(v1)
    t2 = parse_version(v2)
    if t1 < t2:
        return -1
    if t1 > t2:
        return 1
    return 0


def get_schema_version(schema: dict) -> str:
    """Return the 'version' field from a schema dict, defaulting to '0.1.0'."""
    if not isinstance(schema, dict):
        raise SchemaVersionError("Schema must be a dict.")
    return schema.get("version", "0.1.0")


def set_schema_version(schema: dict, version: str) -> dict:
    """Return a copy of *schema* with 'version' set to *version*.

    Validates that *version* is a well-formed semver string.
    """
    if not isinstance(schema, dict):
        raise SchemaVersionError("Schema must be a dict.")
    parse_version(version)  # validate
    updated = dict(schema)
    updated["version"] = version
    return updated
