# AI Native DevCon NYC 2026 — CFP Submission

**Event:** AI Native DevCon, 3–4 November 2026, Industry City, Brooklyn NY
**CFP closes:** 1 October 2026, 11:59 PM EDT
**Submit:** https://sessionize.com/ai-native-devcon-nyc-2026/
**Primary track:** Context Engineering
**Secondary track:** The Agent Enablement Platform

---

## Session Title

Stop Giving Agents Permissions: Give Them Scoped Knowledge Stores

## Session Description

The default agent security model is to grant broad access and then hope the prompt
holds. Connect the agent to the warehouse, give it tools, tell it which data it
should not touch, and trust that the instruction survives inference.

It does not. And the failure mode is not usually dramatic — it is an agent quietly
retrieving the wrong customer definition, using a superseded policy, or answering a
question with data the person asking was never entitled to see.

The instinct is to fix this with permissions: tighten the scope after the incident,
discover the tightened scope blocks real work, widen it again. That loop runs
forever because the scope was guessed rather than derived from what the task
actually required.

This talk presents the alternative that has worked for me in production: scope the
knowledge store, not the permission list. Instead of giving an agent broad retrieval
and a list of prohibitions, give it a retrieval surface that only contains what the
task and the invoking identity justify. The unauthorized information never enters
the context, so no instruction is needed to keep it out.

I will walk through four implementations — scoped retrieval partitioned by
wing/room, an MCP server that enforces scope at the protocol boundary,
ontology-based filtering, and policy middleware around tool calls — and then spend
real time on what that cost. Reliability tradeoffs, eval consistency improvements,
observability, the patterns that worked, and the patterns I would not repeat.

## Why this session fits AI Native DevCon

The CFP asks for experience-driven talks: what you tried, what worked, what failed,
and what you changed to make it stick. That is the shape of this talk. It is built
on four working implementations rather than an architectural proposal, and roughly a
third of it is the lessons-learned section — including approaches that did not pan
out.

Primary track is Context Engineering: this is reusable, testable context, knowledge
and memory, and multi-model portability, since a scoped store works the same way
regardless of which model sits in front of it. It touches the Enablement Platform
track through the MCP scoping implications, which matter for anyone exposing
internal systems to agents through a protocol boundary.

## What attendees will learn

- Why prompt-level prohibitions are not a security boundary, and why the usual
  permission-tightening loop never converges.
- How to derive retrieval scope from the task and invoking identity rather than
  guessing it and retightening after incidents.
- Four concrete implementations of scoped retrieval, including where each one fits
  and where each one breaks down.
- What scoping does to eval consistency — this was the most surprising result for
  me, and it is measurable.
- The MCP implications: what changes when the scope boundary lives at the protocol
  layer rather than inside the agent.
- Patterns to avoid, drawn from the ones I tried first.

## Audience level

Intermediate. Assumes familiarity with retrieval and tool calling. No specific
framework or ontology tooling required.

## Key takeaway

Do not give an agent everything and a list of prohibitions. Give it a retrieval
surface the task and the identity justify. The information you do not want in the
answer should never be in the context.

The first implementation can be narrow: choose one sensitive workflow, derive its
scope from task and identity, filter before inference, and test both an authorized
case and a near-miss case. Measure retrieval precision, denials, and task success
before expanding the scope.

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

The tools demonstrated are open source. Haikai Labs' work informs the framing, but
the session is about the architectural pattern and its measured tradeoffs, not a
product.

## Travel

[Confirm whether travel or accommodation support is needed — that request deadline
is also 1 October 2026.]
