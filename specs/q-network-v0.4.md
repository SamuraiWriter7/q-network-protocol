# Q Network Protocol v0.4 — Question Drift

Version: 0.4.0

## 1. Purpose

Q Network Protocol v0.4 introduces a minimal Question Drift model.

Version 0.1 defined the Question Envelope.

Version 0.2 added Question Provenance.

Version 0.3 added Question Graph.

Version 0.4 defines how changes between related questions MAY be observed and recorded as structural drift signals.

The purpose of v0.4 is not to determine whether a question is "good" or "bad."

Its purpose is to identify when a question lineage changes materially enough that additional review, audit, or caution may be appropriate.

---

## 2. Core Principle

The primary invariant of v0.4 is:

> Drift is an observable change, not a final judgment.

A Question Drift record MAY indicate:

- intent change;
- domain change;
- risk increase;
- authority requirement change;
- derivation depth increase;
- interpretation hops;
- unexpected routing change;
- missing expected audit branch.

However, the existence of drift MUST NOT by itself prove unsafe behavior.

---

## 3. Conceptual Model

A simple lineage may evolve as follows:

```text
Q0
"Assess system safety."

↓ interpretation

Q1
"Check whether the service is reachable."

↓ decomposition

Q2
"Determine whether external access is required."

↓ interpretation

Q3
"Attempt external access."
```

The lineage may be structurally represented as:

```text
Q0
↓
Q1
↓
Q2
↓
Q3
```

Question Drift adds observations such as:

```text
Q0 → Q1
intent_changed

Q1 → Q2
domain_changed

Q2 → Q3
risk_increased
authority_changed
```

---

## 4. Drift Is Not Error

A question MAY change substantially without being incorrect.

Examples include:

- decomposition into a narrower subproblem;
- escalation after new evidence;
- risk increase after discovering a sensitive resource;
- authority change because execution is now required;
- recovery after failure.

Therefore:

> Drift MUST NOT be treated as equivalent to malfunction.

Question Drift exists to support investigation and control.

---

## 5. Drift Record

Version 0.4 introduces a Question Drift Record.

Canonical example:

```yaml
schema_version: "0.4.0"

drift_id: "qdrift-001"
created_at: "2026-10-17T00:00:00Z"

from_question_id: "q-002"
to_question_id: "q-003"

signals:
  - "intent_changed"
  - "risk_increased"
  - "authority_changed"

review_state: "review_recommended"

trace_parent: "trace-drift-001"
```

---

## 6. drift_id

`drift_id` uniquely identifies a Question Drift Record.

Requirements:

- MUST be non-empty;
- SHOULD be unique within the applicable namespace;
- MUST remain stable once referenced.

---

## 7. from_question_id

`from_question_id` identifies the earlier question in the comparison.

Example:

```yaml
from_question_id: "q-002"
```

It MUST NOT equal `to_question_id`.

---

## 8. to_question_id

`to_question_id` identifies the later or derived question being compared.

Example:

```yaml
to_question_id: "q-003"
```

The relationship between the two questions SHOULD be discoverable through Question Graph or Question Provenance where available.

---

## 9. Drift Signals

Version 0.4 defines the following core signals:

```text
intent_changed
domain_changed
risk_increased
risk_decreased
authority_changed
depth_increased
interpretation_hop
routing_changed
audit_missing
recovery_transition
scope_expanded
scope_narrowed
```

These signals describe structural changes.

They do not assign blame.

---

## 10. intent_changed

`intent_changed` indicates that the intent associated with the later question materially differs from the earlier question.

Example:

```text
Q1:
"Assess service health."

Q2:
"Modify the production service."
```

This signal does not automatically mean Q2 is invalid.

It means the intent transition SHOULD be inspectable.

---

## 11. domain_changed

`domain_changed` indicates that the question moved into a materially different operational or semantic domain.

Example:

```text
documentation
↓
filesystem
```

