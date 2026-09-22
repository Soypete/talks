# Session Title

Shared Memory for Agents: A Wiki as the Coordination Substrate

# Session Description

Every agent harness solves memory for one agent. Context windows, compaction,
session logs, vector stores — all of it scoped to a single conversation with a
single model.

That breaks the moment you run more than one agent. A second agent has no idea
what the first one learned, decided, or is currently blocked on. The usual
answers are a shared vector database nobody can audit, or a chat channel that is
unstructured by construction.

This talk presents a different substrate: a plain markdown wiki with a closed
vocabulary, an append-only inbox, and exactly one writer. Agents search it before
acting and capture findings as typed, linked pages. Claims, decisions, and
contradictions accumulate. So do coordination primitives — handoffs, blockers,
acknowledgments, releases — which let agents pass work to each other and record
why they stopped.

The system under discussion is real and running: a Herdr plugin backing a wiki of
roughly 13,800 items, where handoff and blocker pages are written by coding agents
working across several repositories. We will look at the data model, the
single-writer discipline that keeps it consistent, and what breaks when you let
agents write to shared memory without one.

## What attendees will learn

- Why per-agent memory does not compose into multi-agent memory, and where the
  usual substitutes (vector stores, chat channels) lose the properties you need.
- How a closed vocabulary at the write boundary makes agent output structured
  enough to query without constraining what agents can say.
- How single-writer discipline with an append-only inbox gives you concurrent
  agent writes without locks, conflicts, or a coordination protocol.
- How typed coordination primitives — handoff, blocker, ack, release — turn a
  knowledge base into a place agents hand work to each other.
- Why human-readable storage is an operational advantage, not a compromise: the
  memory is greppable, diffable, reviewable, and editable by hand.

## Who this talk is for

Engineers building or operating multi-agent systems, platform engineers thinking
about agent state, and anyone who has watched two agents duplicate each other's
work. Familiarity with agent tooling helps but is not required; the design ideas
are older than agents and mostly borrowed from version control and knowledge
management.

## Key takeaways

Attendees will leave with a concrete, low-infrastructure design for shared agent
memory: a vocabulary at the write boundary, one writer, an inbox that separates
capture from reconciliation, and typed links that make the graph queryable. The
approach runs on a filesystem and a CLI, so it is testable the same afternoon.

## Small print

Vendor-neutral. The plugin discussed is MIT-licensed and open source. No product
pitch, no commercial dependency.

# Value to the community

Multi-agent systems are being assembled faster than their state models are being
designed. Most teams reach for a vector database because it is the available
answer, then discover they cannot audit it, cannot diff it, cannot tell which
agent wrote what, and cannot express that one agent is blocked on another.

This talk offers a substrate built from boring, inspectable parts, and is honest
about the tradeoffs — retrieval is lexical rather than semantic, reconciliation
needs a human in the loop, and a closed vocabulary means rejected captures. Those
constraints are the point, and the talk argues for them explicitly rather than
presenting the design as free of cost.

The material is grounded in a running system with real usage, including the
failure modes encountered along the way.

# Case study?

Partially. The design is general, but the evidence is one running deployment with
real agent traffic rather than a survey of many.

# Talk presented before?

No. [Confirm before submission.]

# Relevant projects

Herdr (terminal multiplexer and plugin host); the LLM-Wiki pattern described by
Andrej Karpathy; Model Context Protocol (for the agent-facing surface); standard
markdown and git tooling.

# Additional resources

- Plugin source: https://github.com/Soypete/herdr-wiki-plugin
- Talk source: `herdr-wiki-shared-memory/talk.md` [Add public URL before submission.]
- Speaker profile: https://soypete.tech/ [Confirm current URL.]
- Domesticating AI podcast: [Add public URL before submission.]

# Submission details

## Event and format

- Submitting for: [Add target conference]
- Track: [Confirm — agentic AI, developer tooling, or architecture]
- Session format: [Confirm length]
- Audience level: Intermediate

## Speaker

- Speaker: Miriah Peterson
- Email: captainnobody1@gmail.com
- Speaker title: CEO, Haikai Labs
- Company: Haikai Labs
- Company website: [Confirm and add URL]
- Country of residence: [Confirm]
- Co-speakers: None currently

## Speaker bio

Miriah Peterson is CEO of Haikai Labs, where she is building a Sovereign Context
Layer for reliable AI. An engineer and educator focused on data engineering and AI
infrastructure, she has built production systems at SchoolAI, Agility Ads, Weave,
Tailscale, MX, and Nav. She created SoyPete Tech, teaches for Boot.dev and
O'Reilly, and hosts Domesticating AI.

## Required acknowledgements

- Content Quality Agreement: Agree
- Code of Conduct: Agree
- Commitment to Inclusivity: Agree
- Consent to share session and personal data with the organizer: Agree
