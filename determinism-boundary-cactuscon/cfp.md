# CactusCon 15 — CFP Submission

**Event:** CactusCon 15, 5–6 February 2027, Mesa Convention Center, Mesa, AZ
**Submit:** https://sessionize.com/cactuscon-15
**CFP closes:** confirm on Sessionize (widget showed 16 Oct 2026)
**Limit:** 2 submissions per speaker. Already submitted: *Sandboxes Are Not
Guardrails*. This is the second and final slot.

---

## Session Title

The Determinism Boundary: Prompts Are Guidelines, Not Access Control

## Description (Sessionize field, 300–1500 chars — this is 1,166)

Remember the Chevy dealership chatbot that agreed to sell a Tahoe for $1? Nobody drove off with a car, because the bot could only say "deal." Now give that bot a refund API, a CRM connector, and a search index that includes payroll. Prompts are like the pirate code: more guidelines than actual rules. Write "never refund more than $500" in all caps, repeat it twice, and it is still language a model interprets, and other language can reinterpret it.

This talk draws the Determinism Boundary: the line between what a model infers and what a system enforces. We break agents two ways: making them do what they shouldn't (unauthorized tool calls and business actions) and making them see what they shouldn't (retrieval and connector leaks that happen before any action). Then we defend each at the layer that can actually say no. We cover why SQL injection is the right history lesson, why ABAC beats system prompts for agent data access, and how identity-aware gateways like Tailscale Aperture, Claude Code managed settings, and tenant-side policy enforcement keep permissions out of the model's hands. Smarter models don't fix this. They find more paths around it.

## Session format

Talk, **20 minutes** (+10 Q&A). Can expand to 50 if the committee prefers.

## Track

Defending (secondary: Breaking)

## Level

Intermediate. Assumes the audience knows what prompt injection and SQL injection
are; no AI/ML background needed.

## Notes to Organizer

This is the companion to my other submission, *Sandboxes Are Not Guardrails*, but
it stands alone and covers different ground. That talk is about containment versus
authorization at the infrastructure layer. This one is about the line between
model inference and enforcement: why prompts, system instructions, and "the model
will know better" are not access control, and where the real enforcement points
belong for both actions and data retrieval. If only one fits the lineup, either
works on its own.

Disclosure: I'm CEO of Haikei Labs, which builds policy enforcement for agents, and
I previously worked at Tailscale. Both appear only as examples alongside Claude
Code's managed settings. The talk is about the architecture pattern, not a product
pitch. Every example uses public sources (the Chevrolet chatbot incident, Tailscale
and Anthropic documentation, NIST SP 800-162 on ABAC).

The talk is based on my essay *The Determinism Boundary* and a segment from the
Domesticating AI podcast on prompt injection and agent security.

---

## What attendees will learn

- Why a system prompt is a request, not a control, and why repeating it louder
  doesn't change that.
- The two failure modes: an agent **doing** something unauthorized (tool calls,
  refunds, config changes) and an agent **seeing** something unauthorized
  (retrieval and connector leaks before any action).
- Why SQL injection is the right history lesson: we fixed it by changing how
  systems treat untrusted input, not by writing sterner notes.
- Where to enforce: at the tool call (the model only emits a structured request),
  at retrieval (authorize before context assembly), and at the gateway (identity
  plus deny-by-default grants).
- Why RBAC breaks down for agents acting across customers and documents, and what
  ABAC adds.
- Why more capable models raise the stakes: more tools, more paths, more ways
  around soft rules.

## Outline (20 min)

1. **$1 Tahoe.** Saying "deal" versus being authorized to make a deal.
2. **Inference is the feature.** Models are good at ambiguity; we want that.
3. **Prompts are the pirate code.** Guidelines, not rules. Four sentences that
   sound like controls.
4. **We've been here: SQL injection.** The fix was architecture, not etiquette.
5. **Two ways to break an agent.** Doing versus seeing.
6. **The boundary.** The model proposes, infrastructure enforces; the tool call is
   just a structured request.
7. **Defenses that say no.** Retrieval-time authorization, ABAC, identity-aware
   gateways (Tailscale Aperture), harness permissions (Claude Code managed
   settings), tenant-side PDP/PEP (Haikei).
8. **Smarter models make this worse.** The eleventh path around your permissions.
9. **Infer probabilistically. Enforce deterministically.**

## Speaker

- **Name:** Miriah Peterson
- **Title:** CEO, Haikei Labs
- **Email:** captainnobody1@gmail.com
- **Twitter/X:** @Soypete
- **Website:** https://soypete.tech/

## Speaker bio

Miriah Peterson is CEO of Haikei Labs, where she builds deterministic policy
enforcement for AI agents. She is an engineer and educator focused on data
engineering and AI infrastructure, and has built production systems at SchoolAI,
Agility Ads, Weave, Tailscale, MX, and Nav. She created SoyPete Tech, teaches for
Boot.dev and O'Reilly, and co-hosts the Domesticating AI podcast.
