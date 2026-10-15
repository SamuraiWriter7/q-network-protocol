# Q Network Protocol v0.3 — Question Graph

Version: 0.3.0

## 1. Purpose

Q Network Protocol v0.3 introduces a minimal Question Graph model.

Version 0.1 defined the Question Envelope.

Version 0.2 added Question Provenance.

Version 0.3 defines how multiple Question Envelopes MAY be connected into an explicit graph that preserves:

- parent-child relationships;
- semantic derivation;
- provenance links;
- routing relationships;
- audit branches;
- recovery branches;
- unresolved branches;
- terminal outcomes.

The purpose of v0.3 is not to create a global knowledge graph.

Its purpose is to make question lineage reconstructable.

---

## 2. Core Principle

The primary invariant of v0.3 is:

> Questions MAY form graphs, but graph structure MUST NOT erase individual question identity.

Each question remains independently identifiable.

The graph describes relationships between Question Envelopes.

It does not replace them.

---

## 3. Conceptual Model

A simple Question Graph may look like:

```text
Q0
├── Q1
│   ├── Q1.1
│   └── Q1.2
├── Q2
└── Q3
```

But Q Network does not assume all structures are strict trees.

A question MAY be related to multiple prior questions.

Example:

```text
Q1 ─────┐
        ├── Q4
Q2 ─────┘
```

Therefore v0.3 uses a graph model rather than a tree-only model.

---

## 4. Graph Components

A minimal Question Graph contains:

```text
nodes
edges
graph_id
created_at
```

Canonical example:

```yaml
schema_version: "0.3.0"

graph_id: "qgraph-001"
created_at: "2026-10-15T02:10:00Z"

nodes:
  - "q-001"
  - "q-002"
  - "q-003"

edges:
  - edge_id: "qe-001"
    from_question_id: "q-001"
    to_question_id: "q-002"
    relation: "derived"

  - edge_id: "qe-002"
    from_question_id: "q-001"
    to_question_id: "q-003"
    relation: "audit"
```

---

## 5. graph_id

`graph_id` uniquely identifies a Question Graph record.

Requirements:

- MUST be non-empty;
- MUST remain stable for the graph record;
- SHOULD be unique within the applicable namespace.

A graph MAY evolve over time.

Graph evolution MUST NOT silently change the identity of previously recorded questions.

---

## 6. nodes

`nodes` contains identifiers of Question Envelopes participating in the graph.

Example:

```yaml
nodes:
  - "q-root-001"
  - "q-derived-001"
  - "q-audit-001"
```

Requirements:

- MUST contain at least one question identifier;
- MUST NOT contain duplicate identifiers;
- each referenced question SHOULD exist or be resolvable externally.

The graph does not require embedding full Question Envelopes.

---

## 7. edges

`edges` describes relationships between questions.

Each edge MUST contain:

```text
edge_id
from_question_id
to_question_id
relation
```

Example:

```yaml
edge_id: "qe-001"
from_question_id: "q-001"
to_question_id: "q-002"
relation: "derived"
```

---

## 8. Edge Relations

v0.3 defines the following core relation types:

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

### derived

The destination question was derived from the source question.

### decomposed_into

The source question was decomposed into the destination subquestion.

### interpreted_as

The destination represents an interpretation or reformulation of the source.

### clarified_by

The destination question exists to clarify the source.

### verified_by

The destination question exists to verify a claim, condition, or premise from the source.

### audited_by

The destination question was generated as an audit branch.

### recovered_by

The destination question was generated as part of recovery.

### routed_to

The destination represents a routing-related continuation where a new Question Envelope was intentionally created.

Simple transport routing does not require a new graph edge.

### superseded_by

The destination question replaces the source as the active formulation.

### unresolved_into

The destination question was generated because the source remained unresolved.

---

## 9. Edge Direction

Edges MUST be directional.

The direction SHOULD represent causal or semantic flow.

Example:

```text
Q0
  ↓ derived
Q1
```

means:

> Q1 was derived from Q0.

