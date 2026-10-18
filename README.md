# Q Network Protocol

**A traceable lifecycle protocol for questions, their provenance, structural drift, incident reconstruction, and structural impact.**

Q Network Protocol is a specification for treating questions as first-class traceable objects in AI and multi-agent systems.

Instead of viewing a question only as the beginning of an answer or action, Q Network records:

- where the question came from;
- how it changed;
- how it relates to other questions;
- where interpretation or risk drift occurred;
- how an incident can be traced backward through question lineage;
- how a question changed assumptions or generated new structures.

The protocol is designed around a simple idea:

> Questions may move between intelligences, but authority does not move merely because the question moves.

---

# 1. Why Q Network Exists

Conventional AI systems often focus on:

```text
Input
↓
Reasoning
↓
Answer / Action
```

This is useful, but insufficient for multi-agent and autonomous systems.

When many agents cooperate, questions themselves begin to move.

```text
Human
↓
Agent A
↓
Question
↓
Agent B
↓
Derived Question
↓
Agent C
↓
Action
```

At that point, several important questions emerge:

- Who created the original question?
- Why was a new question generated?
- Did the meaning change during routing?
- Did risk increase?
- Did authority requirements change?
- Which question led to the action?
- Can an incident be traced back to its originating question?
- Did a question alter the assumptions or structure of the system?

Q Network provides a common structure for answering these questions without requiring unrestricted access to private chain-of-thought.

---

# 2. Core Idea

Q Network treats a question as a traceable protocol object.

The basic lifecycle is:

```text
Question
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

This lifecycle is implemented across six versions:

```text
v0.1 Question Envelope
v0.2 Question Provenance
v0.3 Question Graph
v0.4 Question Drift
v0.5 Incident Backtrace
v0.6 Question Structural Perturbation
```

Together, these form the initial **Q Network Core**.

---

# 3. Core Invariants

Q Network is built around several invariants.

## 3.1 Question Is Not Authority

A question may request an action.

A question does not grant permission to perform that action.

```text
Question
≠ Authority
≠ Permission
≠ Execution Right
```

Authority MUST be determined by a separate authority mechanism.

---

## 3.2 Every Question Has an Origin

A question SHOULD preserve where it came from.

Core origins include:

```text
external
internal
derived
audit
recovery
```

---

## 3.3 Questions May Derive Questions

AI systems may generate new questions from existing questions.

Examples include:

```text
clarification
verification
decomposition
audit
recovery
```

Derived questions SHOULD preserve lineage where possible.

---

## 3.4 Routed Questions Must Remain Traceable

When a question moves across agents, systems, or roles, the system SHOULD preserve enough information to reconstruct its route and lineage.

---

## 3.5 Unresolved Is a Valid State

Q Network does not require every question to be answered.

A question MAY remain:

```text
unresolved
held
rejected
expired
```

without being converted into a fabricated answer.

---

# 4. Q Network Core

## v0.1 — Question Envelope

Version 0.1 defines the basic Question Envelope.

It answers:

> What is this question?

A Question Envelope may include:

```text
question_id
created_at
question_origin
question_type
intent
domain
risk_level
authority
status
context
parent_question_id
derived_from
assigned_to
trace_parent
```

Core question types include:

```text
request
subquestion
verification
clarification
decision
recovery
```

Core statuses include:

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

The key invariant remains:

> Question is not authority.

---

## v0.2 — Question Provenance

Version 0.2 records why a question emerged.

It answers:

> Why did this question arise?

A provenance record may describe:

```text
trigger_event
generated_by
generation_reason
source_question_id
source_intent
interpreted_intent
authority_context_ref
provenance_trace
```

Typical generation reasons include:

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

Question Provenance makes it possible to distinguish:

```text
Original Request
↓
Interpretation
↓
Derived Question
```

without requiring token-level reasoning disclosure.

---

# 5. Private Reasoning Is Not Question Provenance

Q Network does not require hidden chain-of-thought.

The protocol records externally useful transitions such as:

```text
source question
↓
interpreted intent
↓
derived question
```

This distinction is important:

> Private reasoning is internal. Provenance is externally reviewable transition metadata.

---

# 6. v0.3 — Question Graph

Version 0.3 connects questions into a graph.

It answers:

> How is this question connected to other questions?

A Question Graph contains:

```text
graph_id
nodes
edges
graph_status
```

Core relationship types include:

```text
derived
decomposed_into
interpreted_as
clarified_by
verified_by
audited_by
recovered_by
routed_to
superseded_by
unresolved_into
```

Example:

```text
Q0
├─ Q1
├─ Q2
└─ Q3
```

A Question Graph is not restricted to a tree.

It MAY contain:

- multiple roots;
- multiple branches;
- merge points;
- audit branches;
- recovery branches;
- unresolved branches.

Semantic lineage cycles are not permitted in the minimal model.

---

# 7. v0.4 — Question Drift

Version 0.4 records what changed as a question moved through the network.

It answers:

> What changed between related questions?

A Question Drift Record may contain explicit signals such as:

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

Example:

```text
Q1
"Assess system safety"

