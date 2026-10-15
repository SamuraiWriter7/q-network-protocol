# Q Network Protocol v0.2 — Question Provenance

Version: 0.2.0

## 1. Purpose

Q Network Protocol v0.2 extends the v0.1 Question Envelope with explicit question provenance.

Version 0.1 established that a question can be:

- identified;
- derived;
- routed;
- traced;
- answered;
- held;
- rejected;
- expired;
- left unresolved.

Version 0.2 adds a new question:

> Why did this question come into existence?

The purpose of Question Provenance is to preserve enough information to reconstruct the causal lineage of a question without requiring unrestricted access to an AI system's private internal reasoning.

---

## 2. Core Principle

Q Network v0.2 introduces the following invariant:

> Every materially derived question SHOULD preserve the event, interpretation, or prior question that caused it to be generated.

Question Provenance is not intended to expose full chain-of-thought.

It records externally useful causal metadata.

The protocol distinguishes:

```text
Private reasoning
        ≠
Question provenance
```

Question Provenance records the observable transition between coordination objects.

---

## 3. Conceptual Model

A simple question flow may be:

```text
Human Intent
    ↓
Question Q0
    ↓
Interpretation
    ↓
Question Q1
    ↓
Decomposition
    ↓
Question Q2
    ↓
Authority Check
    ↓
Question Q3
    ↓
Action
```

Version 0.1 could preserve:

```text
Q0 → Q1 → Q2 → Q3
```

Version 0.2 additionally preserves:

```text
why Q1 was created
why Q2 was created
why Q3 was created
```

---

## 4. Question Provenance Object

Version 0.2 introduces an OPTIONAL `provenance` object.

Canonical structure:

```yaml
provenance:
  trigger_event: "human_request_received"
  generated_by: "planning-agent"
  generation_reason: "interpretation"

  source_question_id: "q-001"

  source_intent: "assess_system_security"
  interpreted_intent: "verify_external_access"

  authority_context_ref: "authority-context-001"

  provenance_trace: "trace-provenance-001"
```

The object MAY be absent for simple top-level questions.

It SHOULD be present when a question is created through:

- interpretation;
- decomposition;
- audit;
- recovery;
- escalation;
- rerouting with semantic transformation;
- safety reconsideration.

---

## 5. trigger_event

`trigger_event` identifies the observable event that caused generation of the question.

Examples:

```text
human_request_received
question_received
answer_received
action_failed
authority_denied
authority_expired
audit_requested
risk_increased
dependency_failed
timeout_detected
external_state_changed
```

v0.2 does not define a closed global vocabulary.

Implementations MAY define local values.

The field MUST NOT be empty when present.

---

## 6. generated_by

`generated_by` identifies the actor or component that generated the question.

Examples:

```text
planning-agent
audit-agent
recovery-agent
human-reviewer
q-router
```

The identifier MAY represent:

- an AI agent;
- a model;
- a deterministic service;
- a human participant;
- an organizational role.

`generated_by` identifies generation responsibility.

It does not imply execution authority.

---

## 7. generation_reason

`generation_reason` describes the functional reason the new question was created.

Recommended v0.2 values:

```text
interpretation
decomposition
clarification
verification
audit
recovery
escalation
risk_review
authority_check
dependency_check
```

Implementations MAY extend this vocabulary.

A generation reason SHOULD describe the transformation between the source state and the new question.

---

## 8. source_question_id

`source_question_id` identifies the question most directly responsible for generation of the current question.

Example:

```yaml
source_question_id: "q-001"
```

This field complements:

```text
parent_question_id
derived_from
```

The three fields have different roles:

```text
parent_question_id
= structural graph parent

derived_from
= semantic derivation source

source_question_id
= immediate provenance source
```

They MAY contain the same value in simple cases.

---

## 9. source_intent

`source_intent` records the relevant intent associated with the provenance source.

Example:

```yaml
source_intent: "assess_system_security"
```

This allows comparison between the original intent and the newly interpreted intent.

`source_intent` SHOULD NOT replace the canonical `intent` field of another Question Envelope.

It is a provenance snapshot.

---

## 10. interpreted_intent

`interpreted_intent` records the intent inferred or reformulated by the component that generated the current question.

Example:

```yaml
source_intent: "assess_system_security"
interpreted_intent: "verify_external_access"
```

This difference MAY be used by external systems to detect possible semantic drift.

However:

> A difference between source intent and interpreted intent does not itself prove error or unsafe behavior.

Interpretation changes MUST remain subject to external review where appropriate.

---

## 11. authority_context_ref

`authority_context_ref` links the question to an external authority context relevant at the time of generation.

Example:

```yaml
authority_context_ref: "authority-context-017"
```

The referenced object MAY describe:

- available permissions;
- denied permissions;
- expired approval;
- human authorization;
- execution limits;
- delegated scope.

Q Network v0.2 does not define the authority object itself.

The reference MUST NOT be interpreted as authorization.

---

## 12. provenance_trace

`provenance_trace` links to an external Trace or Receipt describing the provenance-generation event.

Example:

```yaml
provenance_trace: "trace-prov-q-002"
```