It MUST NOT be interpreted as:

> Q0 was derived from Q1.

---

## 10. No Self Edges

A question MUST NOT create an edge to itself.

Invalid:

```text
Q1 → Q1
```

Therefore:

```text
from_question_id
!=
to_question_id
```

for every edge.

This is a semantic invariant.

---

## 11. No Duplicate Edge Identity

Each `edge_id` MUST be unique within a Question Graph.

Two edges MAY connect the same pair of questions only if they represent materially different relationships and use different `edge_id` values.

Example:

```text
Q1 ──derived────→ Q2
Q1 ──audited_by─→ Q2
```

is unusual but MAY be valid if both relationships are intentionally recorded.

---

## 12. Graph Nodes Must Cover Edge Endpoints

Every `from_question_id` and `to_question_id` referenced by an edge MUST appear in `nodes`.

Invalid:

```text
nodes:
  - q-001

edge:
  q-001 → q-999
```

if `q-999` is absent from `nodes`.

---

## 13. Parent-Child Compatibility

When Question Envelopes contain:

```text
parent_question_id
derived_from
provenance.source_question_id
```

the Question Graph SHOULD remain compatible with those relationships.

Example:

```text
Q2.parent_question_id = Q1
```

SHOULD normally correspond to an edge such as:

```text
Q1 → Q2
relation = decomposed_into
```

or:

```text
Q1 → Q2
relation = derived
```

Contradictory graph relationships SHOULD be treated as suspicious or invalid according to implementation policy.

---

## 14. Provenance Compatibility

If v0.2 records:

```text
Q2.provenance.source_question_id = Q1
```

the graph SHOULD be able to represent that relation.

Example:

```text
Q1
  ↓ interpreted_as
Q2
```

The exact relation depends on the recorded generation reason.

---

## 15. Generation Reason Mapping

Recommended mappings include:

```text
generation_reason: interpretation
→ interpreted_as

generation_reason: decomposition
→ decomposed_into

generation_reason: clarification
→ clarified_by

generation_reason: verification
→ verified_by

generation_reason: audit
→ audited_by

generation_reason: recovery
→ recovered_by
```

These mappings are RECOMMENDED but not mandatory when an implementation has a justified alternative.

---

## 16. Graph Roots

A Question Graph MAY contain one or more roots.

A root is a question with no incoming graph edge within the current graph scope.

Example:

```text
Q0
├── Q1
└── Q2
```

Q0 is a root.

Multiple roots are valid when a graph joins previously independent question lineages.

Example:

```text
Q0 ─┐
    ├── Q3
Q1 ─┘
```

Both Q0 and Q1 may be roots.

---

## 17. Graph Leaves

A leaf is a question with no outgoing graph edge within the current graph scope.

Leaves MAY represent:

- answered questions;
- unresolved questions;
- rejected questions;
- expired questions;
- terminal audit results;
- pending questions.

A leaf is not automatically a failure.

---

## 18. Cycles

v0.3 distinguishes between:

```text
semantic lineage cycles
```

and:

```text
operational reconsideration
```

A direct semantic derivation cycle SHOULD be prohibited.

Example:

```text
Q1 → Q2 → Q1
```

is invalid if both edges mean semantic derivation.

However, an implementation MAY revisit an earlier topic by creating a new Question Envelope.

Example:

```text
Q1
↓
Q2
↓
Q3
↓
Q4
```

where Q4 asks a question semantically similar to Q1.

This is not a cycle if Q4 has a new identity.

---

## 19. Why New Identity Matters

Q Network does not model repeated thinking by mutating old questions indefinitely.

Instead:

```text
old question
↓ reconsideration
new question
```

This preserves history.

Example:

```text
Q1:
"Is deployment authorized?"

↓ authority expired

Q5:
"Is deployment still authorized under the current authority state?"
```

Q5 SHOULD be a new node.

---

## 20. Question Branches

A graph MAY branch.

Example:

```text
Q0
├── Q1 planning
├── Q2 authority
├── Q3 audit
└── Q4 recovery
```

