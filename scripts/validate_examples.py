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
        "kind": "question_envelope",
    },
    "0.2": {
        "schema": ROOT / "schemas" / "question-envelope-v0.2.schema.json",
        "pass_dir": ROOT / "examples" / "v0.2" / "pass",
        "fail_dir": ROOT / "examples" / "v0.2" / "fail",
        "kind": "question_envelope",
    },
    "0.3": {
        "schema": ROOT / "schemas" / "question-graph-v0.3.schema.json",
        "pass_dir": ROOT / "examples" / "v0.3" / "pass",
        "fail_dir": ROOT / "examples" / "v0.3" / "fail",
        "kind": "question_graph",
    },
    "0.4": {
        "schema": ROOT / "schemas" / "question-drift-v0.4.schema.json",
        "pass_dir": ROOT / "examples" / "v0.4" / "pass",
        "fail_dir": ROOT / "examples" / "v0.4" / "fail",
        "kind": "question_drift",
    },
}


LINEAGE_RELATIONS = {
    "derived",
    "decomposed_into",
    "interpreted_as",
    "clarified_by",
    "verified_by",
    "audited_by",
    "recovered_by",
    "superseded_by",
    "unresolved_into",
}


def load_json(path: Path) -> dict[str, Any]:
    """
    Load a JSON object from disk.
    """

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


