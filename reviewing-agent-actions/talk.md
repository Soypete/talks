---
marp: true
theme: gaia
paginate: true
title: "You Cannot Review Every Agent Action"
description: Attribution, delegation, and audit when agents outpace human review
---

<!-- _class: lead -->

# You Cannot Review
# Every Agent Action

## So what survives instead?

Miriah Peterson · @Soypete
AI Software Factory Summit

---

## Who Am I?

- CEO of Haikai Labs
- Co-host of the **Domesticating AI** podcast
- Building AI systems since 2022

---

<!-- _class: lead -->

# 17,600

## Actions reconstructed from one agent incident.

July 2026. One evaluation task.

<!-- Open with the number. Ask the room to imagine reviewing that queue. Then
point out it was one agent, one task, one afternoon. -->

---

## The Software Factory Premise

```text
more agents · more autonomy · more throughput
```

That premise has a review problem built into it.

```text
1 agent      you can read the diff
10 agents    you skim
100 agents   you approve
1000 agents  you hope
```

**Human review does not scale with the thing it is reviewing.**

---

## The Two Bad Answers

```text
REVIEW EVERYTHING     the factory stops
                      you built expensive autocomplete

REVIEW NOTHING        the factory runs
                      nobody can say what it did
```

Both are real positions people hold.

**Neither is an architecture.**

---

<!-- _class: lead -->

# Review Is the Wrong Unit

## Stop asking "did a human see this action?"

---

## Ask Three Different Questions

```text
1. Could this action have happened at all?
2. On whose authority did it happen?
3. Can we reconstruct it afterward?
```

The first is policy. The second is delegated identity.
The third is audit.

**None of them requires a human in the loop at execution time.**

---

<!-- _class: lead -->

# Question One

# Could It Have Happened?

---

## Constrain the Set, Not the Instance

```text
REVIEWING INSTANCES        CONSTRAINING THE SET
every action, one by one   which actions exist at all
scales with volume         scales with design
human throughput limit     no per-action cost
```

You do not review each SQL query your web app issues.

**You constrained which queries it can issue.**

---

## Shells Break This

```text
model ──▶ bash ──▶ anything the OS permits
```

A shell is not one tool. It is an interface for constructing
unlimited tools.

You cannot write policy about a set you cannot enumerate —
and you cannot review a set you cannot enumerate either.

**Typed tools are what make the set finite.**

---

## Typed Actions Are Reviewable in Advance

```text
❌  kubectl apply -f whatever.yaml

✅  deploy_application(app, environment, version)
```

The second one you can reason about **once**, at design time,
and then stop reasoning about per-invocation.

**Review the contract, not every call under it.**

---

<!-- _class: lead -->

# Question Two

# On Whose Authority?

---

## Attribution Dies at the First Hop

```text
Human ──▶ Agent ──▶ Subagent ──▶ delete_table()
                                      │
                                      ▼
                    audit log: "the agent did it"
```

Nobody can answer who authorized it, what it touched,
or what it cost.

**"The AI decided" is a very convenient place
for responsibility to disappear.**

---

## Two Identities, Carried Together

```text
WORKLOAD IDENTITY     which agent is running?
DELEGATED IDENTITY    whose authority is this?
```

A service account tells the platform which workload made a request.

It cannot tell you which human authorized it.

**Both have to survive every delegation hop.**

---

## What That Looks Like

```python
caller = CallerContext(
    user_id="user-123",
    invoking_subject="user-123",
)

child = caller.delegate(span="subagent-1")

# child.invoking_subject == "user-123"
# child.delegation_depth == 1
```

The subagent gets its own span. **The human rides along unchanged.**

---

## Scope Follows the Human

```text
junior analyst invokes the agent
            ↓
agent operates in the analyst's boundary
            ↓
NOT the service account's warehouse access
```

A delegated subtask should carry a **deliberately scoped**
version of the context required to complete it —

not the full surface available elsewhere in the org.

---

<!-- _class: lead -->

# Question Three

# Can We Reconstruct It?

---

## One Record Per Action

```text
invoking subject          who authorized this
delegation chain          parent span, depth
originating framework     which harness
argument digest           SHA-256, not the arguments
resources touched         what data was involved
policy decision + rule    why allowed or denied
tokens · latency          what it cost
```

Append-only. Emitted **whether or not the call proceeded.**

---

## Why Digest, Not Arguments

```text
arguments          may contain customer data, secrets,
                   PII, proprietary content

SHA-256 digest     proves what was called
                   without copying it into the log
```

An audit trail that leaks the thing it audits is a liability,
not a control.

**You can prove identity of input without retaining input.**

---

## One Instrumentation Path

```text
metrics = rollups over audit records
```

Not a second pipeline that drifts from the first.

If your dashboard and your audit log disagree,
**you have two systems and zero answers.**

---

<!-- _class: lead -->

# What Humans Should Review

## Not actions. Something better.

---

## Move Review Upstream and Downstream

```text
UPSTREAM      the tool contract
              the policy
              the delegation model
              — reviewed once, applies to everything

DOWNSTREAM    exceptions and denials
              anomalies in the audit stream
              the first instance of a new pattern
              — reviewed by volume, not by default
```

**The middle — routine authorized execution — is the part
that should not need you.**

---

## A Denial Is a Review Artifact

```text
policy denied 47 actions this week
            ↓
which rule · which agent · which human · which resource
```

That is a far better review queue than 17,600 approvals.

**Denials are rare, informative, and self-prioritizing.**

---

<!-- _class: lead -->

# The Honest Limits

---

## This Does Not Solve

```text
a correctly authorized action that is wrong
    → policy said yes, the outcome was still bad

a policy that encodes a bad rule
    → determinism enforces mistakes faithfully

drift between stated and actual authority
    → someone widened a scope and nobody noticed
```

Audit tells you what happened.

**It does not tell you it should have.**

---

## What It Does Buy

```text
the factory can run
and you can still answer the question afterward
```

- who authorized this
- what it touched
- what it cost
- which rule permitted it

**That is the difference between autonomy and abdication.**

---

<!-- _class: lead -->

# The Takeaway

## You cannot review every action.

### Constrain the set. Carry the identity. Record the decision.

Then review the contract, the exceptions, and the anomalies —
not the queue.

---

<!-- _class: lead -->

# Thank You

**You Cannot Review Every Agent Action**

Miriah Peterson · @Soypete
Haikai Labs

---

## Sources

**Hugging Face** — Anatomy of a Frontier Lab Agent Intrusion,
July 2026 technical timeline

**NIST SP 800-162** — Attribute Considerations for Access Control

**Agentware** — policy enforcement and audit middleware
[github.com/HaikeiLabs/Agentware](https://github.com/HaikeiLabs/Agentware)

**The Context Engineering Manifesto** — Haikai Labs
