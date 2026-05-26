---
marp: true
theme: gaia
paginate: true
title: "Beyond Memory: Building Reliable Agent Context Infrastructure"
backgroundImage: url('../images/soypete_background.png')
description: How to build reliable agent personalization using context engineering
---

<!-- _class: lead -->

# Beyond Memory

## Building Reliable Agent Context Infrastructure

by Miriah Peterson
@Soypete

---

## Who Am I?

- AI/ML Infrastructure Engineer at SchoolAI
- Creator: MemPalace, Graphify, Ontology-go
- Building production agent systems since 2023
- Organizer: Utah Data Engineering & MLOps Meetups

![bg right:40%](../images/SP_Logo-02.png)

---

<!-- _class: lead -->

# PART 1: THE PROBLEM

---

## The Scenario

You ask an agent: *"How do I install ethernet drivers on Ubuntu?"*

Expected: Instructions for Ubuntu ethernet drivers

Actual: The agent tells you about your numpy budgeting script, your conference travel preferences, and that time you mentioned network hardware in 2023.

---

## What's Happening

The agent is "personalizing" — but incorrectly.

It sees:
- "drivers" → "driver" → "budget script with driver"
- "Ubuntu" → past conversations about Ubuntu
- Connects things that shouldn't connect

This is **not memory failure**. It's **context failure**.

---

## Why Does This Happen?

### From "AI Isn't Getting Smarter"

> "We are scaling preference, not intelligence. AI doesn't discover truth — it learns what we reward."

Models are trained to:
- Agree with you
- Sound confident
- Complete your thinking

**Not** to find the right answer.

---

## The Cost

| Context Window | Cost/Request | Latency |
|----------------|--------------|---------|
| 32K tokens | ~$0.10 | ~1s |
| 128K tokens | ~$0.40 | ~3s |
| 1M tokens | ~$3.00 | ~15s |

More context = more money + more latency + worse quality

---

## Current "Memory" Approaches

| Approach | What It Does | Why It Fails |
|----------|--------------|--------------|
| Chat history | Stores all messages | Expensive, decays, drifts |
| Vector search | Semantic similarity | "Close enough" often wrong |
| Summarization | Compresses conversation | What was lost? |
| Large context | Dump everything | Cost explodes |

---

## The Real Problem

### Two distinct needs, one vague term

| Term | What it means | We need |
|------|---------------|---------|
| **Memory** | Personalizing an experience | Graph-based relationships |
| **Context** | Adding user data to prompts | Structured retrieval |

"Memory" is the wrong abstraction for both.

---

## What We Need

1. **Deterministic** — same query, same result
2. **Few-shot** — inject context only when needed
3. **Cost-aware** — only what's necessary
4. **Validated** — don't hope for correctness

---

<!-- _class: lead -->

# PART 2: THE SOLUTION

---

## Context Engineering

> "Context engineering decides what information is introduced and when, how long it persists, and what gets dropped between steps."

**Not:**
- More system prompts
- More chat history
- Everything upfront

**Yes:**
- Structured state
- Timing over volume
- Validation

---

## Two Problems, Two Solutions

### Problem 1: Memory (Personalization)

**Use: Knowledge Graphs**

- Entity relationships
- Semantic connections
- "What does this user care about?"

### Problem 2: Context (User Data)

**Use: MemPalace**

- SPO hashing for exact retrieval
- Wing/Room/Drawer hierarchy
- One-shot context injection

---

## The Architecture

```
┌─────────────────────────────────────────────┐
│              User Request                   │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│           Problem Classification            │
│    Memory? → Graph    Context? → MemPalace  │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│         Retrieval Strategy                  │
│    (Graph query or SPO lookup)              │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│        Tool Call (Context Injection)        │
│    Exactly right data, right time           │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│              LLM (Task Execution)           │
│    Probabilistic engine + validated input   │
└─────────────────────────────────────────────┘
```

---

<!-- _class: lead -->

# PART 3: THE DEMONSTRATION

---

## Solution 1: Graphify

### Knowledge Graphs for Personalization

```
┌─────────────────────────────────────────────┐
│              Input                          │
│  (files, docs, code, conversations)        │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│           Graph Extraction                  │
│  EXTRACTED | INFERRED | AMBIGUOUS           │
└─────────────────┬───────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│         Knowledge Graph                     │
│                                           │
│  ┌───┐    knows    ┌───┐                  │
│  │A │─────────────│B │                  │
│  └───┘            └───┘                  │
│    │                 │                     │
│  works_at         works_at                │
│    ↓               ↓                      │
│  ┌───┐            ┌───┐                  │
│  │C │            │D │  (relations)       │
│  └───┘            └───┘                  │
└─────────────────────────────────────────────┘
```

---

## Graphify: Audit Trail

Every edge tagged:

- **EXTRACTED** — found in source
- **INFERRED** — logically derived
- **AMBIGUOUS** — uncertain

---

## Solution 2: MemPalace

### Structured Context for User Data

```
┌─────────────────────────────────────────────┐
│                  Wing                       │
│         (Person or Project)                 │
│  ┌─────────────┐  ┌─────────────┐          │
│  │    Room     │  │    Room     │          │
│  │  (Topic)    │  │  (Topic)    │          │
│  │ ┌─────────┐ │  │ ┌─────────┐ │          │
│  │ │ Drawer  │ │  │ │ Drawer  │ │          │
│  │ └─────────┘ │  │ └─────────┘ │          │
│  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────┘
```

- **Wing** — Person or project
- **Room** — Topic within wing
- **Drawer** — Specific memory

---

## MemPalace: SPO Hashing

