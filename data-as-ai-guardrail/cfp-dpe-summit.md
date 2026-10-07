# DPE Summit 2027 — CFP Submission

**Event:** DPE Summit 2027
**Submit:** https://sessionize.com/dpesummit2027/
**CFP close date:** [Confirm on the site before submitting]

---

## Session Title

Data as an AI Guardrail: Ontologies as Inference Models

## Session Description

When an agent hallucinates a relationship, retrieves a superseded policy, or
confidently answers with the wrong definition of a business term, the usual response
is to write a better prompt. Add the rule to the system prompt. Tell the model which
data is authoritative. Explain the schema in prose.

That does not work, and the reason is worth being precise about: the model reads
your instruction in the same context window as the data, with no structural
distinction between the two. A prompt is a suggestion competing with everything else
in the window.

Raw data does not solve it either. Data without semantics is noise to a language
model — it can retrieve five records containing the word "customer" without
establishing which definition of customer governs the decision it is making.

This talk makes the case that the missing layer is one data engineering already
knows how to build. Ontologies formalize the definitions, relationships, and
constraints that turn records into interpretable information, and they can be used
as inference models rather than documentation. That makes them enforceable: a tool
call can be validated against the ontology before it executes, an agent's proposed
relationship can be checked against what the organization says is possible, and a
retrieval result can be filtered by what the schema permits.

We will cover what an ontology actually is, the pipeline for building one from
existing definitions, how knowledge graphs combine ontologies with data, and three
patterns emerging in industry for using them as guardrails — including the agent
validation pattern and the tool call pattern, with a worked example.

## Why this session fits DPE Summit

This is a data engineering talk that happens to be about agents. The argument is
that the reliability problem everyone is attributing to models is substantially a
modeling problem — one with an established discipline behind it. Bill Inmon's answer
to unstructured data turns out to be directly applicable to the LLM era, and the
audience most equipped to act on that is the one that already builds schemas,
lineage, and semantic layers.

It is also practical rather than theoretical. Attendees leave with a pipeline for
building an ontology from definitions they already have, and three concrete patterns
for putting it in the path of an agent.

## What attendees will learn

- Why system-prompt rules are not enforcement, and why "just add it to the prompt"
  fails structurally rather than occasionally.
- Why retrieval alone does not supply meaning: similarity establishes proximity, not
  authority, hierarchy, causality, or which definition governs.
- What an ontology is formally, and the pipeline from existing business definitions
  to a usable one.
- How ontologies function as inference models rather than documentation, which is
  what makes them enforceable.
- Three industry patterns for ontology-based guardrails, including agent validation
  and tool call validation.
- How to start from the ontologies your organization already has without knowing it.

## Audience level

Intermediate. Aimed at data engineers and platform engineers. No prior ontology
or agent-framework experience assumed.

## Key takeaway

The guardrail that actually holds is not a sentence in a prompt. It is a semantic
model the agent's actions are validated against — and building semantic models is
work data engineering already knows how to do.

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

Vendor-neutral. Draws on W3C standards (RDF, OWL, SPARQL) and published work on
knowledge graphs and ontologies. No product demonstration.

## Related writing

- *The Context Engineering Manifesto* — Haikai Labs
- *Escaping the Context Void: Why Your Agents Suck and How to Make Them Better*
