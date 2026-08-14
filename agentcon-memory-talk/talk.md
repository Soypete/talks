---
marp: true
theme: gaia
paginate: true
title: "Your AI Agent Does Not Have Memory: Personalization Is Governed Data Access"
backgroundImage: url('../images/soypete_background.png')
description: "AI memory" systems are usually built from chat history, vector search, summaries, and larger context windows. This talk argues that personalization is not something the model should "remember." Personalization is governed data access.
---

<!-- _class: lead -->

# Your AI Agent Does Not Have Memory

## Personalization Is Governed Data Access

by Miriah Peterson
@Soypete

---

## Who Am I?

- AI/ML Infrastructure Engineer at SchoolAI
- Creator: kei, Pedro-agentware, Graphify, MemPalace
- Building production agent systems since 2023
- Organizer: Utah Data Engineering & MLOps Meetups

![bg right:40%](../images/SP_Logo-02.png)

---

<!-- _class: lead -->

# PART 1: THE BUG

---

## The Scenario

You ask an agent:

> "How do I install ethernet drivers on Ubuntu?"

Expected:

> Instructions for Ubuntu ethernet drivers.

Actual:

> The agent tells you about your numpy budgeting script, your conference travel preferences, and that time you mentioned network hardware in 2023.

---

## That Is Not Memory

The agent did not "remember" wrong.

The system retrieved and injected the wrong context.

It saw:

- "drivers" → "driver" → budgeting script
- "Ubuntu" → old homelab notes
- "network" → conference travel and hardware notes

This is not a memory failure.

It is a **context pipeline failure**.

---

## Why This Happens

Most agent memory systems are built from:

- chat history
- vector search
- summaries
- larger context windows

Those can improve the agent's vibes.

They do not guarantee the right context gets used for the right task.

---

## The Model Is Not the Memory System

Models are good at producing plausible continuations.

They are not good at deciding:

- what state is durable
- what context is relevant
- what data the user is allowed to access
- what should be ignored
- what should be written back

That is infrastructure work.

---

## The Cost of Dumping Context

More context usually means:

- more latency
- more spend
- more distractors
- harder debugging
- weaker guarantees

A bigger context window does not fix context quality.

It just gives the system more room to be wrong.

---

## Current "Memory" Approaches

| Approach | What It Does | Why It Fails |
|---|---|---|
| Chat history | Stores conversation turns | Expensive, noisy, drifts |
| Vector search | Finds semantic similarity | Similar is not correct |
| Summarization | Compresses prior context | Loses source and precision |
| Large context | Dumps more input | Cost and distraction grow |

---

## The Real Problem

"Memory" is hiding several different engineering problems.

| Need | Better name | Engineering primitive |
|---|---|---|
| Personalization | User/world model | Profile store / graph |
| Task execution | Task context | Scoped retrieval |
| Long-running work | Workflow state | Durable state / event log |
| Governance | Context control | Policy, lineage, evals |

Calling all of this "memory" makes us build the wrong system.

---

<!-- _class: lead -->

# PART 2: THE MODEL

---

## Context Engineering

Context engineering decides:

- what information is introduced
- when it is introduced
- how long it persists
- what gets dropped
- what gets written back
- how the system checks itself

This is not prompt engineering.

It is data engineering and reliability engineering for the agent context pipeline.

---

## The Core Principle

# Inject late.

# Inject little.

# Make it checkable.

---

## The Agent Context Pipeline

```text
request
  ↓
classify intent
  ↓
resolve identity + permissions
  ↓
retrieve candidate context
  ↓
filter / rank / validate
  ↓
assemble scoped context
  ↓
inject into model or tool call
  ↓
observe outcome
  ↓
write back state, if allowed
```

---

## The Model Consumes Context

It should not own the context pipeline.

---

## The Production Pattern

1. Classify
   What kind of request is this?

2. Retrieve
   Exact lookup when possible.
   Semantic search when necessary.

3. Authorize
   Is this context allowed for this user/task?

4. Assemble
   Build the smallest useful context packet.

5. Validate
   Check structure, provenance, and output claims.

---

## Retrieval Is Not One Thing

| Retrieval type | Good for | Failure mode |
|---|---|---|
| Key lookup | Known facts | Requires structure upfront |
| SQL / graph query | Relationships | Requires schema/modeling |
| BM25 | Lexical match | Misses semantic equivalents |
| Vector search | Fuzzy recall | Retrieves plausible nonsense |
| Summaries | Compression | Loses source and precision |

Vector search is a recall tool.

It is not a correctness guarantee.

---

## Determinism Matters

