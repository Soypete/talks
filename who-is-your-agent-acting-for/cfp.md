# Who Is Your AI Agent Acting For? — CFP Submission

**Event:** TBD
**Format:** 25–40 minute session
**Best fit:** Enterprise AI; AI governance; security; agent architecture;
CIO/CTO/CISO; data governance; fintech and other regulated industries

---

## Session Title

Who Is Your AI Agent Acting For?

**Subtitle:** Delegated Authority for Enterprise AI Agents

## Session Description (~800 chars)

Giving an AI agent access to Salesforce, Slack, a warehouse, or an internal API
does not answer the most important enterprise question: who is the agent acting
for? A finance executive, support rep, developer, and automated workflow should not
inherit the same authority simply because they use the same model or connector.
This talk introduces delegated identity as a core design requirement for enterprise
agents and shows how identity should shape context assembly, tool availability,
approval boundaries, and auditability. We will separate what the model should
reason about from what infrastructure must enforce, so organizations can give
agents useful autonomy without granting them a universal service account or asking
humans to approve every action.

## Speaker/session pitch

Most enterprise AI conversations focus on model choice, retrieval, or which tools
an agent can connect to. In practice, the harder problem begins after the
connection exists: which employee's authority applies, what subset of company
context should be visible, which operations can execute automatically, and which
require escalation? My work on agent infrastructure and context engineering keeps
converging on the same architectural requirement: the agent must operate on behalf
of an explicit identity, and that identity has to travel with the action. This talk
gives enterprise and technical leaders a practical way to reason about delegation
before agent adoption outruns their existing access-control model.

## Core takeaway

**Identity → Context → Policy → Available Actions → Audit**

## What attendees will learn

- Why "the agent has access to Salesforce" is the wrong unit of authorization, and
  why the shared service account is the default failure.
- The confused deputy problem: an agent holding more authority than the person it
  serves will use that authority on their behalf.
- The five inputs to an agent authorization decision: identity, role, task,
  resource, and workflow.
- How delegated identity changes what data enters the model's context, which tools
  are exposed, and which actions run, escalate, or are forbidden.
- What a defensible audit record looks like: principal, agent, action, resource,
  policy, decision.
- Questions to ask vendors and internal teams before approving an agent rollout.

## Outline

1. **The hidden question.** Every enterprise agent acts for someone. Who?
2. **One agent, four users.** A finance executive, a support rep, a developer, and
   a nightly workflow use the same agent and the same connector. What should each
   one get?
3. **The universal service account.** Why connector-level access becomes the
   union of everyone's permissions, and the confused deputy problem.
4. **Authorization context.** Identity, role, task, resource, workflow.
5. **Identity shapes context.** Authorize before the model sees data, not after.
6. **Identity shapes tools.** Same agent, different available actions.
7. **Approval boundaries.** Autonomous, escalated, and forbidden, and why humans
   can't approve everything.
8. **Auditability.** Tying every consequential action to a principal and a policy.
9. **The architecture.** Identity → context → policy → available actions → audit,
   plus readiness questions for leaders.

## Audience level

Introductory to intermediate. Written for enterprise and technical leaders (CIO,
CTO, CISO, heads of data and platform) and the architects who report to them. No
code required to follow.

## Speaker

- **Name:** Miriah Peterson
- **Title:** CEO, Haikei Labs
- **Email:** captainnobody1@gmail.com
- **Twitter/X:** @Soypete
- **Website:** https://soypete.tech/

## Speaker bio

Miriah Peterson is CEO of Haikei Labs, where she builds a governed context layer
for enterprise AI agents. She is an engineer and educator focused on data
engineering and AI infrastructure, and has built production systems at SchoolAI,
Agility Ads, Weave, Tailscale, MX, and Nav. She created SoyPete Tech, teaches for
Boot.dev and O'Reilly, and co-hosts the Domesticating AI podcast.

## Notes for reviewers

This is an architecture talk, not a product pitch. I lead Haikei Labs and disclose
that on stage. The pattern is vendor-neutral and maps onto standards attendees
already use: OAuth 2.0 Token Exchange (RFC 8693) for delegation, ABAC (NIST SP
800-162) for attribute-based decisions, and existing IdP groups and roles.

## Grounding in existing work

Built from *The Determinism Boundary*, *Are You Building a Company Brain?*,
*Sandboxes Are Not Guardrails*, and *You Cannot Review Every Agent Action*.

## Companion talk

*You Cannot Scale a Sandbox* is the engineering and platform version of this
architecture: containment does not scale into authorization. This talk is the
enterprise and leadership version: delegated identity is the missing prerequisite
for safe autonomy.
