# MLOps World | GenAI Summit CFP Submission

## Session title

Beyond AI Memory: Why Semantic Context Is the Missing Layer in Agentic MLOps

## Recommended event

Both events: November 5–6, 2026 (Toronto, ON) and November 16–19, 2026 (Austin, TX).

The talk is designed for either in-person format and can be adapted for the November 16 virtual session.

## Is there anything in this talk you'll be promoting?

Yes. The talk presents Haikai Labs' architectural perspective on the Sovereign Context Layer and Neural Proxy. It is framed as a vendor-neutral pattern and includes open architectural concepts rather than a product demonstration.

## Session description

We love agents. Since February 2025, developers have built harnesses that turn language models into tools for working with files, code, and computers. But what is the next step in their evolution? What would it take for an agent to escape one user's machine, scale across tasks, and keep working while its user is away?

This talk argues that personalization is not AI memory; it is governed access to meaningful context. We will examine why vector retrieval can return semantically nearby but operationally wrong data, then introduce Context Engineering: classifying tasks, resolving ontology, retrieving scoped data, validating tool calls, and auditing actions.

Attendees will learn a three-layer model: Lexicon for federated, identity-aware data; Syntax for structured meaning and ontological injection; and Pragmatics for enforcing tool calls as authorized speech acts. We will connect the model to agentic MLOps and show how a Neural Proxy can provide this semantic background across models, agents, and enterprise systems.

## Why this talk?

Agentic systems are moving into production, but teams are discovering that retrieval quality and model capability do not solve the deeper problem: agents need to know what data means, which context applies, and whether an action is authorized. This talk gives MLOps and AI engineering practitioners a practical vocabulary for operating that context-to-action pipeline.

The session connects familiar production concerns—data provenance, schemas, access control, model routing, observability, and evaluation—to agent behavior. It also creates a useful distinction between RAG, which retrieves likely context, and semantic infrastructure, which governs meaning and action.

## Audience

AI engineers, MLOps engineers, platform engineers, data engineers, security engineers, and technical leaders responsible for deploying reliable agentic systems. The session assumes familiarity with APIs and production software systems, but not with any particular agent framework or ontology tool.

## Key takeaways

- Personalization is governed data access, not simply model memory.
- Vector similarity is retrieval infrastructure, not a complete semantic model.
- Lexicon, Syntax, and Pragmatics provide three practical layers for context engineering.
- Ontologies and structured definitions reduce ambiguity around entities and sensitive fields.
- Tool calls should be validated as actions with purpose, identity, and policy—not treated as free-form model output.
- Agentic MLOps must operate context, tools, policies, traces, and outcomes alongside models.
- A Neural Proxy or agentic middleware layer can preserve semantic and action rules across agents and model providers.

## Talk outline — 30 minutes

1. **The failure of AI memory — 5 minutes**
   - Why “remember more” does not solve wrong context or unauthorized action.
   - The context void and the thesis: personalization is governed data access.
2. **Three layers of Context Engineering — 12 minutes**
   - Lexicon: federated data, provenance, sovereignty, and identity-aware access.
   - Syntax: ontological injection and structured meaning.
   - Pragmatics: tool calls as speech acts and enforceable operations.
3. **Precision coaching example — 5 minutes**
   - A deadlift-carry coaching example showing semantic and pragmatic constraints.
4. **Building the infrastructure — 6 minutes**
   - Neural Proxy, BYOA, model agnosticism, traces, and policy evaluation.
5. **Conclusion and Q&A — 2 minutes**
   - From Prompt Engineering to Semantic Engineering.

## Relevant projects and technologies

Kubernetes, OpenTelemetry, Open Policy Agent, Model Context Protocol, LangChain, PydanticAI, vector databases, OAuth 2.0, and attribute-based access control. These are discussed as architectural building blocks, not as endorsements.

## Speaker information

- Email: captainnobody1@gmail.com
- First name: Miriah
- Last name: Peterson
- Job title: CEO
- Company: Haikai Labs
- Cell phone: [Add private contact number]
- Current location/city: [Confirm]
- Preferred pronoun: She/Her
- Bio photo URL: [Add public LinkedIn or photo URL]

## Speaker bio