For reliable systems, we need to ask:

- Can the same query produce the same context?
- Can we explain why this context was selected?
- Can we prove the user was allowed to access it?
- Can we test retrieval behavior across releases?
- Can we prevent bad state from being written back?

If not, the agent does not have memory.

It has vibes with persistence.

---

<!-- _class: lead -->

# PART 3: THE CONTROLS

---

## Four Controls for Agent Context

| Control | What it gives you |
|---|---|
| Provenance | Where the context came from |
| Scoped retrieval | Only the context needed for this task |
| Policy enforcement | Who/what can access or inject context |
| Semantic validation | Whether the output is structurally allowed |

These are the pieces that turn memory from a feature into infrastructure.

---

## Control 1: Provenance

Every piece of context should be tagged by how it was created.

Examples:

- EXTRACTED — found directly in source material
- INFERRED — derived from other known facts
- AMBIGUOUS — possible, but not safe to treat as truth

The system should know the difference.

The model usually will not.

---

### Example: Graphify

Knowledge Graphs for Personalization

```
Input
(files, docs, code, conversations)
  ↓
Graph extraction
(EXTRACTED | INFERRED | AMBIGUOUS)
  ↓
Knowledge graph
(entities + relationships + provenance)
```

Graph traversal is useful for personalization because personalization is relational.

The question is not just "what text is similar?"

The question is "what does this user care about, and how do those facts relate?"

---

## Control 2: Scoped Retrieval

Task context should be retrieved for the current request.

Not dumped from every prior interaction.

A useful context system should know:

- the subject
- the predicate
- the object or expected object type
- the source
- the scope
- the TTL
- the confidence/provenance level

This makes retrieval smaller and easier to test.

---

### Example: kei — Task-Based Scoped Retrieval

Harness Tokens Define Context Scope

```
Harness token: kh_live_abc123
  → identifies org + permissions
  → defines what tools are available
  → scopes retrieval to authorized resources
```

The token is not just authentication.

It is a context boundary that governs what the agent can access.

Every request carries its scope with it.

---

## Exact Retrieval Beats Similarity When You Need Facts

```python
# Exact Subject-Predicate-Object retrieval
result = spo_store.get(
    subject="ubuntu",
    predicate="has_package_manager"
)

# Returns a known fact from a scoped store.
# Not the nearest embedding.

# Use semantic search for discovery.
# Use structured lookup when correctness matters.
```

---

## Hybrid Retrieval Is a Policy Decision

```python
# When you need discovery
vector_results = collection.query(
    "driver installation",
    n=3
)

# When you need a known fact
exact_result = spo_store.get(
    subject="ubuntu",
    predicate="has_package_manager"
)

# Then validate what is allowed into context.

# The important decision is not "vector or graph."
# The important decision is what guarantees the task requires.
```

---

## Control 3: Policy Enforcement

Context injection is a permissioned operation.

The system should ask:

- Who is making the request?
- What task are they performing?
- What tools are available?
- What context can be used?
- What context must be excluded?
- What budget applies?

Agents should not get ambient access to everything.

---

### Example: kei-proxy — Authorization Before Execution

Context Control in Production

```
Agent / LLM
  ↓ tool call (e.g., github.create_pr)
kei-proxy authorize
  ↓
ABAC Engine: authorize(user, action, resource, service)
  ↓
permit/deny + scoped credential injection
  ↓
Tool executes with only authorized context
```

The proxy owns the boundary.

The model can request tools.

The system decides whether that request is valid and what credentials to provide.

---

### kei-proxy Authorize Flow

```bash
# Agent requests tool
kei-proxy authorize \
  --user U1234 \
  --tool github.create_pr \
  --action github:write \
  --resource repo:schoolai/frontend

# Returns (if permitted):
{
  "decision": "permit",
  "credential": {
    "value": "ghp_xxxxx",
    "injection": {"type": "bearer", "header": "Authorization"}
  }
}
```

---

## Control 4: Semantic Validation

The output should be checked against what the system knows.

Not every sentence can be proven.

But structured claims can be validated.

Examples:

- Is this relationship allowed?
- Is this object type valid?
- Did this claim come from retrieved context?
- Is the model inventing a relation that violates the schema?

---

### Context Engineering Needs Three Things

Reliable agent behavior requires:

```
┌─────────────────────────────────────────────────┐
│  PRAGMATICS                                     │
│  What is the user trying to accomplish?         │
│  (task classification, intent detection)        │
├─────────────────────────────────────────────────┤
│  SEMANTICS                                      │
│  What does the data mean?                       │
│  (knowledge graphs, relationships, provenance)  │
├─────────────────────────────────────────────────┤
│  DATA                                           │
│  What information is available and allowed?     │
│  (scoped retrieval, ABAC policies, credentials) │
└─────────────────────────────────────────────────┘
```

