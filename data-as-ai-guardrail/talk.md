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

## The Problem: AI Works with Unstructured Data

AI primarily processes **text** — which is inherently unstructured.

Traditional data modeling doesn't work here:
- No ERDs or schemas for natural language
- No foreign keys or constraints
- No built-in validation

**Without structure, how do we validate AI outputs?**

---

## The Context Problem

The word **"fire"** means completely different things:

- 🔥 A flame burning
- 🔫 Discharge a weapon
- 💼 Terminate employment
- 🎯 "You're on fire!" (excelling)

In structured data, context is **explicit** (column names, relationships).
In text, context must be **derived**.

<!-- This is Bill Inmon's key insight about unstructured data -->

---

## Bill Inmon's Insight

> "The data model for structured data is the ERD. The data model for unstructured text is the **ontology/taxonomy**."

**Structured Data** → ERD as compass (inward-facing, internal processes)
**Unstructured Text** → Ontology as compass (external-facing, world knowledge)

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

- **Unstructured data needs ontologies** like structured data needs ERDs
- **AI naturally understands** semantic relationships
- **Ontologies enable deterministic validation** of AI outputs
- **Agentic AI can self-validate** through ontology inference
- **Combines flexibility with rigor** — trustworthy autonomous pipelines

---

<!-- _class: lead -->

# Questions?

---

## Resources

- [Mastering Unstructured Data](https://williaminmon.substack.com/p/mastering-unstructured-data-data) - Bill Inmon
- [OWL Web Ontology Language](https://www.w3.org/OWL/)
- [RDFLib (Python)](https://rdflib.readthedocs.io/)

**Follow me:**
- Substack: [@soypetetech](https://substack.com/@soypetetech)
- Twitch: [twitch.tv/soypetetech](https://twitch.tv/soypetetech)
- GitHub: [github.com/soypetetech](https://github.com/soypetetech)
