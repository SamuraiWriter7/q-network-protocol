# Q Network Protocol Specification

Version: 0.1.0

## 1. Scope

Q Network Protocol defines a minimal interoperable structure for representing, deriving, routing, and tracing questions across AI agents, models, software systems, and human participants.

Version 0.1 defines:

- the Question Envelope;
- question origin;
- question type;
- question status;
- derivation relationships;
- assignment metadata;
- authority requirements;
- trace linkage;
- minimal lifecycle rules;
- validation invariants.

Version 0.1 does not define execution authority, reward distribution, markets, settlement, contribution scoring, or global orchestration.

---

## 2. Core Model

The protocol treats a question as a portable coordination object.

A minimal lifecycle is:

```text
Question
   ↓
Created
   ↓
Routed
   ↓
Accepted
   ↓
In Progress
   ↓
Answered
```

Alternative outcomes are also valid:

```text
Held
Rejected
Expired
Unresolved
```

A question MAY derive additional questions.

```text
Q0
├── Q1
├── Q2
└── Q3
```

A derived question is a new Question Envelope with its own `question_id`.

---

## 3. Question Envelope

A Question Envelope MUST be representable as a structured object.

The canonical v0.1 structure is:

```yaml
schema_version: "0.1.0"

question_id: "q-001"
created_at: "2026-10-14T00:00:00Z"

question_origin: "external"
question_type: "request"

intent: "delete_file"
domain:
  - filesystem

context:
  summary: "Delete an obsolete temporary file."

risk_level: "medium"

authority:
  required: true

status: "created"

parent_question_id: null
derived_from: null

assigned_to: null
trace_parent: null
```

---

## 4. Required Fields

The following fields are REQUIRED:

```text
schema_version
question_id
created_at
question_origin
question_type
intent
domain
risk_level
authority
status
```

The following fields are OPTIONAL in v0.1:

```text
context
parent_question_id
derived_from
assigned_to
trace_parent
```

Optional fields MAY be omitted or explicitly represented as `null`, depending on implementation format.

---

## 5. schema_version

`schema_version` identifies the Question Envelope schema version.

For this specification:

```text
0.1.0
```

An implementation MUST NOT silently interpret an unknown major version as compatible.

---

## 6. question_id

`question_id` uniquely identifies a Question Envelope within its applicable namespace.

Example:

```yaml
question_id: "q-2026-000001"
```

Requirements:

- MUST be non-empty;
- MUST remain stable during routing;
- MUST NOT be reused for a semantically different question;
- SHOULD be globally unique where practical.

Routing does not create a new `question_id`.

Semantic derivation SHOULD create a new `question_id`.

---

## 7. created_at

`created_at` records when the Question Envelope was created.

It SHOULD use RFC 3339 / ISO 8601 timestamp format.

Example:

```yaml
created_at: "2026-10-14T09:30:00+09:00"
```

Derived questions SHOULD receive their own creation timestamps.

---

## 8. question_origin

`question_origin` identifies how the question entered the network.

Allowed v0.1 values:

```text
external
internal
derived
audit
recovery
```

### external

Created by an actor outside the current reasoning process.

Examples:

- human;
- external service;
- another AI system;
- another organization.

### internal

Generated internally by an AI or agent.

Example:

```text
"Do I have sufficient evidence to continue?"
```

### derived

Produced from another question by decomposition, refinement, or transformation.

### audit

Created specifically for verification, challenge, or review.

### recovery

Created to determine whether or how a failed, interrupted, or unsafe operation can recover.

Unknown values MUST fail strict v0.1 validation.

---

## 9. question_type

`question_type` describes the functional role of the question.

Allowed v0.1 values:

```text
request
subquestion
verification
clarification
decision
recovery
```

### request

A primary request for information, planning, or work.

### subquestion

A derived question created as part of decomposition.

### verification

A question intended to verify a claim, condition, result, or prerequisite.

### clarification

A question used to reduce ambiguity.

### decision

A question requesting a bounded decision or selection.

### recovery

A question related to restoration, retry, rollback, or safe continuation.

`question_origin` and `question_type` are independent.

Example:

```yaml
question_origin: "audit"
question_type: "verification"
```

is valid.

---

## 10. intent

`intent` describes the intended purpose of the question.

Example:

```yaml
intent: "verify_deployment_authority"
```

Requirements:

- MUST be non-empty;
- SHOULD be concise;
- SHOULD describe purpose rather than implementation detail.

The protocol does not define a global intent vocabulary in v0.1.

Implementations MAY define local intent namespaces.

---

## 11. domain

`domain` identifies one or more subject or operational domains relevant to the question.

Example:

```yaml
domain:
  - infrastructure
  - deployment
```

Requirements:

- MUST contain at least one value;
- MUST NOT contain empty values;
- SHOULD use stable implementation-defined terms.