Without all three, you get vibes instead of reliability.

---

### Example: Graphify — Knowledge Graphs

Knowledge Graphs Provide Semantic Structure

```
┌─────────────────────────────────────────────────┐
│  Input                                          │
│  (files, docs, code, conversations)             │
│    ↓                                            │
│  Graph extraction                               │
│  (entities + relationships + provenance)        │
│    ↓                                            │
│  Queryable knowledge graph                      │
└─────────────────────────────────────────────────┘
```

Graph traversal answers: "What does this user care about, and how do those facts relate?"

---

### Ontology Validation

```go
func ValidateOutput(output string, ontology *Ontology) error {
    claims := ParseClaims(output)

    for _, claim := range claims {
        if !ontology.IsValidTriple(
            claim.Subject,
            claim.Predicate,
            claim.Object,
        ) {
            return fmt.Errorf("invalid: %s", claim)
        }
    }
    return nil
}
```

---

<!-- _class: lead -->

# PART 4: EVALUATION

---

## What We Test

Reliable context systems need regression tests.

Not just vibe checks.

Test whether:

- the right context was retrieved
- the wrong context was excluded
- permissions were enforced
- context stayed within budget
- the output used supported claims
- write-back created valid state
- repeated runs stayed consistent

---

## Experiment Results

| System | Avg Turns | Avg Search | Latency |
|---|---|---|---|
| LLMWiki | 1.00 | 1.00 | 3.86ms |
| Graphify | 1.00 | 1.00 | 0.01ms |
| MemPalace | 0.60 | 0.60 | 6.99ms |

Result: Scoped retrieval reduced unnecessary search/turns while keeping retrieval explicit.

The point is not that one store wins forever.

The point is that retrieval behavior became measurable.

---

## The Pattern Across Systems

| Need | Control | Example |
|---|---|---|
| Pragmatics | Task classification | Intent routing |
| Semantics | Relationship model | Graphify / knowledge graphs |
| Data | Scoped retrieval + policies | kei harness tokens + ABAC |
| Tool access | Policy boundary | kei-proxy + ABAC |
| Output checking | Semantic constraints | Ontology-go |
| Regression safety | Evaluation harness | Agent tests |

This is context infrastructure.

Not prompt decoration.

---

<!-- _class: lead -->

# PART 5: WHERE THIS GOES

---

## Future Agent State

Reliable long-running agents need:

- retrieval-aware orchestration
- versioned context stores
- context data contracts
- audit logs for context injection
- durable workflow state
- permissioned write-back (via ABAC)
- shared governed state for multi-agent systems

Not shared chat logs.

---

## Multi-Agent Systems Need Governed State

If multiple agents coordinate through chat history, you get:

- state drift
- unclear ownership
- untestable handoffs
- duplicated context
- permission leaks

Shared state should be explicit.

Readable by agents.

Governed by systems.

Tested like infrastructure.

---

## The Final Algorithm

1. Classify the task.
2. Resolve identity, scope, and permissions.
3. Retrieve using the strongest retrieval guarantee available.
4. Assemble the smallest useful context packet.
5. Inject context through a controlled boundary.
6. Validate claims and tool outputs.
7. Observe behavior.
8. Write back only valid state.

---

## What We Learned

"Memory" conflates too many problems.

Production agents need separate systems for:

- personalization
- task context
- workflow state
- authorization
- validation
- evaluation

The model is not the memory system.

The system builds memory through governed state and scoped context retrieval.

---

## Key Takeaway

AI memory is not something the model has.

It is something the system builds.

Reliable agents need governed context pipelines:

scoped retrieval, durable state, provenance, permissions, and validation.

---

## Open Source

kei — governance and authorization for agent systems

Pedro-agentware — agent middleware

MemPalace — scoped semantic memory

Graphify — knowledge graph extraction

---

## In Production

We apply these principles at SchoolAI:

- **Task classification**: routing to scoped knowledge stores
- **Governed retrieval**: ABAC policy before vector search
- **Scoped context**: agents only see authorized data
- **Provenance tracking**: audit trail on all context usage

---

## References

Why I Hate "Context Engineering"

Data as an AI Guardrail

AI Reliability Engineering

Unit Testing Your Agents

AI Isn't Getting Smarter

---

<!-- _class: lead -->

# Questions?

## Miriah Peterson

### @Soypete
