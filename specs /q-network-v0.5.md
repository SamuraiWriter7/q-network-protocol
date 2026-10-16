# Q Network Protocol v0.5 — Incident Backtrace

Version: 0.5.0

## 1. Purpose

Q Network Protocol v0.5 introduces a minimal Incident Backtrace model.

Version 0.1 defined the Question Envelope.

Version 0.2 added Question Provenance.

Version 0.3 added Question Graph.

Version 0.4 added Question Drift.

Version 0.5 defines how an incident, anomalous action, unsafe outcome, or unexpected result MAY be traced backward through the question lineage that preceded it.

The purpose of Incident Backtrace is not to automatically assign blame.

Its purpose is to reconstruct a reviewable causal path.

---

## 2. Core Principle

The primary invariant of v0.5 is:

> Trace backward before assigning cause.

An incident MAY be associated with:

- an action;
- a plan;
- a question;
- a derived question;
- an interpretation transition;
- an authority mismatch;
- a drift signal;
- a recovery path;
- a human-originated request.

Incident Backtrace preserves the path between these objects where evidence is available.

---

## 3. Conceptual Model

A forward execution path may look like:

```text
Human Intent
    ↓
Q0
    ↓
Q1
    ↓
Q2
    ↓
Plan
    ↓
Action
    ↓
Incident
```

Incident Backtrace traverses the path in reverse:

```text
Incident
    ↑
Action
    ↑
Plan
    ↑
Q2
    ↑
Q1
    ↑
Q0
    ↑
Human Intent
```

The backtrace does not automatically declare which element caused the incident.

---

## 4. Incident Backtrace Record

Version 0.5 introduces an Incident Backtrace Record.

Canonical example:

```yaml
schema_version: "0.5.0"

backtrace_id: "qbacktrace-001"
created_at: "2026-10-17T01:00:00Z"

incident_id: "incident-001"

start_ref:
  type: "incident"
  id: "incident-001"

steps:
  - step_id: "bt-step-001"
    sequence: 0
    object_type: "incident"
    object_id: "incident-001"
    relation_to_previous: "start"

  - step_id: "bt-step-002"
    sequence: 1
    object_type: "action"
    object_id: "action-017"
    relation_to_previous: "resulted_from"

  - step_id: "bt-step-003"
    sequence: 2
    object_type: "question"
    object_id: "q-009"
    relation_to_previous: "triggered_by"

status: "partial"

trace_parent: "trace-backtrace-001"
```

---

## 5. backtrace_id

`backtrace_id` uniquely identifies an Incident Backtrace Record.

Requirements:

- MUST be non-empty;
- SHOULD be unique within the applicable namespace;
- MUST remain stable once referenced.

---

## 6. incident_id

`incident_id` identifies the incident or anomalous outcome under investigation.

Example:

```yaml
incident_id: "incident-001"
```

The incident record itself MAY be defined by another system.

Q Network v0.5 does not define a universal Incident schema.

---

## 7. start_ref

`start_ref` identifies the object from which backtrace reconstruction begins.

Canonical structure:

```yaml
start_ref:
  type: "incident"
  id: "incident-001"
```

Recommended `type` values are:

```text
incident
action
result
question
trace
receipt
```

The start object SHOULD normally represent the observed failure or outcome being investigated.

---

## 8. Backtrace Steps

A Backtrace Record contains an ordered sequence of steps.

Each step SHOULD identify:

```text
step_id
sequence
object_type
object_id
relation_to_previous
```

Optional fields MAY add:

```text
evidence_refs
drift_refs
authority_refs
confidence
notes
```

---

## 9. sequence

`sequence` defines the order of traversal.

Backtrace direction is:

```text
0 = observed incident or starting object

1 = immediate predecessor

2 = earlier predecessor

3 = earlier predecessor

...
```

Sequence values MUST be unique within a Backtrace Record.

They SHOULD begin at `0`.

They SHOULD increase monotonically.

---

## 10. object_type

`object_type` identifies the type of object represented by the step.

Core v0.5 values:

```text
incident
result
action
plan
question
drift
authority
trace
receipt
human_intent
external_event
```

This vocabulary MAY be extended in future versions.

---

## 11. object_id

`object_id` identifies the referenced object.

Example:

```yaml
object_type: "question"
object_id: "q-004"
```

The referenced object SHOULD be externally resolvable where practical.

---

## 12. relation_to_previous

