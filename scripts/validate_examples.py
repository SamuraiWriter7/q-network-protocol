#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = (
    ROOT
    / "schemas"
    / "question-envelope-v0.1.schema.json"
)

PASS_DIR = (
    ROOT
    / "examples"
    / "v0.1"
    / "pass"
)

FAIL_DIR = (
    ROOT
    / "examples"
    / "v0.1"
    / "fail"
)


class SemanticValidationError(ValueError):
    """Raised when an example violates Q Network semantic invariants."""


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object from disk."""

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}: "
            f"{exc.msg} at line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError(
            f"Expected top-level JSON object in {path}, "
            f"got {type(data).__name__}"
        )

    return data


def build_validator(schema: dict[str, Any]) -> Draft202012Validator:
    """Create a Draft 2020-12 validator with format checking."""

    Draft202012Validator.check_schema(schema)

    return Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )


def validate_schema(
    instance: dict[str, Any],
    validator: Draft202012Validator,
) -> list[str]:
    """
    Validate an instance against the JSON Schema.

    Returns a list of human-readable error messages.
    """

    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: list(error.absolute_path),
    )

    messages: list[str] = []

    for error in errors:
        location = ".".join(
            str(part)
            for part in error.absolute_path
        )

        if not location:
            location = "<root>"

        messages.append(
            f"{location}: {error.message}"
        )

    return messages


def validate_semantics(instance: dict[str, Any]) -> list[str]:
    """
    Validate semantic invariants that are difficult or inappropriate
    to express directly in JSON Schema v0.1.
    """

    errors: list[str] = []

    question_id = instance.get("question_id")
    parent_question_id = instance.get("parent_question_id")
    derived_from = instance.get("derived_from")

    # ------------------------------------------------------------
    # Invariant:
    # A question MUST NOT be its own parent.
    # ------------------------------------------------------------
    if (
        question_id is not None
        and parent_question_id is not None
        and question_id == parent_question_id
    ):
        errors.append(
            "parent_question_id must not equal question_id"
        )

    # ------------------------------------------------------------
    # Invariant:
    # A question MUST NOT be semantically derived from itself.
    # ------------------------------------------------------------
    if (
        question_id is not None
        and derived_from is not None
        and question_id == derived_from
    ):
        errors.append(
            "derived_from must not equal question_id"
        )

    return errors


def collect_examples(directory: Path) -> list[Path]:
    """Return all JSON example files in deterministic order."""

    if not directory.exists():
        return []

    return sorted(
        path
        for path in directory.rglob("*.json")
        if path.is_file()
    )


def print_errors(
    schema_errors: list[str],
    semantic_errors: list[str],
) -> None:
    """Print validation errors in a consistent format."""

    if schema_errors:
        print("    [schema-errors]")

        for error in schema_errors:
            print(f"      - {error}")

    if semantic_errors:
        print("    [semantic-errors]")

        for error in semantic_errors:
            print(f"      - {error}")


def validate_pass_example(
    path: Path,
    validator: Draft202012Validator,
) -> bool:
    """
    PASS examples must satisfy both:
      1. JSON Schema validation
      2. Semantic validation
    """

    print(f"[PASS expected] {path.relative_to(ROOT)}")

    try:
        instance = load_json(path)
    except ValueError as exc:
        print(f"    [json-fail] {exc}")
        return False

    schema_errors = validate_schema(
        instance,
        validator,
    )

    semantic_errors = validate_semantics(instance)

    if schema_errors or semantic_errors:
        print("    [unexpected FAIL]")
        print_errors(
            schema_errors,
            semantic_errors,
        )
        return False

    print("    [schema-ok]")
    print("    [semantic-ok]")
    print("    [result] PASS")

    return True


def validate_fail_example(
    path: Path,
    validator: Draft202012Validator,
) -> bool:
    """
    FAIL examples must fail either:
      1. JSON Schema validation
      OR
      2. Semantic validation

    If both validations pass, the negative example is invalid.
    """

    print(f"[FAIL expected] {path.relative_to(ROOT)}")

    try:
        instance = load_json(path)
    except ValueError as exc:
        # Malformed JSON is considered a valid negative case.
        print(f"    [json-fail] {exc}")
        print("    [result] EXPECTED FAIL")
        return True

    schema_errors = validate_schema(
        instance,
        validator,
    )

    semantic_errors = validate_semantics(instance)

    if not schema_errors and not semantic_errors:
        print("    [schema-ok]")
        print("    [semantic-ok]")
        print(
            "    [unexpected PASS] "
            "Negative example passed all validation."
        )
        return False

    if schema_errors:
        print("    [schema-fail]")
    else:
        print("    [schema-ok]")

    if semantic_errors:
        print("    [semantic-fail]")
    else:
        print("    [semantic-ok]")

    print_errors(
        schema_errors,
        semantic_errors,
    )

    print("    [result] EXPECTED FAIL")

    return True


def main() -> int:
    print("=== Q Network Protocol v0.1 Validation ===")
    print()

    # ------------------------------------------------------------
    # Load schema
    # ------------------------------------------------------------

    if not SCHEMA_PATH.exists():
        print(
            f"[fatal] Schema not found: "
            f"{SCHEMA_PATH.relative_to(ROOT)}"
        )
        return 1

    try:
        schema = load_json(SCHEMA_PATH)
        validator = build_validator(schema)
    except Exception as exc:
        print(f"[fatal] Unable to load schema: {exc}")
        return 1

    print(
        f"[schema-ok] "
        f"{SCHEMA_PATH.relative_to(ROOT)}"
    )
    print()

    # ------------------------------------------------------------
    # Discover examples
    # ------------------------------------------------------------

    pass_examples = collect_examples(PASS_DIR)
    fail_examples = collect_examples(FAIL_DIR)

    if not pass_examples:
        print(
            f"[fatal] No PASS examples found in "
            f"{PASS_DIR.relative_to(ROOT)}"
        )
        return 1

    if not fail_examples:
        print(
            f"[fatal] No FAIL examples found in "
            f"{FAIL_DIR.relative_to(ROOT)}"
        )
        return 1

    total = 0
    matched = 0

    pass_total = 0
    pass_matched = 0

    fail_total = 0
    fail_matched = 0

    # ------------------------------------------------------------
    # PASS examples
    # ------------------------------------------------------------

    print("=== PASS Examples ===")
    print()

    for example in pass_examples:
        total += 1
        pass_total += 1

        result = validate_pass_example(
            example,
            validator,
        )

        if result:
            matched += 1
            pass_matched += 1

        print()

    # ------------------------------------------------------------
    # FAIL examples
    # ------------------------------------------------------------

    print("=== FAIL Examples ===")
    print()

    for example in fail_examples:
        total += 1
        fail_total += 1

        result = validate_fail_example(
            example,
            validator,
        )

        if result:
            matched += 1
            fail_matched += 1

        print()

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------

    print("=== Validation Summary ===")
    print()

    print(
        f"PASS examples : "
        f"{pass_matched}/{pass_total} matched expectation"
    )

    print(
        f"FAIL examples : "
        f"{fail_matched}/{fail_total} matched expectation"
    )

    print(
        f"TOTAL         : "
        f"{matched}/{total} matched expectation"
    )

    print()

    if matched != total:
        print("[validation-failed]")
        return 1

    print("[validation-passed]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
