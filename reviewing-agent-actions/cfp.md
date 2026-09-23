# AI Software Factory Summit — CFP Submission

**Event:** AI Software Factory Summit (Moderne)
**Details:** https://moderne.ai/ai-software-factory
**CFP close date:** [Confirm on the site before submitting]

---

## Session Title

You Cannot Review Every Agent Action

## Session Description

In July 2026, a single agent on a single evaluation task produced roughly 17,600
reconstructed actions. Imagine that review queue. Now imagine a software factory
running a hundred agents continuously.

The software factory premise — more agents, more autonomy, more throughput — has a
review problem built into it. Human review does not scale with the thing it is
reviewing. One agent, you read the diff. Ten, you skim. A hundred, you approve. A
thousand, you hope.

There are two common responses and both are bad. Review everything, and the factory
stops; you have built expensive autocomplete. Review nothing, and the factory runs
but nobody can say what it did. Neither is an architecture.

This talk argues that review is the wrong unit, and replaces it with three
questions that do not require a human at execution time. Could this action have
happened at all — which is a question about constraining the set of possible
actions rather than inspecting instances. On whose authority did it happen — which
requires carrying both workload identity and delegated human identity through every
subagent hop, because attribution otherwise dies at the first one and every log
downstream says "the agent did it." And can we reconstruct it afterward — which
requires one append-only record per action carrying the invoking subject,
delegation chain, argument digest, resources touched, policy decision, and cost.

We will also be honest about what this does not solve: a correctly authorized
action can still be wrong, a bad policy is enforced faithfully, and scope drift is
invisible to audit. Audit tells you what happened. It does not tell you it should
have.

## Why this session fits the AI Software Factory Summit

Factories are exactly where this problem bites. The value proposition is autonomous
production at volume, and the governance model most teams carry over was designed
for a world where a human read every change. This session does not argue for
slowing the factory down. It argues for moving human attention upstream to the tool
contract, the policy, and the delegation model — reviewed once, applied to
everything — and downstream to denials, exceptions, and anomalies, which are rare
and self-prioritizing. The middle, routine authorized execution, is the part that
should not need a person.

## What attendees will learn

- Why constraining the set of possible actions scales while reviewing instances
  does not, and why a general-purpose shell makes the set unenumerable.
- Why attribution dies at the first delegation hop, and how to carry workload
  identity and delegated human identity together through subagent spans.
- What belongs in an audit record, and why argument digests rather than arguments —
  an audit trail that leaks what it audits is a liability, not a control.
- How to move human review upstream to contracts and downstream to exceptions.
- Why a denial queue is a better review artifact than an approval queue.

## Key takeaway

You cannot review every action. Constrain the set, carry the identity, record the
decision — then review the contract, the exceptions, and the anomalies rather than
the queue. That is the difference between autonomy and abdication.

## Audience level

Intermediate. For engineers and engineering leaders operating agents at volume.

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

Vendor-neutral. The audit record shape shown is from Agentware, which is
MIT-licensed open source, and appears as one implementation of the pattern rather
than as a product pitch. The incident figures come from Hugging Face's published
technical timeline.

## Related writing

- *Sandboxes Are Not Guardrails*
- *The Determinism Boundary*
- *The Context Engineering Manifesto*