def build_validator(
    schema: dict[str, Any],
) -> Draft202012Validator:
    """
    Build a Draft 2020-12 JSON Schema validator.
    """

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
    Return human-readable schema validation errors.
    """

    errors = sorted(
        validator.iter_errors(instance),
        key=lambda error: (
            list(error.absolute_path),
            error.message,
        ),
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


# ============================================================
# v0.1 / v0.2 Question Envelope semantics
# ============================================================


def validate_common_question_semantics(
    instance: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    question_id = instance.get("question_id")
    parent_question_id = instance.get("parent_question_id")
    derived_from = instance.get("derived_from")

    if (
        isinstance(question_id, str)
        and isinstance(parent_question_id, str)
        and question_id == parent_question_id
    ):
        errors.append(
            "parent_question_id must not equal question_id"
        )

    if (
        isinstance(question_id, str)
        and isinstance(derived_from, str)
        and question_id == derived_from
    ):
        errors.append(
            "derived_from must not equal question_id"
        )

    return errors


def validate_v02_question_semantics(
    instance: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    question_id = instance.get("question_id")
    provenance = instance.get("provenance")

    if not isinstance(provenance, dict):
        return errors

    source_question_id = provenance.get(
        "source_question_id"
    )

    if (
        isinstance(question_id, str)
        and isinstance(source_question_id, str)
        and question_id == source_question_id
    ):
        errors.append(
            "provenance.source_question_id "
            "must not equal question_id"
        )

    return errors


def validate_question_envelope_semantics(
    instance: dict[str, Any],
    version: str,
) -> list[str]:
    errors = validate_common_question_semantics(
        instance
    )

    if version == "0.2":
        errors.extend(
            validate_v02_question_semantics(
                instance
            )
        )

    return errors


# ============================================================
# v0.3 Question Graph semantics
# ============================================================


def find_lineage_cycle(
    nodes: list[str],
    edges: list[dict[str, Any]],
) -> list[str] | None:
    """
    Detect a directed cycle among semantic lineage relations.
    """

    adjacency: dict[str, list[str]] = {
        node: []
        for node in nodes
    }

    for edge in edges:
        relation = edge.get("relation")

        if relation not in LINEAGE_RELATIONS:
            continue

        source = edge.get("from_question_id")
        target = edge.get("to_question_id")

        if not isinstance(source, str):
            continue

        if not isinstance(target, str):
            continue

        if source not in adjacency:
            continue

        if target not in adjacency:
            continue

        adjacency[source].append(target)

    state: dict[str, int] = {
        node: 0
        for node in nodes
    }

    stack: list[str] = []
    stack_index: dict[str, int] = {}

    def visit(
        node: str,
    ) -> list[str] | None:
        state[node] = 1

        stack_index[node] = len(stack)
        stack.append(node)

        for neighbor in adjacency.get(node, []):
            neighbor_state = state.get(
                neighbor,
                0,
            )

            if neighbor_state == 0:
                cycle = visit(
                    neighbor
                )

                if cycle is not None:
                    return cycle

            elif neighbor_state == 1:
                start = stack_index[neighbor]

                return (
                    stack[start:]
                    + [neighbor]
                )

        stack.pop()
        stack_index.pop(
            node,
            None,
        )

        state[node] = 2

        return None

    for node in nodes:
        if state[node] != 0:
            continue

        cycle = visit(
            node
        )

        if cycle is not None:
            return cycle

    return None


def validate_question_graph_semantics(
    instance: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    raw_nodes = instance.get(
        "nodes",
        [],
    )

    raw_edges = instance.get(
        "edges",
        [],
    )

    if not isinstance(raw_nodes, list):
        return errors

    if not isinstance(raw_edges, list):
        return errors

    nodes = [
        node
        for node in raw_nodes
        if isinstance(node, str)
    ]

    edges = [
        edge
        for edge in raw_edges
        if isinstance(edge, dict)
    ]

    node_set = set(nodes)
    seen_edge_ids: set[str] = set()

    for index, edge in enumerate(edges):
        edge_id = edge.get(
            "edge_id"
        )

        source = edge.get(
            "from_question_id"
        )

        target = edge.get(
            "to_question_id"
        )

        edge_label = (
            edge_id
            if isinstance(edge_id, str)
            else f"<edge-index-{index}>"
        )

        # ----------------------------------------------------
        # Self edge
        # ----------------------------------------------------

        if (
            isinstance(source, str)
            and isinstance(target, str)
            and source == target
        ):
            errors.append(
                f"edge {edge_label}: "
                "from_question_id must not equal "
                "to_question_id"
            )

        # ----------------------------------------------------
        # Endpoint integrity
        # ----------------------------------------------------

        if (
            isinstance(source, str)
            and source not in node_set
        ):
            errors.append(
                f"edge {edge_label}: "
                f"from_question_id '{source}' "
                "is not present in nodes"
            )

        if (
            isinstance(target, str)
            and target not in node_set
        ):
            errors.append(
                f"edge {edge_label}: "
                f"to_question_id '{target}' "
                "is not present in nodes"
            )

        # ----------------------------------------------------
        # Duplicate edge identity
        # ----------------------------------------------------

        if isinstance(edge_id, str):
            if edge_id in seen_edge_ids:
                errors.append(
                    f"duplicate edge_id: {edge_id}"
                )
            else:
                seen_edge_ids.add(
                    edge_id
                )

    # --------------------------------------------------------
    # Semantic lineage cycles
    # --------------------------------------------------------

    cycle = find_lineage_cycle(
        nodes,
        edges,
    )

    if cycle is not None:
        errors.append(
            "semantic lineage cycle detected: "
            + " -> ".join(cycle)
        )

    return errors


# ============================================================
# v0.4 Question Drift semantics
# ============================================================


def validate_question_drift_semantics(
    instance: dict[str, Any],
) -> list[str]:
    """
    Validate semantic invariants introduced by Question Drift v0.4.
    """

    errors: list[str] = []

    from_question_id = instance.get(
        "from_question_id"
    )

    to_question_id = instance.get(
        "to_question_id"
    )

    signals_raw = instance.get(
        "signals",
        [],
    )

    signals = {
        signal
        for signal in signals_raw
        if isinstance(signal, str)
    } if isinstance(signals_raw, list) else set()

    # --------------------------------------------------------
    # No self comparison
    # --------------------------------------------------------

    if (
        isinstance(from_question_id, str)
        and isinstance(to_question_id, str)
        and from_question_id == to_question_id
    ):
        errors.append(
            "from_question_id must not equal "
            "to_question_id"
        )

    # --------------------------------------------------------
    # Contradictory risk signals
    # --------------------------------------------------------

    if (
        "risk_increased" in signals
        and "risk_decreased" in signals
    ):
        errors.append(
            "signals must not contain both "
            "risk_increased and risk_decreased"
        )

    # --------------------------------------------------------
    # Contradictory scope signals
    # --------------------------------------------------------

    if (
        "scope_expanded" in signals
        and "scope_narrowed" in signals
    ):
        errors.append(
            "signals must not contain both "
            "scope_expanded and scope_narrowed"
        )

    return errors


# ============================================================
# Semantic validation dispatcher
# ============================================================


def validate_semantics(
    instance: dict[str, Any],
    version: str,
    kind: str,
) -> list[str]:
    if kind == "question_envelope":
        return validate_question_envelope_semantics(
            instance,
            version,
        )

    if kind == "question_graph":
        return validate_question_graph_semantics(
            instance
        )

    if kind == "question_drift":
        return validate_question_drift_semantics(
            instance
        )

    return [
        f"unknown validation kind: {kind}"
    ]


# ============================================================
# Example discovery
# ============================================================


def collect_examples(
    directory: Path,
) -> list[Path]:
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
        print(
            "    [schema-errors]"
        )

        for error in schema_errors:
            print(
                f"      - {error}"
            )

    if semantic_errors:
        print(
            "    [semantic-errors]"
        )

        for error in semantic_errors:
            print(
                f"      - {error}"
            )


# ============================================================
# PASS / FAIL example validation
# ============================================================


def validate_pass_example(
    path: Path,
    validator: Draft202012Validator,
    version: str,
    kind: str,
) -> bool:
    print(
        f"[PASS expected] "
        f"{path.relative_to(ROOT)}"
    )

    try:
        instance = load_json(
            path
        )

    except ValueError as exc:
        print(
            f"    [json-fail] {exc}"
        )
        return False

    schema_errors = validate_schema(
        instance,
        validator,
    )

    semantic_errors = validate_semantics(
        instance,
        version,
        kind,
    )

    if (
        schema_errors
        or semantic_errors
    ):
        print(
            "    [unexpected FAIL]"
        )

        print_errors(
            schema_errors,
            semantic_errors,
        )

        return False

    print(
        "    [schema-ok]"
    )

    print(
        "    [semantic-ok]"
    )

    print(
        "    [result] PASS"
    )

    return True


def validate_fail_example(
    path: Path,
    validator: Draft202012Validator,
    version: str,
    kind: str,
) -> bool:
    print(
        f"[FAIL expected] "
        f"{path.relative_to(ROOT)}"
    )

    try:
        instance = load_json(
            path
        )

    except ValueError as exc:
        print(
            f"    [json-fail] {exc}"
        )

        print(
            "    [result] EXPECTED FAIL"
        )

        return True

    schema_errors = validate_schema(
        instance,
        validator,
    )

    semantic_errors = validate_semantics(
        instance,
        version,
        kind,
    )

    if (
        not schema_errors
        and not semantic_errors
    ):
        print(
            "    [schema-ok]"
        )

        print(
            "    [semantic-ok]"
        )

        print(
            "    [unexpected PASS] "
            "Negative example passed all validation."
        )

        return False

    if schema_errors:
        print(
            "    [schema-fail]"
        )
    else:
        print(
            "    [schema-ok]"
        )

    if semantic_errors:
        print(
            "    [semantic-fail]"
        )
    else:
        print(
            "    [semantic-ok]"
        )

    print_errors(
        schema_errors,
        semantic_errors,
    )

    print(
        "    [result] EXPECTED FAIL"
    )

    return True


# ============================================================
# Version validation
# ============================================================


def validate_version(
    version: str,
    config: dict[str, Any],
) -> tuple[int, int, int, int, bool]:
    schema_path: Path = config[
        "schema"
    ]

    pass_dir: Path = config[
        "pass_dir"
    ]

    fail_dir: Path = config[
        "fail_dir"
    ]

    kind: str = config[
        "kind"
    ]

    print(
        f"=== Q Network Protocol "
        f"v{version} Validation ==="
    )

    print()

    # --------------------------------------------------------
    # Schema
    # --------------------------------------------------------

    if not schema_path.exists():
        print(
            f"[fatal] Schema not found: "
            f"{schema_path.relative_to(ROOT)}"
        )

        return (
            0,
            0,
            0,
            0,
            True,
        )

    try:
        schema = load_json(
            schema_path
        )

        validator = build_validator(
            schema
        )

    except Exception as exc:
        print(
            f"[fatal] Unable to load schema: "
            f"{exc}"
        )

        return (
            0,
            0,
            0,
            0,
            True,
        )

    print(
        f"[schema-ok] "
        f"{schema_path.relative_to(ROOT)}"
    )

    print()

    # --------------------------------------------------------
    # Examples
    # --------------------------------------------------------

    pass_examples = collect_examples(
        pass_dir
    )

    fail_examples = collect_examples(
        fail_dir
    )

    if not pass_examples:
        print(
            f"[fatal] No PASS examples found in "
            f"{pass_dir.relative_to(ROOT)}"
        )

        return (
            0,
            0,
            0,
            0,
            True,
        )

    if not fail_examples:
        print(
            f"[fatal] No FAIL examples found in "
            f"{fail_dir.relative_to(ROOT)}"
        )

        return (
            0,
            0,
            0,
            0,
            True,
        )

    pass_total = 0
    pass_matched = 0

    fail_total = 0
    fail_matched = 0

    # --------------------------------------------------------
    # PASS
    # --------------------------------------------------------

    print(
        "=== PASS Examples ==="
    )

    print()

    for example in pass_examples:
        pass_total += 1

        if validate_pass_example(
            example,
            validator,
            version,
            kind,
        ):
            pass_matched += 1

        print()

    # --------------------------------------------------------
    # FAIL
    # --------------------------------------------------------

    print(
        "=== FAIL Examples ==="
    )

    print()

    for example in fail_examples:
        fail_total += 1

        if validate_fail_example(
            example,
            validator,
            version,
            kind,
        ):
            fail_matched += 1

        print()

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print(
        "=== Version Summary ==="
    )

    print()

    print(
        f"PASS examples : "
        f"{pass_matched}/{pass_total} "
        f"matched expectation"
    )

    print(
        f"FAIL examples : "
        f"{fail_matched}/{fail_total} "
        f"matched expectation"
    )

    print()

    return (
        pass_matched,
        pass_total,
        fail_matched,
        fail_total,
        False,
    )


# ============================================================
# Main
# ============================================================


def main() -> int:
    print(
        "=== Q Network Protocol Validation ==="
    )

    print()

    total_matched = 0
    total_cases = 0
    fatal_errors = 0

    version_results: list[
        tuple[str, int, int]
    ] = []

    for version, config in VERSIONS.items():
        (
            pass_matched,
            pass_total,
            fail_matched,
            fail_total,
            fatal_error,
        ) = validate_version(
            version,
            config,
        )

        if fatal_error:
            fatal_errors += 1

            print(
                f"[v{version}] FATAL"
            )

            print()
            print(
                "-" * 60
            )
            print()

            continue

        version_matched = (
            pass_matched
            + fail_matched
        )

        version_total = (
            pass_total
            + fail_total
        )

        total_matched += (
            version_matched
        )

        total_cases += (
            version_total
        )

        version_results.append(
            (
                version,
                version_matched,
                version_total,
            )
        )

        print(
            f"[v{version}] "
            f"{version_matched}/"
            f"{version_total} "
            f"matched expectation"
        )

        print()
        print(
            "-" * 60
        )
        print()

    # --------------------------------------------------------
    # Final summary
    # --------------------------------------------------------

    print(
        "=== Final Validation Summary ==="
    )

    print()

    for (
        version,
        matched,
        total,
    ) in version_results:
        print(
            f"v{version}: "
            f"{matched}/{total} "
            f"matched expectation"
        )

    print()

    print(
        f"TOTAL : "
        f"{total_matched}/{total_cases} "
        f"matched expectation"
    )

    if fatal_errors:
        print(
            f"FATAL : "
            f"{fatal_errors} "
            f"version validation error(s)"
        )

    print()

    if (
        fatal_errors > 0
        or total_matched != total_cases
    ):
        print(
            "[validation-failed]"
        )
        return 1

    print(
        "[validation-passed]"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
