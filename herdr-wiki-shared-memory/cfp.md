# Session Title

Shared Memory for Agents: A Wiki as the Coordination Substrate

# Session Description

Multi-agent systems eventually coordinate through whatever shared state is
available—often chat logs, package caches, or undocumented files. This talk
presents a running markdown-based knowledge system with a closed vocabulary,
append-only inbox, single-writer reconciliation, typed links, and coordination
primitives for handoffs, blockers, acknowledgments, and releases. Attendees will
learn how to build shared agent memory that is searchable, diffable, auditable,
and usable across multiple agent harnesses without requiring a large
infrastructure investment.

## What attendees will learn

- Why agents coordinate whether or not you plan for it, and why the substrate
  they reach for is chosen by availability rather than design.
- Why per-agent memory does not compose into multi-agent memory, and where the
  usual substitutes (vector stores, chat channels) lose the properties you need.
- How a closed vocabulary at the write boundary makes agent output structured
  enough to query without constraining what agents can say.
- How single-writer discipline with an append-only inbox gives you concurrent
  agent writes without locks, conflicts, or a coordination protocol.
- Why promotion from inbox to graph should be deterministic: the agent classifies
  at capture time, the boundary validates, and nothing reinterprets it later.
- How typed coordination primitives — handoff, blocker, ack, release — turn a
  knowledge base into a place agents hand work to each other, including real
  orchestrator-to-worker traffic: workers acknowledging assignments, splitting a
  task between them, and handing back what they deliberately left undone.
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
about the tradeoffs — retrieval is lexical rather than semantic, classification
rests entirely on the capturing agent, and a closed vocabulary means rejected
captures. Those
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
