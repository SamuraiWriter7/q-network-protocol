# Changelog

All notable changes to Q Network Protocol are documented in this file.

The format is based on a versioned protocol lifecycle rather than application release cadence.

---

## [0.6.0] — Question Structural Perturbation

### Added

- Added **Question Structural Perturbation** as the sixth Q Network Core layer.
- Added the conceptual symbol `Qψ`.
- Added observable structural signals:
  - `assumption_changed`
  - `problem_frame_changed`
  - `design_target_changed`
  - `reversal_detected`
  - `new_questions_generated`
  - `new_structure_generated`
- Added:
  - `affected_assumptions`
  - `generated_question_count`
  - `downstream_question_refs`
  - `downstream_structure_refs`
- Added perturbation classifications:
  - `low`
  - `moderate`
  - `high`
  - `structural`
- Added review states:
  - `none`
  - `observe`
  - `structural_review_recommended`
  - `independent_review_recommended`
  - `human_review_required`
- Added optional detection metadata:
  - `detected_by`
  - `detection_method`
  - `evidence_refs`
  - `trace_parent`
  - `local_score`
- Added explicit QSP invariants:
  - High Qψ must never imply High Authority.
  - Structural significance must be supported by observable evidence.
  - Numeric Qψ scoring is optional and method-local.
  - Structural impact increases review needs, not privileges.

### Validation

Added semantic validation for:

- generated question count consistency;
- downstream question reference consistency;
- downstream structure reference consistency;
- all-false signal classification;
- structural classification without material evidence;
- mismatch between generated-question signals and downstream evidence;
- mismatch between structure-generation signals and downstream structure references.

### Examples

Added PASS examples for:

- minimal structural perturbation;
- structural perturbation;
- question branching perturbation.

Added FAIL examples for:

- structural classification with all signals false;
- generated question count mismatch;
- downstream structure mismatch;
- downstream question mismatch.

### Notes

Version 0.6 marks a natural boundary for the initial **Q Network Core**.

The protocol lifecycle now covers:

```text
Question Creation
↓
Origin
↓
Relationship
↓
Change
↓
Investigation
↓
Structural Effect
```

---

## [0.5.0] — Incident Backtrace

### Added

- Added **Incident Backtrace** for reverse reconstruction of incident lineage.
- Added Backtrace Records containing:
  - `backtrace_id`
  - `incident_id`
  - `start_ref`
  - `status`
  - ordered `steps`
- Added backtrace object types:
  - `incident`
  - `result`
  - `action`
  - `plan`
  - `question`
  - `drift`
  - `authority`
  - `trace`
  - `receipt`
  - `human_intent`
  - `external_event`
- Added relation types including:
  - `start`
  - `resulted_from`
  - `executed_from`
  - `planned_from`
  - `triggered_by`
  - `derived_from`
  - `interpreted_from`
  - `audited_from`
  - `recovered_from`
  - `authorized_by`
  - `observed_in`
  - `recorded_by`
  - `associated_with`
- Added confidence levels:
  - `confirmed`
  - `supported`
  - `inferred`
  - `uncertain`
- Added Backtrace statuses:
  - `open`
  - `partial`
  - `reconstructed`
  - `closed`
  - `inconclusive`
  - `invalid`
- Added investigative candidate flags:
  - `meaning_shift`
  - `risk_escalation`
  - `authority_gap`
  - `routing_anomaly`
  - `audit_missing`
  - `recovery_failure`
  - `scope_expansion`
  - `trace_gap`
  - `evidence_conflict`

### Validation

Added semantic validation for:

- duplicate `step_id`;
- duplicate `sequence`;
- missing sequence `0`;
- non-contiguous sequence values;
- `start_ref` mismatch;
- invalid or repeated `start` relations;
- self-predecessor relationships.

### Examples

Added PASS examples for:

- minimal backtrace;
- question lineage reconstruction;
- partial backtrace;
- inconclusive backtrace.

Added FAIL examples for:

- duplicate sequence;
- duplicate step ID;
- start reference mismatch;
- multiple start relations;
- non-contiguous sequence;
- self predecessor.

### Notes

Version 0.5 formalized two important investigative principles:

> Trace backward before assigning cause.

and:

> Missing evidence must remain missing.

---

## [0.4.0] — Question Drift

### Added

- Added **Question Drift** for recording observable changes between related questions.
- Added drift signals:
  - `intent_changed`
  - `domain_changed`
  - `risk_increased`
  - `risk_decreased`
  - `authority_changed`
  - `depth_increased`
  - `interpretation_hop`
  - `routing_changed`
  - `audit_missing`
  - `recovery_transition`
  - `scope_expanded`
  - `scope_narrowed`
- Added review states:
  - `none`
  - `observe`
  - `review_recommended`
  - `hold_recommended`
  - `human_review_required`
- Added optional detection metadata:
  - `detected_by`
  - `detection_method`
  - `trace_parent`
  - `local_score`
- Added support for adjacent and multi-step drift observation.
- Added explicit distinction between:
  - observable drift;
  - review recommendation;
  - authority enforcement.

### Validation

Added semantic validation for:

- self-comparison;
- contradictory risk signals;
- contradictory scope signals.

Schema validation also rejects empty signal arrays.

### Examples

Added PASS examples for:

- minimal drift;
- risk and authority drift;
- recovery drift.

Added FAIL examples for:

- self comparison;
- contradictory risk signals;
- contradictory scope signals;
- empty signals.

### Notes

Version 0.4 established:

> Drift identifies change; it does not declare fault.

and:

> A Drift Record may recommend review, but it does not grant, revoke, or exercise authority.

---

## [0.3.0] — Question Graph

### Added

- Added **Question Graph** for representing relationships between Question Envelopes.
- Added graph fields:
  - `graph_id`
  - `created_at`
  - `graph_status`
  - `nodes`
  - `edges`
