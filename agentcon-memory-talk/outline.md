# MLOps World CFP Submission: Beyond AI Memory

**Target event:** MLOps World  
**Track recommendation:** AI Engineering / Production Reliability / Data Governance  
**Strategic goal:** Position Haikai as the essential “Semantic Background” for production agents, moving the industry from prompt engineering to semantic engineering.

## 1. CFP Submission

### Title

Beyond AI Memory: Why Semantic Context is the Missing Layer in Agentic Infrastructure

### Description

Current agentic frameworks rely on generic harnesses that infer intent, leading to hallucinations and security breaches. This talk argues that personalization is not something the model should “remember”; it is governed data access.

We will dissect the failure of vector-based “memory” systems in production, where agents retrieve semantically nearby but operationally wrong context. Instead, we introduce Context Engineering: a pipeline that classifies tasks, retrieves scoped data via ontological injection, enforces ABAC permissions, and validates actions before execution.

Attendees will learn how to move personalization out of the prompt and into infrastructure using three layers:

1. **Lexicon (Data Sovereignty):** Ensure data stays federated and access is identity-aware.
2. **Syntax (Semantic Precision):** Inject structured meaning so models do not guess what entities such as “SSN” or “Patient History” mean.
3. **Pragmatics (Speech Acts):** Enforce rigid tool definitions to prevent unauthorized actions.

This session provides a practical model for building agents that personalize behavior through structured state and explicit semantics, eliminating the “Context Void” and improving reliability in regulated environments.

### Why This Talk?

- **Solves a real problem:** MLOps engineers are struggling with retrieval accuracy and security; this offers a structural solution rather than another tool.
- **Category creation:** Introduces Haikai’s core differentiator—lexicon, semantics, and pragmatics—to an audience that needs reliability and precision.
- **Vendor-neutral but Haikai-aligned:** The talk presents an architectural pattern that maps directly to Haikai’s Neural Proxy capabilities.

## 2. Talk Outline and Key Talking Points

### Introduction: The Failure of “AI Memory” — 5 minutes

- Open with an agent retrieving semantically nearby but operationally wrong data.
- Current agents operate in a Context Void: they guess at meaning because they lack structured background information about data sensitivity and tool usage.
- Thesis: personalization is not memory; it is governed data access.

### Part 1: The Three Layers of Context Engineering — 15 minutes

#### Layer 1: Lexicon (Data Sovereignty)

- Explain why data consolidation is a trap for enterprises.
- Introduce federated data sovereignty: connect to data where it lives without storing or training on it.
- Key concept: ABAC-enforced access control at the tool-call level.

#### Layer 2: Syntax (Semantic Precision)

- Explain how models hallucinate because they do not know what “SSN” means in a specific organizational context.
- Introduce ontological injection: dynamically inject structured relationships so the model understands entity importance.

#### Layer 3: Pragmatics (Speech Acts)

- Explain why sandboxes are insufficient: they restrict where an agent runs, not whether an action is appropriate.
- Introduce pragmatic enforcement: validate tool arguments against business rules before execution.

### Part 2: The “Light Vertical” Proof—Precision Coaching — 10 minutes

- Case study: AI-powered physical-therapy coaching for deadlifts.
- Semantics in action: the agent understands biomechanical terms such as “form breakdown” and “RPE” because they are explicitly defined in the ontology.
- Pragmatics in action: the system enforces safe weight limits and stops unsafe movements through rigid tool definitions, not guesswork.
- Takeaway: generic AI coaches guess; agents with a semantic background understand.

### Part 3: Building the Infrastructure — 10 minutes

- Introduce the Neural Proxy: middleware between the agent and the world that enforces the three layers.
- Bring Your Own Agent: the context layer works with any agent framework and any model.
- Model agnosticism: swapping models does not remove security or business logic because enforcement lives in infrastructure.

### Conclusion: The Future of Agentic Infrastructure — 5 minutes

- Move from prompt engineering to semantic engineering.
- Keep enterprise data sovereign and provide a governed background for intelligent action.
- Final thought: an agent without structured data, semantics, and pragmatics is guessing at intent. It needs a semantic background to act with precision and safety.

## 3. Strategic Notes for Delivery

- **Archetype:** Maintain a Sage tone—wise, precise, and foundational. Avoid hype; focus on structural integrity and reliability.
- **Counterpoint:** Critique frontier-model data monopolies and generic harnesses that infer intent without turning the session into a product pitch.
- **Visual metaphor:** A foreground shape—the agent—emerging from a rich, structured background pattern, or *haikei*.
- **Q&A:** “How is this different from RAG?” RAG retrieves data. A semantic context layer also governs meaning, permission, and action.
