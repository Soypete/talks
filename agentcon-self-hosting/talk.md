---
marp: true
theme: gaia
paginate: true
title: "Self-Hosting Agents: What Changes When Models Become Infrastructure"
backgroundImage: url('../images/soypete_background.png')
description: Operational lessons from running open models in self-hosted agent systems
---

<!-- _class: lead -->

# Self-Hosting Agents

## What Changes When Models Become Infrastructure

by Miriah Peterson
@Soypete

---

## Who Am I?

- AI/ML Infrastructure Engineer at SchoolAI
- Creator: Pedro CLI, Pedro Agentware, MemPalace, Graphify
- Building agent systems since 2022
- Running open models on local and homelab infrastructure
- Interested in what happens when AI becomes normal infrastructure

![bg right:40%](../images/SP_Logo-02.png)

---

<!-- _class: lead -->

# PART 1: THE API HIDES THE SYSTEM

---

## Hosted APIs Make Agents Look Simple

```
User request
  → hosted model API
  → tool call
  → response
```

The API hides the hard parts:

- model loading
- GPU scheduling
- memory pressure
- retries
- routing
- observability
- cost accounting
- failure recovery

---

## Agents Break the Illusion

A chatbot can fail once.

An agent can fail 40 times in a loop.

Agent systems expose every hidden reliability problem:

- malformed tool calls
- invalid JSON
- bad context
- repeated retries
- slow inference
- missing observability
- expensive long-running workflows

---

<!-- _class: lead -->

# PART 2: WHAT SELF-HOSTING EXPOSES

---

## The Model Becomes Part of the Platform

When you self-host, the model is no longer an API dependency.

It becomes infrastructure you operate.

That means you own:

- latency
- throughput
- GPU memory
- model selection
- serving backend behavior
- evaluation
- reliability
- cost

---

## GPU Memory Is a Product Constraint

With hosted APIs, context length feels like a product feature.

With self-hosted models, context length is infrastructure pressure.

Every extra token competes with:

- batch size
- concurrency
- model size
- KV cache
- latency
- throughput

---

## Throughput vs Latency

Self-hosted inference forces tradeoffs:

| Goal | What You Optimize | What You Risk |
|---|---|---|
| Low latency | small model, short context | lower capability |
| High throughput | batching, queues | slower user feedback |
| Better quality | larger model, more context | VRAM pressure |
| More concurrency | smaller models | more routing complexity |

---

<!-- _class: lead -->

# PART 3: WHY AGENTS MAKE THIS HARDER

---

## Open Models Behave Differently in Agent Workflows

A model can look good in chat and still fail as an agent.

Agent workflows require:

- structured output
- tool-call consistency
- schema discipline
- multi-step planning
- context stability
- recovery from partial failure

---

## Quantization Is Not Free

Quantization makes self-hosting possible.

It can also change behavior.

You have to evaluate:

- tool-call format stability
- reasoning consistency
- latency gains
- memory savings
- failure modes
- task-specific accuracy

---

## Reliability Moves Outside the Model

Hosted APIs encourage us to ask:

> Which model is smart enough?

Self-hosted agents force a better question:

> What system makes the model reliable enough?

Reliability comes from:

- retries
- schema validation
- tool constraints
- context routing
- eval harnesses
- failure recovery

---

## The Real Problem

We're using sledgehammers for everything:

- Rename a variable? → Full reasoning model
- Write a test? → Multiple coordinating agents
- Fix a bug? → Send entire codebase in context

**Bigger is NOT better when context engineering handles the complexity**

---

<!-- _class: lead -->

# PART 4: LESSONS FROM PEDRO

---

## Case Study: Pedro CLI

Pedro started as a CLI.

Then it became an agent system.

That changed the engineering problem:

- command execution
- tool calling
- model routing
- context assembly
- workflow state
- evaluation
- observability

---

## What Failed

The hard parts were not the demo moments.

The hard parts were:

- repeated bad tool calls
- context that was close but wrong
- models that changed behavior under quantization
- missing state between steps
- debugging agent behavior after the fact
- knowing whether a run actually succeeded

---

## What Worked

The useful pattern was not "use a bigger model."

It was:

- smaller task scope
- better context packets
- stricter tools
- retry logic outside the model
- evals for known workflows
- observability around agent behavior

---

## The Key Insight

> "Given a proper harness, small local models can perform incredibly well. When you have a system that can try everything, it will eventually get it right as long as you can prevent it from getting it wrong in the meantime."

**— HN Comment on Forge (ACM CAIS 2026)**

---

## Forge Guardrails

### The breakthrough (ACM CAIS 2026):

| Model | Without Forge | With Forge |
|-------|---------------|------------|
| **Ministral 8B** | 53% | **99.3%** |
| Claude Sonnet | 87.2% | 100% |
| Mistral-Nemo 12B (llama.cpp) | 7% | 83% |

**Key insight: The serving backend matters 75 points!**

---

## How Forge Works

### Five guardrail layers:

