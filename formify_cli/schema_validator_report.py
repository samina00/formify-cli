"""Schema field-level rule validation with structured report output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from formify_cli.schema_validator_rules import apply_rule, list_rules, RuleError


class FieldRuleReportError(Exception):
    """Raised when report generation fails due to bad input."""


@dataclass
class FieldRuleResult:
    field_name: str
    rule: str
    passed: bool
    message: str = ""


@dataclass
class FieldRuleReport:
    results: list[FieldRuleResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    def failures(self) -> list[FieldRuleResult]:
        return [r for r in self.results if not r.passed]

    def summary_line(self) -> str:
        total = len(self.results)
        failed = len(self.failures())
        if total == 0:
            return "No rules evaluated."
        if failed == 0:
            return f"All {total} rule(s) passed."
        return f"{failed}/{total} rule(s) failed."

    def as_text(self) -> str:
        lines = [self.summary_line()]
        for r in self.results:
            status = "PASS" if r.passed else "FAIL"
            line = f"  [{status}] {r.field_name!r} — {r.rule}"
            if not r.passed and r.message:
                line += f": {r.message}"
            lines.append(line)
        return "\n".join(lines)


def validate_field_rules(
    field_def: dict[str, Any],
    value: Any,
    field_name: str = "",
) -> FieldRuleReport:
    """Run all applicable rules for a single field against a value."""
    if not isinstance(field_def, dict):
        raise FieldRuleReportError("field_def must be a dict")
    if not field_name:
        field_name = field_def.get("name", "<unknown>")

    results: list[FieldRuleResult] = []
    for rule_name in list_rules():
        if rule_name not in field_def:
            continue
        try:
            apply_rule(rule_name, value, field_def)
            results.append(FieldRuleResult(field_name, rule_name, True))
        except RuleError as exc:
            results.append(FieldRuleResult(field_name, rule_name, False, str(exc)))

    return FieldRuleReport(results=results)


def validate_schema_rules(
    schema: dict[str, Any],
    data: dict[str, Any],
) -> dict[str, FieldRuleReport]:
    """Validate all fields in a schema against provided data."""
    if not isinstance(schema, dict) or "fields" not in schema:
        raise FieldRuleReportError("schema must be a dict with a 'fields' key")
    if not isinstance(data, dict):
        raise FieldRuleReportError("data must be a dict")

    reports: dict[str, FieldRuleReport] = {}
    for field_def in schema["fields"]:
        name = field_def.get("name", "")
        value = data.get(name)
        reports[name] = validate_field_rules(field_def, value, name)
    return reports
