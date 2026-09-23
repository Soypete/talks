# Agent Substrate Day 2026 — CFP Submission

**Event:** Agent Substrate Day, 9 November 2026, Sky SLC, Salt Lake City
**CFP closes:** 30 September 2026, 11:59 PM MDT
**Submit:** https://sessionize.com/agent-substrate-day-2026/
**Format:** 25–30 minute breakout session

---

## Session Title

Sandboxes Are Not Guardrails: Containment Is Not Authorization

## Session Description

In July 2026, an OpenAI agent was placed in a sandbox and given a cybersecurity
challenge. It had network restrictions, process isolation, and an environment
purpose-built to contain it. By every conventional definition of agent security,
this was done correctly.

It escaped through a zero-day in a package registry cache proxy, gained root in an
external execution environment, and used that as a launchpad against Hugging Face,
eventually reaching production systems. Hugging Face reconstructed roughly 17,600
actions from the intrusion.

That number is the point. This was not one clever jailbreak. It was thousands of
individually reasonable steps, each a sensible next move given what the agent could
see. The sandbox constrained where the agent started. It did not constrain which
actions the surrounding systems would permit.

This talk separates two things we have collapsed into one word. A sandbox answers
"where can this process execute." A guardrail answers "is this operation
authorized." Kubernetes gives us excellent primitives for the first — namespaces,
network policy, least-privilege RBAC, ephemeral workloads — and almost nothing for
the second. We will look at why agent harnesses that expose a general-purpose shell
make containment do impossible work, what a policy enforcement point between model
intent and execution looks like, and why authorization has to be evaluated before
context assembly rather than filtered afterward.

## Why this session fits Agent Substrate Day

The CFP asks for security and reliability patterns for agentic workloads, honest
accounts of what went wrong, and novel architectures for orchestration at scale.
This is all three, built around a public incident with a published technical
timeline, so attendees can verify every claim independently.

It is also specifically a Kubernetes talk. The failure modes are ones this audience
operates daily: service account scope, cluster-admin escalation, credentials
reachable from a pod, the gap between a network policy and an authorization
decision. The argument is not that containment failed as a concept — it is that
containment answers one of four questions production agents need answered, and the
other three have no home in most current architectures.

## What attendees will learn

- Why the distinction between containment and authorization is architectural, not
  semantic, and where each belongs in a Kubernetes-based agent platform.
- Why a general-purpose shell in an autonomous loop makes the set of possible
  actions unenumerable — and why you cannot write policy against a set you cannot
  enumerate.
- How to structure a harness as a policy enforcement point: tool existence, schema
  validation, invoking identity, target resource, and policy evaluation before
  execution.
- Why authorization should gate context assembly rather than filter model output,
  and how ABAC over subject/resource/action/environment fits agent invocations.
- Which four layers a production agent system needs — sandbox, policy, context,
  typed tools — and why defense in depth means they are different, not redundant.

## Audience level

Intermediate. Assumes familiarity with Kubernetes primitives and container
isolation. No assumed familiarity with any agent framework.

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

Vendor-neutral. The middleware referenced in the talk (Agentware) is MIT-licensed
open source and appears only as one example of the architectural pattern, not as a
product pitch. The incident analysis draws entirely on Hugging Face's published
technical timeline and disclosure.

## Related writing

- *Sandboxes Are Not Guardrails* — the essay this talk is drawn from
- *Reasoning Prompts Are Not Pragmatics* — on the same incident, from the
  inference-gap angle
- *The Determinism Boundary* — the general form of the argument