1. **Retry nudges** — 24-49 point drops when disabled
2. **Error recovery** — ~10 point gains
3. **Step enforcement** — Conditional workflow ordering
4. **Rescue parsing** — Fix malformed tool calls
5. **Context compaction** — VRAM-aware token budgets

---

## Why It Works

### Guardrails do what bigger models do internally:

```
Without guardrails:
  Agent → Tool Call → Fail → Dead end

With guardrails:
  Agent → Tool Call → Fail → "You called the wrong tool" → Retry
  Agent → Tool Call → Fail → "JSON malformed" → Retry
  Agent → Tool Call → Success → Continue
```

**Small model + guardrails ≈ big model without the cost**

---

## The Serving Backend Surprise

### Same model, different backends:

| Backend | Accuracy (Mistral-Nemo 12B) |
|---------|------------------------------|
| llama.cpp (native function calling) | 7% |
| Llamafile (prompt mode) | 83% |
| Ollama | ~30% |

**75 point swing from infrastructure alone**

---

## The Token Budget Crisis

### What's happening in production:

```
User Request → Agent Swarm → $2.50/request, 250k tokens, 60s latency
```

| Metric | Frontier API | Local Small Model |
|--------|--------------|-------------------|
| Cost/task | $2.50 | $0.01 |
| Latency | 60s | 3s |
| Tokens/task | 250k | 8k |

**Your agent system might be the most expensive part of your stack**

---

## Context Engineering: MemPalace

### Your custom skills enable right-sized models:

```python
# MemPalace: Semantic memory with Wing/Room/Drawer hierarchy
/mempalace init ~/code/project    # Initialize palace
/mempalace watch ~/code           # Auto-mine on changes
/mempalace query "How does auth work?"  # Semantic search
```

**Quality context > quantity of tokens**

---

## Context Engineering: Graphify

### Turn codebase into navigable knowledge graph:

```
/graphify ~/code/project          # Full pipeline
/graphify query "How does X connect to Y?"  # Graph traversal
/graphify path "AuthModule" "Database"  # Shortest path
```

**Extract relationships, not dump entire files**

---

<!-- _class: lead -->

# PART 5: PRACTICAL ARCHITECTURE

---

## A Practical Self-Hosted Agent Architecture

```
Request
  → classify task
  → assemble scoped context
  → route to right-sized model
  → validate tool calls
  → execute workflow
  → evaluate result
  → escalate when needed
```

The model is only one component.

---

## The Hybrid Architecture

### Production-ready pattern:

```python
def handle_request(request):
    # Step 1: Use right-sized model with guardrails
    result = small_model.complete(request)
    
    # Step 2: Check confidence
    if result.confidence < 0.7:
        # Step 3: Escalate only when needed
        return frontier_model.complete(request)
    
    return result
```

**80% handled by small model, 20% escalated**

---

## When Self-Hosting Makes Sense

Self-hosting is worth considering when you need:

- data control
- fixed infrastructure costs
- low-latency local workflows
- custom routing
- open model experimentation
- agent observability
- infrastructure ownership

---

## When Self-Hosting Does Not Make Sense

Do not self-host just because it feels cooler.

Hosted APIs may be better when you need:

- fastest path to product
- broad model capability
- minimal infra ownership
- managed scaling
- fewer operational responsibilities

---

## The Results

### Real production numbers:

| Metric | Before | After |
|--------|--------|-------|
| Token consumption | 250k/task | 8k/task |
| Latency | 45s | 3s |
| Cost | $2.50/task | $0.02/task |
| Reliability | 70% | 95% |

**97% cost reduction, acceptable quality tradeoffs**

---

## Bigger Isn't Better: Qwen3.6-27B Evidence

### From Hacker News benchmarks:

- Qwen 3.5-4B does simple coding tasks perfectly
- 3x faster, 9x cheaper than "best" models
- Speed enables real-time interactive usage

> "The right model depends on the job. Big models still shine in vague contexts or for breadth, but the small ones just need help on longer multi-step workflows."

---

## The Takeaway

### The model is not the system.

Self-hosting agents forces you to build the system:

- serving
- routing
- context
- tools
- retries
- evals
- observability

**Self-hosting agents forces us to stop treating models like magic APIs and start treating them like infrastructure.**

---

## Open Source

- [Pedro CLI](https://github.com/soypete/pedro-cli) — Agent with MiniMax
- [MemPalace](https://github.com/soypete/mempalace) — Semantic memory
- [Graphify](https://github.com/soypete/graphify) — Knowledge graphs
- [Pedro Agentware](https://github.com/anomalyco/pedro-agentware) — Agent middleware
- [Forge](https://github.com/antoinezambelli/forge) — Guardrails (ACM CAIS 2026)

---

## References

- [Forge: Guardrails for Small Models](https://news.ycombinator.com/item?id=48192383)
- [I Replaced Claude Code with MiniMax](https://soypetetech.substack.com)
- [Agent Cost Analysis](https://soypetetech.substack.com)
- [Context Engineering Best Practices](https://soypetetech.substack.com)

---

<!-- _class: lead -->

# Questions?

## Miriah Peterson
### @Soypete