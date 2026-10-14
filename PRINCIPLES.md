# Q Network Protocol — Principles

Version: 0.1.0

## Overview

Q Network Protocol defines a minimal structure for representing, deriving, routing, and tracing questions across AI agents, models, and human participants.

The protocol does not assume that every question must produce an answer.

It also does not treat a question as permission to act.

The purpose of v0.1 is to establish a small set of invariants that allow questions to move through heterogeneous AI systems without losing origin, derivation, status, or authority boundaries.

---

## Principle 1 — Question Is Not Authority

A question, request, instruction, or derived subquestion MUST NOT be interpreted as execution authority by itself.

A Question Envelope MAY express an intent to perform an action, but execution permission MUST be established through a separate authority mechanism.

```text
Question
   ↓
Interpretation / Planning
   ↓
Authority Check
   ↓
Execution
```

The existence of a question MUST NOT imply:

- permission to access a resource;
- permission to modify a resource;
- permission to invoke a privileged tool;
- permission to delegate authority;
- permission to increase privileges.

Q Network separates:

```text
"What should be done?"
```

from:

```text
"May it be done?"
```

---

## Principle 2 — Every Question Has Origin

Every Question Envelope MUST identify how the question entered the network.

The minimum supported origins in v0.1 are:

```text
external
internal
derived
audit
recovery
```

### external

A question originating from outside the current AI reasoning process.

Examples include:

- a human request;
- another system;
- another organization;
- an external AI agent.

### internal

A self-generated question used by an AI system to inspect or reconsider its own planned behavior.

Example:

```text
"Do I actually have permission to delete this file?"
```

### derived

A question produced by decomposing or transforming another question.

Example:

```text
Parent:
"Plan this trip."

Derived:
"What transportation options are available?"
```

### audit

A question generated for verification, challenge, or independent review.

Example:

```text
"Is the evidence supporting this action still valid?"
```

### recovery

A question generated while attempting to recover from a failure, interruption, unsafe state, or unresolved operation.

Example:

```text
"Can this operation be safely resumed?"
```

Origin MUST remain traceable even after the question is routed to another participant.

---

## Principle 3 — Questions May Derive Questions

A question MAY produce one or more additional questions.

Q Network therefore treats decomposition as a first-class operation.

Example:

```text
Q0: "Deploy the service safely."
│
├── Q1: "Has the build passed?"
├── Q2: "Is production authorization valid?"
├── Q3: "What is the rollback path?"
└── Q4: "Has human approval been recorded?"
```

A derived question SHOULD reference its parent question.

At minimum, implementations SHOULD support:

```text
parent_question_id
derived_from
```

Question derivation MUST NOT erase the origin of the original question.

A derived question MUST NOT inherit authority automatically from its parent.

---

## Principle 4 — Every Routed Question Is Traceable

A question transferred between participants MUST retain enough information to reconstruct its path through the network.

An implementation SHOULD be able to determine:

- where the question originated;
- which question produced it;
- which participant received it;
- what status it entered;
- whether it produced an answer, action, or further question.

A minimal trace path may take the form:

```text
question_id
    ↓
agent_id
    ↓
answer_id
    ↓
action_id
    ↓
result_id
```

Not every question will produce every downstream object.

Traceability MUST NOT require unrestricted access to the internal reasoning state of an AI system.

Q Network prefers shared external traces over full internal-state sharing.

---

## Principle 5 — Unresolved Is a Valid State

A question MUST NOT be forced into an answer when sufficient evidence, authority, capability, or confidence is unavailable.

The following outcomes are valid:

```text
ANSWERED
HELD
REJECTED
EXPIRED
UNRESOLVED
```

An implementation MAY support additional states, provided their meaning is explicitly defined.

`UNRESOLVED` means that the system was unable to produce a justified resolution.

It MUST NOT be interpreted as protocol failure.

Examples include:

- insufficient evidence;
- conflicting evidence;
- unavailable specialist capability;
- missing authority;
- unresolved ambiguity;
- unavailable external dependency.

Q Network explicitly permits a system to preserve a question without inventing an answer.

---

# Supporting Invariants

## Question Identity Must Be Stable

Every Question Envelope MUST contain a stable `question_id`.

A question MUST NOT silently receive a new identity merely because it was routed to another participant.

If the semantic question materially changes, a new derived question SHOULD be created instead.

---

## Derivation Must Be Explicit

Implementations MUST NOT silently rewrite a question into a substantially different question without preserving the derivation relationship.

When transformation changes scope, intent, risk, or authority requirements, the resulting question SHOULD be represented as a new Question Envelope.

---

## Authority Must Not Propagate Implicitly

Authority attached to one operation, participant, or question MUST NOT automatically propagate to derived questions.

Example:

```text
Q0:
"Read the deployment log."

Authorized:
read-only access

Q1:
"Restart the production service."
```

The authority associated with Q0 MUST NOT authorize Q1.

---

## Status Must Be Explicit

Every active Question Envelope MUST contain a status.

The minimum v0.1 lifecycle is:

```text
CREATED
   ↓
ROUTED
   ↓
ACCEPTED
   ↓
IN_PROGRESS
   ↓
ANSWERED
```

Alternative terminal or suspended states include:

```text
HELD
REJECTED
EXPIRED
UNRESOLVED
```

Transitions SHOULD be recorded when practical.

---

## Routing Must Not Rewrite Origin

A router MAY change:

- assignment;
- destination;
- priority;
- routing metadata.

A router MUST NOT rewrite:

- original question identity;
- question origin;
- derivation history;

unless a new derived Question Envelope is created.

---

# Non-Goals of v0.1

Q Network Protocol v0.1 does not define:

- agent markets;
- monetary rewards;
- royalty distribution;
- contribution weighting;
- semantic reputation systems;
- model selection economics;
- settlement protocols;
- autonomous execution authority;
- global orchestration;
- mandatory reasoning methods.

These concerns may be mapped to Q Network through separate specifications.

---

# Design Philosophy

Q Network is based on a simple idea:

> AI systems do not need to be directly fused together in order to cooperate.

They can instead share structured questions.

A question can be:

- created;
- derived;
- routed;
- challenged;
- held;
- answered;
- left unresolved;
- transformed into another question.

This allows heterogeneous systems to cooperate without requiring identical models, shared internal state, or centralized control.

The protocol therefore treats the question as a portable coordination object.

---

# Core Statement

> Questions may move between intelligences, but authority does not move merely because the question moves.

And:

> A question is allowed to remain a question.