↓ interpretation

Q2
"Determine whether external access is required"

↓ execution-oriented transition

Q3
"Attempt external access"
```

Possible drift signals:

```text
intent_changed
risk_increased
authority_changed
```

Question Drift is observational.

It does not authorize or prohibit actions by itself.

---

# 8. Drift Is Not Authority

A Drift Record MAY recommend review.

It MUST NOT:

```text
grant authority
revoke authority
execute an action
override policy
assign blame
```

A review state may be:

```text
none
observe
review_recommended
hold_recommended
human_review_required
```

but any actual authority requirement MUST come from an external authority or policy system.

---

# 9. v0.5 — Incident Backtrace

Version 0.5 introduces reverse investigation.

It answers:

> After an incident, how do we trace the lineage backward?

A forward path may look like:

```text
Human Intent
↓
Q0
↓
Q1
↓
Plan
↓
Action
↓
Incident
```

Incident Backtrace reverses the direction:

```text
Incident
↑
Action
↑
Plan
↑
Q1
↑
Q0
↑
Human Intent
```

The purpose is not automatic blame assignment.

The purpose is evidence-preserving reconstruction.

---

# 10. Backtrace Principles

Incident Backtrace follows three important principles.

## Trace backward before assigning cause

An incident is the end of a path.

The path SHOULD be reconstructed before causal conclusions are made.

## Missing evidence must remain missing

If the history is incomplete:

```text
Incident
↑
Action
↑
Q7
↑
?
```

the system SHOULD record:

```text
status = partial
```

rather than inventing the missing step.

## Inconclusive is valid

Conflicting evidence MAY result in:

```text
status = inconclusive
```

The protocol does not force certainty where certainty does not exist.

---

# 11. Incident Backtrace Status

Core statuses include:

```text
open
partial
reconstructed
closed
inconclusive
invalid
```

Backtrace steps may include:

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

Candidate investigative flags include:

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

These are investigative markers.

They are not final causes.

---

# 12. Human Attribution Boundary

Q Network follows this model:

```text
AI / tooling
→ reconstruct evidence

Human / authorized review
→ evaluate evidence

Governance process
→ determine final attribution
```

Q Network does not require an AI system to assign final guilt, responsibility, or liability.

---

# 13. v0.6 — Question Structural Perturbation

Version 0.6 introduces **Question Structural Perturbation**.

Conceptually, this may be represented as:

```text
Qψ
```

It answers:

> What assumptions, questions, or structures changed because this question existed?

Qψ is not a score for how intelligent or creative a question is.

It represents observable structural effect.

---

# 14. From Question to Structural Change

A normal question flow may be:

```text
Question
↓
Routing
↓
Answer / Action
↓
Trace
```

A structurally significant question may instead produce:

```text
Question
↓
Structural Perturbation
↓
Assumption Shift
↓
New Questions
↓
New Structure
↓
Trace
```

This treats the question as a possible source of structural change.

---

# 15. Qψ Signals

Core Question Structural Perturbation signals include:

```text
assumption_changed
problem_frame_changed
design_target_changed
reversal_detected
new_questions_generated
new_structure_generated
```

Additional observations may include:

```text
affected_assumptions
generated_question_count
downstream_question_refs
downstream_structure_refs
```

---

# 16. Qψ Classification

Core classifications are:

```text
low
moderate
high
structural
```

These are not rankings of question quality.

They represent observed structural significance.

For example:

```text
low
→ minor effect

moderate
→ assumption or framing adjustment

high
→ substantial downstream change

structural
→ identifiable structural branching point
```

---

# 17. High Qψ Must Never Imply High Authority

This is a mandatory Q Network invariant.

```text
High Qψ
≠ High Authority
≠ Permission
≠ Execution Right
```

A structurally significant question MAY:

```text
change interpretation
generate hypotheses
create new questions
propose redesign
trigger structural review
```

It MUST NOT automatically:

```text
expand privilege
approve execution
override policy
bypass review
```

---

# 18. High Structural Impact Means More Review, Not More Privilege

A high-impact question may follow:

```text
High / Structural Qψ
↓
Structural Review
↓
Alternative Interpretation
↓
Independent Review
↓
Human Review where required
↓
Possible Structural Revision
```

The greater the structural effect, the more carefully the change SHOULD be reviewed.

---

# 19. Q Network Lifecycle

The complete initial lifecycle is:

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
        ↓
Question Structural Perturbation
```

