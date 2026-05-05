"""Demo showing schema_validator_rules and rule_renderer working together."""

from formify_cli.schema_validator_rules import apply_all_rules, list_rules
from formify_cli.rule_renderer import render_rule_attrs, render_rule_hint, describe_rules


def demo_available_rules():
    print("=== Available Rules ===")
    for rule in list_rules():
        print(f"  - {rule}")
    print()


def demo_rule_validation():
    print("=== Rule Validation ===")
    field = {
        "name": "username",
        "rules": {
            "min_length": 3,
            "max_length": 20,
            "pattern": r"[a-zA-Z0-9_]+",
        },
    }
    for value in ["jo", "valid_user", "this name has spaces!"]:
        errors = apply_all_rules(field, value)
        status = "PASS" if not errors else f"FAIL: {errors}"
        print(f"  '{value}' -> {status}")
    print()


def demo_html_attrs():
    print("=== HTML Attributes from Rules ===")
    field = {
        "rules": {
            "min_length": 8,
            "max_length": 64,
            "pattern": r".{8,}",
        }
    }
    attrs = render_rule_attrs(field)
    print(f"  Attrs string: {attrs.strip()}")
    print()


def demo_hint_rendering():
    print("=== Rule Hint HTML ===")
    field = {"rules": {"min_length": 5, "max_length": 50}}
    hint = render_rule_hint(field, "email-hint")
    print(f"  {hint}")
    print()
    descriptions = describe_rules(field)
    print("  Descriptions:")
    for d in descriptions:
        print(f"    - {d}")
    print()


def main():
    demo_available_rules()
    demo_rule_validation()
    demo_html_attrs()
    demo_hint_rendering()


if __name__ == "__main__":
    main()
