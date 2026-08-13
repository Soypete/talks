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
- Building AI systems since 2022

---

<!-- _class: lead -->

# What Is an Agent?

```text
observe → decide → call a tool → inspect the result
   ↑                                      ↓
   └──────────────── repeat ──────────────┘
```

## A model running inside a loop

<!-- A chat response is usually one inference. An agent keeps returning to the
model between actions. The harness—not the model alone—owns tools, state, retries,
and the stopping condition. -->

---

## What Do Agents Enable?

| Stage | Agent behavior |
|---|---|
| **One-off** | complete a task while I wait |
| **Background** | run a workflow without me watching |
| **Autonomous** | notice, decide, act, and recover |
| **Always on** | keep doing the job whenever work appears |

**The value grows as the agent needs less of my attention.**

<!-- Start with the familiar one-off coding or research agent. Background agents
run on a schedule or queue. Autonomous agents decide which actions to take and how
to recover. The end state is not one magical run; it is a dependable worker that is
available whenever new work arrives. -->

---

## From One-Off to Always On

```text
prompted once → scheduled → event-driven → continuously available
```

An always-on agent needs:

- durable state between runs
- tools it can call without supervision
- recovery when a step fails
- inference whenever new work arrives

**The agent stops being a feature and becomes infrastructure.**

<!-- Do not discuss cost yet. Establish the operational change: one-off agents can
borrow an endpoint for a moment; always-on agents depend on inference as a persistent
part of the system. Availability, state, recovery, and scheduling now matter. -->

---

<!-- _class: lead -->

# Always Means Always

