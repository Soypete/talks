# You Cannot Scale a Sandbox — CFP Submission

**Event:** TBD
**Format:** 25–40 minute breakout session
**Tracks:** Agent infrastructure; platform engineering; DevOps/SRE; cloud-native AI;
AI security; coding agents; enterprise AI architecture

---

## Session Title

You Cannot Scale a Sandbox: What UNIX Time-Sharing Teaches Us About Governing
Agent Fleets

**Alternate subtitle:** Why Containment Is Not an Enterprise Operating Model for
Autonomous Agents

## Core thesis

A sandbox is an execution primitive, not an authorization model. One agent in one
sandbox is the 1960s answer to sharing a computer: give every user their own
machine. UNIX did not scale that way. It scaled by making identity travel with every
process and putting one reference monitor between every process and every
resource. Agent fleets need the same thing, and the kernel cannot provide it,
because the resources agents touch are APIs, warehouses, and SaaS tools on the
other side of the network.

## Session Description (as submitted)

Sandboxes are essential for containing code execution, but they are not a scalable
authorization model for autonomous agents. As companies move from one coding agent
on one laptop to fleets of agents acting across users, tools, data, and workflows,
the problem changes from "where can this process run?" to "which actions should
this identity be allowed to take?" This talk explores what breaks when sandboxing
becomes the primary control strategy and shows how production agent infrastructure
needs delegated identity, typed tool interfaces, deterministic policy enforcement,
approval boundaries, and auditability. The goal is not to make agents less capable,
but to let models reason freely while infrastructure determines which actions are
allowed to become real.

## Session Description (long, unsubmitted draft)

Every agent security conversation eventually lands on "put it in a sandbox." That
advice is correct and incomplete. A sandbox restricts a filesystem, a network, or a
process. Inside it, the agent can still hold credentials, call APIs, and read data
that lets it take valid but unauthorized actions. One coding agent on one laptop can
live with that gap. A fleet of agents acting for hundreds of users cannot.

UNIX hit the same scaling wall in 1974. Thompson and Ritchie's time-sharing paper
describes a system where many users share one machine safely. Giving each user a
separate computer (the sandbox approach) was not the answer. Three choices made it
work. Every process carries a user identity. Every resource is reached through one
mediated interface. Permission is checked once, at `open()`, and the process gets
back a handle rather than raw access. The sandbox was never the security model. The
kernel was.

Agents break that arrangement. The resources they act on (Salesforce, Slack, a
warehouse, an internal API, an LLM provider) are not files the kernel mediates.
They sit across the network, reached with whatever token is sitting in the
sandbox's environment. Inside the sandbox, identity often collapses into one
shared service account, and the general-purpose shell makes the set of possible
actions unenumerable.

This talk rebuilds the UNIX model one layer up. We will look at:

- **Identity on every call.** Identity-aware gateways such as Tailscale Aperture
  attach a user or workload identity to every LLM request using identity the
  network already established, so nobody distributes API keys and every call has
  an owner.
- **Mediation at the context layer.** A governed context layer, the pattern we are
  building at Haikei, decides which data, tools, and actions exist for an
  identity and task before the model sees anything.
- **Handles, not secrets.** Typed tools act as file descriptors: authorized once,
  scoped to a resource, audited on use.

The goal is not less capable agents. Models should reason freely while
infrastructure decides which actions are allowed to happen.

## What attendees will learn

- Why sandboxing answers "where can this process execute" but cannot answer "whose
  authority is this" or "should this action exist," and why those gaps get wider
  with every agent you add.
- What the UNIX time-sharing design actually got right (identity per process,
  a single reference monitor, permission at `open()`, file descriptors as
  capabilities) and which parts of that model agents lose when their resources
  move across the network.
- Why a general-purpose shell makes the action surface unbounded, and how typed
  tools with schemas restore an enumerable set you can write policy against.
- How identity-aware network gateways (e.g. Tailscale Aperture) and governed
  context layers (e.g. Haikei) split the work: one attaches identity to traffic,
  the other decides what context and capabilities that identity gets.
