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

**The reward for making an agent effective is a larger workload.**

---

## Utilization Changes the Economics

Then each job grows:

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

## Before: Local Capability Meant MoE

**Big capacity. Consumer economics. Sparse compute.**

```text
397B total parameters
       ↓ route each token
 17B active parameters
```

**Only the routed experts compute each token.**

<!-- Large dense models were a GPU economics problem: every weight had to be
available for every token, the full model needed enough fast memory, consumer VRAM
imposed a hard ceiling, and adding GPUs added cost and operational complexity.
MoE was the practical consumer path to big-model capacity. A router selects a subset
of experts per token, reducing active compute. Expert offloading can keep inactive
experts in CPU memory and move selected experts to GPU, but the full model still lives
somewhere and CPU-to-GPU transfer adds latency. MoE routes experts, not ordinary
transformer layers. Sources: https://arxiv.org/abs/2101.03961 and
https://arxiv.org/abs/2603.19289 -->

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

<!-- _class: lead -->

# Now: Small, Dense, and Actually Local

## 27B parameters · all active · one RTX 5090

**We genuinely do not know the ceiling yet.**

<!-- Qwen3.6-27B is a 27B dense model, post-trained for agentic coding and
structured tool use, and small enough to run on one high-end consumer GPU when
quantized. With a dense model, every model parameter participates in every token.
Source: https://huggingface.co/Qwen/Qwen3.6-27B -->

---

## What We Know Today

These models are:

1. **trained on tool calls** — not merely prompted into them
2. **fast** — fast enough for iterative agent loops
3. **available** — the weights and serving stack are ours to operate

---

## The Bet: Ask the Model to Infer Less

Good context engineering supplies:

- the exact task
- the smallest relevant context
- narrow tool schemas
- explicit workflow state
- machine-checkable success criteria

**Less ambiguity means less inference—which is exactly how a smaller model can do the job.**

Pedro Agentware is based on this premise—and on Forge's reliability pattern.

<!-- Forge: https://github.com/antoinezambelli/forge -->

---

<!-- _class: lead -->

# Pedro Agentware

## Forge, ported beyond Python

---

## 1. Preserve Native Tool Calling

```text
model-native tools → normalized call → your agent framework
```

- use the model's trained tool-call format
- preserve structured tool schemas
- normalize backend differences at the boundary

**Do not prompt a model to imitate a capability it already has.**

---

## 2. Port Zambelli's Guardrails

Forge makes self-hosted tool calls reliable with:

- **response validation** — reject unknown or malformed calls
- **rescue parsing** — recover structured calls emitted in the wrong format
- **corrective retries** — tell the model what failed and try again
- **step enforcement** — constrain ordering when a workflow needs it

Pedro Agentware ports that reliability pattern to **Go, Python, and TypeScript**.

<!-- Antoine Zambelli's Forge: https://github.com/antoinezambelli/forge -->

---

## 3. Abstract Context Compaction

```text
messages + tool results + token budget
                    ↓
       compact while preserving the job
```

- keep recent decisions and necessary tool state
- summarize or drop stale intermediate data
- fit the context to the model and hardware budget

**The harness manages the window so the smaller model can stay focused.**

---

## Real Agent #1: Pedro Tag in Discord

```python
async def start_game_tool(
    context: RunContext[AgentDeps], game_type: str
) -> str:
    """Start an interactive game with the user."""
    if game_type == "20_questions":
        game_lookup_id = context.deps.thread_id \
            or context.deps.channel_id
        # Create and persist the game state...
```

The agent receives `start_game_tool`; Discord supplies the conversation and thread state.

**LIVE: `@Pedro, play 20 Questions.`**

<!-- Real source: ~/code/pedro/pedro-tag/src/pedro_service/agent.py and
src/pedro_service/games/twenty_questions.py -->

---

## Real Agent #2: Reddit Recommendations

```python
def build_suggestion_agent():
    tools = [
        get_interesting_posts,
        get_trending_subreddits,
        send_discord_message,
    ]
    mw, _ = build_middleware()
    return create_react_agent(
        model=get_llm(), tools=apply_middleware(tools, mw),
        prompt=SystemMessage(content=SUGGESTION_SYSTEM_PROMPT),
    )
```

Local inference analyzes the week's results, then sends ranked subreddit and author recommendations to Discord.

<!-- Real source: ~/code/pedro/pedro-bots/src/core/agents/suggestion.py -->

---

## 📷 DISCORD OUTPUT PLACEHOLDER

# RedditWatch Weekly Suggestions

**DROP THE DISCORD RECOMMENDATIONS SCREENSHOT HERE**

- subreddits to consider adding
- authors to consider following
- one-line evidence from the week's classified posts

<!-- TODO: Replace with the real Discord output screenshot. -->

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

## Production Hosting: vLLM

Reach for vLLM when **GPU throughput and concurrency** matter.

- continuous batching
- request scheduling
- production metrics
- OpenAI-compatible API
- model-native tool parsing

**This is my default for a dedicated NVIDIA inference server.**

<!-- Source: https://docs.vllm.ai -->

---

## Production Hosting: llama.cpp

Reach for llama.cpp when **portability and hardware flexibility** matter.

- GGUF quantizations
- NVIDIA, AMD, Apple Silicon, CPU, and more
- lightweight server
- parallel decoding
- OpenAI-compatible function calling

**This is my default when the hardware or model format drives the decision.**

<!-- Source: https://github.com/ggml-org/llama.cpp -->

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

**Make inference infrastructure a first priority—or keep paying someone else to.**

---

## GPU Scheduling Is Hard

Everything interacts:

- model weights and KV cache compete for VRAM
- batching improves throughput but delays individual requests
- queues need priorities, limits, and backpressure
- failures can strand work or GPU capacity

**A fast model does not make a reliable serving system.**

---

## Keep the Control Plane on CPU

Pay for inexpensive, always-on CPU to handle:

- API, authentication, and request routing
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
4. Put validation, rescue, and corrective retries around tool calls.
5. Capture successful trajectories and train a toggleable LoRA.

---

<!-- _class: lead -->

# Miriah Peterson · @Soypete

## CEO & founder, stealth startup

## Co-host, **Domesticating AI** podcast

---

<!-- _class: lead -->

# If Asked: What About Model Quality?

## Model-quality comparisons are not the focus of this talk.

The question here is whether the smallest reliable model can complete **your defined job** at the utilization and cost you need.

<!-- Use this appendix slide only if the question comes up after the outro. -->