or:

```text
analysis
↓
production_operations
```

Domain change MAY increase operational impact.

---

## 12. risk_increased

`risk_increased` indicates that the later question has a higher risk classification than the earlier question.

Example:

```text
medium
↓
high
```

This is a structural observation.

The protocol does not define a universal policy response.

---

## 13. risk_decreased

`risk_decreased` indicates that the later question has a lower risk classification.

Example:

```text
high
↓
medium
```

A risk decrease SHOULD NOT automatically bypass previously required controls.

---

## 14. authority_changed

`authority_changed` indicates that authority requirements materially changed between questions.

Example:

```text
Q1:
authority.required = false

Q2:
authority.required = true
```

This is especially important when a lineage moves from analysis to execution.

---

## 15. depth_increased

`depth_increased` indicates that the current question exists deeper in the derivation graph than an earlier comparison point.

This signal MAY be used for:

- runaway decomposition detection;
- complexity monitoring;
- review triggers;
- resource control.

v0.4 does not define a universal maximum depth.

---

## 16. interpretation_hop

`interpretation_hop` indicates that a new question was generated by interpretation or reformulation rather than simple decomposition.

Example:

```text
Q1
↓ interpreted_as
Q2
```

Multiple interpretation hops MAY deserve additional review because semantic meaning can change at each step.

---

## 17. routing_changed

`routing_changed` indicates that responsibility moved to a materially different processing class or role.

Example:

```text
Planner
↓
Executor
```

or:

```text
Audit Agent
↓
Execution Agent
```

Simple infrastructure-level transport changes SHOULD NOT automatically trigger this signal.

---

## 18. audit_missing

`audit_missing` indicates that an expected audit or verification branch was not observed where local policy expected one.

Example:

```text
high-risk execution-related question
↓
no audit branch
```

This signal depends on external policy.

Q Network v0.4 does not define when audit is mandatory.

---

## 19. recovery_transition

`recovery_transition` indicates that a question lineage entered a recovery path.

Example:

```text
operation failed
↓
recovery question generated
```

Recovery is not itself abnormal.

This signal exists because recovery paths often require fresh authority and updated assumptions.

---

## 20. scope_expanded

`scope_expanded` indicates that the later question covers a broader target, resource set, domain, or effect.

Example:

```text
"Check this file"
↓
"Check all production files"
```

Scope expansion MAY require additional review.

---

## 21. scope_narrowed

`scope_narrowed` indicates that a later question became more specific or restricted.

Example:

```text
"Review the deployment system"
↓
"Verify only the rollback configuration"
```

Scope narrowing is often desirable but is still useful to record.

---

## 22. Drift Signal Multiplicity

A single transition MAY carry multiple signals.

Example:

```yaml
signals:
  - "intent_changed"
  - "domain_changed"
  - "risk_increased"
  - "authority_changed"
```

Signals SHOULD be unique within a Drift Record.

---

## 23. review_state

A Drift Record MAY contain a review state.

Recommended values:

```text
none
observe
review_recommended
hold_recommended
human_review_required
```

These values represent suggested review posture.

They do not grant or revoke authority.

---

## 24. none

`none` indicates that drift was recorded but no additional review posture is currently suggested.

---

## 25. observe

`observe` indicates that the transition should remain visible to monitoring systems.

No interruption is implied.

---

## 26. review_recommended

`review_recommended` indicates that an additional automated or human review MAY be appropriate.

---

## 27. hold_recommended

`hold_recommended` indicates that pausing progression MAY be appropriate until additional verification occurs.

The Drift Record itself does not enforce the hold.

---

## 28. human_review_required

`human_review_required` indicates that external policy requires human review before further progression.

The source of this requirement MUST come from an external policy or authority system.

The Drift Record does not create that authority requirement itself.

---

## 29. Drift Does Not Grant Control

Question Drift is observational.

