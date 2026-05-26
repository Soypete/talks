---
marp: true
theme: gaia
paginate: true
title: "Bigger Isn't Better: The Right-Sized Model Revolution"
backgroundImage: url('../images/soypete_background.png')
description: Why specialized smaller models with guardrails beat expensive frontier models
---

<!-- _class: lead -->

# Bigger Isn't Better

## The Right-Sized Model Revolution for AI Agents

by Miriah Peterson
@Soypete

---

## Who Am I?

- AI/ML Infrastructure Engineer at SchoolAI
- Creator: Pedro CLI, MemPalace, Graphify, custom skills
- Building agent systems since 2022
- Running local models on consumer hardware

![bg right:40%](../images/SP_Logo-02.png)

---

<!-- _class: lead -->

# PART 1: THE PROBLEM

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

## The Hidden Cost of "Best" Models

### The math doesn't add up:

- Claude Opus: $15/M tokens → $2.50 per simple request
- GPT-4o: $2.50/M tokens → $0.50 per request  
- MiniMax: $0.40/M tokens → $0.01 per request

> "We built agents to save time. Now they cost more than the developers they replace."

---

## The Real Problem

### We're using sledgehammers for everything:

- Rename a variable? → Full reasoning model
- Write a test? → Multiple coordinating agents
- Fix a bug? → Send entire codebase in context

**Bigger is NOT better when context engineering handles the complexity**

---

## The Key Insight

### The industry is waking up:

> "Given a proper harness, small local models can perform incredibly well. When you have a system that can try everything, it will eventually get it right as long as you can prevent it from getting it wrong in the meantime."

**— HN Comment on Forge (ACM CAIS 2026)**

---

<!-- _class: lead -->

# PART 2: THE SOLUTION

---

## The New Paradigm

### Not "bigger model" → "right-sized model + guardrails"

```
┌─────────────────────────────────────────────────────────┐
│              Old Approach                               │
│  Request → [72B General Model] → Response              │
│            $2.50, 60 seconds, 250k tokens              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              New Approach                               │
│  Request → [8B Specialized + Guardrails] → Response    │
│            $0.01, 3 seconds, 8k tokens                 │
└─────────────────────────────────────────────────────────┘
```

---

## What Changed: 16 Parallel Sessions on a Pi

### Consumer hardware can now scale:

![bg right](https://pbs.twimg.com/media/GuBqNq5WAAA5pEM?format=jpg&name=medium)

- NVIDIA demo: 16 concurrent agent sessions on Raspberry Pi
- Small models enable parallelism that big models can't
- Cost per task drops with horizontal scaling

---

## What Changed: Forge Guardrails

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

## Bigger Isn't Better: Qwen3.6-27B Evidence

### From Hacker News benchmarks:

- Qwen 3.5-4B does simple coding tasks perfectly
- 3x faster, 9x cheaper than "best" models
- Speed enables real-time interactive usage

> "The right model depends on the job. Big models still shine in vague contexts or for breadth, but the small ones just need help on longer multi-step workflows."

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

## Context Engineering: MemPalace Skill

### Your custom skills enable right-sized models:

```python
# MemPalace: Semantic memory with Wing/Room/Drawer hierarchy
/mempalace init ~/code/project    # Initialize palace
/mempalace watch ~/code           # Auto-mine on changes
/mempalace query "How does auth work?"  # Semantic search
```

**Quality context > quantity of tokens**

---

## Context Engineering: Graphify Skill

### Turn codebase into navigable knowledge graph:

```
/graphify ~/code/project          # Full pipeline
/graphify query "How does X connect to Y?"  # Graph traversal
/graphify path "AuthModule" "Database"  # Shortest path
```

**Extract relationships, not dump entire files**

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

<!-- _class: lead -->

# PART 3: THE DEMONSTRATION

---

## Pedro CLI with MiniMax

### Live coding with right-sized model:

```go
func (p *PedroCLI) Run(ctx context.Context) error {
    for {
        input := p.readInput()
        
        // Route to right-sized model
        model := p.selectModel(input)
        
        // Build minimal context (not entire codebase)
        context := p.buildContext(input)
        
        // Call MiniMax (~2s, ~$0.01)
        response := model.Complete(ctx, context, input)
        
        // Execute tool calls
        for _, tc := range response.ToolCalls {
            p.executeTool(tc)
        }
    }
}
```

---

## Context with MemPalace

### Not "how much" but "what matters":

```python
# Don't: Send everything (50k tokens)
messages = [
    {"role": "system", "content": entire_codebase},
    {"role": "user", "content": user_request},
]

# Do: Send only what's relevant (2k tokens)
messages = [
    {"role": "system", "content": relevant_docs},  # MemPalace retrieval
    {"role": "system", "content": function_signature},
    {"role": "user", "content": user_request},
]
```

---

## Guardrails in Action

### Structured tool calling:

```json
{
  "tool": "edit_file",
  "arguments": {
    "file_path": "src/main.go",
    "old_string": "func foo() {",
    "new_string": "func bar() {"
  }
}
```

**With Forge: automatic retry on malformed JSON, schema validation**

---

## The Takeaway

### Bigger isn't better

### Right-sized + guardrails + context engineering = frontier results at 2% of the cost

---

<!-- _class: lead -->

# SUMMARY

---

## What We Learned

### Problem
- Agent swarms burn massive tokens ($2-50/request)
- Latency kills productivity
- Diminishing returns on bigger models

### Solution
- Right-sized specialized models (7-8B)
- Guardrails (Forge pattern) for reliability
- Context engineering (MemPalace, Graphify)
- Parallel execution on consumer hardware

### Demonstration
- Pedro CLI with MiniMax
- 97% cost reduction
- Acceptable quality tradeoffs

---

## For Engineering Leaders

1. **Audit your agent costs** — You might be shocked
2. **Try small + guardrails** — 97% savings is worth the experiment
3. **Build escalation paths** — Small first, big when needed

---

## For Platform Engineers

1. **Serving backend matters** — 75 point swings possible
2. **Guardrails are infrastructure** — Not optional
3. **Parallelize horizontally** — 16 sessions on a Pi

---

## For Agent Framework Maintainers

1. **Default to smaller models** — Don't assume everyone needs GPT-4
2. **Build guardrails in** — Retry, recovery, validation
3. **Measure everything** — Token burn, latency, reliability

---

## Open Source

- [Pedro CLI](https://github.com/soypete/pedro-cli) — Agent with MiniMax
- [MemPalace](https://github.com/soypete/mempalace) — Semantic memory
- [Graphify](https://github.com/soypete/graphify) — Knowledge graphs
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