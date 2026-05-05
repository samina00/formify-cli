"""Renders HTML5 constraint attributes from field rule definitions."""

from formify_cli.schema_validator_rules import list_rules


_RULE_TO_HTML_ATTR = {
    "min_length": "minlength",
    "max_length": "maxlength",
    "pattern": "pattern",
    "min_value": "min",
    "max_value": "max",
}


def rules_to_html_attrs(field: dict) -> dict:
    """Convert field['rules'] dict to HTML attribute key-value pairs."""
    rules = field.get("rules", {})
    if not isinstance(rules, dict):
        return {}
    attrs = {}
    for rule_name, param in rules.items():
        html_attr = _RULE_TO_HTML_ATTR.get(rule_name)
        if html_attr:
            attrs[html_attr] = str(param)
    return attrs


def render_rule_attrs(field: dict) -> str:
    """Return a string of HTML attributes derived from field rules."""
    attrs = rules_to_html_attrs(field)
    if not attrs:
        return ""
    return " " + " ".join(f'{k}="{v}"' for k, v in sorted(attrs.items()))


def describe_rules(field: dict) -> list[str]:
    """Return human-readable descriptions of rules for aria/hint text."""
    rules = field.get("rules", {})
    if not isinstance(rules, dict):
        return []
    descriptions = []
    if "min_length" in rules:
        descriptions.append(f"Minimum length: {rules['min_length']} characters.")
    if "max_length" in rules:
        descriptions.append(f"Maximum length: {rules['max_length']} characters.")
    if "pattern" in rules:
        descriptions.append(f"Must match pattern: {rules['pattern']}.")
    if "min_value" in rules:
        descriptions.append(f"Minimum value: {rules['min_value']}.")
    if "max_value" in rules:
        descriptions.append(f"Maximum value: {rules['max_value']}.")
    return descriptions


def render_rule_hint(field: dict, hint_id: str) -> str:
    """Render a <span> hint element describing field rules, or empty string."""
    descriptions = describe_rules(field)
    if not descriptions:
        return ""
    text = " ".join(descriptions)
    return f'<span id="{hint_id}" class="field-hint">{text}</span>'