Or conceptually:

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

# 20. Example Lifecycle

A simple example may look like:

```text
Human:
"How can AI safety be improved?"

↓ Q0

Q1:
"Should stronger prevention be used?"

↓ interpretation / perturbation

Q2:
"Why must prevention be the primary strategy?"

↓ Qψ = structural

Assumption Shift:
Prevention-only
↓
Recovery + Resilience

↓ new questions

Q3:
"How should recovery paths work?"

Q4:
"Can AI safety operate like an immune system?"

↓ new structures

Recovery-First Model
Structural Immunity Model
```

Q Network can preserve the lineage from the original question to the resulting structure.

---

# 21. Repository Structure

A typical repository layout is:

```text
.
├── README.md
├── PRINCIPLES.md
├── CHANGELOG.md
├── requirements.txt
│
├── specs/
│   ├── q-network-v0.2.md
│   ├── q-network-v0.3.md
│   ├── q-network-v0.4.md
│   ├── q-network-v0.5.md
│   └── q-network-v0.6.md
│
├── schemas/
│   ├── question-envelope-v0.1.schema.json
│   ├── question-envelope-v0.2.schema.json
│   ├── question-graph-v0.3.schema.json
│   ├── question-drift-v0.4.schema.json
│   ├── incident-backtrace-v0.5.schema.json
│   └── question-structural-perturbation-v0.6.schema.json
│
├── examples/
│   ├── v0.1/
│   │   ├── pass/
│   │   └── fail/
│   ├── v0.2/
│   │   ├── pass/
│   │   └── fail/
│   ├── v0.3/
│   │   ├── pass/
│   │   └── fail/
│   ├── v0.4/
│   │   ├── pass/
│   │   └── fail/
│   ├── v0.5/
│   │   ├── pass/
│   │   └── fail/
│   └── v0.6/
│       ├── pass/
│       └── fail/
│
├── scripts/
│   └── validate_examples.py
│
└── .github/
    └── workflows/
        └── validate.yml
```

---

# 22. Validation Model

Q Network separates validation into two layers.

## JSON Schema Validation

Schemas validate structural properties such as:

```text
required fields
types
enum values
identifier formats
array constraints
basic object structure
```

## Semantic Validation

The validator checks relationships that are difficult or undesirable to encode directly in JSON Schema.

Examples include:

```text
self-reference
duplicate identifiers
graph cycles
missing graph endpoints
contradictory drift signals
start-reference mismatch
non-contiguous backtrace sequence
QSP signal/reference inconsistency
```

This creates a clear separation:

```text
Schema
= Is the object structurally valid?

Semantic Validator
= Do the relationships make sense?
```

---

# 23. Running Validation

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run validation:

```bash
python scripts/validate_examples.py
```

The validator checks all PASS and FAIL examples across supported protocol versions.

A successful run ends with:

```text
[validation-passed]
```

---

# 24. GitHub Actions

Validation may be run automatically through:

```text
.github/workflows/validate.yml
```

The workflow validates the repository on events such as:

```text
push
pull_request
workflow_dispatch
```

The test matrix may include multiple supported Python versions.

---

# 25. PASS and FAIL Examples

Each protocol version contains both positive and negative examples.

Example structure:

```text
examples/v0.4/pass/
examples/v0.4/fail/
```

PASS examples demonstrate valid protocol objects.

FAIL examples intentionally violate either:

```text
Schema rules
```

or:

```text
Semantic rules
```

This makes the protocol executable as a conformance specification rather than only descriptive documentation.

---

# 26. Design Philosophy

Q Network follows several design preferences.

## Prefer explicit structure

Observable fields are preferred over hidden interpretation.

## Prefer references over copied state

External authority, Trace, Receipt, and other systems SHOULD be referenced instead of duplicated where practical.

## Prefer unresolved states over fabricated certainty

The protocol permits:

```text
unresolved
partial
inconclusive
```

when evidence is insufficient.

## Prefer review over automatic escalation

Greater semantic or structural impact SHOULD increase scrutiny rather than privilege.

## Prefer append-oriented history

Historical observations SHOULD not be silently rewritten.

---

# 27. Security Considerations

Q Network implementations SHOULD consider:

