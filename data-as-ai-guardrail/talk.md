---
marp: true
theme: default
paginate: true
title: Data as an AI Guardrail
backgroundImage: url('../images/soypete_background.png')
description: Using Ontologies to Ground Agentic AI
---

<!-- _class: lead -->

# Data as an AI Guardrail
### Using Ontologies to Ground Agentic AI
by: Miriah Peterson

---

## Who Am I?

- Data Engineer at SchoolAI
- Organizer of GoWest, Forge Utah
- SoyPeteTech: Substack, Twitch, YouTube
- Building [Pedro](https://github.com/soypetetech/IAM_pedro) — AI bot with semantic grounding

![bg right](../images/pedro.gif)

---

## The Problem: AI Agents Hallucinate

LLMs confidently generate **plausible-sounding nonsense**.

- Fabricated facts presented as truth
- Invented citations and references
- Logically inconsistent reasoning
- Domain violations that sound correct

**Autonomous agents amplify this risk** — they act on their own outputs.

---

## We've Solved This Before

Data engineers have spent **entire careers** validating data:

- Schema enforcement
- Referential integrity
- Business rule validation
- Data quality pipelines

We have **decades of validated data stores** — why aren't we using them to ground AI?

---

## The Gap: Structured vs Unstructured

| Structured Data | Unstructured Text |
|-----------------|-------------------|
| ERD/Schema | ??? |
| Foreign keys | ??? |
| Constraints | ??? |
| Explicit context | Derived context |

The word **"fire"** = flame? weapon? termination? excellence?

**AI works with text. Text has no schema.**

---

## Bill Inmon's Answer

> "The data model for structured data is the ERD. The data model for unstructured text is the **ontology/taxonomy**."

**Ontologies are the schema for text.**

| Structured Data | Unstructured Text |
|-----------------|-------------------|
| ERD/Schema | **Ontology** |
| Foreign keys | **Relationships** |
| Constraints | **Inference rules** |

📖 [Mastering Unstructured Data](https://williaminmon.substack.com/p/mastering-unstructured-data-data) - Bill Inmon

---

## What is an Ontology?

An ontology provides semantic structure for unstructured data:

- **Vocabulary**: Domain-specific terms and definitions
- **Taxonomy**: Hierarchical organization of concepts
- **Relationships**: How concepts connect to each other
- **Context**: Disambiguation of ambiguous terms

```
Animal
├── Mammal
│   ├── Dog → barks, has_fur, is_pet
│   └── Cat → meows, has_fur, is_pet
└── Bird
    └── Parrot → speaks, has_feathers, is_pet
```

---

## Ontologies in Practice: OWL/RDF

```turtle
@prefix edu: <http://example.org/education#> .

edu:Concept a owl:Class .
edu:Prerequisite a owl:ObjectProperty ;
    rdfs:domain edu:Concept ;
    rdfs:range edu:Concept .

edu:Algebra a edu:Concept ;
    edu:prerequisite edu:Arithmetic ;
    edu:teaches "solving equations" .

edu:Calculus a edu:Concept ;
    edu:prerequisite edu:Algebra ;
    edu:teaches "rates of change" .
```

<!-- Ontologies define what concepts exist and how they relate -->

---

## The Key Insight: AI Can Inference on Ontologies

LLMs understand semantic relationships **natively**.

An AI agent can:
1. Traverse ontology hierarchies
2. Query relationships between concepts
3. Validate assertions against defined semantics
4. Infer new knowledge from existing relationships

**This makes ontologies natural guardrails for AI.**

---

## Ontologies as AI Guardrails

Traditional guardrails:
- Prompt engineering (fragile)
- Output filtering (reactive)
- LLM self-critique (inconsistent)

**Ontology-based guardrails:**
- Deterministic validation
- Domain-grounded reasoning
- Self-correcting through inference
- Auditable decision paths

---

## Three Patterns Emerging in Industry

**1. Ontology as Schema Constraint**
Constrain outputs to typed predicate space, then verify
— Apple ODKE+, Graph-Constrained Reasoning (GCR)

**2. Ontology as Context Engineering**
Organize what context gets retrieved and injected
— Palantir Ontology-Augmented Generation (OAG)

**3. Ontology Behind Tool Calls**
KG schema drives what functions exist and how they're called
— FNCTOD (ACL 2024), edge device function calling

---

## The Agent Validation Pattern

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Agent     │────▶│   Ontology   │────▶│  Validated  │
│  generates  │     │   validates  │     │   Output    │
│  assertion  │     │   via query  │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
        │                  │
        │                  ▼
        │           ┌──────────────┐
        └──────────▶│   Reject +   │
                    │   Retry      │
                    └──────────────┘
```

Agent makes claim → Queries ontology → Validates or rejects

---

## Tool Call Pattern

```python
def validate_assertion(assertion: str, ontology: Graph) -> bool:
    """
    Agent tool: Validate an assertion against the ontology.
    Returns True if semantically valid, False otherwise.
    """
    # Parse assertion into subject-predicate-object
    triple = parse_assertion(assertion)

    # Query ontology for validity
    query = f"""
    ASK WHERE {{
        {triple.subject} {triple.predicate} {triple.object} .
    }}
    """
    return ontology.query(query)
```

<!-- The agent can call this tool to self-validate -->

---

## Agent Workflow with Ontology Validation

```python
async def generate_with_validation(prompt: str):
    # 1. Generate initial response
    response = await llm.generate(prompt)

    # 2. Extract claims from response
    claims = extract_claims(response)

    # 3. Validate each claim against ontology
    for claim in claims:
        if not validate_assertion(claim, domain_ontology):
            # 4. Regenerate with feedback
            response = await llm.generate(
                f"{prompt}\nNote: {claim} is invalid. "
                f"Reason: {get_violation(claim, domain_ontology)}"
            )

    return response
```

---

## Real Example: Educational Content

**Procedural Knowledge Ontology** for validating learning content:

```
Assertion: "Students should learn calculus before algebra"

Ontology Query:
  - calculus.prerequisite = algebra ✓
  - algebra.prerequisite = calculus ✗

Result: INVALID - violates prerequisite chain
Agent Action: Regenerate with correct ordering
```

The ontology provides **ground truth** for domain knowledge.

---

## Why This Matters for Agentic AI

**Autonomous agents need self-correction mechanisms**

| Approach | Deterministic | Auditable | Domain-Aware |
|----------|--------------|-----------|--------------|
| Prompt Engineering | ❌ | ❌ | ❌ |
| Output Filtering | ✅ | ✅ | ❌ |
| LLM Self-Critique | ❌ | ❌ | ❌ |
| **Ontology Inference** | ✅ | ✅ | ✅ |

Ontologies combine AI flexibility with formal rigor.

---

## Building Your Own

1. **Define your domain vocabulary**
   - What concepts exist? What terms matter?

2. **Establish relationships**
   - Hierarchies, prerequisites, constraints

3. **Create inference tools**
   - SPARQL queries, graph traversal, validation functions

4. **Wire into agent loop**
   - Tool calls for validation before output

---

## Key Takeaways

- **Hallucination is a data validation problem** — we know how to solve those
- **Ontologies are schemas for text** — apply data engineering to AI
- **AI natively understands** semantic relationships
- **Deterministic validation** beats prompt engineering
- **Your data engineering expertise transfers** — use it to ground AI

---

<!-- _class: lead -->

# Questions?

---

## References: Ontology as Guardrail

- [ODKE+: Ontology-Guided Knowledge Extraction](https://machinelearning.apple.com/research/odke) — Apple, 2025
- [Graph-Constrained Reasoning (GCR)](https://arxiv.org/html/2410.13080v1) — arXiv, 2024

## References: Ontology as Context

- [Ontology-Augmented Generation](https://www.palantir.com/docs/foundry/ontology/ontology-augmented-generation) — Palantir Docs
- [Building with AIP: Data Tools for RAG/OAG](https://blog.palantir.com/building-with-palantir-aip-data-tools-for-rag-oag-b3b509c8b0f3) — Palantir Blog

---

## References: Ontology Behind Tool Calls

- [FNCTOD: Function Calling for Task-Oriented Dialogue](https://aclanthology.org/2024.acl-long.471.pdf) — ACL 2024
- [LLMs + KGs via Function Calling](https://ceur-ws.org/Vol-3853/paper7.pdf) — CEUR Workshop
- [Less is More: Function Calling on Edge](https://www.engr.siu.edu/staff/iraklis.anagnostopoulos/files/papers/Less_is_More_Optimizing_Function_Calling_for_LLM_Execution_on_Edge_Devices.pdf) — SIU

## Foundational

- [Mastering Unstructured Data](https://williaminmon.substack.com/p/mastering-unstructured-data-data) — Bill Inmon

---

<!-- _class: lead -->

# Thank You!

**@soypetetech** — Substack, Twitch, YouTube, GitHub
