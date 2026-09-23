# AI Native DevCon NYC 2026 — CFP Submission

**Event:** AI Native DevCon, 3–4 November 2026, Industry City, Brooklyn NY
**CFP closes:** 1 October 2026, 11:59 PM EDT
**Submit:** https://sessionize.com/ai-native-devcon-nyc-2026/
**Primary track:** Agent Orchestration
**Secondary track:** The Agent Enablement Platform

---

## Session Title

The Determinism Boundary: Where Agent Reasoning Ends and Infrastructure Begins

## Session Description

We have spent two years making models better at reasoning through ambiguity.
Chain-of-thought, ReAct, Tree of Thoughts, planning steps, reflection, clarifying
questions — all of it genuinely useful, and all of it aimed at the same problem:
helping a model navigate a situation it was not given enough information about.

None of it answers whether the action is permitted.

That distinction is easy to lose inside an agent loop, and it gets expensive once
the loop runs unattended. A model can reason that a $700 refund is the right
business outcome. If the invoking employee can approve $500, better reasoning
should not change the answer. The policy is not evidence to weigh against the
customer's circumstances — it is a boundary around the operation.

This talk draws the line explicitly. On one side, the model interprets, infers,
ranks, plans, and proposes. On the other, infrastructure decides what is actually
allowed. We will look at the four places that boundary appears — context assembly,
tool exposure, action validation, and audit — and why three of them are usually
missing. We will also look at why "a better model will fix this" gets the direction
wrong: a more capable model discovers more options, uses more tools, and traverses
more systems, which expands the space of reachable actions rather than shrinking
the need for explicit limits.

The argument is grounded in the July 2026 agent intrusion, where roughly 17,600
individually reasonable actions compounded into a production compromise. Not one
jailbreak — thousands of sensible next moves.

## Why this session fits AI Native DevCon

The CFP asks for what actually works in agentic coding at scale, with a clear
spread from introductory to genuinely expert, and explicitly welcomes technical
deep dives. This is a systems-design talk for people already running agents, aimed
at the gap between an agent that demos well and one an organization will approve
for production.

It fits Agent Orchestration most directly — bounded autonomy, supervision and
quality gates, failure and recovery — and touches the Enablement Platform track
through policy enforcement points and platform-level guardrails. It is
experience-driven rather than theoretical, and it is honest about the fact that
almost none of the machinery is new: authentication, schemas, policy engines,
RBAC and ABAC all predate agents. The novelty is that the caller is now a model
constructing requests no engineer wrote.

## What attendees will learn

- How to tell a reasoning problem from an authorization problem, and why treating
  the second as the first is the most common architectural mistake in agent systems.
- The four places the determinism boundary appears — context assembly, tool
  exposure, action proposal, and audit — and what belongs on each side of it.
- Why authorization must gate context assembly rather than filter model output, and
  what that changes about retrieval design.
- How to structure a harness as a policy enforcement point rather than an
  ask-execute-repeat loop.
- Why model capability expands the reachable action space, making explicit
  boundaries more important as models improve rather than less.

## Audience level

Intermediate to advanced. Assumes familiarity with agent loops and tool calling.
No specific framework assumed.

## Key takeaway

The model can propose. Infrastructure decides whether the proposal becomes real. If
the policy says no, the answer is no, regardless of how convincing the reasoning
trace is.

## Speaker

- **Name:** Miriah Peterson
- **Title:** CEO, Haikai Labs
- **Email:** captainnobody1@gmail.com
- **Twitter/X:** @Soypete
- **Website:** https://soypete.tech/

## Speaker bio

Miriah Peterson is CEO of Haikai Labs, where she is building a Sovereign Context
Layer for reliable AI. An engineer and educator focused on data engineering and AI
infrastructure, she has built production systems at SchoolAI, Agility Ads, Weave,
Tailscale, MX, and Nav. She created SoyPete Tech, teaches for Boot.dev and
O'Reilly, and hosts the Domesticating AI podcast.

## Notes for reviewers

No product pitch. Haikai Labs' work informs the framing, but the talk presents a
vendor-neutral architectural pattern and the referenced middleware is MIT-licensed
open source. The incident analysis uses Hugging Face's published technical timeline.

## Travel

[Confirm whether travel or accommodation support is needed — the deadline for that
request is also 1 October 2026.]

## Related writing

- *The Determinism Boundary* — the essay this talk is drawn from
- *Reasoning Prompts Are Not Pragmatics* — the inference-gap argument in detail
- *Sandboxes Are Not Guardrails* — the same boundary, from the containment side