```python
# Exact Subject-Predicate-Object retrieval
def make_spo_key(subject, predicate, obj):
    return hash(f"{subject}|{predicate}|{obj}")

# Query: "miriah works_at"
# Returns: EXACT match, not "similar"

result = spo_store.get(
    subject="miriah",
    predicate="works_at"
)
# Result: {"schoolai", "known_since": "2024"}
```

---

## MemPalace: Dual Retrieval

```python
# When you need search
vector_results = collection.query(
    "driver installation",
    n=3
)

# When you need exact answer
exact_result = spo_store.get(
    subject="ubuntu",
    predicate="has_package_manager"
)

# Combine for precision + recall
```

---

## Solution 3: Pedro Middleware

### Context Control in Production

```
┌─────────────────────────────────────┐
│           Agent / LLM               │
└──────────────┬──────────────────────┘
               │ Tool Call
               ▼
┌─────────────────────────────────────┐
│        Agent Middleware              │
│  ┌───────────────────────────────┐  │
│  │  Context Control              │  │
│  │  - trusted/untrusted          │  │
│  └───────────────────────────────┘  │
│  ┌───────────────────────────────┐  │
│  │  Tool Control                 │  │
│  │  - permission                 │  │
│  │  - validation                 │  │
│  └───────────────────────────────┘  │
└──────────────┬──────────────────────┘
               │ Allowed/Blocked
               ▼
┌─────────────────────────────────────┐
│        Tool Execution               │
└─────────────────────────────────────┘
```

---

## Middleware Code

```go
func (m *Middleware) CallTool(
    ctx context.Context,
    name string,
    args map[string]interface{},
) (*ToolResult, error) {
    // 1. Context control
    callerCtx := m.extractCallerContext(ctx)

    // 2. Validate against policy
    decision := m.policy.Evaluate(callerCtx, name, args)
    if decision.Action == Deny {
        return nil, fmt.Errorf("denied: %s", decision.Reason)
    }

    // 3. Execute
    return m.executor.CallTool(ctx, name, args)
}
```

---

## Context Injection via Tool Call

```go
type ContextTool struct {
    store *MemPalaceStore
}

func (t *ContextTool) Execute(ctx context.Context, args map[string]interface{}) (*ToolResult, error) {
    query := args["query"].(string)
    wing := args["wing"].(string)

    // Exact SPO retrieval, not vector search
    result := t.store.Get(wing, query)

    // Inject only what's needed
    return &ToolResult{
        Content: result.Context,
    }, nil
}
```

---

## Solution 4: Ontology-go

### Semantic Models as Guardrails

```
┌─────────────────────────────────────────────┐
│              TBOX                           │
│         (Schema/Ontology)                   │
│                                           │
│  class: Person                             │
│  property: worksAt → Organization          │
│  property: knows → Person                  │
└─────────────────────────────────────────────┘
                    ↓ maps to
┌─────────────────────────────────────────────┐
│              ABOX                           │
│         (Instance Data)                     │
│                                           │
│  miriah worksAt SchoolAI                    │
│  miriah knows john                          │
└─────────────────────────────────────────────┘
```

---

## Ontology Validation

```go
// Validate output against ontology
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

> "An ontology is a schema for language. It doesn't make language smarter — it makes it checkable."

---

## Experiment Results

| System | Avg Turns | Avg Search | Latency |
|--------|-----------|------------|---------|
| LLMWiki | 1.00 | 1.00 | 3.86ms |
| Graphify | 1.00 | 1.00 | 0.01ms |
| **MemPalace** | **0.60** | **0.60** | **6.99ms** |

**Result:** Few-shot/one-shot retrieval achieved

---

## When to Use What

| Need | Solution | Why |
|------|----------|-----|
| Personalization | Graphify | Entity relationships |
| User context | MemPalace | Exact SPO retrieval |
| Validation | Ontology-go | Schema enforcement |
| Tool control | Middleware | Policy enforcement |

---

## The Algorithm

```
1. Classify: Memory (graph) or Context (SPO)?
2. Retrieve: Structured query, not semantic search
3. Inject: Via tool call at right time
4. Validate: Don't hope, check
```

---

<!-- _class: lead -->

# SUMMARY

---

## What We Learned

### Problem
- "Memory" conflates two distinct needs
- Current approaches are expensive and unreliable
- Models optimize for confidence, not correctness

### Solution
- **Memory** → Knowledge graphs (Graphify)
- **Context** → SPO retrieval (MemPalace)
- **Control** → Middleware + Ontologies

### Demonstration
- Code from production systems
- Experiment results proving effectiveness

---

## For Senior Leadership

1. Context engineering is **solved** — it's infrastructure
2. Cost control through structured retrieval
3. Reliability = measurable consistency

---

## For Engineers

1. **Memory ≠ Context** — different problems, different solutions
2. **Tool calls > chat history** — inject when needed
3. **Validate > hope** — check outputs

---

## Open Source

- [MemPalace](https://github.com/soypete/mempalace) — Semantic memory
- [Graphify](https://github.com/soypete/graphify) — Knowledge graphs
- [Ontology-go](https://github.com/soypete/ontology-go) — RDF/OWL
- [Pedro-agentware](https://github.com/soypete/pedro-agentware) — Middleware

---

## References

- [Why I Hate "Context Engineering"](https://soypetetech.substack.com/p/why-i-hate-the-term-context-engineering)
- [Data as an AI Guardrail](https://soypetetech.substack.com/p/data-as-an-ai-guardrail)
- [AI Reliability Engineering](https://soypetetech.substack.com/p/ai-reliability-engineering)
- [Unit Testing Your Agents](https://soypetetech.substack.com/p/unit-testing-your-agents)
- [AI Isn't Getting Smarter](https://soypetetech.substack.com/p/ai-isnt-getting-smarter-were-just)

---

<!-- _class: lead -->

# Questions?

## Miriah Peterson
### @Soypete