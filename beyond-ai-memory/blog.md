# Beyond AI Memory: The Missing Layer in Agentic MLOps

We love agents.

They can read documents, inspect code, call tools, update systems, and help people complete work. Since the release of Claude Code in February 2025, the industry has invested heavily in agent harnesses that turn language models into practical computer interfaces.

That progress raises a more important question:

> What is the next step in the evolution of agents?

The first generation of harnesses is closely tied to a user's machine. It has a filesystem, shell, local skills, credentials, and state. The next generation must operate across enterprise data and services, scale tasks independently, and continue working when the user closes the laptop.

That is where the memory metaphor starts to fail.

## Personalization is not memory

When an agent gives a wrong answer, we often assume it forgot something. More context, a larger context window, or another vector search may appear to be the solution.

But many production failures are not missing-memory problems. They are meaning and access problems.

The agent may retrieve a document that is semantically close but operationally wrong. It may not know which definition of a field is authoritative, whether two records refer to the same entity, whether the information is allowed for the current user, or whether a proposed action is appropriate.

Personalization is not simply what the model remembers about a person. Personalization is the data and meaning that the person is authorized to use for a specific purpose.

## The context void

An agent operating in a context void has to guess:

- Which data source is authoritative?
- What does this entity mean in this organization?
- Which version or jurisdiction applies?
- What does a sensitive field allow the agent to do?
- Which action is the user actually authorizing?

That uncertainty compounds across the agent loop:

```text
Wrong context
     ↓
Wrong interpretation
     ↓
Wrong tool arguments
     ↓
Real-world consequence
```

This is why agent reliability cannot be measured only by whether a model produces a plausible response. We need to evaluate the entire context-to-action pipeline.

## From Prompt Engineering to Semantic Engineering

Prompt engineering focuses on instructions: how do we phrase a request so the model behaves?

Semantic engineering focuses on infrastructure: how do we provide structured meaning, scoped context, and enforceable actions?

The difference is important. A prompt can tell the model that an SSN is sensitive. A semantic layer can define the entity, connect it to a person, specify masking rules, record its source, and require an identity-aware policy decision before the value is returned.

The model should receive the meaning it needs at task time. It should not be expected to reconstruct an organization's ontology from scattered examples.

## Three layers of Context Engineering

### 1. Lexicon: the organization’s data environment

The lexicon is the information an organization manages: entities, relationships, definitions, provenance, sensitivity, ownership, and authoritative sources.

This does not require copying every source into a single memory store. Data can remain federated where it lives, provided that access is identity-aware and the system can resolve which source and definition apply.

The goal is not data consolidation for its own sake. The goal is reliable context with clear ownership and scope.

### 2. Syntax: structured meaning

Syntax is how meaning is represented and supplied to the model.

Consider a field named `SSN`. Depending on the organization and task, it may be a regulated identifier, a masked display value, a verification attribute, or data the current user must never receive.

An ontology can make those relationships explicit:

```text
SSN
 ├── is_a: regulated_identifier
 ├── belongs_to: person
 ├── display: masked_only
 ├── allowed_purpose: identity_verification
 └── access: identity_and_policy_required
```

This structured context is more precise than retrieving another paragraph that happens to mention “SSN.”

### 3. Pragmatics: actions with purpose

Pragmatics asks what an agent is doing by saying something. A tool call is not merely text. It is a speech act that may send a message, change a record, approve a request, or trigger a workflow.

The system must validate the act:

```text
MODEL       “I want to update a patient record.”
SEMANTICS   “Which patient, field, purpose, and source?”
PRAGMATICS  “Is this actor allowed to make this change?”
EXECUTION   “Perform only the validated operation.”
```

Rigid tool definitions and pre-execution policy checks turn fluent intent into an enforceable interface.

## Why RAG is not enough

Retrieval-augmented generation is an important component of an agent system. It helps retrieve likely context.

But retrieval does not, by itself, establish:

- whether the context is authoritative
- what the entities mean in the current domain
- whether the user can access it
- whether the requested action is allowed

RAG finds information. Semantic infrastructure governs meaning and action.

## A precision-coaching example

Consider an agent coaching an athlete through a deadlift carry. The athlete says, “My form broke down at RPE 8.”

A generic coach can offer a reasonable-sounding suggestion: use less weight and focus on form.

A contextual coach needs a more precise model. It must know what “form breakdown” means in this program, how RPE is defined for this athlete, which movement and load are being discussed, and which safety limits apply.

The ontology might connect `form_breakdown` to a movement, a biomechanical signal, a severity threshold, and a safe response. A tool such as `adjust_training_load` can then validate the athlete, movement, load range, injury constraints, and coaching authority before changing the plan.

The point is not that a model cannot discuss exercise. The point is that reliable personalization comes from structured semantics and constrained action—not from asking the model to guess better.

## The Neural Proxy

Haikai Labs is building toward a middleware layer that sits between an agent and the systems it can affect: a Neural Proxy for semantic context and governed action.

The layer can:

- classify the task
- resolve relevant ontology and data sources
- retrieve identity-aware context
- route requests across models and tools
- evaluate ABAC policies
- validate tool arguments
- trace decisions and outcomes

This architecture supports Bring Your Own Agent. LangChain, PydanticAI, custom harnesses, and future agent runtimes should be able to use the same semantic and action layer. Models can change without changing the meaning of an organization’s data or the rules around its actions.

## The future of agentic MLOps

MLOps for agents is not only model deployment. It is the operation of the entire context-to-action pipeline:

```text
Data and ontology
       ↓
Context retrieval
       ↓
Model reasoning
       ↓
Tool validation
       ↓
Execution and audit
```

That pipeline needs versions, tests, traces, policy evaluations, and outcome measurements. The production unit is not the model in isolation. It is the model situated in a semantic background.

The industry is moving from Prompt Engineering to Semantic Engineering. The next generation of agents will not simply remember more. They will operate with better definitions, narrower context, and clearer authority.

An agent without structured data, semantics, and pragmatics is a stochastic system guessing at intent. Give it a Semantic Background, and intelligent action can become precise, personalized, and production-ready.

