---
marp: true
theme: gaia
paginate: true
title: "Who Is Your AI Agent Acting For?"
backgroundImage: url('../images/soypete_background.png')
description: Delegated authority for enterprise AI agents
---

<!-- _class: lead -->

# Who Is Your AI Agent Acting For?

## Delegated authority for enterprise AI agents

Miriah Peterson · @Soypete

---

## Who Am I?

- CEO of Haikei Labs: a governed context layer for enterprise agents
- Previously: SchoolAI, Weave, Tailscale, MX, Nav
- Co-host of the **Domesticating AI** podcast
- Data and platform infrastructure in regulated industries

---

## The question everyone asks

> "Which tools can our agent connect to?"

- Salesforce ✔
- Slack ✔
- Snowflake ✔
- Internal billing API ✔

**Connected.** Now what?

---

<!-- _class: lead -->

# The question that matters

## Who is the agent acting for?

---

## One agent. Four users.

| Who | Asks the agent to… |
|---|---|
| **CFO** | "Summarize Q3 margin by customer" |
| **Support rep** | "Refund this customer's last invoice" |
| **Developer** | "Why did the billing job fail last night?" |
| **Nightly workflow** | "Reconcile yesterday's payments" |

Same model. Same connectors.

**Should they get the same authority?**

---

## What usually happens

```text
CFO ─────────┐
Support rep ─┤
Developer ───┼──▶ agent ──▶ svc-ai-agent@corp ──▶ Salesforce, Snowflake, Billing
Workflow ────┘
```

One **service account**, scoped for the broadest use case.

Effective permission for every user = **the union of everyone's.**

---

## The confused deputy

Norm Hardy, 1988:

A program with **more authority than its caller** gets tricked into using that
authority **on the caller's behalf.**

- Support rep asks for "all invoices over $10k"
- The agent can see them, so it returns them
- Nothing was hacked. **The architecture did what it was built to do.**

<!-- The agent is the deputy. The service account is the authority. The user
didn't need to be malicious, just curious. -->

---

## Why "the agent has access" is the wrong unit

Your existing access model is built on **people and roles.**

The agent erased the person.

```text
Before:  alice → Salesforce        (alice's permissions)
After:   alice → agent → Salesforce (the agent's permissions)
```

Adoption is now running ahead of your access-control model.

---

<!-- _class: lead -->

# Delegated identity

## The agent acts **on behalf of** someone, and that someone travels with the action.

---

## Five inputs to every decision

| Input | Question |
|---|---|
| **Identity** | Who is the principal? |
| **Role** | What is that principal entitled to in general? |
| **Task** | What job is the agent doing right now? |
| **Resource** | Which exact record, account, or document? |
| **Workflow** | Is this interactive, scheduled, or chained from another agent? |

Roles alone aren't enough. Two support reps can serve **different customers.**

<!-- This is ABAC (NIST SP 800-162) in leadership language. -->

---

## Delegation already has a standard

OAuth 2.0 Token Exchange (RFC 8693):

```text
subject = alice@corp       (who the action is for)
actor   = support-agent    (who is performing it)
```

- The agent never holds more authority than **alice + the agent's own limits**
- Both identities appear in the token and **in the log**

You don't need to invent this. You need to **require** it.

---

<!-- _class: lead -->

# Identity → Context → Policy → Available Actions → Audit

---

## 1. Identity shapes context

What enters the model's context depends on **who asked.**

| CFO asks about margin | Support rep asks about margin |
|---|---|
| Customer-level revenue + cost | "I can't share margin data" |
| Contract terms | Their own accounts' invoices |

**Authorize before the model sees data.** Filtering the answer after is too late:
it already read it.

---

## 2. Identity shapes available tools

Same agent, different toolbox:

| Principal | Tools offered |
|---|---|
| CFO | `query_finance_mart`, `export_report` |
| Support rep | `read_invoice`, `refund_invoice` |
| Developer | `read_job_logs`, `rerun_job` |
| Nightly workflow | `reconcile_payments` (and nothing else) |

A tool the model never sees is a tool it **can't be talked into using.**

---

## 3. Identity shapes approval boundaries

| Tier | Example | For whom |
|---|---|---|
| **Autonomous** | Refund ≤ $100 | Support rep, own accounts |
| **Escalated** | Refund $100–$2,000 | Rep proposes, lead approves |
| **Forbidden** | Refund > $2,000, any account | Everyone, via agent |

Same tool, same model. **Different outcome per principal.**

---

## You can't approve every action

```text
"Just have a human approve everything"
        ↓
500 agents × thousands of actions/day
        ↓
approval fatigue → rubber stamp
```

Escalation works when it's **rare and meaningful.**

Policy settles the routine. Humans decide what matters.

---

## 4. Identity makes audit possible

Every consequential action should answer:

- **Principal**: who it was for
- **Agent**: who performed it
- **Action + resource**: what, on which record
- **Policy**: which rule allowed or escalated it
- **Decision**: allowed / denied / approved by whom

"The AI service account did it" is not an audit finding.
**It's an audit failure.**

---

## The model vs. the infrastructure

| The model reasons about | Infrastructure enforces |
|---|---|
| What the user probably means | Who the user is |
| Which approach solves the task | Which data they may see |
| Which tool would help | Which tools exist for them |
| What to propose next | Whether it runs, escalates, or stops |

**Let the model reason freely. Don't let it decide authority.**

---

## The architecture

```text
   Identity         IdP: user, group, workload
      ↓
   Context          only what this principal may see for this task
      ↓
   Policy           identity · role · task · resource · workflow
      ↓
   Available        typed tools: autonomous / escalated / forbidden
   Actions
      ↓
   Audit            principal + agent + action + policy + decision
```

---

## Questions to ask before you approve a rollout

1. When the agent calls a system, **whose identity** does that system see?
2. Can two users get **different context** from the same question?
3. Are tools filtered **per principal**, or is it one toolbox for all?
4. What can run **without a human**, and who decided that?
5. Can we trace any action back to **a person and a policy**?

If the answer to #1 is "a service account," **start there.**

---

## A first step

1. Pick one agent already in production
2. List every credential it uses
3. For each: **whose authority is this, really?**
4. Replace the broadest one with **delegated, per-user** access
5. Log principal + agent on every call

---

<!-- _class: lead -->

# Useful autonomy
# without a universal service account

## Identity → Context → Policy → Available Actions → Audit

---

<!-- _class: lead -->

# Thank You

Miriah Peterson · @Soypete · soypete.tech

*Further reading:* The Determinism Boundary · Sandboxes Are Not Guardrails ·
You Cannot Review Every Agent Action

---

## Sources

- Norm Hardy, *The Confused Deputy (or why capabilities might have been invented)*, ACM SIGOPS OSR, 1988
- IETF RFC 8693, *OAuth 2.0 Token Exchange*, 2020
- NIST SP 800-162, *Guide to Attribute Based Access Control (ABAC)*