![width:620px](https://media.giphy.com/media/v1.Y2lkPWVjZjA1ZTQ3NjBuM3NmdnhlMzIybW45YWJmbHRhbDV4NHZvcHphaTNvOW9pN2czbiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/TdwziQPhbNAzK/giphy.gif)

## What happens when the agent never clocks out?

<!-- Let the GIF breathe. The point is not that every agent must run in a hot loop.
It is that useful automation creates demand for an agent that is ready continuously,
whether triggered by a message, schedule, queue, webhook, or new data. -->

---

<!-- _class: lead -->

# The Problem

## “Always on” means a model is running somewhere

| You pay | The provider pays |
|---|---|
| tokens on every turn | compute for every token |
| repeated agent loops | accelerators and memory |
| availability | idle capacity and scheduling |

## Someone is always paying for the inference.

<!-- This is the pivot. For the customer, metered tokens turn agent activity into
recurring spend. For the provider, each token consumes accelerator time, memory
bandwidth, capacity, cooling, and power. Providers therefore have the same incentive
we do: reduce the compute required per token. That incentive helped push MoE models
into the mainstream. -->

---

## MoE: More Capacity, Less Compute per Token

Instead of using every parameter for every token, a router selects a few experts:

```text
397B total parameters
       ↓ route each token
 17B active parameters
```

**Providers serve a more capable model without activating the whole model each time.**

**Local hosts can keep inactive experts in system RAM and move selected experts through the GPU.**

<!-- MoE expands total capacity without making every token pay for every expert.
This lowers active compute, which matters at provider scale. It also made surprisingly
powerful models accessible to local hosts: the complete quantized model can live in
larger, cheaper CPU memory while only routed experts are staged through limited GPU
VRAM. The tradeoff is CPU-to-GPU transfer latency and bandwidth. Shared attention and
other non-expert layers still run; MoE routes expert feed-forward blocks, not arbitrary
transformer layers. Sources: https://arxiv.org/abs/2101.03961 and
https://arxiv.org/abs/2603.19289 -->

---

<!-- _class: lead -->

# “We Are Kids in a Candy Store”

> “We are kids in a candy store.”
>
> — Chris Brousseau

## [▶ Watch the short on YouTube](https://youtube.com/shorts/ljxaBcd5zx8)

<!-- Open the link in a browser during the talk, then return to the deck. This is
the emotional pivot: the old consumer constraint has changed. -->

---

<!-- _class: lead -->

# The Solution

## Small, dense, and actually local

### Qwen3.6-27B · all parameters active · one RTX 5090

**We genuinely do not know the ceiling yet.**

<!-- Qwen3.6-27B is a 27B dense model, post-trained for agentic coding and
structured tool use, and small enough to run on one high-end consumer GPU when
quantized. With a dense model, every model parameter participates in every token.
What we know: these models are trained for tools, fast enough for iterative loops,
and available for us to operate. Source: https://huggingface.co/Qwen/Qwen3.6-27B -->

---

## Ask the Model to Infer Less

| Give the model | So it does not guess about |
|---|---|
| one exact task | intent |
| scoped context | relevance |
| narrow tools + workflow state | available actions |
| machine-checkable success | whether the job is done |

## Less ambiguity → less inference

**That is what lets a smaller model do the job.**

<!-- Good context engineering transfers work from probabilistic inference into the
harness. But even a well-scoped small model has less margin for malformed outputs,
bad recovery, and context growth. That creates the next problem. -->

---

<!-- _class: lead -->

# The Subproblem

## Small models have less margin for ambiguity and recovery

One bad turn can become three expensive turns—or a complete restart.

---

## Forge: Reliability Outside the Model

Antoine Zambelli's Forge adds:

1. **response validation**
2. **rescue parsing**
3. **corrective retry nudges**
4. **optional workflow enforcement**
5. **context compaction**

**The model proposes the next action; the harness makes the loop survivable.**

<!-- Forge is a reliability layer for self-hosted tool calling, not another agent
or planner. It preserves model-native tool calls, catches unknown or malformed calls,
rescues structured calls emitted in fences/XML/vendor formats, and feeds actionable
errors back to the model. Repo: https://github.com/antoinezambelli/forge -->

---

## Why Forge Does “Crazy” Stuff

```text
wrong format
    ↓
rescue the call ──or── explain the error and retry
    ↓
continue the same job with compacted context
```

- rescue avoids paying for another inference
- precise nudges prevent blind retries
- step enforcement stops repeated or premature actions
- compaction stops every turn from carrying the whole past

**Reliability guardrails are token controls.**

<!-- Connect each mechanism to the bill. Rescue parsing converts already-paid-for
output into a usable call. A corrective retry is more expensive than rescue but much
cheaper than restarting without guidance. Step enforcement prevents loops. Compaction
reduces the repeated input cost on every remaining turn. Forge reports taking an 8B
local model from single digits to 84% across its 26-scenario v0.7.0 evaluation suite;
use the paper for the methodology and ablations: Zambelli, “Forge: Closing the Agentic
Reliability Gap Between Self-Hosted and Frontier Language Models,”
https://doi.org/10.1145/3786335.3813193 -->

---

## Pedro Agentware

### Forge's reliability pattern, ported beyond Python

```text
native tool calling
      +
validation, rescue, retries
      +
context compaction
      ↓
Go · Python · TypeScript
```

**The same harness idea around whichever agent framework you already use.**

<!-- Pedro Agentware is a port of Forge's pattern to other languages. Do not discuss
policy enforcement; that belongs to the unmerged Kei plugin and is not part of this
talk. -->

---

<!-- _class: lead -->

# Demo: One GPU, Real Agents

## Qwen3.6-27B · RTX 5090 · my house

We need to prove **speed, tool use, and completed work**.

---

## 🎬 Speed: Over the Wire + Local

```text
conference laptop → internet → home GPU

agent → local endpoint → home GPU
```

**DROP MATCHED BENCHMARK VIDEO(S) HERE**

Compare:

- time to first token
- prompt processing speed
- generation speed

<!-- Use the same prompt, quantization, context, and generation settings for both.
The goal is not a model leaderboard. Separate network latency from inference speed
and show that the loop is fast enough to feel interactive. -->

---

## Tool Calls: Pedro Tag in Discord

```python
async def start_game_tool(
    context: RunContext[AgentDeps], game_type: str
) -> str:
    if game_type == "20_questions":
        game_id = context.deps.thread_id \
            or context.deps.channel_id
        # Create and persist game state...
```

**LIVE: `@Pedro, play 20 Questions.`**

<!-- Real source: ~/code/pedro/pedro-tag/src/pedro_service/agent.py and
src/pedro_service/games/twenty_questions.py. Call out the turns: tool schema in,
tool call out, game state and user answer back in, repeated until success. This is
exactly the token multiplication described at the beginning. -->

---

## Completed Work: Reddit Recommendations

```python
tools = [
    get_interesting_posts,
    get_trending_subreddits,
    send_discord_message,
]
agent = create_react_agent(model=get_llm(), tools=tools)
```

**SHOW THE REDDITWATCH RECOMMENDATIONS IN DISCORD**

Local inference reads the week's results, recommends communities and authors, and delivers the result.

<!-- Real source: ~/code/pedro/pedro-bots/src/core/agents/suggestion.py. This is the
proof of a defined recurring job, not a toy prompt. Point out the chain of tool turns
and why reliable completion matters more than one impressive response. -->

---

## Production Serving

| **vLLM** | **llama.cpp** |
|---|---|
| NVIDIA throughput | hardware portability |
| continuous batching | GGUF quantizations |
| scheduling + metrics | lightweight server |
| OpenAI-compatible tools | OpenAI-compatible tools |

**Ollama and LM Studio are excellent development tools.**

<!-- I would start production evaluation with vLLM or llama.cpp. Use vLLM for a
dedicated NVIDIA server where concurrency matters. Use llama.cpp when hardware or
GGUF portability drives the decision. I would not use Ollama or LM Studio as my
production serving layer. Sources: https://docs.vllm.ai and
https://github.com/ggml-org/llama.cpp -->

---

## Every Turn Has a Token Bill

```text
instructions + tools + history + result → next decision
```

Every turn carries forward:

- instructions and tool schemas
- relevant conversation and workflow state
- tool results from the previous turn

**A ten-turn job repeatedly pays to reconstruct the model's working state.**

<!-- Now introduce cost, after the audience has seen what always-on automation can
do and watched the local model perform. Tool schemas are input tokens. Tool arguments
are output tokens. Tool results return as more input tokens. In a naive agent, the
same instructions, schemas, and history are sent again on every turn. The useful unit
is cost per completed job, not cost per prompt. -->

---

## Reliability Multiplies the Bill

```text
bad call → error → retry → corrected call → verification
```

One mistake can add several turns—or restart the job.

- rescue parsing reuses output already generated
- corrective nudges avoid blind retries
- compaction reduces every remaining turn

**Reliability guardrails are also token controls.**

<!-- A malformed call consumes output tokens; the error becomes input; the retry
replays context; verification adds another turn. A late failure carries the most
accumulated context. If the harness gives up and restarts, it may repay the entire
job. Tie this back to why Forge does seemingly crazy recovery work. -->

---

## When the Economics Work

### Pros

- recurring per-token rent becomes fixed infrastructure
- well-defined jobs fit smaller, efficient models
- high utilization amortizes the GPU
- good context engineering reduces inference and tokens

### Costs

- idle GPU time is still your bill
- model loading creates cold starts
- scheduling, queues, memory, and failures become your problem

**Known job + reliable harness + high utilization = a compelling local case.**

---

<!-- _class: lead -->

# The Takeaway

## Find the smallest model that reliably completes the job.

1. Measure tokens, turns, runtime, and completion rate.
2. Reduce ambiguity with context engineering.
3. Put validation, rescue, retries, and compaction around the loop.
4. Keep the inference infrastructure utilized.

**Optimize the system—not just the model.**

---

<!-- _class: lead -->

# Miriah Peterson · @Soypete

## CEO & founder, stealth startup

## Co-host, **Domesticating AI** podcast

---

<!-- _class: lead -->

# Appendix

## Optional discussion after the outro

---

## Where This Goes Next: LoRAs

Long-running agents create labeled trajectories:

```text
task + context + tool calls → successful result
```

- specialize the model for the repeated job
- improve accuracy
- reduce context shipped per request
- toggle adapters without another always-on model

<!-- Unsloth Studio is an approachable on-ramp from captured trajectories to a
first LoRA. It is not the production inference server. -->

---

## Keep the Control Plane on CPU

```text
request → CPU queue → wake GPU → batch → drain → stop GPU
```

Use inexpensive, always-on CPU for:

- API, authentication, and routing
- queues, context assembly, and scheduling
- health checks and GPU lifecycle

<!-- Keep the agent available without paying GPU rates while it waits. The tradeoff
is that model loading becomes a cold-start budget. Further reading:
https://northflank.com/blog/runpod-vs-modal -->

---

## GPU Scheduling Is Hard

- model weights and KV cache compete for VRAM
- batching improves throughput but adds request latency
- queues require priorities, limits, and backpressure
- failures can strand work or GPU capacity

**A fast model does not make a reliable serving system.**

---

## If Asked: What About Model Quality?

Model-quality comparisons are not the focus of this talk.

The relevant question is whether the smallest reliable model can complete **your defined job** at the utilization and cost you need.
