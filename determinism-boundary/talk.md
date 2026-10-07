---
marp: true
theme: gaia
paginate: true
title: "The Determinism Boundary"
description: Where probabilistic reasoning should end and infrastructure should begin
---

<!-- _class: lead -->

# The Determinism Boundary

## Where reasoning ends and infrastructure begins

Miriah Peterson · @Soypete
AI Native DevCon · Brooklyn

---

## Who Am I?

- CEO of Haikai Labs
- Co-host of the **Domesticating AI** podcast
- Building AI systems since 2022

---

<!-- _class: lead -->

# Models Are Probabilistic

## That is not a defect.

It is the entire reason they are useful.

---

## Good Questions for a Model

> Resolve this customer issue.

```text
issue a refund?      apply a credit?
escalate?            replace the order?
ask for more info?
```

No objectively correct answer. Interpretation, ranking, judgment.

**This is exactly where probabilistic reasoning belongs.**

---

## Now Change the Question

> Can this employee approve a $2,000 refund?

```text
identity + role + resource + amount + policy
                    ↓
              allow / deny
```

Same inputs, same answer, every time.

The model may reason the refund is the best business outcome.

## That does not create authority.

<!-- This pair of slides is the whole talk in miniature. Everything after is
elaboration. -->

---

<!-- _class: lead -->

# Reasoning Is Not Enforcement

---

## Four Sentences That Sound Like Controls

```text
"This user probably should not have payroll access."
                                  → not access control

"Policy says managers may approve up to $500."
                                  → not authorization

"Deleting this seems dangerous, I should confirm."
                                  → not a safety boundary

"I'll only use the approved tools."
                                  → not a tool restriction
```

**Reasoning helps a model choose among possibilities.
It should not create permission.**

---

## Why We Keep Making This Mistake

Every model failure has the same tempting fix:

```text
task is hard        → add a planning step
answer unreliable   → add chain-of-thought
strategy failed     → add ReAct
one path is wrong   → add Tree of Thoughts
request ambiguous   → have it ask the user
```

All genuinely useful. All about navigating ambiguity.

**None of them answer whether the action is permitted.**

---

<!-- _class: lead -->

# The Boundary

```text
MODEL          interpret · infer · rank · plan · propose
─────────────────────────────────────────────────────────
INFRASTRUCTURE identity · policy · resource · allow/deny
```

## The model proposes. Infrastructure disposes.

---

## The Shape of the Loop

```text
CONVENTIONAL
  prompt ──▶ model ──▶ tool

BOUNDED
  intent
    ──▶ model reasoning
    ──▶ proposed typed action
    ──▶ deterministic validation
    ──▶ execution
    ──▶ observed authorized result
```

This does not remove ReAct. **It bounds ReAct.**

<!-- The agent still reasons, reconsiders, asks for clarification. What it cannot
do is turn a plausible interpretation into a new permission. -->

---

<!-- _class: lead -->

# The Boundary Is Not Just the Tool Call

## It appears four times.

---

## 1. When Context Is Assembled

```text
❌  retrieve payroll data → tell the model not to disclose it
✅  the user is unauthorized → the data never enters context
```

Access is decided **before** information reaches the model.

---

## 2. When Tools Are Exposed

```text
❌  generic delete_resource() + "do not delete accounts"
✅  the tool is not in this agent's schema
```

A prompt can ask a model not to do something.
A system can make it unavailable.

**Those are not equivalent guarantees.**

---

## 3. When the Action Is Proposed

```text
refund_amount = 700
user_limit    = 500
                 ↓
               DENY
```

No reasoning trace is persuasive enough to change this.

The policy is not evidence to weigh against the customer's
circumstances. **It is a boundary around the operation.**

---

## 4. After Execution

```text
who requested it
which identity the agent acted under
which resource was affected
which policy allowed or denied it
what actually happened
```

Determinism is not only the final allow/deny.

**It is the structure surrounding probabilistic reasoning.**

---

<!-- _class: lead -->

# The Same Mistake, Four Disguises

---

## All One Boundary Error

| The claim | Why it fails |
|---|---|
| reasoning prompts are pragmatics | inference ≠ rules of use |
| sandboxes are guardrails | containment ≠ authorization |
| prompt instructions are policy | prose ≠ enforcement |
| retrieval is access control | finding ≠ permission to use |

**Every one puts responsibility on the wrong side of the same line.**

---

<!-- _class: lead -->

# "Better Models Will Fix This"

## I think the opposite.

---

## Capability Expands the Action Space

```text
more capable model
        ↓
discovers more options
uses more tools
traverses more systems
constructs better plans
        ↓
larger space of reachable actions
```

**Greater reasoning ability makes explicit boundaries
more important, not less.**

The smartest possible model still should not reason its way
into permissions it does not have.

---

## The Evidence Is Already In

July 2026. An agent in a sandbox, given a security challenge.

```text
17,600 reconstructed actions
```

Not one jailbreak — thousands of individually reasonable steps.
Each new capability it discovered became another possible action.

**The failure was letting the space of *discoverable* actions
get close to the space of *permissible* ones.**

---

<!-- _class: lead -->

# What To Build

---

## The Harness as Enforcement Point

Before any tool executes:

1. does this tool exist in this agent's schema?
2. do the arguments validate?
3. which human initiated this?
4. which resource does it target?
5. is that identity, via this agent, in this task, authorized?

**Only then does execution happen.**

Closer to an API gateway than a chat loop.

---

## None of This Is New

```text
authentication        API contracts
type systems          schemas
policy engines        RBAC · ABAC
service boundaries    validation
```

Software engineering spent decades separating business logic
from authorization.

**None of it became obsolete when an LLM entered the architecture.**

Agents make it more important — the caller now constructs
requests no engineer wrote.

---

<!-- _class: lead -->

# The Takeaway

## Let the model reason about the work.

## Let infrastructure decide what reality permits.

If the policy says no, the answer is no —
**no matter how convincing the argument.**

---

<!-- _class: lead -->

# Thank You

**The Determinism Boundary**

Miriah Peterson · @Soypete
Haikai Labs

---

## Sources

**The Context Engineering Manifesto** — Haikai Labs

**Hugging Face** — [Anatomy of a Frontier Lab Agent Intrusion](https://huggingface.co/blog/agent-intrusion-technical-timeline),
July 2026 technical timeline

**NIST SP 800-162** — Attribute Considerations for Access Control Systems

Chain-of-Thought · ReAct · Tree of Thoughts · ReSpAct

---

<!-- _class: lead -->

# Bonus

## Questions this gets

---

## "Doesn't this make agents less useful?"

It makes them **deployable**.

```text
unbounded agent    impressive demo, ships to nobody
bounded agent      narrower, runs in production
```

Every constraint here is one you already accept from a web
application. We do not consider an API less useful because it
checks authorization.

**The alternative is not a more capable agent.
It is an agent nobody will approve.**

---

## "Where does the policy come from?"

Mostly it already exists.

```text
refund limits          → already in your finance system
data access rules      → already in your IdP
deployment approvals   → already in your CI config
who owns what          → already in your org chart
```

The work is usually not writing new policy.

**It is making existing policy reachable at inference time
instead of living in a Confluence page.**

---

## "What about agents that need to explore?"

Exploration and authority are separable.

```text
EXPLORE     read broadly, propose freely, plan
ACT         narrow, typed, authorized, audited
```

Let the agent investigate the incident, read the logs, form a
hypothesis, and propose restarting the service.

**Then check whether it may restart the service.**