- forged provenance;
- fake question lineage;
- manipulated graphs;
- fabricated drift;
- missing audit branches;
- false authority references;
- artificial Qψ inflation;
- fabricated downstream structures;
- deleted Trace records;
- evidence conflicts;
- malicious routing;
- blame laundering.

Protocol records SHOULD be treated as evidence requiring verification.

---

# 28. Privacy Considerations

Q Network does not require unrestricted reasoning logs.

Implementations SHOULD minimize unnecessary disclosure of:

- hidden chain-of-thought;
- private prompts;
- credentials;
- personal information;
- confidential infrastructure;
- proprietary strategy;
- unrelated historical context.

The protocol focuses on externally reviewable structural transitions.

---

# 29. Non-Goals

Q Network Core does not define:

- universal reasoning transparency;
- chain-of-thought disclosure;
- automatic blame assignment;
- legal liability;
- universal authority systems;
- automatic execution permission;
- universal question quality scores;
- creativity rankings;
- intelligence rankings;
- economic rewards;
- idea ownership;
- copyright ownership;
- patent priority.

These may be handled by separate systems or future extension protocols.

---

# 30. Relationship to Authority Systems

Q Network may reference authority information.

It does not replace an authority system.

The relationship is:

```text
Question
↓
Interpretation
↓
Authority Check
↓
Authorized Action
```

not:

```text
Question
↓
Automatic Authority
```

---

# 31. Relationship to Trace and Receipts

Q Network is designed to interoperate with Trace and Receipt systems.

A full lifecycle may look like:

```text
Question
↓
Provenance
↓
Graph
↓
Drift
↓
Authority
↓
Action
↓
Receipt
↓
Incident Backtrace
↓
Structural Perturbation
```

Q Network does not require one specific Trace implementation.

---

# 32. Relationship to Multi-Agent Systems

Q Network is especially useful where:

- multiple AI agents cooperate;
- questions are decomposed;
- questions are rerouted;
- different models independently review work;
- authority is separated from reasoning;
- recovery agents create new questions;
- audit agents inspect plans;
- question lineage matters after incidents.

The protocol can be used without requiring a central controller.

---

# 33. Q Network as a Question Lifecycle Protocol

The central perspective of Q Network is:

> A question has a lifecycle.

A question may be:

```text
created
↓
interpreted
↓
derived
↓
routed
↓
answered
↓
held
↓
audited
↓
recovered
↓
traced
↓
structurally significant
```

Tracking this lifecycle makes AI systems easier to inspect without requiring direct access to every internal reasoning step.

---

# 34. Q Network Core Boundary

Version 0.6 marks a natural boundary for the initial Q Network Core.

The core now covers:

```text
Creation
Origin
Relationship
Change
Investigation
Structural Effect
```

Future work SHOULD generally build on this core rather than indefinitely expanding the same lifecycle.

Possible extension areas include:

```text
Question-to-Structure Lineage
Structural Emergence
Question Contribution
Attribution
Reward
Inter-Network Question Circulation
```

These may become separate specifications where appropriate.

---

# 35. Protocol Summary

| Version | Component | Main Question |
|---|---|---|
| v0.1 | Question Envelope | What is this question? |
| v0.2 | Question Provenance | Why did this question arise? |
| v0.3 | Question Graph | How is it connected to other questions? |
| v0.4 | Question Drift | What changed as it moved? |
| v0.5 | Incident Backtrace | How do we trace backward after an incident? |
| v0.6 | Question Structural Perturbation | What structure changed because this question existed? |

---

# 36. Core Statements

Q Network treats questions as traceable objects rather than disposable prompts.

Its authority invariant is:

> Questions may move between intelligences, but authority does not move merely because the question moves.

Its uncertainty invariant is:

> A question is allowed to remain a question.

Its investigation invariant is:

> Trace backward before assigning cause.

Its evidence invariant is:

> Missing evidence must remain missing.

Its structural invariant is:

> A question may change structure without gaining authority.

Its Qψ invariant is:

> High Qψ must never imply High Authority.

Its measurement principle is:

> Prefer explicit structural signals over universal question scores.

And its conceptual statement is:

> An answer-changing question is useful.  
> An assumption-changing question is strong.  
> When a question changes structure and generates new questions, the wind has moved.

---

# 37. Status

Q Network Protocol Core currently includes:

```text
v0.1
v0.2
v0.3
v0.4
v0.5
v0.6
```

JSON Schemas, PASS/FAIL examples, semantic validation, and automated validation are provided for the supported versions.

The v0.1–v0.6 series represents the first complete Q Network Core lifecycle.