Branches MAY progress independently.

A blocked branch MUST NOT automatically block unrelated branches unless external policy requires it.

---

## 21. Audit Branches

Audit questions SHOULD appear explicitly as graph branches.

Example:

```text
Q0
├── Q1 execution planning
└── Q2 audit
```

This makes it possible to reconstruct whether an audit path existed before an action occurred.

---

## 22. Authority Branches

Authority checks MAY be represented as question branches.

Example:

```text
Q0: "Delete the file"
│
├── Q1: "Which file?"
│
└── Q2: "Is deletion authorized?"
```

The existence of Q2 does not grant execution authority.

Graph representation MUST preserve the invariant:

> Question Graph ≠ Authority Graph.

---

## 23. Recovery Branches

Recovery questions SHOULD preserve their relationship to the question or operation that triggered recovery.

Example:

```text
Q1
↓ action failure
Q2 recovery question
```

Graph relation:

```text
Q1
  ↓ recovered_by
Q2
```

Expired or revoked authority MUST NOT automatically propagate along this edge.

---

## 24. Unresolved Branches

An unresolved question MAY generate a new question.

Example:

```text
Q1
status = unresolved
        ↓
Q2
"What additional evidence is required?"
```

Recommended relation:

```text
unresolved_into
```

This preserves uncertainty instead of overwriting it.

---

## 25. Graph Status

A Question Graph MAY carry a graph-level status.

Recommended values:

```text
open
stable
closed
partial
invalid
```

### open

The graph may continue to receive nodes or edges.

### stable

The current graph is internally consistent but may still evolve.

### closed

The graph is considered complete for the current task or incident scope.

### partial

The graph is known to be incomplete.

### invalid

The graph violates required structural or semantic invariants.

Graph status does not replace individual question status.

---

## 26. Question Graph Object

Canonical v0.3 structure:

```yaml
schema_version: "0.3.0"

graph_id: "qgraph-001"
created_at: "2026-10-15T02:20:00Z"

graph_status: "open"

nodes:
  - "q-root-001"
  - "q-derived-001"
  - "q-audit-001"

edges:
  - edge_id: "qe-001"
    from_question_id: "q-root-001"
    to_question_id: "q-derived-001"
    relation: "decomposed_into"

  - edge_id: "qe-002"
    from_question_id: "q-root-001"
    to_question_id: "q-audit-001"
    relation: "audited_by"
```

---

## 27. Minimal Graph

A valid graph MAY contain a single node and no edges.

Example:

```yaml
schema_version: "0.3.0"

graph_id: "qgraph-single-001"
created_at: "2026-10-15T02:21:00Z"

graph_status: "open"

nodes:
  - "q-001"

edges: []
```

This represents a question lineage that has not yet branched or derived further questions.

---

## 28. Multi-Source Questions

A new question MAY emerge from multiple source questions.

Example:

```text
Q1 ─┐
    ├── Q3
Q2 ─┘
```

Q3 may integrate evidence or ambiguity from both Q1 and Q2.

The graph MAY represent this using multiple incoming edges.

Example:

```text
Q1 → Q3
Q2 → Q3
```

This is one reason v0.3 uses a graph rather than a strict tree.

---

## 29. Merge Questions

A question MAY act as a convergence point.

Example:

```text
Q1 analysis
Q2 audit
Q3 authority
   \ | /
    Q4
```

Q4 may ask:

> "Given analysis, audit, and authority state, should processing continue?"

The merged question remains subject to its own authority and provenance requirements.

---

## 30. Graph and Routing

Routing events SHOULD NOT create graph nodes merely because a question changed destination.

Example:

```text
Q1
Agent A → Agent B
```

If the semantic question is unchanged:

```text
same Question Envelope
same graph node
```

should normally be preserved.

A new node SHOULD be created only when the question itself materially changes.

---

## 31. Graph and Answers

v0.3 does not define an Answer Graph.

A question node MAY later link to:

