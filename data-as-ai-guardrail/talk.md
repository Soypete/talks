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
- Organizer of UDEM and MLOps Utah Meetups
- SoyPeteTech: Substack, Twitch, YouTube

![bg right](../images/SP_Logo-02.png)

---

<!-- _class: lead -->

# How many data engineers here are building agentic AI systems?

---

## The Locked Potential of Data

We have **petabytes** of curated, validated enterprise data.

- Data warehouses with decades of business logic
- Knowledge bases with domain expertise
- Curated datasets with referential integrity

**Yet AI agents largely ignore it** — they generate from prompts without data validation.

<!-- When you query ChatGPT or use AI for search, how do you validate the results? -->

---

## The Problem: AI Agents Hallucinate

LLMs confidently generate **plausible-sounding nonsense**.

- Fabricated facts presented as truth
- Invented citations and references
- Logically inconsistent reasoning
- Domain violations that sound correct

---

<!-- _class: lead -->

# [Autonomous agents amplify this risk without guardrails](https://soypetetech.substack.com/p/optimizing-into-chaos-why-ai-agents?r=1vuifh)

### They act on their own outputs

---

## What is a Guardrail?

A **guardrail** is a mechanism for **systematically verifying** that LLM outputs remain bounded within:

- **Ideas** — factual claims, domain knowledge, valid concepts
- **Context** — relevant scope, appropriate framing, business rules
- **Actions** — permitted operations, safe behaviors, authorized decisions

Guardrails shift validation from *hoping the model behaves* to *enforcing that it does*.

---

## "Just Add It to the System Prompt"

The naive solution: stuff guardrails into the prompt.

```
You MUST follow these 47 rules...
You MUST NOT make claims about...
You MUST validate against these constraints...
```

**The more context you add, the less reliably it follows any single rule.**

System prompts don't scale as guardrails.

<!-- Note: Capital letters DO make a difference in prompts, but length increases processing time and I've seen system prompts get ignored entirely. -->

---

## Raw Data Isn't Enough Either

You can retrieve data, but AI can't **infer relationships** without semantic context.

```sql
SELECT * FROM products WHERE category_id = 5;
```

The AI sees rows. It doesn't know:
- What "category 5" means in your domain
- How products relate to inventory, pricing, compliance
- What business rules constrain valid states

---

<!-- _class: lead -->

# Data without semantics is just noise to an LLM.

---

## Bill Inmon's Answer

> "The data model for structured data is the ERD. The data model for unstructured text is the **ontology/taxonomy**."