- Added graph statuses:
  - `open`
  - `stable`
  - `closed`
  - `partial`
  - `invalid`
- Added relationship types:
  - `derived`
  - `decomposed_into`
  - `interpreted_as`
  - `clarified_by`
  - `verified_by`
  - `audited_by`
  - `recovered_by`
  - `routed_to`
  - `superseded_by`
  - `unresolved_into`
- Added support for:
  - multiple roots;
  - multiple leaves;
  - branches;
  - merge points;
  - audit branches;
  - recovery branches.
- Added distinction between operational routing and semantic lineage.

### Validation

Added semantic validation for:

- self edges;
- missing endpoints;
- duplicate edge IDs;
- semantic lineage cycles.

`routed_to` is intentionally excluded from lineage-cycle detection because operational routing cycles do not necessarily imply semantic derivation cycles.

### Examples

Added PASS examples for:

- minimal question graph;
- decomposition graph;
- audit branch graph;
- multi-source graph.

Added FAIL examples for:

- self edge;
- missing endpoint;
- duplicate edge ID;
- semantic cycle.

### Notes

Version 0.3 expanded Q Network from individual Question Envelopes into multi-question structure.

---

## [0.2.0] — Question Provenance

### Added

- Added **Question Provenance** to explain why a question was generated.
- Added optional provenance fields:
  - `trigger_event`
  - `generated_by`
  - `generation_reason`
  - `source_question_id`
  - `source_intent`
  - `interpreted_intent`
  - `authority_context_ref`
  - `provenance_trace`
- Added recommended generation reasons:
  - `interpretation`
  - `decomposition`
  - `clarification`
  - `verification`
  - `audit`
  - `recovery`
  - `escalation`
  - `risk_review`
  - `authority_check`
  - `dependency_check`
- Added support for recording meaning transitions without requiring private chain-of-thought.
- Added distinction between:
  - graph parent;
  - semantic source;
  - immediate provenance source.

### Validation

Added semantic validation preventing:

```text
provenance.source_question_id == question_id
```

Schema validation also enforces key provenance dependencies such as:

- generation reason requiring generator identity;
- interpreted intent requiring source intent.

### Examples

Added PASS examples for:

- question provenance;
- audit provenance;
- recovery provenance.

Added FAIL examples for:

- self provenance source;
- missing generator;
- missing source intent;
- unknown generation reason.

### Notes

Version 0.2 established the principle:

> Private reasoning is not Question Provenance.

The protocol records externally reviewable transition metadata rather than unrestricted internal reasoning.

---

## [0.1.0] — Question Envelope

### Added

- Introduced the initial **Question Envelope**.
- Added core fields:
  - `schema_version`
  - `question_id`
  - `created_at`
  - `question_origin`
  - `question_type`
  - `intent`
  - `domain`
  - `risk_level`
  - `authority`
  - `status`
- Added optional lineage and routing fields:
  - `context`
  - `parent_question_id`
  - `derived_from`
  - `assigned_to`
  - `trace_parent`
- Added question origins:
  - `external`
  - `internal`
  - `derived`
  - `audit`
  - `recovery`
- Added question types:
  - `request`
  - `subquestion`
  - `verification`
  - `clarification`
  - `decision`
  - `recovery`
- Added statuses:
  - `created`
  - `routed`
  - `accepted`
  - `in_progress`
  - `answered`
  - `held`
  - `rejected`
  - `expired`
  - `unresolved`
- Added risk levels:
  - `low`
  - `medium`
  - `high`
  - `critical`
- Added minimal authority declaration through:
  - `authority.required`

### Validation

Added schema and semantic validation for:

- required Question Envelope fields;
- valid question origins;
- valid authority Boolean type;
- routing assignment requirements;
- derived-question source requirements;
- self-parent relationships;
- self-derived relationships.

### Examples

Added PASS examples for:

- external questions;
- derived subquestions;
- internal audit questions;
- unresolved questions;
- recovery questions.

Added FAIL examples for:

- derived questions without a source;
- invalid authority type;
- routed questions without assignment;
- self-derived questions;
- self-parent questions;
- unknown origins.

### Notes

Version 0.1 established the foundational Q Network invariants:

> Question is not Authority.

> Every Question has an Origin.

> Questions may derive Questions.

> Every Routed Question should remain Traceable.

> Unresolved is a Valid State.

---

# Q Network Core Timeline

```text
v0.1
Question Envelope
        ↓
v0.2
Question Provenance
        ↓
v0.3
Question Graph
        ↓
v0.4
Question Drift
        ↓
v0.5
Incident Backtrace
        ↓
v0.6
Question Structural Perturbation
```

The v0.1–v0.6 series forms the first complete Q Network Core lifecycle.

---

# Core Design Evolution

The protocol evolved from:

```text
Question
→ Answer
```

toward:

```text
Question
→ Provenance
→ Relationship
→ Drift
→ Investigation
→ Structural Effect
```

The current core therefore treats questions not only as inputs to AI systems, but as traceable objects capable of creating downstream structural change.

---

# Current Core Invariants

The Q Network Core currently preserves the following principles:

> Questions may move between intelligences, but authority does not move merely because the question moves.

> A question is allowed to remain a question.

> Trace backward before assigning cause.

> Missing evidence must remain missing.

> A question may change structure without gaining authority.

> High Qψ must never imply High Authority.

> Prefer explicit structural signals over universal question scores.

---

# Future Extensions

Future work may explore separate extension layers such as:

- Question-to-Structure Lineage;
- Structural Emergence;
- Question Contribution;
- Attribution;
- Reward;
- Inter-Network Question Circulation.

These extensions are intentionally outside the initial v0.1–v0.6 Q Network Core.
