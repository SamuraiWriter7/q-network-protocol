#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]

VERSIONS = {
    "0.1": {
        "schema": ROOT / "schemas" / "question-envelope-v0.1.schema.json",
        "pass_dir": ROOT / "examples" / "v0.1" / "pass",
        "fail_dir": ROOT / "examples" / "v0.1" / "fail",
    },
    "0.2": {
        "schema": ROOT / "schemas" / "question-envelope-v0.2.schema.json",
        "pass_dir": ROOT / "examples" / "v0.2" / "pass",
        "fail_dir": ROOT / "examples" / "v0.2" / "fail",
    },
}


def load_json(path: Path) -> dict[str, Any]:
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
    Draft202012Validator.check_schema(schema)

    return Draft202012Validator(
        schema,
        format_checker=FormatChecker(),
    )


def validate_schema(
    instance: dict[str, Any],
    validator: Draft202012Validator,
) -> list[str]:
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


def validate_common_semantics(
    instance: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    question_id = instance.get("question_id")
    parent_question_id = instance.get("parent_question_id")
    derived_from = instance.get("derived_from")

    if (
        question_id is not None
        and parent_question_id is not None
        and question_id == parent_question_id
    ):
        errors.append(
            "parent_question_id must not equal question_id"
        )

    if (
        question_id is not None
        and derived_from is not None
        and question_id == derived_from
    ):
        errors.append(
            "derived_from must not equal question_id"
        )

    return errors


def validate_v02_semantics(
    instance: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    question_id = instance.get("question_id")
    provenance = instance.get("provenance")

    if isinstance(provenance, dict):
        source_question_id = provenance.get(
            "source_question_id"
        )

        if (
            question_id is not None
            and source_question_id is not None
            and question_id == source_question_id
        ):
            errors.append(
                "provenance.source_question_id "
                "must not equal question_id"
            )

    return errors


def validate_semantics(
    instance: dict[str, Any],
    version: str,
) -> list[str]:
    errors = validate_common_semantics(instance)

    if version == "0.2":
        errors.extend(
            validate_v02_semantics(instance)
        )

    return errors


def collect_examples(directory: Path) -> list[Path]:
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
    version: str,
) -> bool:
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

    semantic_errors = validate_semantics(
        instance,
        version,
    )

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
    version: str,
) -> bool:
    print(f"[FAIL expected] {path.relative_to(ROOT)}")

    try:
        instance = load_json(path)
    except ValueError as exc:
        print(f"    [json-fail] {exc}")
        print("    [result] EXPECTED FAIL")
        return True

    schema_errors = validate_schema(
        instance,
        validator,
    )

    semantic_errors = validate_semantics(
        instance,
        version,
    )

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


def validate_version(
    version: str,
    config: dict[str, Path],
) -> tuple[int, int, int, int]:
    schema_path = config["schema"]
    pass_dir = config["pass_dir"]
    fail_dir = config["fail_dir"]

    print(
        f"=== Q Network Protocol v{version} Validation ==="
    )
    print()

    if not schema_path.exists():
        print(
            f"[fatal] Schema not found: "
            f"{schema_path.relative_to(ROOT)}"
        )
        return 0, 0, 0, 1

    try:
        schema = load_json(schema_path)
        validator = build_validator(schema)
    except Exception as exc:
        print(f"[fatal] Unable to load schema: {exc}")
        return 0, 0, 0, 1

    print(
        f"[schema-ok] "
        f"{schema_path.relative_to(ROOT)}"
    )
    print()

    pass_examples = collect_examples(pass_dir)
    fail_examples = collect_examples(fail_dir)

    if not pass_examples:
        print(
            f"[fatal] No PASS examples found in "
            f"{pass_dir.relative_to(ROOT)}"
        )
        return 0, 0, 0, 1

    if not fail_examples:
        print(
            f"[fatal] No FAIL examples found in "
            f"{fail_dir.relative_to(ROOT)}"
        )
        return 0, 0, 0, 1

    pass_total = 0
    pass_matched = 0
    fail_total = 0
    fail_matched = 0

    print("=== PASS Examples ===")
    print()

    for example in pass_examples:
        pass_total += 1

        if validate_pass_example(
            example,
            validator,
            version,
        ):
            pass_matched += 1

        print()

    print("=== FAIL Examples ===")
    print()

    for example in fail_examples:
        fail_total += 1

        if validate_fail_example(
            example,
            validator,
            version,
        ):
            fail_matched += 1

        print()

    print("=== Version Summary ===")
    print()

    print(
        f"PASS examples : "
        f"{pass_matched}/{pass_total} matched expectation"
    )

    print(
        f"FAIL examples : "
        f"{fail_matched}/{fail_total} matched expectation"
    )

    print()

    return (
        pass_matched,
        pass_total,
        fail_matched,
        fail_total,
    )


def main() -> int:
    print("=== Q Network Protocol Validation ===")
    print()

    total_matched = 0
    total_cases = 0
    fatal_errors = 0

    for version, config in VERSIONS.items():
        (
            pass_matched,
            pass_total,
            fail_matched,
            fail_total,
        ) = validate_version(
            version,
            config,
        )

        if (
            pass_total == 0
            and fail_total == 0
        ):
            fatal_errors += 1
            continue

        version_matched = (
            pass_matched
            + fail_matched
        )

        version_total = (
            pass_total
            + fail_total
        )

        total_matched += version_matched
        total_cases += version_total

        print(
            f"[v{version}] "
            f"{version_matched}/{version_total} "
            f"matched expectation"
        )
        print()
        print("-" * 60)
        print()

    print("=== Final Validation Summary ===")
    print()

    print(
        f"TOTAL : "
        f"{total_matched}/{total_cases} "
        f"matched expectation"
    )

    if fatal_errors:
        print(
            f"FATAL : "
            f"{fatal_errors} version validation error(s)"
        )

    print()

    if (
        fatal_errors > 0
        or total_matched != total_cases
    ):
        print("[validation-failed]")
        return 1

    print("[validation-passed]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