This MAY be used to reconstruct events such as:

```text
Q0 received
↓
Planner interpretation
↓
Q1 generated
```

without exposing unrestricted private reasoning.

---

## 13. Provenance and Private Reasoning

Q Network MUST NOT require hidden chain-of-thought or unrestricted reasoning logs for provenance conformance.

A conforming provenance record MAY capture:

```text
Input question
Generated question
Generation reason
Actor
Timestamp
Authority context reference
Trace reference
```

without recording private token-level reasoning.

The protocol therefore distinguishes:

```text
Explainable transition metadata
        from
Private reasoning content
```

---

## 14. Meaning Shift

Version 0.2 recognizes that the meaning of a question MAY change during derivation.

Example:

```text
Q0:
"Assess the security of this system."

        ↓ interpretation

Q1:
"Determine whether the external service can be reached."

        ↓ derivation

Q2:
"Attempt external access."
```

This sequence is not automatically invalid.

However, provenance SHOULD make the semantic transitions observable.

Implementations MAY later compute drift indicators from these transitions.

v0.2 does not define a mandatory Question Drift Score.

---

## 15. Provenance Chain

Questions MAY form provenance chains.

Example:

```text
Q0
│
├─ provenance: human_request_received
│
▼
Q1
│
├─ provenance: interpretation
│
▼
Q2
│
├─ provenance: decomposition
│
▼
Q3
│
├─ provenance: authority_check
│
▼
Q4
```

A system SHOULD be able to traverse such a chain backward where referenced records remain available.

---

## 16. Incident Backtrace Compatibility

v0.2 is designed to support future incident reconstruction.

Conceptually:

```text
Incident
↑
Action
↑
Plan
↑
Question
↑
Source Question
↑
Interpretation
↑
Original Question
↑
Human Intent
```

v0.2 does not define a complete Incident Backtrace protocol.

It ensures that Question Provenance contains enough structure for later specifications to build one.

---

## 17. Provenance Creation Rules

A provenance object SHOULD be created when a new question results from a material cognitive or operational transition.

Examples include:

### Interpretation

```text
"Check safety"
↓
"What safety property should be verified?"
```

### Decomposition

```text
"Deploy safely"
↓
"Has the build passed?"
```

### Authority Check

```text
"Delete the file"
↓
"Is deletion authorized?"
```

### Audit

```text
"Proceed with deployment"
↓
"Is the evidence current?"
```

### Recovery

```text
"Operation failed"
↓
"Can the operation be safely resumed?"
```

---

## 18. Provenance MUST NOT Grant Authority

The presence of provenance metadata MUST NOT authorize an action.

This is invalid:

```text
provenance:
  authority_context_ref: "approval-001"

therefore:

execution_authorized = true
```

The referenced authority record MUST be independently evaluated by the applicable authority mechanism.

The v0.1 invariant remains unchanged:

> Question Is Not Authority.

---

## 19. Provenance MUST NOT Rewrite History

Once a provenance relationship has been recorded and relied upon, implementations SHOULD NOT silently rewrite it.

Corrections SHOULD be represented as:

- a new provenance event;
- a superseding record;
- an explicit correction;
- a trace amendment.

Historical provenance SHOULD remain auditable where practical.

---

## 20. Provenance and Routing

Simple routing does not require new provenance.

Example:

```text
Q1
Agent A → Agent B
```

If the semantic meaning is unchanged, the same question MAY be routed without generating a new Question Envelope.

However:

```text
Q1:
"Verify account status."

Router transforms it into:

Q2:
"Disable the account."
```

This is a semantic transformation.

A new Question Envelope MUST be created and SHOULD contain provenance.

---

## 21. Provenance and Question Derivation

For a derived question, implementations SHOULD preserve both graph and provenance relationships.

Example:

```yaml
question_id: "q-002"
question_origin: "derived"

parent_question_id: "q-001"
derived_from: "q-001"

provenance:
  trigger_event: "question_received"
  generated_by: "planning-agent"
  generation_reason: "decomposition"
  source_question_id: "q-001"
```

This allows future systems to reconstruct both:

```text
Question Graph
```

and:

```text
Causal Generation Path
```

---

## 22. Provenance and Audit Questions

An audit question SHOULD indicate the object or question that triggered the audit.

Example:

```yaml
question_origin: "audit"
question_type: "verification"

provenance:
  trigger_event: "risk_increased"
  generated_by: "audit-agent"
  generation_reason: "audit"
  source_question_id: "q-004"
```

The audit question does not inherit authority from the source question.

---

## 23. Provenance and Recovery Questions

A recovery question SHOULD preserve the failure or interruption trigger.

Example:

```yaml
question_origin: "recovery"
question_type: "recovery"

provenance:
  trigger_event: "action_failed"
  generated_by: "recovery-agent"
  generation_reason: "recovery"
  source_question_id: "q-009"
```

Expired or revoked authority MUST NOT automatically carry into the recovery path.

---

## 24. Provenance Validation Invariants

A conforming v0.2 provenance object SHOULD satisfy the following semantic invariants.

### No Self Source

```text
provenance.source_question_id
!=
question_id
```