Miriah Peterson is CEO of Haikai Labs, where she is building a Sovereign Context Layer for reliable AI. An engineer and educator focused on data engineering and AI infrastructure, she has built production systems at SchoolAI, Agility Ads, Weave, Tailscale, MX, and Nav. She created SoyPete Tech, teaches for Boot.dev and O'Reilly, and hosts Domesticating AI.

## Form responses

- Have you presented this talk, or related material before?: No / [Confirm before submission]
- If yes, where and when?: Not applicable unless the answer changes.
- Is anything being promoted?: Yes — Haikai Labs' Sovereign Context Layer and Neural Proxy, presented as an architectural pattern.
- Permission or organizational clearance: Yes / [Confirm]
- Agree to be recorded and share slides: Yes, to both / [Confirm]
- May the committee contact me about refinements?: Yes, that's fine!
- Relevant industries: Computer Software; Information Technology & Services; Banking & Financial Services; Hospital & Health Care; Insurance; Marketing & Advertising.

## Additional resources

- Lo Agent: https://github.com/IMJONEZZ/lo-agent
- Company website: [Add confirmed Haikai Labs URL]
- Speaker profile: [Add confirmed URL]
- Talk repository: [Add public repository URL]

## Proceedings contribution

- Willing to contribute insights to the official conference proceedings?: Yes

### Before → After State

Before, agents treated memory as unscoped retrieval: older conversations and semantically similar documents could be mixed with current context, even when they were stale or operationally incorrect. After, context is resolved through task classification, ontology, identity-aware retrieval, and validated tool calls. We evaluate the change through stale-context scenarios, retrieval comparisons, and action-validation tests rather than claiming production metrics we do not yet have.

### Core Building Blocks

- Task classification and intent resolution
- Federated data access
- Ontologies and entity definitions
- Scoped retrieval and provenance
- Attribute-based access control
- Structured tool definitions
- Pre-execution action validation
- Agentware / Neural Proxy
- Model routing and model abstraction
- Tracing, evaluation, and audit logs

### Concrete Takeaways

- Treat personalization as governed data access, not simply model memory.
- Do not assume vector similarity means operational relevance.
- Track which definitions, sources, and versions informed an answer.
- Inject structured ontology only when it is relevant to the current task.
- Treat tool calls as actions that require identity, purpose, and authorization.
- Keep policy enforcement outside the prompt and model reasoning.
- Evaluate the full context-to-action pipeline, not only generated text.
- Use model-agnostic middleware so semantics and policies survive model changes.

### Architecture / Workflow Description

```text
User request
     ↓
Task classification
     ↓
Ontology and entity resolution
     ↓
Identity-aware data retrieval
     ↓
Context assembly
     ↓
Model reasoning
     ↓
Tool-call validation
     ↓
ABAC / policy decision
     ↓
API execution
     ↓
Trace, evaluation, and audit
```

Agentware—the Neural Proxy or agentic middleware—sits between the agent and enterprise systems. It supplies relevant semantic context and memory, routes calls to approved data sources and tools, validates structured tool calls, and records outcomes.

### Failures, Trade-offs, or What Didn’t Work

- Treating conversation history as authoritative memory allowed stale decisions to resurface.
- Vector similarity alone retrieved related but operationally incorrect context.
- Putting all business rules into prompts made behavior difficult to test and enforce.
- Broad tools and unrestricted connectors increased the action surface unnecessarily.
- Centralizing all enterprise data into one memory store created governance and freshness concerns.
- Ontologies improve precision but require ongoing ownership, versioning, and maintenance.
- Stronger validation adds latency and implementation cost, but reduces the risk of incorrect actions.

### Tools / Models / Methods Used

- Lo Agent as a local agent-harness example
- LLM tool/function calling
- Retrieval-augmented generation
- Ontologies and semantic schemas
- Attribute-based access control
- API-based data connectors
- Agentware / Neural Proxy
- Structured tool calls for context retrieval and action execution
- Evaluation scenarios for stale context and unauthorized actions
- OpenTelemetry-style tracing and audit events
- Model-agnostic model routing

### Links to Repositories, Docs, or Write-ups

- Lo Agent: https://github.com/IMJONEZZ/lo-agent
- Haikai Labs website: [Add confirmed URL]
- Public write-up: [Add blog URL when published]