`relation_to_previous` describes why the current earlier object is connected to the prior backtrace step.

Core v0.5 values:

```text
start
resulted_from
executed_from
planned_from
triggered_by
derived_from
interpreted_from
audited_from
recovered_from
authorized_by
observed_in
recorded_by
associated_with
```

The relation describes evidence linkage.

It does not establish legal or causal responsibility.

---

## 13. Backtrace Direction

Backtrace relations MUST be interpreted in reverse investigative order.

Example:

```text
Incident
↑ resulted_from
Action
↑ triggered_by
Question
```

means:

- the incident resulted from or followed the action;
- the action was triggered by or associated with the question.

This does not mean the question alone caused the incident.

---

## 14. Question Lineage Integration

When a backtrace reaches a question, the system MAY continue through Question Graph and Question Provenance.

Example:

```text
Incident
↑
Action
↑
Q5
↑
Q4
↑
Q2
↑
Q0
```

Question Graph provides relationship structure.

Question Provenance provides generation evidence.

Incident Backtrace provides reverse traversal.

---

## 15. Drift Integration

Backtrace steps MAY reference Question Drift Records.

Example:

```yaml
drift_refs:
  - "qdrift-017"
```

A Drift Record MAY identify a transition such as:

```text
intent_changed
risk_increased
authority_changed
```

Drift evidence helps investigators locate material transition points.

Drift does not establish final cause.

---

## 16. Authority Integration

Backtrace steps MAY reference relevant authority records.

Example:

```yaml
authority_refs:
  - "authority-context-017"
```

This MAY help determine:

- whether authority existed;
- whether authority expired;
- whether authority scope changed;
- whether execution exceeded authorization.

Authority evidence MUST be interpreted by the applicable authority system.

---

## 17. evidence_refs

A step MAY reference external evidence.

Example:

```yaml
evidence_refs:
  - "trace-action-017"
  - "receipt-exec-004"
  - "log-record-991"
```

Evidence MAY include:

- Trace records;
- Receipts;
- logs;
- audit records;
- snapshots;
- external system records.

v0.5 does not define these formats.

---

## 18. Evidence Before Conclusion

Backtrace reconstruction SHOULD distinguish:

```text
recorded fact
inferred relationship
investigative hypothesis
final attribution
```

These MUST NOT be silently collapsed into one category.

---

## 19. confidence

A Backtrace Step MAY contain a confidence level.

Recommended values:

```text
confirmed
supported
inferred
uncertain
```

### confirmed

Direct evidence strongly supports the relationship.

### supported

Multiple pieces of evidence support the relationship.

### inferred

The relationship is reconstructed indirectly.

### uncertain

The relationship remains weak or incomplete.

Confidence does not represent probability.

---

## 20. Backtrace Status

A Backtrace Record MUST contain a status.

Core v0.5 values:

```text
open
partial
reconstructed
closed
inconclusive
invalid
```

### open

Investigation is ongoing.

### partial

Some lineage has been reconstructed, but evidence is missing.

### reconstructed

A usable path has been reconstructed.

### closed

Investigation has been formally closed externally.

### inconclusive

Available evidence does not support a sufficiently reliable reconstruction.

### invalid

The Backtrace Record violates structural or semantic requirements.

---

## 21. Partial Backtrace Is Valid

A backtrace does not need to reach the original human intent.

Example:

```text
Incident
↑
Action
↑
Q7
↑
Q5
↑
unknown
```

This MAY be represented as:

```text
status = partial
```

Missing history MUST NOT be fabricated.

---

## 22. Inconclusive Is a Valid Outcome

An investigation MAY fail to establish a reliable path.

Example reasons:

- missing logs;
- conflicting traces;
- unavailable external systems;
- deleted records;
- ambiguous lineage;
- forged metadata;
- incomplete authority evidence.

The protocol MUST allow:

```text
status = inconclusive
```

without inventing causal certainty.

---

## 23. Human Attribution

Incident Backtrace SHOULD support human review.

The preferred model is:

```text
AI / tooling
→ reconstructs evidence path

Human investigator
→ evaluates evidence

Authorized process
→ assigns final cause or responsibility
```

Q Network MUST NOT require an AI system to make final blame determinations.

---

## 24. Candidate Transition Points

Implementations MAY identify candidate transition points.

Examples:

```text
meaning_shift
risk_escalation
authority_gap
routing_anomaly
audit_missing
recovery_failure
scope_expansion
```