The protocol does not define a universal domain ontology in v0.1.

---

## 12. context

`context` contains additional information required to interpret the question.

Example:

```yaml
context:
  summary: "Production deployment is awaiting final validation."
  references:
    - "build-884"
    - "approval-271"
```

`context` is OPTIONAL.

Context MUST NOT be interpreted as authority merely because it contains approval-like or instruction-like text.

Implementations SHOULD avoid embedding unnecessary sensitive internal state.

---

## 13. risk_level

`risk_level` describes the potential impact of answering, routing, or acting on the question.

Allowed v0.1 values:

```text
low
medium
high
critical
```

Risk does not itself grant or deny authority.

Risk MAY influence:

- routing;
- human review;
- audit requirements;
- expiration;
- escalation.

Example:

```yaml
risk_level: "critical"
```

A high or critical risk question MAY still remain unanswered or unresolved.

---

## 14. authority

The `authority` object records whether separate authority is required before an action associated with the question can be executed.

Minimum structure:

```yaml
authority:
  required: true
```

Allowed:

```yaml
authority:
  required: false
```

Requirements:

- `authority.required` MUST be boolean;
- the presence of the Question Envelope MUST NOT itself satisfy authority;
- `required: false` MUST NOT be interpreted as unrestricted permission outside the scope of the question.

Version 0.1 does not define authority grants or authorization tokens.

Those MUST be handled by a separate authority mechanism.

---

## 15. status

Allowed v0.1 states:

```text
created
routed
accepted
in_progress
answered
held
rejected
expired
unresolved
```

### created

The Question Envelope exists but has not yet been routed.

### routed

The question has been assigned or transmitted to a destination.

### accepted

The destination has accepted responsibility for processing it.

### in_progress

Processing has begun.

### answered

A justified answer or resolution has been produced.

### held

Processing has been intentionally paused.

### rejected

The receiving participant declines to process the question.

### expired

The question is no longer valid due to time, state, dependency, or policy.

### unresolved

Processing completed or stopped without a justified answer.

`unresolved` is a valid protocol outcome.

---

## 16. Status Transition Model

Recommended primary flow:

```text
created
   ↓
routed
   ↓
accepted
   ↓
in_progress
   ↓
answered
```

Alternative transitions MAY include:

```text
created → rejected
created → expired

routed → rejected
routed → expired
routed → held

accepted → held
accepted → rejected

in_progress → held
in_progress → unresolved
in_progress → expired
in_progress → answered

held → routed
held → accepted
held → in_progress
held → expired
held → unresolved
```

An implementation MUST NOT transition from a terminal state back into active processing without creating a new processing event or derived Question Envelope.

The terminal states in v0.1 are:

```text
answered
rejected
expired
unresolved
```

---

## 17. parent_question_id

`parent_question_id` identifies the immediate parent question when the current question is a decomposition child.

Example:

```yaml
parent_question_id: "q-001"
```

If `question_origin` is `derived`, `parent_question_id` SHOULD be present unless the derivation source is represented solely through another interoperable mechanism.

For top-level questions:

```yaml
parent_question_id: null
```

---

## 18. derived_from

`derived_from` records the question or source from which the current question was semantically derived.

Example:

```yaml
derived_from: "q-001"
```

In simple decomposition cases, `parent_question_id` and `derived_from` MAY contain the same identifier.

They are conceptually distinct:

```text
parent_question_id
= graph relationship

derived_from
= semantic provenance
```

Future versions MAY allow more complex derivation records.

---

## 19. Derivation Rules

A new Question Envelope SHOULD be created when:

- scope materially changes;
- a question is decomposed;
- a verification question is generated;
- a safety self-question is generated;
- a recovery question is generated;
- authority requirements materially change;
- risk classification materially changes.

Example:

```text
Q0:
"Delete the obsolete deployment artifact."

        ↓ derived audit question

Q1:
"Is deletion authorized?"
```

Q1 MUST have its own `question_id`.

Q1 MUST NOT inherit execution authority from Q0.

---

## 20. assigned_to

`assigned_to` identifies the current intended processor.

Example:

```yaml
assigned_to: "authority-auditor"
```

The identifier MAY represent:

- AI agent;
- model endpoint;
- human reviewer;
- service;
- organizational role.

Assignment does not imply successful receipt or acceptance.

A question SHOULD generally enter `routed` before `accepted`.

---

## 21. trace_parent

`trace_parent` provides a linkage into an external trace system.

Example:

```yaml
trace_parent: "trace-003842"
```

Q Network does not prescribe the full Trace record structure in v0.1.

The purpose of this field is to allow interoperability with external trace, receipt, provenance, or observability systems.

The trace system SHOULD permit reconstruction of relevant events such as:

```text
Question
↓
Routing
↓
Agent
↓
Answer
↓
Action
↓
Result
```