- answer records;
- action records;
- trace records;
- receipts;
- incident records.

These external mappings are outside the core v0.3 graph.

---

## 32. Graph and Incident Reconstruction

Question Graph is designed to support future incident backtrace.

Example:

```text
Q0 Human Intent
│
└── Q1 Interpretation
     │
     └── Q2 Decomposition
          │
          ├── Q3 Audit
          │
          └── Q4 Execution-related Question
               │
               └── Incident
```

An investigator may traverse:

```text
Incident
↑
Q4
↑
Q2
↑
Q1
↑
Q0
```

Question Graph provides lineage.

It does not itself assign causal blame.

---

## 33. Graph Visualization

Implementations MAY visualize a Question Graph.

Recommended visual indicators include:

```text
origin
relation
risk level
question status
authority-required state
audit branches
recovery branches
unresolved branches
```

Example:

```text
Q0 external
│
├─ Q1 derived
│
│  └─ Q3 audit
│
└─ Q2 derived
   └─ Q4 unresolved
```

Visualization is optional and not part of schema conformance.

---

## 34. Semantic Drift Compatibility

v0.3 does not define Question Drift scoring.

However, the graph SHOULD preserve enough structure for future drift analysis.

Potential future analysis may examine:

```text
Q0 → Q1 → Q2 → Q3
```

and compare:

- intent changes;
- domain changes;
- risk changes;
- authority requirements;
- interpretation transitions;
- graph depth.

This is reserved for a future version.

---

## 35. Graph Depth

Implementations MAY calculate graph depth.

Depth MAY be useful for:

- detecting runaway decomposition;
- identifying long reasoning chains;
- triggering human review;
- resource control.

v0.3 does not prescribe a maximum depth.

---

## 36. Branching Factor

Implementations MAY calculate branching factor.

An unusually high branching factor MAY indicate:

- over-decomposition;
- uncertainty explosion;
- excessive routing;
- broad search behavior.

However, a high branching factor is not automatically invalid.

---

## 37. Graph Integrity

A conforming Question Graph MUST satisfy:

```text
every edge endpoint exists in nodes

from_question_id != to_question_id

edge_id values are unique

node identifiers are unique
```

The graph SHOULD also avoid contradictory lineage.

---

## 38. Referential Integrity

Question Graph references Question Envelope identifiers.

A graph implementation SHOULD be able to resolve those identifiers when full reconstruction is required.

If some referenced questions are unavailable, the graph SHOULD be marked or treated as partial.

---

## 39. Partial Graphs

Partial graphs are valid when not all lineage records are available.

Example reasons:

- external organization boundary;
- unavailable historical trace;
- privacy boundary;
- deleted non-required context;
- incomplete incident evidence.

A partial graph MUST NOT falsely claim completeness.

---

## 40. Graph Mutation

Graphs MAY evolve as questions are generated.

Implementations SHOULD prefer append-oriented updates.

New nodes and edges may be added.

Previously relied-upon lineage SHOULD NOT be silently rewritten.

Corrections SHOULD be explicit.

---

## 41. Graph Corrections

If an edge was recorded incorrectly, implementations SHOULD preserve an auditable correction.

Possible approaches include:

```text
edge status
superseding edge
correction event
trace amendment
```

v0.3 does not define a mandatory correction format.

---

## 42. Security Considerations

Implementations SHOULD consider:

- forged graph edges;
- fabricated parent relationships;
- hidden audit branches;
- omitted authority questions;
- graph truncation;
- false provenance merging;
- deliberate self-reinforcing cycles;
- malicious over-expansion.

Graph structure SHOULD be treated as evidence, not unquestioned truth.

---

## 43. Privacy Considerations

Question Graphs MAY reveal sensitive operational relationships.

Implementations SHOULD avoid unnecessary exposure of:

- private internal reasoning;
- personal data;
- confidential prompts;
- credentials;
- secret infrastructure identifiers.

The graph should preserve causal structure without requiring unrestricted reasoning disclosure.

---

