"""Generates a human-readable validation report from form data validation results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


class ReportError(Exception):
    """Raised when a report cannot be generated."""


@dataclass
class ValidationReport:
    """Holds a structured validation report."""

    total_fields: int = 0
    passed_fields: int = 0
    failed_fields: int = 0
    errors: Dict[str, List[str]] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return self.failed_fields == 0

    def summary_line(self) -> str:
        status = "PASSED" if self.is_valid else "FAILED"
        return (
            f"Validation {status}: "
            f"{self.passed_fields}/{self.total_fields} fields valid."
        )

    def as_text(self) -> str:
        lines = [self.summary_line()]
        if self.errors:
            lines.append("")
            lines.append("Errors:")
            for field_name, messages in self.errors.items():
                for msg in messages:
                    lines.append(f"  [{field_name}] {msg}")
        return "\n".join(lines)


def build_report(
    schema: dict,
    validation_errors: Dict[str, List[str]],
) -> ValidationReport:
    """Build a ValidationReport from a schema and a dict of field errors.

    Args:
        schema: The parsed form schema dict (must contain 'fields').
        validation_errors: Mapping of field name -> list of error strings,
            as returned by FormValidator.

    Returns:
        A populated ValidationReport instance.

    Raises:
        ReportError: If schema is invalid or inputs are wrong types.
    """
    if not isinstance(schema, dict) or "fields" not in schema:
        raise ReportError("schema must be a dict with a 'fields' key.")
    if not isinstance(validation_errors, dict):
        raise ReportError("validation_errors must be a dict.")

    fields_list = schema["fields"]
    if not isinstance(fields_list, list):
        raise ReportError("schema['fields'] must be a list.")

    total = len(fields_list)
    failed_names = {k for k, v in validation_errors.items() if v}
    failed = len(failed_names)
    passed = total - failed

    return ValidationReport(
        total_fields=total,
        passed_fields=max(passed, 0),
        failed_fields=failed,
        errors={k: list(v) for k, v in validation_errors.items() if v},
    )
