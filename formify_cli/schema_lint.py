"""Schema linting: detect common issues and anti-patterns in form schemas."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class SchemaLintError(Exception):
    """Raised when linting cannot be performed."""


@dataclass
class LintResult:
    warnings: list[str] = field(default_factory=list)
    hints: list[str] = field(default_factory=list)

    @property
    def has_issues(self) -> bool:
        return bool(self.warnings or self.hints)

    def summary_line(self) -> str:
        w = len(self.warnings)
        h = len(self.hints)
        if not self.has_issues:
            return "No issues found."
        parts = []
        if w:
            parts.append(f"{w} warning(s)")
        if h:
            parts.append(f"{h} hint(s)")
        return "Schema lint: " + ", ".join(parts) + "."

    def as_text(self) -> str:
        lines = [self.summary_line()]
        for msg in self.warnings:
            lines.append(f"  [WARN]  {msg}")
        for msg in self.hints:
            lines.append(f"  [HINT]  {msg}")
        return "\n".join(lines)


_KNOWN_TYPES = {"text", "email", "number", "select", "textarea", "checkbox", "radio", "date", "password", "url"}
_RECOMMENDED_ATTRS = {"email": "placeholder", "text": "placeholder"}


def lint_schema(schema: Any) -> LintResult:
    """Analyse *schema* and return a :class:`LintResult` with warnings/hints."""
    if not isinstance(schema, dict):
        raise SchemaLintError("Schema must be a dict.")
    if "fields" not in schema:
        raise SchemaLintError("Schema missing 'fields' key.")

    result = LintResult()
    fields_list = schema["fields"]

    if not schema.get("title", "").strip():
        result.hints.append("Schema has no 'title'; consider adding one for better accessibility.")

    seen_names: set[str] = set()
    for i, f in enumerate(fields_list):
        tag = f.get("name") or f"field[{i}]"

        ftype = f.get("type", "")
        if ftype not in _KNOWN_TYPES:
            result.warnings.append(f"'{tag}': unknown field type '{ftype}'.")

        if not f.get("label", "").strip():
            result.warnings.append(f"'{tag}': missing or empty 'label'; harms accessibility.")

        name = f.get("name", "")
        if not name:
            result.warnings.append(f"Field at index {i}: missing 'name' attribute.")
        elif name in seen_names:
            result.warnings.append(f"Duplicate field name '{name}' detected.")
        else:
            seen_names.add(name)

        if ftype in _RECOMMENDED_ATTRS and not f.get(_RECOMMENDED_ATTRS[ftype]):
            result.hints.append(f"'{tag}': adding a 'placeholder' improves usability for {ftype} fields.")

        if ftype in {"select", "radio"} and not f.get("options"):
            result.warnings.append(f"'{tag}': '{ftype}' field has no 'options'.")

    return result