## 44. Validation Invariants

A conforming v0.3 Question Graph MUST satisfy:

### Graph Identity

```text
graph_id exists
graph_id is non-empty
```

### Nodes

```text
nodes contains at least one identifier
nodes contains no duplicates
```

### Edges

```text
each edge has edge_id
each edge has from_question_id
each edge has to_question_id
each edge has relation
```

### Endpoint Integrity

```text
from_question_id in nodes
to_question_id in nodes
```

### Self Edge

```text
from_question_id != to_question_id
```

### Edge Identity

```text
edge_id values are unique
```

---

## 45. Example — Decomposition Graph

```yaml
schema_version: "0.3.0"

graph_id: "qgraph-decomposition-001"
created_at: "2026-10-15T02:25:00Z"

graph_status: "stable"

nodes:
  - "q-trip-001"
  - "q-transport-001"
  - "q-hotel-001"
  - "q-budget-001"

edges:
  - edge_id: "qe-trip-001"
    from_question_id: "q-trip-001"
    to_question_id: "q-transport-001"
    relation: "decomposed_into"

  - edge_id: "qe-trip-002"
    from_question_id: "q-trip-001"
    to_question_id: "q-hotel-001"
    relation: "decomposed_into"

  - edge_id: "qe-trip-003"
    from_question_id: "q-trip-001"
    to_question_id: "q-budget-001"
    relation: "decomposed_into"
```

---

## 46. Example — Audit Branch

```text
Q0
├── Q1 planning
└── Q2 audit
```

Graph:

```yaml
nodes:
  - "q-000"
  - "q-plan-001"
  - "q-audit-001"

edges:
  - edge_id: "qe-001"
    from_question_id: "q-000"
    to_question_id: "q-plan-001"
    relation: "decomposed_into"

  - edge_id: "qe-002"
    from_question_id: "q-000"
    to_question_id: "q-audit-001"
    relation: "audited_by"
```

---

## 47. Invalid Example — Self Edge

```yaml
edge_id: "qe-invalid-001"
from_question_id: "q-001"
to_question_id: "q-001"
relation: "derived"
```

Invalid.

---

## 48. Invalid Example — Missing Node

```yaml
nodes:
  - "q-001"

edges:
  - edge_id: "qe-invalid-002"
    from_question_id: "q-001"
    to_question_id: "q-999"
    relation: "derived"
```

Invalid because `q-999` is not in `nodes`.

---

## 49. Invalid Example — Duplicate Edge Identity

```yaml
edges:
  - edge_id: "qe-001"
    from_question_id: "q-001"
    to_question_id: "q-002"
    relation: "derived"

  - edge_id: "qe-001"
    from_question_id: "q-001"
    to_question_id: "q-003"
    relation: "audit"
```

Invalid.

---

## 50. Relationship to Earlier Versions

v0.1 answers:

> What is this question?

v0.2 answers:

> Why did this question arise?

v0.3 answers:

> How is this question connected to the other questions?

Together:

```text
Question Envelope
        ↓
Question Provenance
        ↓
Question Graph
```

form the first three structural layers of Q Network.

---

## 51. Non-Goals of v0.3

Version 0.3 does not define:

- semantic distance;
- Question Drift Score;
- causal blame;
- graph database implementation;
- mandatory visualization;
- answer graphs;
- authority graphs;
- contribution graphs;
- payment graphs;
- global agent orchestration.

These remain separate concerns.

---

## 52. Future Direction

The expected progression remains:

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

Question Graph provides the structural basis required for drift and incident reconstruction.

---

## 53. Core Statements

Q Network Protocol v0.3 defines explicit relationships between questions.

Its structural invariant is:

> Every graph edge must connect distinct, identifiable questions.

Its historical invariant is:

> Reconsideration creates new questions rather than silently rewriting old ones.

Its safety invariant is:

> A graph may explain how a question lineage evolved, but graph structure never grants authority.

Its investigative principle is:

> To understand an AI action, reconstruct the graph of questions that preceded it.