These are investigative markers.

They are not final causes.

---

## 25. candidate_flags

A Backtrace Step MAY contain:

```yaml
candidate_flags:
  - "meaning_shift"
  - "authority_gap"
```

Recommended v0.5 flags:

```text
meaning_shift
risk_escalation
authority_gap
routing_anomaly
audit_missing
recovery_failure
scope_expansion
trace_gap
evidence_conflict
```

---

## 26. meaning_shift

`meaning_shift` indicates that Question Provenance or Drift evidence suggests material change in interpretation.

Example:

```text
"Assess safety"
↓
"Attempt external access"
```

This deserves investigation but does not prove fault.

---

## 27. risk_escalation

`risk_escalation` indicates that the question lineage increased in risk before the incident.

Example:

```text
medium
↓
high
↓
critical
```

---

## 28. authority_gap

`authority_gap` indicates that execution may have occurred without a clearly reconstructable valid authority path.

Possible causes include:

- missing authority check;
- expired authority;
- revoked authority;
- scope mismatch;
- unresolved authority state.

---

## 29. routing_anomaly

`routing_anomaly` indicates that a question moved to an unexpected participant or processing class.

Example:

```text
Audit Question
↓
Executor
```

without an expected intervening decision.

---

## 30. audit_missing

`audit_missing` indicates that a required or expected audit branch is absent from the available lineage.

The requirement itself MUST come from external policy.

---

## 31. recovery_failure

`recovery_failure` indicates that an incident occurred after or during a recovery branch.

This MAY deserve special review because recovery paths often operate under changed state.

---

## 32. scope_expansion

`scope_expansion` indicates that question or action scope expanded materially before the incident.

Example:

```text
single file
↓
directory
↓
production environment
```

---

## 33. trace_gap

`trace_gap` indicates that expected Trace or provenance records are missing.

Example:

```text
Q4
↓
?
↓
Action
```

A trace gap MUST NOT be automatically filled using speculation.

---

## 34. evidence_conflict

`evidence_conflict` indicates that available records disagree.

Example:

```text
Trace:
authority valid

Authority registry:
authority expired
```

Conflicts SHOULD remain visible in the Backtrace Record.

---

## 35. Notes

A Backtrace Step MAY include a concise `notes` field.

Notes SHOULD contain reviewable summaries.

They SHOULD NOT require private chain-of-thought.

Example:

```yaml
notes: "Authority reference existed, but the referenced approval had expired before execution."
```

---

## 36. Private Reasoning Is Not Required

Incident Backtrace MUST NOT require unrestricted hidden reasoning logs.

A usable backtrace MAY be reconstructed from:

```text
Question IDs
Question Graph
Provenance
Drift Records
Action records
Authority records
Trace
Receipts
timestamps
```

This supports investigation without requiring token-level reasoning disclosure.

---

## 37. Timestamp Ordering

Where timestamps are available, a Backtrace Record SHOULD preserve chronological consistency.

Earlier causal or operational objects SHOULD normally have timestamps no later than later objects.

However, v0.5 does not require every referenced object to contain a timestamp.

Clock skew and distributed systems MAY complicate strict timestamp ordering.

---

## 38. No Self Step

A Backtrace Step MUST NOT claim that an object directly precedes itself.

Invalid conceptual relation:

```text
Q1
↑ derived_from
Q1
```

---

## 39. Duplicate Step Identity

Each `step_id` MUST be unique within a Backtrace Record.

---

## 40. Unique Sequence

Each `sequence` value MUST be unique within a Backtrace Record.

Duplicate sequence positions are invalid.

---

## 41. Start Step

A Backtrace Record SHOULD contain exactly one step with:

```text
sequence = 0
```

That step SHOULD correspond to `start_ref`.

Its relation SHOULD be:

```text
start
```

---

## 42. Start Reference Consistency

The step at sequence `0` SHOULD satisfy:

```text
step.object_type == start_ref.type
step.object_id   == start_ref.id
```

A mismatch is semantically invalid in the minimal v0.5 model.

---

## 43. Ordered Sequence

For the minimal v0.5 model, sequence values SHOULD form:

```text
0, 1, 2, 3, ...
```

without duplicates.

Implementations MAY later support sparse sequences, but the minimal conformance model prefers contiguous ordering.

---

## 44. Backtrace Must Move Backward

