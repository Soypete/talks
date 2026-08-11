---
marp: true
theme: gaia
paginate: true
title: "Self-Hosting Agents: Small Dense Models Change the Economics"
description: When sustained agent token use makes efficient local inference a first-class infrastructure concern
---

<!-- _class: lead -->

# Self-Hosting Agents

## Small Dense Models Change the Economics

Miriah Peterson · @Soypete<br>
AI Builder Day · August 14, 2026

---

## Who Am I?

- CEO & founder of a stealth startup
- Co-host of the **Domesticating AI** podcast
- Creator of Pedro Agentware
- Building agent systems since 2022
- Running open models on local and homelab infrastructure

---

## Effective Agents Are Token Engines

```text
observe → reason → tool call → result
   ↑                              ↓
   └──────────── repeat ──────────┘
```

Agents spend tokens on every:

- decision
- tool result
- retry and recovery
- context refresh
- verification step

**The useful unit is not cost per prompt. It is cost per completed job.**

---

## Success Creates Utilization

Once an agent reliably completes a job, you want more of it:

- more jobs
- more frequent runs
- longer workflows
- more tools and verification
- eventually: always available

```text
useful agent → more runtime → more tokens → recurring API spend
```

**At sustained utilization, inference economics become architecture.**

---

<!-- _class: lead -->

# The Local Model Just Changed

---

## Why We Hosted MoE

For frontier-ish capability, large dense models were a GPU economics problem:

- every weight had to be available for every token
- the full model needed enough fast memory
- consumer VRAM imposed a hard ceiling
- adding GPUs added cost and operational complexity

**MoE was the practical consumer path to big-model capacity.**

---

## What MoE Bought Us

A router selects only a subset of experts for each token:

```text
397B total parameters
       ↓ route each token
 17B active parameters
```

That means less active compute per token.

With expert offloading, inactive experts can live in CPU memory while selected experts move to the GPU.

**The full model still lives somewhere; CPU↔GPU transfer becomes the tradeoff.**

<!-- Speaker note: MoE does not mean fewer transformer layers. The tradeoff is
sparse expert activation: fewer parameters participate in each token. Offloading is
an inference implementation choice and introduces transfer latency. Sources:
https://arxiv.org/abs/2101.03961 and https://arxiv.org/abs/2603.19289 -->

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

# “We Are Kids in a Candy Store”

<iframe
  width="315"
  height="560"
  src="https://www.youtube.com/embed/ljxaBcd5zx8"
  title="We are kids in a candy store"
  frameborder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
  allowfullscreen>
</iframe>

**Small dense models have opened a new design space.**

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

---

<!-- _class: lead -->

# One GPU, Real Agents

## Qwen3.6-27B · RTX 5090 · my house

The experiment is operational: **can ordinary agent stacks use this as infrastructure?**

---

## 🎬 BENCHMARK VIDEO PLACEHOLDER

### Over the wire

```text
conference laptop
      ↓ internet
home inference endpoint
      ↓
Qwen3.6-27B on RTX 5090
```

**DROP OVER-THE-WIRE BENCHMARK VIDEO HERE**

<!-- TODO: Include latency, prompt tokens/sec, and generation tokens/sec overlay. -->

---

## 🎬 BENCHMARK VIDEO PLACEHOLDER

### Local network / on-box

```text
agent → OpenAI-compatible endpoint → local GPU
```

**DROP LOCAL BENCHMARK VIDEO HERE**

The delta tells us what is inference—and what is the network.

<!-- TODO: Use the same prompt and generation settings as over-the-wire. -->

---

## PydanticAI: Point the Agent Home

```python
provider = OpenAIProvider(
    base_url="https://home.example/v1",
    api_key="local",
)
model = OpenAIModel("Qwen/Qwen3.6-27B", provider=provider)
agent = Agent(model, tools=[guarded_write, guarded_shell])

result = agent.run_sync("Fix the failing test")
```

