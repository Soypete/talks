---
marp: true
theme: gaia
paginate: true
title: "Beyond AI Memory"
description: "Why semantic context is the missing layer in agentic MLOps"
---

<!-- _class: lead -->

# Beyond AI Memory

## Why Semantic Context Is the Missing Layer in Agentic MLOps

Miriah Peterson · CEO, Haikai Labs

MLOps World | GenAI Summit 2026

---

<!-- _class: lead -->

# We Love Agents

Agents can read, reason, call tools, and take action.

They are becoming a new interface to software.

## But capability is not understanding.

---

# The Memory Metaphor Is Misleading

When an agent gives a wrong answer, we often ask:

> “Why didn’t it remember?”

But many failures are not missing memories.

They are missing meaning, scope, and authorization.

## Personalization is governed data access.

---

# The Context Void

```text
User request
     ↓
      LLM
     ↓
Plausible answer or action
```

The model may not know:

- which data is authoritative
- what an entity means in this organization
- which user or purpose applies
- whether the requested action is permitted

So it guesses.

---

# Semantically Nearby Can Be Operationally Wrong

Vector search can retrieve something related to the query.

But “related” is not the same as:

- the right customer
- the right version
- the right jurisdiction
- the right sensitivity class
- the right action context

Similarity is useful retrieval infrastructure. It is not a business meaning layer.

---

# A Retrieval Failure Can Become an Action Failure

```text
Wrong context
     ↓
Wrong interpretation
     ↓
Wrong tool arguments
     ↓
Real-world consequence
```

The production problem is not only hallucination.

It is ungrounded action.

---

# From Prompt Engineering to Semantic Engineering

Prompt engineering asks:

> How do we phrase instructions so the model behaves?

Semantic engineering asks:

> How do we give the system structured meaning, scoped context, and enforceable actions?

The second question belongs in infrastructure.

---

# Context Engineering

Context engineering is a pipeline:

```text
Classify task
     ↓
Resolve meaning and scope
     ↓
Retrieve authorized context
     ↓
Select constrained tools
     ↓
Validate action
     ↓
Execute and audit
```

The model participates in the loop. It does not own the loop.

---

<!-- _class: lead -->

# Three Layers of Semantic Context

## Lexicon · Syntax · Pragmatics

---

# Layer 1: Lexicon

## What does the organization know?

The lexicon is the controlled information environment:

- entities and relationships
- data definitions
- authoritative sources
- sensitivity and retention
- ownership and provenance

This is more than a pile of documents.

---

# Lexicon Is Federated Context

```text
CRM       Warehouse       EHR       GitHub
 │           │             │          │
 └───────────┴─────────────┴──────────┘
              ↓
       Context infrastructure
```

The goal is not to copy every source into one memory store.

The goal is to connect to data where it lives and preserve identity-aware access.

---

# Layer 2: Syntax

## What does this data mean here?

“SSN” may mean:

- a regulated identifier
- a masked display field
- a customer verification attribute
- a value the current user must never receive

The model needs structured relationships, not just nearby text.

---

# Ontological Injection

```text
SSN
 ├── is_a: regulated_identifier
 ├── belongs_to: person
 ├── display: masked_only
 ├── allowed_purpose: identity_verification
 └── access: identity_and_policy_required
```

Inject the relevant structure at task time.

Do not expect the model to infer your ontology from examples.

---

# Layer 3: Pragmatics

## What is the agent doing by saying this?

An agent’s tool call is a speech act:

```text
“Send this message.”
“Change this record.”
“Approve this request.”
```

The system must validate the act, not just generate fluent language.

---

# Tool Calls Need Meaning and Rules

```text
MODEL
  “I want to update a patient record.”

SEMANTICS
  “Which patient, field, purpose, and source?”

PRAGMATICS
  “Is this actor allowed to make this change?”

EXECUTION
  “Perform only the validated operation.”
```

Rigid tool definitions turn intent into an enforceable interface.

---

# Sandboxes Are Not Semantic Boundaries

A sandbox can restrict:

- where the process runs
- which files it can see
- which network it can reach

That is valuable.

But it does not define what a business entity means or whether a proposed action is appropriate.

Execution isolation and semantic enforcement solve different problems.

---

<!-- _class: lead -->

# A Small Vertical Makes This Visible

## Precision coaching for a deadlift carry

---

# Generic Coach vs. Contextual Coach

```text
User: “My form broke down at RPE 8.”
```

Generic agent:

> “Try less weight and focus on form.”

Contextual agent understands:

- what “form breakdown” means in this program
- what RPE means for this athlete
- which movement and load are being discussed
- which safety limits apply

---

# Semantics in Action

```text
form_breakdown
 ├── movement: deadlift_carry
 ├── signal: lumbar_flexion
 ├── severity: threshold_exceeded
 └── response: reduce_load_and_stop_set
```

The ontology turns domain language into operational meaning.

---

# Pragmatics in Action

```text
adjust_training_load(
  athlete,
  movement,
  load,
  reason
)
```

Before execution, middleware validates:

- athlete identity
- allowed load range
- current injury constraints
- coach or clinician authority
- required safety response

Generic AI coaches guess. Contextual agents can be constrained.

---

# The Neural Proxy

```text
Agent
  ↓
Neural Proxy / Agentic Middleware
  ├── task classification
  ├── context and ontology resolution
  ├── identity and ABAC evaluation
  ├── tool validation
  ├── model routing
  └── audit and feedback
  ↓
Enterprise systems
```

The middleware is the semantic background around the model.

---

# Bring Your Own Agent

The semantic layer should not depend on one harness or one model.

```text
LangChain   PydanticAI   Custom harness
      \         |         /
       └── Semantic middleware ──┘
              |
       GPT · Claude · Llama
```

Models can change.

The meaning and action rules should remain stable.

---

# What MLOps Must Operate

MLOps for agents is not only model deployment.

It also operates:

- ontology and schema versions
- retrieval and context quality
- policy decisions
- tool contracts
- model and middleware traces
- action outcomes

The production unit is the whole context-to-action pipeline.

---

# RAG Is One Component

```text
RAG
  retrieves likely context

Semantic context
  defines meaning and scope

Pragmatic enforcement
  validates what the agent may do
```

RAG helps an agent find information.

Semantic engineering helps the agent understand and act on it safely.

---

# The Evolution

```text
Prompt engineering
        ↓
Context engineering
        ↓
Semantic engineering
        ↓
Agentic infrastructure
```

We are moving from optimizing responses to operating reliable action systems.

---

# Final Thought

An agent without structured data, semantics, and pragmatics is a stochastic system guessing at intent.

Give it a semantic background.

Then intelligence can become precise, personalized, and production-ready.

---

<!-- _class: lead -->

# Thank You

## Beyond AI Memory

### Why Semantic Context Is the Missing Layer in Agentic MLOps

Miriah Peterson · Haikai Labs