A Drift Record MUST NOT itself:

- authorize execution;
- revoke authority;
- terminate an agent;
- enforce a hold;
- assign blame.

Control actions MUST be handled by separate systems.

---

## 30. trace_parent

`trace_parent` MAY link the Drift Record to an external Trace or Receipt.

Example:

```yaml
trace_parent: "trace-qdrift-001"
```

This MAY allow reconstruction of:

```text
Question transition
↓
Drift detection
↓
Review
↓
Later action
```

---

## 31. Detection Source

Implementations MAY record who or what detected drift.

Recommended optional field:

```yaml
detected_by: "drift-monitor-agent"
```

The detector MAY be:

- deterministic logic;
- rule engine;
- semantic model;
- auditor;
- human reviewer.

Detection source does not determine final correctness.

---

## 32. detection_method

Implementations MAY record the method used to identify drift.

Recommended values include:

```text
structural
rule_based
semantic
hybrid
human
```

### structural

Derived from explicit protocol fields.

### rule_based

Derived from policy or deterministic rules.

### semantic

Derived from semantic comparison.

### hybrid

Combination of structural and semantic methods.

### human

Recorded directly by a human reviewer.

---

## 33. Structural Drift

Structural Drift uses protocol fields directly.

Examples:

```text
risk_level changed
authority.required changed
domain changed
graph depth increased
routing role changed
```

Structural Drift is generally easier to reproduce and audit than opaque semantic scoring.

v0.4 RECOMMENDS structural drift as the baseline implementation.

---

## 34. Semantic Drift

Semantic Drift compares meaning between questions.

Possible implementations MAY use:

- embeddings;
- semantic classifiers;
- language models;
- symbolic comparison;
- human judgment.

v0.4 does not prescribe a specific algorithm.

Semantic output SHOULD be treated as evidence rather than unquestioned fact.

---

## 35. No Mandatory Drift Score

Version 0.4 intentionally does not define a universal numeric Question Drift Score.

A value such as:

```text
Drift = 73
```

may appear precise without explaining what changed.

Q Network prefers explicit observable signals.

Example:

```text
intent_changed
risk_increased
authority_changed
```

is often more operationally useful.

---

## 36. Optional Local Score

Implementations MAY define a local drift score.

If used, it MUST NOT replace explicit drift signals.

Example:

```yaml
local_score:
  value: 0.74
  method: "local-semantic-v2"
```

Scores SHOULD identify the method used.

Scores from different methods MUST NOT be assumed comparable.

---

## 37. Question Graph Compatibility

Drift Records SHOULD reference questions that exist within a Question Graph where applicable.

Example:

```text
Q1
↓ interpreted_as
Q2
```

may produce:

```text
interpretation_hop
intent_changed
```

The graph provides structure.

The Drift Record provides observed transition characteristics.

---

## 38. Provenance Compatibility

Question Provenance MAY provide evidence for Drift Signals.

Example:

```yaml
source_intent: "assess_system_security"
interpreted_intent: "attempt_external_access"
```

may support:

```text
intent_changed
```

However, implementations SHOULD avoid inferring unsafe behavior solely from the difference.

---

## 39. Multi-Step Drift

Drift MAY be evaluated between adjacent questions:

```text
Q1 → Q2
```

or across multiple lineage steps:

```text
Q0 → Q4
```

Adjacent drift helps identify local transition points.

Long-range drift helps identify cumulative deviation.

---

## 40. Root-to-Current Comparison

Implementations MAY compare a current question to the root question of a lineage.

Example:

```text
Q0
↓
Q1
↓
Q2
↓
Q3
```

Comparison:

```text
Q0 ↔ Q3
```

may reveal cumulative changes not obvious in any single edge.

---

## 41. Cumulative Drift

Multiple individually reasonable transitions MAY produce a large cumulative shift.

Example:

```text
Q0
"Assess safety"

↓
Q1
"Check network exposure"

↓
Q2
"Verify reachable services"

↓
Q3
"Attempt privileged external access"
```

Each step may appear small.

The full lineage may nevertheless deserve review.

v0.4 allows recording cumulative drift without defining a mandatory numerical formula.

---

## 42. Drift and Incident Prevention

Question Drift MAY support pre-incident intervention.

Example:

```text
Q0
↓
Q1
↓
Q2
↓
Q3
   ⚠ intent_changed
   ⚠ risk_increased
   ⚠ authority_changed
↓
review_recommended
```

A separate policy layer MAY then:

```text
continue
audit
hold
request human review
```

---

## 43. Drift and Incident Investigation

After an incident, Drift Records MAY help identify where the lineage changed materially.

Example:

```text
Incident
↑
Q5
↑
Q4   ⚠ authority_changed
↑
Q3   ⚠ risk_increased
↑
Q2   ⚠ intent_changed
↑
Q1
↑
Q0
```

This does not prove causal responsibility.

It identifies candidate transition points for investigation.

---

## 44. Drift Record Object

Canonical v0.4 example:

```yaml
schema_version: "0.4.0"

drift_id: "qdrift-001"
created_at: "2026-10-17T00:00:00Z"

from_question_id: "q-002"
to_question_id: "q-003"

signals:
  - "intent_changed"
  - "risk_increased"
  - "authority_changed"

review_state: "review_recommended"

detected_by: "drift-monitor-agent"
detection_method: "structural"

trace_parent: "trace-qdrift-001"
```

---

## 45. Minimal Drift Record

A minimal valid Drift Record MAY contain:

```yaml
schema_version: "0.4.0"

drift_id: "qdrift-minimal-001"
created_at: "2026-10-17T00:01:00Z"

from_question_id: "q-001"
to_question_id: "q-002"

signals:
  - "depth_increased"

review_state: "observe"
```

---

## 46. No Self Comparison

A Drift Record MUST NOT compare a question to itself.

Invalid:

```text
from_question_id = q-001
to_question_id   = q-001
```

A new Question Envelope SHOULD exist if reconsideration occurred.

---

## 47. Empty Signals

A Drift Record MUST contain at least one signal.

Invalid:

```yaml
signals: []
```

If no drift signal exists, a Drift Record SHOULD generally not be created.

---

## 48. Duplicate Signals

Signals MUST NOT be duplicated within a single Drift Record.

Invalid:

```yaml
signals:
  - "risk_increased"
  - "risk_increased"
```

---

## 49. Contradictory Risk Signals

A single Drift Record SHOULD NOT contain both:

```text
risk_increased
risk_decreased
```

for the same comparison.

Such a record is semantically contradictory unless an implementation explicitly models multiple independent risk dimensions.

v0.4 treats this as invalid in the minimal model.

---

## 50. Contradictory Scope Signals

A single Drift Record SHOULD NOT contain both:

```text
scope_expanded
scope_narrowed
```

for the same comparison.

The minimal v0.4 model treats this as invalid.

---

## 51. Detection Method Consistency

If `detected_by` is present, `detection_method` SHOULD also be present.

If a local semantic score is recorded, the method SHOULD identify how that score was produced.

---

## 52. Partial Evidence

A Drift Record MAY be created when only partial evidence is available.

Implementations MAY mark such records externally as provisional.

Question Drift SHOULD remain revisable through auditable correction rather than silent replacement.

---

## 53. Drift Corrections

If a Drift Signal was incorrectly recorded, implementations SHOULD preserve correction history.

Possible approaches include:

```text
superseding drift record
correction event
trace amendment
record status
```

v0.4 does not define a mandatory correction format.

---

## 54. Security Considerations

Implementations SHOULD consider:

- forged drift records;
- suppressed drift signals;
- malicious over-reporting;
- false semantic-shift claims;
- drift-trigger manipulation;
- fabricated detector identities;
- review-state inflation;
- review-state suppression.