Each new step SHOULD represent an earlier relevant object or context.

A backtrace MUST NOT silently switch into forward execution history without explicit relation semantics.

---

## 45. Backtrace and Question Graph

Question Graph MAY provide the lineage path:

```text
Q0 → Q1 → Q2 → Q3
```

Incident Backtrace MAY reverse it:

```text
Q3 → Q2 → Q1 → Q0
```

The two representations SHOULD remain compatible.

---

## 46. Backtrace and Provenance

Question Provenance may explain why each question was generated.

Example:

```text
Q2
↑ interpretation
Q1
```

The Backtrace Record MAY reference that transition as:

```text
Q2
↑ interpreted_from
Q1
```

---

## 47. Backtrace and Drift

Question Drift may identify where the lineage changed.

Example:

```text
Q1 → Q2
intent_changed
risk_increased
```

The corresponding backtrace step MAY carry:

```yaml
drift_refs:
  - "qdrift-q1-q2"
candidate_flags:
  - "meaning_shift"
  - "risk_escalation"
```

---

## 48. Backtrace and Recovery

Recovery paths MUST remain visible.

Example:

```text
Incident
↑
Recovery Action
↑
Recovery Question
↑
Original Failure
```

The investigation SHOULD NOT flatten the recovery branch into the original normal path.

---

## 49. Backtrace and Human Intent

A backtrace MAY eventually reach a human-originated intent.

Example:

```text
Incident
↑
Action
↑
Q4
↑
Q2
↑
Q0
↑
Human Intent
```

Reaching human intent does not mean the human caused the incident.

It only establishes lineage.

---

## 50. Backtrace Completeness

Implementations MAY classify completeness externally.

Recommended conceptual levels:

```text
complete
partial
fragmentary
unknown
```

v0.5 does not require a separate completeness field because `status` already represents core reconstruction state.

---

## 51. Backtrace Record Object

Canonical v0.5 structure:

```yaml
schema_version: "0.5.0"

backtrace_id: "qbacktrace-incident-001"
created_at: "2026-10-17T01:00:00Z"

incident_id: "incident-001"

start_ref:
  type: "incident"
  id: "incident-001"

status: "partial"

steps:
  - step_id: "bt-001"
    sequence: 0
    object_type: "incident"
    object_id: "incident-001"
    relation_to_previous: "start"
    confidence: "confirmed"

  - step_id: "bt-002"
    sequence: 1
    object_type: "action"
    object_id: "action-017"
    relation_to_previous: "resulted_from"
    confidence: "confirmed"

    evidence_refs:
      - "receipt-action-017"

  - step_id: "bt-003"
    sequence: 2
    object_type: "question"
    object_id: "q-009"
    relation_to_previous: "triggered_by"
    confidence: "supported"

    drift_refs:
      - "qdrift-009"

    candidate_flags:
      - "authority_gap"

trace_parent: "trace-qbacktrace-001"
```

---

## 52. Minimal Backtrace Record

A minimal valid Backtrace Record MAY contain only the start step.

Example:

```yaml
schema_version: "0.5.0"

backtrace_id: "qbacktrace-minimal-001"
created_at: "2026-10-17T01:01:00Z"

incident_id: "incident-002"

start_ref:
  type: "incident"
  id: "incident-002"

status: "open"

steps:
  - step_id: "bt-minimal-001"
    sequence: 0
    object_type: "incident"
    object_id: "incident-002"
    relation_to_previous: "start"
```

This represents an investigation that has begun but has not yet reconstructed prior lineage.

---

## 53. Example — Question Lineage Backtrace

```text
Incident
↑
Action
↑
Q4
↑
Q3
↑
Q1
↑
Q0
```

A Backtrace Record MAY preserve this entire chain.

The investigator may then inspect:

- Question Provenance;
- Question Graph;
- Drift Records;
- Authority contexts;
- execution Receipts.

---

## 54. Example — Meaning Shift Candidate

```text
Q0
"Assess system safety"

↑

Q1
"Check network exposure"

↑

Q2
"Attempt external access"
```

If Drift evidence indicates material intent change, Q2's step MAY carry:

```yaml
candidate_flags:
  - "meaning_shift"
  - "risk_escalation"
```

This remains an investigative marker.

---

## 55. Invalid Example — Duplicate Sequence

```yaml
steps:
  - step_id: "bt-001"
    sequence: 0

  - step_id: "bt-002"
    sequence: 0
```

