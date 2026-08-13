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

## Every Turn Has a Token Bill

```text
instructions + tool schemas + history + new result → next decision
```

The model repeatedly reads:

- its instructions
- every available tool definition
- relevant conversation and workflow state
- tool results from the previous turn

**The useful unit is cost per completed job—not cost per prompt.**

<!-- Tool schemas are input tokens. Tool arguments are output tokens. Tool results
return as more input tokens. In a naive agent, the same instructions, schemas, and
history are sent again on every turn. A ten-turn job does not merely pay for ten
short answers; it repeatedly pays to reconstruct the model's working state. -->

---

## Reliability Multiplies the Bill

```text
bad tool call → error result → retry → corrected call → verification
```

One mistake can add several turns:

- malformed arguments
- the wrong tool
- a repeated action
- a failed verification

**A failure late in the loop wastes the most accumulated context.**

<!-- Explain that an agent failure is rarely isolated. The malformed call consumes
output tokens; the error becomes input; the retry replays context; verification adds
another turn. If the harness gives up and restarts, it may repay the entire job. This
is why reliable tool calling is also a cost optimization. -->

---

## Success Creates Utilization

Once an agent reliably completes a job, you want:

- more jobs
- more frequent runs
- longer workflows
- more tools and verification
- eventually: always available

```text
useful agent → more runtime → more tokens → recurring API spend
```

**At sustained utilization, inference economics become architecture.**

<!-- This is the central problem. Agents are not easy, hosted or otherwise. But
once the system is effective, the natural response is to maximize its use. The cost
curve changes from occasional API calls to a persistent compute workload. -->

---

<!-- _class: lead -->

# The Problem

## Useful agents become recurring token workloads

The question is no longer “Which API is cheapest?”

## It is “Where should this compute live?”

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
MoE was the practical consumer path to big-model capacity. Expert offloading can
keep inactive experts in CPU memory and move selected experts to GPU, but the full
model still lives somewhere and CPU-to-GPU transfer adds latency. MoE routes experts,
not ordinary transformer layers. Sources: https://arxiv.org/abs/2101.03961 and
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
