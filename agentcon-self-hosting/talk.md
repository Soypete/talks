---
marp: true
theme: gaia
paginate: true
title: "Self-Hosting Agents: Small Dense Models Change the Math"
backgroundImage: url('../images/soypete_background.png')
description: What changes when fast, tool-trained dense models become local infrastructure
---

<!-- _class: lead -->

# Self-Hosting Agents

## Small Dense Models Change the Math

Miriah Peterson · @Soypete<br>
TODO_CONFERENCE_NAME · Friday

---

## Who Am I?

- CEO & founder of a stealth startup
- Co-host of the **Domesticating AI** podcast
- Creator of Pedro Agentware
- Building agent systems since 2022
- Running open models on local and homelab infrastructure

![bg right:40%](../images/SP_Logo-02.png)

---

## Hosted APIs Make Agents Look Simple

```text
request → model API → tool call → result
```

The API hides:

- model loading and memory pressure
- GPU scheduling and concurrency
- retries, routing, and failure recovery
- latency, observability, and cost accounting

**Self-hosting makes the hidden system your system.**

---

## Agents Break the Illusion

A chatbot can fail once.

An agent can fail 40 times in a loop.

- malformed tool calls
- invalid arguments
- repeated retries
- runaway context
- partial side effects

**The model is only one component in the reliability boundary.**

---

<!-- _class: lead -->

# The Local Model Just Changed

---

## Before: Local Capability Meant MoE

Mixture-of-Experts models made large *total* parameter counts practical.

But each token activates only a subset of the experts:

```text
397B total parameters
       ↓ route each token
 17B active parameters
```

You store the whole model; each token uses only part of it.

<!-- Speaker note: MoE does not mean fewer transformer layers. The tradeoff is
sparse expert activation: fewer parameters participate in each token. -->

---

## Now: Small, Dense, and Actually Local

With a dense model, **every model parameter participates in every token**.

Qwen3.6-27B is:

- 27B dense parameters
- post-trained for agentic coding
- trained for structured tool use
- small enough to run on one high-end consumer GPU when quantized

We genuinely do not know the ceiling yet.

<!-- Source: https://huggingface.co/Qwen/Qwen3.6-27B -->

---

<!-- _class: lead -->

# 🎬 VIDEO PLACEHOLDER

## Christopher TODO_SURNAME

> “We are kids in a candy store.”

**DROP SHORT VIDEO CLIP HERE**

<!-- TODO: Replace this entire slide with the clip or a poster frame. -->

---

## What We Know Today

These models are:

1. **trained on tool calls** — not merely prompted into them
2. **fast** — fast enough for iterative agent loops
3. **available** — the weights and serving stack are ours to operate

Model-quality comparisons are not the point of this talk.<br>
**TODO: confirm that this one-line aside is the right framing.**

---

## The Bet: Ask the Model to Infer Less

Good context engineering supplies:

- the exact task
- the smallest relevant context
- narrow tool schemas
- explicit policy and workflow state
- machine-checkable success criteria

**Less ambiguity means less inference—which is exactly how a smaller model can do the job.**

---

<!-- _class: lead -->

# Pedro Agentware

## Policy enforcement at the tool-call boundary

---

## The Boundary, Not Another Agent

```text
agent proposes tool call
          ↓
 Pedro Agentware evaluates policy
      ↙ allow     deny ↘
 execute        explain + recover
```

- deterministic controls outside the model
- the same policy idea across Go, Python, and TypeScript
- audit the decision before a side effect occurs

**The model proposes. Policy disposes.**

---

## Go: Wrap the Dangerous Tool

```go
// Conceptual API sketch
guardedShell := agentware.Protect(shellTool,
    agentware.DenyArgs("rm", "--force"),
    agentware.RequireWorkspacePath(),
)

result, err := guardedShell.Call(ctx, toolCall)
```

Same pedagogical shape: one tool call in, one result out.<br>
New subject: **policy is checked before execution.**

---

## Python: Make Policy Composable

```python
# Conceptual API sketch
guarded_write = protect(
    write_file,
    policies=[workspace_only(), deny_secrets()],
)

result = await guarded_write(tool_call)
```

Framework adapters can change. The enforcement point does not.

---

## TypeScript: Keep the Audit Trail

```ts
// Conceptual API sketch
const guardedFetch = protect(fetchTool, {
  policies: [allowHosts(["api.internal"]), denyPrivateIPs()],
  audit: true,
});

const result = await guardedFetch(toolCall);
```

For long-running agents, **why a call ran** matters as much as what ran.
