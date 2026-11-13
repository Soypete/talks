# DataTune Nashville 2027 — CFP draft

**Status:** Draft, not submitted  
**Event:** DataTune Nashville, March 12–13, 2027  
**CFP deadline:** November 15, 2026  
**Submission:** https://www.datatuneconf.com/speak.html  
**Audience:** Data engineers, analytics engineers, data platform practitioners  
**Proposed length:** 60 minutes  
**Related existing talk:** [Data as an AI Guardrail](talk.md)  
**Source essay:** *The Semantic Background* (Haikei Labs, November 10, 2026); original Substack permalink to verify before submission.

## Title

Access Is Not Context: What Data Engineering Must Build for AI Agents

## Abstract

Give an AI agent access to your warehouse, dashboards, support tickets, and operational logs, and it can retrieve a lot of data. That does not mean it understands what those records mean to your business. A field name is not a definition; a database connection is not a permission to act; and the latest query result is not necessarily the authoritative answer.

We will follow a concrete operational incident — a checkout problem spanning logs, tickets, business metrics, and multiple systems — and ask what an agent actually needs to investigate it reliably. We will separate the lexicon of business terms, the semantic relationships and source authority behind those terms, and the pragmatic limits on which actions it may take. Then we will trace a governed workflow: asking the semantic layer which sources and metrics apply, querying the data, and executing a narrowly authorized follow-up action.

The goal is not to put another wall of prose into a prompt. It is to show how data engineers can make business context queryable, testable, and reusable across agents, while still enforcing identity and tool boundaries in the harness.

## Takeaways

- Distinguish data access, business semantics, and authorization for actions.
- Identify what belongs in an ontology/semantic layer rather than in a prompt.
- Design an agent workflow that queries both business definitions and operational data.
- Test source selection, tool calls, and permission boundaries rather than trusting a plausible final answer.

## Proposed 60-minute flow

1. 0–8 min: Why an agent with every connector can still answer the wrong question
2. 8–20 min: Checkout incident across fragmented sources
3. 20–35 min: Lexicon, semantic relationships, source authority, metrics
4. 35–48 min: Governed tool sequence, identity, approvals, deterministic deny
5. 48–55 min: Behavior-based evaluations and failure cases
6. 55–60 min: Q&A

## Editorial checks before submission

- Verify the full case-study details and any claimed outcomes against the source essay.
- Link the exact Substack article permalink, not a guessed slug.
- Only promise a live demo after confirming a reproducible environment.
- Check Nashville travel against pending March 15 Barcelona submissions.
