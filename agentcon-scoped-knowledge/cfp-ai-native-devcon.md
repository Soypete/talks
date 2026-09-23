# AI Native DevCon NYC 2026 — CFP Submission

**Event:** AI Native DevCon, 3–4 November 2026, Industry City, Brooklyn NY
**CFP closes:** 1 October 2026, 11:59 PM EDT
**Submit:** https://sessionize.com/ai-native-devcon-nyc-2026/
**Primary track:** Context Engineering
**Secondary track:** The Agent Enablement Platform

---

## Session Title

Scoped Knowledge Stores: Applying a Sovereign Context Framework to Your Agents

## Session Description

The default agent architecture is model-centric: connect the agent to the warehouse,
give it tools, tell it which data it should not touch, and trust the prompt to hold.
That asks a probabilistic model to reconstruct the organization's data, meaning,
identity, and authority while it is trying to complete the task.

It does not. And the failure mode is not usually dramatic — it is an agent quietly
retrieving the wrong customer definition, using a superseded policy, or answering a
question with data the person asking was never entitled to see.

The instinct is to fix this with permissions: tighten the scope after the incident,
discover the tightened scope blocks real work, widen it again. That loop runs
forever because the scope was guessed rather than derived from what the task
actually required.

This talk applies Haikei Labs' Sovereign Context Framework to a concrete design:
scope the knowledge store, not just the permission list. A scoped store is the
Semantic Background for a task. It implements the Law of Lexicon by exposing only
governed information whose source, authority, freshness, ownership, and access
conditions are known. Ontology and entity filters implement the Law of Semantics by
making definitions and relationships explicit. Tool and policy middleware implement
the Law of Pragmatics by separating what the model may propose from what
infrastructure may authorize.

Instead of giving an agent broad retrieval and a list of prohibitions, give it a
retrieval surface that the task and invoking identity justify. The goal is reduced
exposure before inference, not a promise that models are incapable of error.

I will walk through four implementations — scoped retrieval partitioned by
wing/room, a protocol gateway that enforces scope at the tool boundary,
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
track through the protocol-scoping implications, which matter for anyone exposing
internal systems to agents through a tool or protocol boundary.

## What attendees will learn

- Why prompt-level prohibitions are not a security boundary, and why the usual
  permission-tightening loop never converges.
- How scoped stores provide a Semantic Background by applying the Laws of Lexicon,
  Semantics, and Pragmatics at different system boundaries.
- How to derive retrieval scope from the task and invoking identity rather than
  guessing it and retightening after incidents.
- Four concrete implementations of scoped retrieval, including where each one fits
  and where each one breaks down.
- What scoping does to eval consistency — this was the most surprising result for
  me, and it is measurable.
- The protocol implications: what changes when the scope boundary lives at the
  tool boundary rather than inside the agent.
- Patterns to avoid, drawn from the ones I tried first.

## Audience level

Intermediate. Assumes familiarity with retrieval and tool calling. No specific
framework or ontology tooling required.

## Key takeaway

Do not give an agent everything and a list of prohibitions. Give it a governed
retrieval surface the task and identity justify, then enforce action policy outside
the model. Context engineering is the work of making the model's background
explicit.

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