- Why authorization belongs before context assembly, the `open()` check, rather
  than as a filter on model output.
- A checklist for what a scalable agent control plane must make deterministic:
  principal, task, resource, operation, policy decision, and audit record.

## Outline

1. **Sandboxes solve containment.** What they do well, and the four questions
   they leave unanswered.
2. **One machine per user did not scale in 1974 either.** UNIX time-sharing as
   the original multi-tenant problem.
3. **What made UNIX safe.** UID on every process, the kernel as reference
   monitor, check-at-open, file descriptors as capabilities, setuid as explicit
   delegation.
4. **What agents lose.** Resources leave the kernel's reach; tokens in the
   environment replace the UID; `bash` makes the action set unenumerable.
5. **Identity on the wire.** Identity-aware gateways put the UID back on every
   request (Tailscale Aperture as the worked example).
6. **The reference monitor, rebuilt.** A governed context layer: identity →
   context → policy → available actions → audit (Haikei as the worked example).
7. **Handles, not secrets.** Typed tools as file descriptors, with brokered
   credentials, scoped resources, and deterministic policy decision and
   enforcement points.
8. **What your control plane must make deterministic.** A concrete first step for
   teams scaling past one agent in one sandbox.

## Why this talk, why now

Teams are moving from one coding agent on a laptop to fleets of agents in shared
infrastructure. The default control they reach for is the one that worked locally:
another sandbox. This talk gives platform teams a vocabulary and an architecture for
the next step, grounded in a 50-year-old system design that already solved the
multi-tenant version of this problem once.

## Audience level

Intermediate. Assumes familiarity with containers and basic access control. No
agent framework knowledge required. UNIX history is explained, not assumed.

## Speaker

- **Name:** Miriah Peterson
- **Title:** CEO, Haikei Labs
- **Email:** captainnobody1@gmail.com
- **Twitter/X:** @Soypete
- **Website:** https://soypete.tech/

## Speaker bio

Miriah Peterson is CEO of Haikei Labs, where she is building a governed context
layer for reliable AI agents. She is an engineer and educator focused on data
engineering and AI infrastructure, and has built production systems at SchoolAI,
Agility Ads, Weave, Tailscale, MX, and Nav. She created SoyPete Tech, teaches for
Boot.dev and O'Reilly, hosts the Domesticating AI podcast, and is writing a book on
context engineering.

## Speaker/session pitch

I have spent my career building data and platform infrastructure in regulated
environments. My recent work is on what changes when AI agents move from local
experiments into shared enterprise infrastructure. The mistake I keep seeing is
treating sandboxing as though it scales into a complete agent governance model. It
does not. Once agents operate across many users, tools, and workflows, containment
cannot say whose authority the agent inherits, which operations are permitted, or
when an action needs approval. This talk connects UNIX's original multi-user design,
cloud-native identity, and authorization architecture into a pattern teams can use
as they scale past one agent in one sandbox.

## Notes for reviewers

Tailscale Aperture and Haikei appear as examples of two architectural layers
(identity on the network, mediation at the context layer), not as product pitches.
I previously worked at Tailscale and currently lead Haikei Labs; both are disclosed
on stage. Each layer is described so attendees can build or buy it. The UNIX
material draws on Ritchie and Thompson, *The UNIX Time-Sharing System* (CACM,
1974), and Saltzer, Reed, and Clark, *End-to-End Arguments in System Design* (1984).

## Grounding in existing work

This synthesizes *Sandboxes Are Not Guardrails*, *The Determinism Boundary*,
*Anatomy of a Cloud-Native Agent*, *You Cannot Review Every Agent Action*, and
Chapter 12, "The UNIX Philosophy of AI Systems," from my forthcoming context
engineering book.

## Companion talk

*Who Is Your AI Agent Acting For?* is the enterprise and leadership version of this
architecture. This talk is the engineering and platform version: containment does
not scale into authorization.