Typed tools and outputs; local inference behind a familiar API.

<!-- API shape: https://ai.pydantic.dev/models/openai/ -->

---

## LangChain DeepAgents: Same Endpoint, Longer Loop

```python
model = init_chat_model(
    "openai:Qwen/Qwen3.6-27B",
    base_url="https://home.example/v1",
    api_key="local",
)
agent = create_deep_agent(
    model=model,
    tools=[guarded_write, guarded_shell],
)

agent.invoke({"messages": [{"role": "user", "content": task}]})
```

Planning changes the workload—not the serving contract.

<!-- API shape: https://docs.langchain.com/oss/python/deepagents/overview -->

---

## Production Inference Hosting

| | **vLLM** | **llama.cpp** |
|---|---|---|
| Reach for it when | GPU throughput and concurrency matter | GGUF portability and hardware flexibility matter |
| Production strengths | batching, scheduling, metrics | small footprint, broad backends, parallel decoding |
| Agent interface | OpenAI-compatible API + tool parsing | OpenAI-compatible API + function calling |

**These are the two production-grade defaults I would start from.**

<!-- Sources: https://docs.vllm.ai and https://github.com/ggml-org/llama.cpp -->

---

## Development Tools Deserve Their Place

**Ollama** and **LM Studio** are great for development:

- download a model quickly
- compare quantizations
- test prompts and tool templates
- give a team a friendly local on-ramp

I would not run either as my production serving layer.

**Unsloth Studio desktop** is also not production serving—but keep it nearby. We will come back to it.

---

## The Economics Work—For the Right Job

### Pros

- A reliable agent creates sustained token demand.
- For long-term use, self-hosting is cheaper for **well-defined jobs**.
- Fixed infrastructure replaces recurring per-token rent.
- Better context engineering makes the model infer less.
- Smaller models become viable because the system carries more of the burden.

**Known workload + high utilization + efficient small model = a compelling local case.**

---

## The GPU Is Still Infrastructure

### Cons

- A rented cloud GPU is unreasonable unless you can keep it busy roughly **24 hours a day**.
- If utilization is bursty, you need a cycling story: start, warm, drain, and stop.
- Cold starts and model loading become product latency.
- GPU scheduling is hard: memory, queues, batching, priorities, and failure recovery all interact.

**Make inference infrastructure a first priority—or keep paying someone else to.**

---

## Keep the Control Plane on CPU

Pay for inexpensive, always-on CPU to handle:

- API, authentication, and policy
- queues, context assembly, and scheduling
- health checks and GPU lifecycle

**Keep the agent available without paying GPU rates while it waits.**

<!-- Further reading: https://northflank.com/blog/runpod-vs-modal -->

---

## Cycle the GPU Around the Work

```text
request → CPU queue → wake GPU → batch inference → drain → stop GPU
```

- queue enough work to justify the start
- batch requests to raise utilization
- drain cleanly before shutdown
- release the expensive capacity when idle

**Model loading becomes a cold-start budget you must design around.**

<!-- Further reading: https://northflank.com/blog/runpod-vs-modal -->

---

## LoRAs Are the Natural Extension of Tool Calls

Once agents run long enough, they produce labeled data:

```text
task + context + tool calls → successful result
```

Train a LoRA on those successful trajectories:

- improve accuracy on the job you actually run
- reduce the context shipped with every request
- toggle the adapter on and off—no separate always-on model cost

**Unsloth Studio is the on-ramp from agent traces to the first adapter.**

---

<!-- _class: lead -->

# Next Steps

1. Measure one reliable agent job: tokens, runtime, and frequency.
2. Find the smallest efficient model that completes it.
3. Keep the control plane on CPU; cycle and saturate the GPU.
4. Put policy enforcement around every tool call.
5. Capture successful trajectories and train a toggleable LoRA.

---

<!-- _class: lead -->

# Miriah Peterson · @Soypete

## CEO & founder, stealth startup

## Co-host, **Domesticating AI** podcast