Drift records SHOULD be treated as evidence.

---

## 55. Privacy Considerations

Question Drift SHOULD avoid requiring private chain-of-thought.

A conforming implementation MAY compare:

- intent labels;
- domain labels;
- risk values;
- authority metadata;
- graph relations;
- externally shareable summaries.

Full internal reasoning disclosure is not required.

---

## 56. Validation Invariants

A conforming v0.4 Drift Record MUST satisfy:

### Identity

```text
drift_id exists
drift_id is non-empty
```

### Question Pair

```text
from_question_id exists
to_question_id exists
from_question_id != to_question_id
```

### Signals

```text
signals contains at least one value
signals contains no duplicates
```

### Contradiction

```text
NOT (
  risk_increased
  AND
  risk_decreased
)
```

and:

```text
NOT (
  scope_expanded
  AND
  scope_narrowed
)
```

### Review State

`review_state` MUST be a defined v0.4 value.

---

## 57. Example — Risk and Authority Drift

```yaml
schema_version: "0.4.0"

drift_id: "qdrift-risk-auth-001"
created_at: "2026-10-17T00:10:00Z"

from_question_id: "q-analysis-001"
to_question_id: "q-execution-001"

signals:
  - "intent_changed"
  - "risk_increased"
  - "authority_changed"

review_state: "human_review_required"

detected_by: "structural-drift-monitor"
detection_method: "structural"

trace_parent: "trace-qdrift-risk-auth-001"
```

---

## 58. Example — Recovery Drift

```yaml
schema_version: "0.4.0"

drift_id: "qdrift-recovery-001"
created_at: "2026-10-17T00:11:00Z"

from_question_id: "q-operation-001"
to_question_id: "q-recovery-001"

signals:
  - "recovery_transition"
  - "authority_changed"

review_state: "review_recommended"

detected_by: "recovery-monitor"
detection_method: "structural"
```

---

## 59. Invalid Example — Self Comparison

```yaml
from_question_id: "q-001"
to_question_id: "q-001"
```

Invalid.

---

## 60. Invalid Example — Contradictory Risk

```yaml
signals:
  - "risk_increased"
  - "risk_decreased"
```

Invalid in the minimal v0.4 model.

---

## 61. Invalid Example — Empty Signals

```yaml
signals: []
```

Invalid.

---

## 62. Relationship to Earlier Versions

v0.1 answers:

> What is this question?

v0.2 answers:

> Why did this question arise?

v0.3 answers:

> How is this question connected to other questions?

v0.4 answers:

> What changed as the question moved through the network?

Together:

```text
Question Envelope
        ↓
Question Provenance
        ↓
Question Graph
        ↓
Question Drift
```

form the first four structural layers of Q Network.

---

## 63. Non-Goals of v0.4

Version 0.4 does not define:

- a universal semantic-distance algorithm;
- a universal numerical Drift Score;
- causal blame;
- incident attribution;
- automatic shutdown;
- automatic authority revocation;
- hidden chain-of-thought inspection;
- reward penalties;
- reputation scoring.

These remain separate concerns.

---

## 64. Future Direction

Expected progression:

```text
v0.1
Question Envelope

v0.2
Question Provenance

v0.3
Question Graph

v0.4
Question Drift

v0.5
Incident Backtrace
```

Question Drift provides candidate transition points that Incident Backtrace may later use.

---

## 65. Core Statements

Q Network Protocol v0.4 defines Question Drift as observable structural change across a question lineage.

Its primary invariant is:

> Drift identifies change; it does not declare fault.

Its safety invariant is:

> A Drift Record may recommend review, but it does not grant, revoke, or exercise authority.

Its transparency principle is:

> Prefer explicit structural signals over opaque universal scores.

Its investigative principle is:

> When a lineage changes materially, record where and how it changed before deciding what that change means.