A question MUST NOT identify itself as its own provenance source.

---

### Generated By Must Be Explicit

If a provenance object contains a `generation_reason`, it SHOULD identify `generated_by`.

---

### Source Relationship Must Be Coherent

If both are present:

```text
source_question_id
derived_from
```

they MAY differ, but implementations SHOULD be able to explain the distinction.

Unexplained contradictory provenance SHOULD be treated as suspicious or invalid according to local policy.

---

### Authority Context Is Referential Only

```text
authority_context_ref
```

MUST NOT itself satisfy an authority requirement.

---

### Provenance Does Not Replace Trace

Question Provenance describes causal origin.

Trace describes observable events.

Implementations SHOULD NOT assume these are equivalent.

---

## 25. Recommended v0.2 Question Envelope

Example:

```yaml
schema_version: "0.2.0"

question_id: "q-002"
created_at: "2026-10-14T02:00:00Z"

question_origin: "derived"
question_type: "verification"

intent: "verify_external_access_requirement"

domain:
  - security
  - network

risk_level: "high"

authority:
  required: false

status: "routed"

parent_question_id: "q-001"
derived_from: "q-001"

assigned_to: "security-audit-agent"
trace_parent: "trace-q-001"

provenance:
  trigger_event: "question_received"
  generated_by: "planning-agent"
  generation_reason: "interpretation"

  source_question_id: "q-001"

  source_intent: "assess_system_security"
  interpreted_intent: "verify_external_access_requirement"

  authority_context_ref: "authority-context-001"
  provenance_trace: "trace-prov-q-002"
```

---

## 26. Invalid Provenance Example — Self Source

```yaml
question_id: "q-001"

provenance:
  source_question_id: "q-001"
```

Invalid.

A question cannot be the event source of its own creation.

---

## 27. Invalid Provenance Example — Authority Inference

```yaml
authority:
  required: true

provenance:
  authority_context_ref: "approval-001"
```

If an implementation concludes solely from this reference that execution is authorized, the implementation is semantically non-conformant.

---

## 28. Invalid Provenance Example — Silent Interpretation Rewrite

Original:

```text
"Check whether this service is healthy."
```

Internal interpretation:

```text
"Modify the production service."
```

If the transformed intent creates a materially different question, the implementation MUST NOT silently overwrite the original question.

A new Question Envelope SHOULD be created with provenance connecting the two.

---

## 29. Question Provenance vs Question Graph

Question Graph answers:

> Which questions are connected?

Question Provenance answers:

> Why was each connection created?

Example:

```text
Question Graph:

Q0
├── Q1
└── Q2
```

Provenance adds:

```text
Q0
├── Q1 [decomposition]
└── Q2 [audit]
```

Future versions MAY formally standardize this graph.

---

## 30. Question Provenance vs Trace

Trace:

```text
Q1 routed at 10:00
Q1 accepted at 10:01
Q2 created at 10:02
```

Provenance:

```text
Q2 was created because Q1 required an authority verification step.
```

They are complementary.

---

## 31. Question Provenance vs Incident Attribution

Question Provenance does not declare:

```text
"Q3 caused the incident."
```

It records evidence such as:

```text
Q3 was derived from Q2.
Q3 changed interpreted intent.
Q4 was generated without an authority context.
An action followed Q4.
```

Final causal attribution MAY require:

- human investigation;
- additional logs;
- authority records;
- environmental evidence;
- external audit.

---

## 32. Human Review

AI systems MAY identify candidate provenance anomalies.

Examples:

```text
possible interpretation shift
missing authority context
unusual derivation depth
unexpected routing destination
risk increase
```

AI-generated anomaly detection SHOULD be treated as investigative evidence, not final causal judgment.

The preferred model is:

```text
AI
→ maps causal candidates

Human
→ determines final attribution
```

---

## 33. Compatibility With v0.1

v0.2 SHOULD remain conceptually compatible with v0.1.

A v0.1 Question Envelope without `provenance` remains meaningful.

A v0.2 implementation MAY process a v0.1 Question Envelope with reduced provenance capabilities.

Version 0.2 adds provenance rather than replacing the core Question Envelope model.

---

## 34. Non-Goals of v0.2

Version 0.2 does not define:

- full Question Graph serialization;
- Question Drift Score;
- semantic-distance algorithms;
- causal responsibility scoring;
- incident blame assignment;
- hidden reasoning disclosure;
- global provenance storage;
- reward distribution;
- contribution weighting;
- economic settlement.

These remain candidates for later versions or mappings.

---

## 35. Future Direction

Potential future progression:

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

The versions SHOULD remain composable rather than collapsing all responsibilities into one schema.

---

## 36. Core Statements

Q Network Protocol v0.2 adds a provenance layer to the Question Envelope.

Its primary invariant is:

> A derived question should preserve enough evidence to explain what caused it to exist.

Its safety invariant remains:

> Provenance may explain an action path, but provenance never grants authority.

Its transparency principle is:

> Record the transition between questions without requiring unrestricted disclosure of private reasoning.

Its investigative principle is:

> When an incident occurs, follow the lineage of questions backward before assigning cause.
