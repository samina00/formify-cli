"""Demonstrates schema_freezer: freeze, inspect, and thaw schemas."""

from __future__ import annotations

from types import MappingProxyType

from formify_cli.schema_freezer import freeze_schema, is_frozen, safe_copy, thaw_schema


SAMPLE_SCHEMA = {
    "title": "Registration Form",
    "fields": [
        {"name": "username", "type": "text", "label": "Username", "required": True},
        {"name": "email", "type": "email", "label": "Email", "required": True},
        {"name": "age", "type": "number", "label": "Age", "required": False},
    ],
}


def demo_freeze_and_inspect() -> None:
    print("=== Freeze & Inspect ===")
    frozen = freeze_schema(SAMPLE_SCHEMA)
    print(f"is_frozen(original): {is_frozen(SAMPLE_SCHEMA)}")
    print(f"is_frozen(frozen):   {is_frozen(frozen)}")
    print(f"Title: {frozen['title']}")
    print(f"Fields type: {type(frozen['fields']).__name__}")
    print()


def demo_immutability() -> None:
    print("=== Immutability ===")
    frozen = freeze_schema(SAMPLE_SCHEMA)
    try:
        frozen["title"] = "Hacked"  # type: ignore[index]
    except TypeError as exc:
        print(f"Cannot mutate frozen schema: {exc}")
    print()


def demo_thaw() -> None:
    print("=== Thaw ===")
    frozen = freeze_schema(SAMPLE_SCHEMA)
    thawed = thaw_schema(frozen)
    thawed["title"] = "Modified After Thaw"
    print(f"Thawed title: {thawed['title']}")
    print(f"Frozen title unchanged: {frozen['title']}")
    print()


def demo_safe_copy() -> None:
    print("=== Safe Copy ===")
    copy1 = safe_copy(SAMPLE_SCHEMA)
    copy1["title"] = "Copy 1"
    copy2 = safe_copy(SAMPLE_SCHEMA)
    print(f"Original: {SAMPLE_SCHEMA['title']}")
    print(f"Copy 1:   {copy1['title']}")
    print(f"Copy 2:   {copy2['title']}")
    print()


def main() -> None:
    demo_freeze_and_inspect()
    demo_immutability()
    demo_thaw()
    demo_safe_copy()


if __name__ == "__main__":
    main()