📖 [Mastering Unstructured Data](https://williaminmon.substack.com/p/mastering-unstructured-data-data) - Bill Inmon

---

## Ontologies are the schema for text

| Structured Data | Unstructured Text |
|-----------------|-------------------|
| ERD/Schema | **Ontology** |
| Foreign keys | **Relationships** |
| Constraints | **Inference rules** |

---

<!-- _class: lead -->

# What is an Ontology?

---

## Ontology: A Formal Definition

> "At its core, an ontology is a **formal, explicit specification of a shared conceptualization** — an agreement about what things exist in a particular domain, how they relate to each other, and what we call them."

— [Jessica Talisman](https://jessicatalisman.substack.com/p/ontologiessome-perspectives), Semantic Engineer & Author of *Intentional Arrangement*

**Key distinction:** Ontologies use logic-based reasoning and can **infer new knowledge** from existing statements.

---

## The Ontology Pipeline

Building semantic knowledge systems follows a progression:

| Step | Structure | What It Provides |
|------|-----------|------------------|
| 1 | **Controlled Vocabulary** | Curated list of approved terms |
| 2 | **Metadata Standards** | Consistent attribute definitions |
| 3 | **Taxonomy** | Hierarchical parent-child relationships |
| 4 | **Thesaurus** | Synonyms, related terms, broader/narrower |
| 5 | **Ontology** | Formal logic + inference rules |
| 6 | **Knowledge Graph** | Instantiated data + relationships |

📖 [The Ontology Pipeline](https://moderndata101.substack.com/p/the-ontology-pipeline) — Jessica Talisman

---

## Definitions: Building Blocks

**Controlled Vocabulary**
> "The simplest reliable agreement a team can make about language — a curated, finite list of approved terms, each with one intended meaning."

**Taxonomy**
> "Takes the controlled vocabulary and transforms it into a hierarchical structure. The beginning of creating relationships between concepts."

**Ontology**
> "The ultimate controlled vocabulary — not just a list of terms, but a complete knowledge structure that captures concepts, entities, attributes, properties and how these things are related."

---

## An ontology provides semantic structure for unstructured data

```
Animal
├── Mammal
│   ├── Dog → barks, has_fur, is_pet
│   └── Cat → meows, has_fur, is_pet
└── Bird
    └── Parrot → speaks, has_feathers, is_pet
```

<!--
- Vocabulary: Domain-specific terms and definitions
- Taxonomy: Hierarchical organization of concepts
- Relationships: How concepts connect to each other
- Context: Disambiguation of ambiguous terms
-->

---

## You Already Use Ontologies

An ontology is a **semantic data model** — a certain type of knowledge graph organized in a specific way.

You interact with ontologies every time you search:
- **Google Search** — Knowledge Graph connects entities and concepts
- **Amazon** — Product taxonomies, categories, and relationships
- **Medical systems** — Disease classifications and drug interactions

They power the semantic understanding behind modern search and recommendation systems.

---

## The Key Insight: Ontologies as Inference Models

Ontologies are **semantic models** — similar to ML models, you can inference off of them and make deductions.

They're built for **human traversal** and reasoning.

**But do they work for AI traversal?**

Can an AI agent:
1. Traverse ontology hierarchies?
2. Query relationships between concepts?
3. Validate assertions against defined semantics?
4. Infer new knowledge from existing relationships?

---

## Revisiting Guardrails: Traditional Approaches

Traditional guardrails for AI systems:
- **Prompt engineering** — fragile
- **Output filtering** — reactive
- **LLM self-critique** — inconsistent

[Without proper guardrails, autonomous agents can optimize into chaos](https://soypetetech.substack.com/p/optimizing-into-chaos-why-ai-agents?r=1vuifh)

---

## Ontology-Based Guardrails

A different approach:
- **Deterministic validation** — against defined semantics
- **Domain-grounded reasoning** — using enterprise knowledge
- **Self-correcting through inference** — logical deduction
- **Auditable decision paths** — traceable reasoning

---

## Three Patterns Emerging in Industry

**1. Ontology as Schema Constraint**
Constrain outputs to typed predicate space, then verify
— [Apple ODKE+](https://machinelearning.apple.com/research/odke), [Graph-Constrained Reasoning (GCR)](https://arxiv.org/html/2410.13080v1)

**2. Ontology as Context Engineering**
Organize what context gets retrieved and injected
— [Palantir Ontology-Augmented Generation (OAG)](https://www.palantir.com/docs/foundry/ontology/ontology-augmented-generation)

**3. Ontology Behind Tool Calls**
KG schema drives what functions exist and how they're called
— [FNCTOD (ACL 2024)](https://aclanthology.org/2024.acl-long.471.pdf), [edge device function calling](https://www.engr.siu.edu/staff/iraklis.anagnostopoulos/files/papers/Less_is_More_Optimizing_Function_Calling_for_LLM_Execution_on_Edge_Devices.pdf)

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

**[Procedural Knowledge Ontology](https://www.linkedin.com/pulse/process-knowledge-management-jessica-talisman-kt3ce/)** for validating learning content:

```
Assertion: "Students should learn calculus before algebra"

Ontology Query:
  - calculus.prerequisite = algebra ✓
  - algebra.prerequisite = calculus ✗

Result: INVALID - violates prerequisite chain
Agent Action: Regenerate with correct ordering
```

The ontology provides **ground truth** for domain knowledge.

Implementation: [PKO Experiment in Professor Pedro](https://github.com/Soypete/professor_pedro/pull/22) — AI assistant with semantic grounding

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
- [The Ontology Pipeline](https://moderndata101.substack.com/p/the-ontology-pipeline) — Jessica Talisman
- [Ontologies—Some Perspectives](https://jessicatalisman.substack.com/p/ontologiessome-perspectives) — Jessica Talisman
- [Controlled Vocabularies](https://jessicatalisman.substack.com/p/controlled-vocabularies) — Jessica Talisman

---

<!-- _class: lead -->

# Thank You!

**@soypetetech** — Substack, Twitch, YouTube, GitHub