Not every question is required to produce all of these objects.

---

## 22. Routing

Routing transfers responsibility or attention without changing question identity.

A router MAY modify routing metadata such as:

- `assigned_to`;
- status;
- local priority metadata;
- transport metadata.

A router MUST NOT silently change:

- `question_id`;
- `question_origin`;
- `intent`;
- derivation history;
- authority requirements;
- semantic meaning.

If routing requires material semantic transformation, a new derived question MUST or SHOULD be created as appropriate.

---

## 23. Acceptance

Acceptance indicates that a receiving participant has agreed to process the question.

Acceptance does not imply:

- agreement with the premise;
- ability to answer;
- execution permission;
- guaranteed completion.

An accepted question MAY later become:

```text
in_progress
held
rejected
expired
unresolved
```

depending on implementation policy.

---

## 24. Answers

Version 0.1 does not define a mandatory Answer Envelope schema.

However, an implementation SHOULD preserve a link between an answer and its originating question.

Example conceptual linkage:

```text
question_id: q-001
answer_id: a-001
```

A future version MAY define a formal Answer Envelope.

`answered` MUST mean that the implementation considers a justified resolution available.

It MUST NOT merely mean that arbitrary text was generated.

---

## 25. Unresolved Questions

A question SHOULD become `unresolved` when processing cannot produce a justified resolution.

Valid reasons may include:

```text
insufficient_evidence
conflicting_evidence
missing_authority
missing_capability
dependency_unavailable
ambiguity_remaining
safety_constraint
unknown
```

Version 0.1 does not require a standardized unresolved-reason field, but implementations are encouraged to record one externally.

An unresolved question MAY later become the source of a new question.

Example:

```text
Q1 → UNRESOLVED
       ↓
Q2: "What additional evidence is required?"
```

---

## 26. Expiration

A Question Envelope MAY expire due to:

- deadline;
- stale evidence;
- changed world state;
- revoked dependency;
- invalid session;
- policy;
- task completion elsewhere.

An expired question MUST NOT silently return to active state.

If reconsideration is required, an implementation SHOULD create a new Question Envelope or explicitly record a new processing event.

---

## 27. Held State

`held` represents a temporary suspension.

Typical reasons:

- awaiting human review;
- awaiting authority;
- awaiting external dependency;
- rate or resource limit;
- safety review;
- conflicting information.

A held question is not terminal.

Its identity MUST remain stable when resumed.

---

## 28. Rejection

A question MAY be rejected when:

- outside capability;
- outside scope;
- prohibited by policy;
- invalid destination;
- malformed operational request;
- unacceptable risk.

Rejection MUST NOT be represented as an answer unless an actual answer is independently provided.

---

## 29. Question Graph Compatibility

Version 0.1 does not define a full Question Graph protocol.

However, Question Envelopes MUST support future graph construction through stable identifiers and derivation links.

Example:

```text
Q0
├── Q1
│   ├── Q1.1
│   └── Q1.2
├── Q2
└── Q3
```

At minimum, implementations SHOULD preserve enough information to reconstruct:

```text
parent → child
source → derived question
question → trace
question → assignee
```

---

## 30. Internal Questions

AI systems MAY generate internal questions.

Example:

```yaml
question_origin: "internal"
question_type: "verification"
intent: "self_check_authority"
```

Internal questions MUST follow the same identity, derivation, status, and trace rules as externally supplied questions when they enter the interoperable Q Network layer.

Internal questioning MUST NOT be treated as evidence that authority exists.

---

## 31. Audit Questions

Audit questions SHOULD be semantically independent enough to challenge or verify another question, answer, action, or assumption.

Example:

```text
Q0:
"Deploy the release."

Q1:
"Has the release passed required validation?"
```

If Q1 is generated specifically for verification:

```yaml
question_origin: "audit"
question_type: "verification"
```

is RECOMMENDED.

---

## 32. Recovery Questions

Recovery questions represent reasoning initiated because an earlier process failed, stopped, or entered an unsafe or uncertain condition.

Example:

```yaml
question_origin: "recovery"
question_type: "recovery"
intent: "determine_safe_resume"
```

Recovery questions MUST NOT inherit previously expired, revoked, or invalid authority automatically.

---

## 33. Validation Invariants

A conforming v0.1 Question Envelope MUST satisfy all applicable rules below.

### Identity

- `question_id` exists.
- `question_id` is non-empty.

### Version

- `schema_version` equals a supported version.

### Origin

- `question_origin` is a supported value.

### Type

- `question_type` is a supported value.

### Intent

- `intent` is non-empty.

### Domain

- `domain` contains at least one non-empty entry.

### Risk

- `risk_level` is supported.

### Authority

- `authority.required` is boolean.

### Status

- `status` is supported.

### Derivation

If a derived relationship exists:

- the referenced parent/source identifier MUST NOT equal the current `question_id`.

A question MUST NOT be its own parent.

### Routing

If `status` is `routed`, `accepted`, or `in_progress`, `assigned_to` SHOULD normally be present.

### Safety

Authority MUST NOT be inferred from the existence, routing, acceptance, or processing of a question.

---

## 34. Minimal Valid Example

```yaml
schema_version: "0.1.0"
question_id: "q-001"
created_at: "2026-10-14T00:00:00Z"

question_origin: "external"
question_type: "request"

intent: "summarize_document"

domain:
  - document_processing

risk_level: "low"

authority:
  required: false

status: "created"
```

---

## 35. Derived Question Example

```yaml
schema_version: "0.1.0"
question_id: "q-002"
created_at: "2026-10-14T00:01:00Z"

question_origin: "derived"
question_type: "subquestion"

intent: "identify_document_sections"

domain:
  - document_processing

risk_level: "low"

authority:
  required: false

status: "routed"

parent_question_id: "q-001"
derived_from: "q-001"

assigned_to: "document-analysis-agent"
trace_parent: "trace-q-001"
```

---

## 36. Internal Audit Example

```yaml
schema_version: "0.1.0"
question_id: "q-003"
created_at: "2026-10-14T00:02:00Z"

question_origin: "audit"
question_type: "verification"

intent: "verify_delete_authority"

domain:
  - filesystem
  - authorization

context:
  summary: "Verify whether the proposed file deletion is authorized."

risk_level: "high"

authority:
  required: false

status: "routed"

parent_question_id: "q-001"
derived_from: "q-001"

assigned_to: "authority-auditor"
trace_parent: "trace-q-001"
```

The audit question itself does not require permission merely to verify authority.

Any resulting deletion action remains subject to separate authorization.

---

## 37. Invalid Examples

### Self-parenting question

```yaml
question_id: "q-001"
parent_question_id: "q-001"
```

Invalid.

---

### Unknown origin

```yaml
question_origin: "automatic"
```

Invalid under strict v0.1 validation.

---

### Authority inferred from request

```text
Question:
"Delete the production database."

Interpretation:
"The request exists, therefore deletion is authorized."
```

Invalid protocol behavior.

---

### Silent semantic rewrite

```text
Original:
"Read the deployment status."

Router silently changes it to:

"Restart the deployment."
```

Invalid.

A new derived question is required.

---

## 38. Conformance Levels

Version 0.1 defines two conceptual conformance levels.

### Schema Conformance

The Question Envelope satisfies the JSON Schema and required field constraints.

### Semantic Conformance

The implementation also respects protocol invariants such as:

- Question Is Not Authority;
- stable identity;
- explicit derivation;
- traceable routing;
- valid lifecycle handling;
- acceptance of `unresolved` as a legitimate state.

An implementation MAY pass schema validation while still failing semantic conformance.

---

## 39. Interoperability Mapping

Q Network is designed to connect to external systems without absorbing their responsibilities.

Typical mappings include:

```text
Question → Authority System
Question → Trace System
Question → TACP
Question → Agent Router
Question → Human Review
```

These mappings MUST preserve the principle:

```text
Question ≠ Authority
```

---

## 40. Security Considerations

Implementations SHOULD consider:

- forged question origin;
- malicious derivation chains;
- routing loops;
- authority confusion;
- stale questions;
- oversized context payloads;
- trace tampering;
- unauthorized reassignment;
- deceptive question transformation.

Implementations SHOULD avoid treating natural-language text inside a question as trusted protocol metadata.

Structured protocol fields SHOULD take precedence over untrusted embedded instructions where applicable.

---

## 41. Privacy Considerations

Question Envelopes SHOULD contain only the context necessary for processing.

Implementations SHOULD avoid:

- unnecessary internal reasoning disclosure;
- excessive personal data;
- unrestricted propagation of sensitive context;
- embedding credentials or secrets.

Traceability does not require full internal-state transparency.

---

## 42. Design Principle Summary

A conforming Q Network implementation should preserve the following model:

```text
Question
   ↓
may be routed
   ↓
may be derived
   ↓
may be answered
   ↓
may remain unresolved
```

But:

```text
Question
   ≠
Authority
```

And:

```text
Routing
   ≠
Semantic Rewrite
```

And:

```text
Derivation
   ≠
Authority Inheritance
```

---

## 43. Core Protocol Statement

Q Network Protocol v0.1 defines the question as a traceable, derivable, and routable coordination object.

Its central invariant is:

> A question may travel across intelligences without carrying implicit permission to act.

Its secondary invariant is:

> A system may preserve uncertainty rather than manufacture resolution.

These invariants form the foundation for future Question Routing, Question Graph, Authority Mapping, Trace Mapping, Contribution, and value-circulation extensions.