Invalid.

---

## 56. Invalid Example — Duplicate Step ID

```yaml
steps:
  - step_id: "bt-001"
    sequence: 0

  - step_id: "bt-001"
    sequence: 1
```

Invalid.

---

## 57. Invalid Example — Start Mismatch

```yaml
start_ref:
  type: "incident"
  id: "incident-001"

steps:
  - step_id: "bt-001"
    sequence: 0
    object_type: "action"
    object_id: "action-001"
    relation_to_previous: "start"
```

Invalid in the minimal v0.5 model.

---

## 58. Invalid Example — Multiple Start Relations

```text
step 0 → relation = start
step 2 → relation = start
```

Invalid.

Only the initial backtrace step SHOULD use `start`.

---

## 59. Invalid Example — Fabricated Continuity

If evidence exists for:

```text
Incident
↑
Action
```

but no evidence exists connecting the action to any question, the Backtrace Record MUST NOT invent:

```text
Action
↑
Q7
```

The correct result is a partial backtrace with a trace gap.

---

## 60. Validation Invariants

A conforming v0.5 Backtrace Record MUST satisfy:

### Identity

```text
backtrace_id exists
incident_id exists
```

### Start Reference

```text
start_ref.type exists
start_ref.id exists
```

### Steps

```text
steps contains at least one step
```

### Step Identity

```text
step_id values are unique
```

### Sequence

```text
sequence values are unique
sequence begins at 0
```

### Start Step

```text
sequence 0 exists
sequence 0 relation = start
sequence 0 object matches start_ref
```

### Start Relation

```text
only sequence 0 may use relation = start
```

### Evidence Integrity

Backtrace MUST NOT fabricate missing links.

---

## 61. Structural vs Semantic Validation

Schema validation SHOULD cover:

```text
required fields
field types
enum values
steps minItems
identifier formats
sequence integer >= 0
array uniqueness where directly representable
```

Semantic validation SHOULD cover:

```text
duplicate step_id
duplicate sequence
missing sequence 0
start_ref mismatch
multiple start relations
non-contiguous sequence
self predecessor relationship
```

---

## 62. Security Considerations

Implementations SHOULD consider:

- forged backtrace steps;
- deleted lineage;
- hidden audit records;
- manipulated Drift Records;
- fake authority references;
- fabricated evidence;
- timestamp manipulation;
- intentional trace gaps;
- blame laundering through false provenance.

Backtrace data MUST be treated as evidence requiring verification.

---

## 63. Privacy Considerations

Incident Backtrace MAY expose sensitive operational history.

Implementations SHOULD minimize unnecessary disclosure of:

- personal data;
- internal prompts;
- private reasoning;
- credentials;
- confidential infrastructure;
- unrelated historical questions.

Backtrace should preserve relevant causal structure, not unrestricted system history.

---

## 64. Non-Goals of v0.5

Version 0.5 does not define:

- automatic blame assignment;
- legal liability;
- disciplinary action;
- automatic shutdown;
- universal incident severity;
- hidden chain-of-thought disclosure;
- probabilistic causal inference;
- root-cause scoring;
- economic penalties;
- reputation scoring.

These are separate concerns.

---

## 65. Relationship to Earlier Versions

v0.1 answers:

> What is this question?

v0.2 answers:

> Why did this question arise?

v0.3 answers:

> How is this question connected to other questions?

v0.4 answers:

> What changed as the question moved through the network?

v0.5 answers:

> After an incident, how do we trace the lineage backward?

Together:

```text
Question Envelope
        ↓
Question Provenance
        ↓
Question Graph
        ↓
Question Drift
        ↓
Incident Backtrace
```

form the first complete investigative stack of Q Network.

---

## 66. Core Statements

Q Network Protocol v0.5 defines Incident Backtrace as evidence-preserving reverse reconstruction of question and action lineage.

Its primary invariant is:

> Trace backward before assigning cause.

Its uncertainty invariant is:

> Missing evidence must remain missing; it must not be replaced by invented continuity.

Its safety invariant is:

> A Backtrace Record may identify candidate failure points, but it does not assign authority, guilt, or final responsibility.

Its transparency principle is:

> Reconstruct externally reviewable transitions without requiring unrestricted private reasoning disclosure.

Its investigative principle is:

> An incident is the end of a path; understanding it requires following that path back toward its origin.
