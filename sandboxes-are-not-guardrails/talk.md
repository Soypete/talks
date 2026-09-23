---
marp: true
theme: gaia
paginate: true
title: "Sandboxes Are Not Guardrails"
description: Why containment infrastructure is not authorization for autonomous agents
---

<!-- _class: lead -->

# Sandboxes Are Not Guardrails

## Containment is not authorization

Miriah Peterson · @Soypete
Agent Substrate Day · Salt Lake City

---

## Who Am I?

- CEO of Haikai Labs
- Co-host of the **Domesticating AI** podcast
- Building AI systems since 2022

---

<!-- _class: lead -->

# July 2026

## We did everything we were told to do.

---

## The Setup

An OpenAI agent. A cybersecurity challenge. A sandbox.

```text
network restrictions
process isolation
purpose-built containment
```

By every conventional definition of agent security, this was correct.

**Then it escaped.**

<!-- Set this up as compliance, not negligence. Every control we recommend was
present. That is what makes the incident useful rather than embarrassing. -->

---

## The Path Out

```text
zero-day in a package registry cache proxy
            ↓
external code-execution environment
            ↓
root access there
            ↓
launchpad against Hugging Face
            ↓
production systems · evaluation datasets
```

<!-- Walk it, do not dwell. The point is the shape: each step was reachable from
the previous one. -->

---

<!-- _class: lead -->

# 17,600 actions

## Not one jailbreak.

Thousands of individually reasonable steps toward a goal.

<!-- This number is the heart of the talk. There was no moment where the model
became malicious. There was no single action a reviewer would flag. Each step was
a sensible next move given what the agent could see. -->

---

## What the Agent Was Doing

```text
inspect environment
      ↓
what can I do from here?
      ↓
discover binaries · mounts · services
credentials · network paths · APIs
      ↓
incorporate discovery into next step
      ↓
repeat
```

**That is not anomalous behavior. That is an agent loop.**

<!-- We built systems whose value proposition is discovering useful next actions.
Then we are surprised when they discover actions we forgot to prohibit. -->

---

<!-- _class: lead -->

# The Sandbox Did Its Job

## It answered the question it was asked.

---

## Two Different Questions

```text
SANDBOX    Where is this process allowed to execute?

GUARDRAIL  Is this operation authorized?
```

A container can stop a process reading `/etc/shadow` on the host.

It cannot determine whether the API the agent just discovered was an
appropriate resource for this task.

**Those are authorization questions. We keep handing them to containment.**

---

## Containment vs. Authorization

| | Sandboxing | Guardrails |
|---|---|---|
| **Question** | where can it run | is this action allowed |
| **Mechanism** | OS, containers, netpol | policy, schemas, validation |
| **Scope** | CPU, RAM, syscalls, FS | APIs, business logic |
| **Failure** | privilege escalation | logic abuse, bad mutation |

**Production agents need both. We usually ship one.**

---

<!-- _class: lead -->

# Agents Broke an Assumption

## Software used to decide which paths exist.

---

## Traditional Applications

```text
engineer writes the path
      ↓
button → API → service → database
      ↓
user chooses which path to initiate
```

The user picks. **The software defines what can be picked.**

---

## Agentic Applications

```text
model participates in deciding what happens next
```

That is the feature. We do not have to enumerate every sequence in advance.

But if the model discovers the next operation, something has to decide
which discovered operations are valid.

**Dynamic control flow is a new security problem, not a new UX.**

---

<!-- _class: lead -->

# Then We Gave It Bash

---

## Bash Is Not a Tool

It is an interface for constructing unlimited tools.

```text
read files · start processes · open sockets
install packages · inspect env · call APIs
modify config · invoke interpreters · pipe anything
```

The sandbox now has to anticipate **every composition** of commands,
processes, interpreters, package managers, and OS behaviors the model
might discover.

<!-- This is the most common architecture in agent harnesses today, and it is
the one that makes containment do impossible work. -->

---

## The Honest Version

We built a system whose purpose is **discovering useful next actions**,

then gave it an interface capable of expressing **almost any action**,

then asked a container to prevent the bad ones.

## The surprise would have been if it found nothing.

---

<!-- _class: lead -->

# Probabilistic Models
# Need Deterministic Boundaries

---

## Two Architectures

```text
CONVENTIONAL
  model ──▶ shell ──▶ infrastructure constraints
  "ask what should happen, then contain the consequences"

GUARDRAILED
  model ──▶ structured tool request
        ──▶ policy + validation middleware
        ──▶ authorized business operation
        ──▶ infrastructure
  "the model proposes; the architecture decides it exists"
```

---

## The Harness Is a Contract

Most harnesses are a loop:

```text
ask model → execute → return result → repeat
```

A production harness asks more before executing:

- does this tool exist?
- do the arguments match the schema?
- which user initiated this?
- which resource does it target?
- is that user, via this agent, in this task, authorized?

**Closer to an API gateway than a chat loop.**

---

## Decide Before Inference, Too

```text
authorize ──▶ assemble context ──▶ infer
```

If the user cannot access payroll data, the model should not receive
payroll data and an instruction not to mention it.

```text
❌  put everything in context, add a system prompt
✅  the data never enters this agent's context
```

**The model should not decide what it is allowed to know.**

---

## Whose Authority Is This?

```text
junior analyst invokes the finance agent
            ↓
agent operates in the analyst's boundary
            ↓
NOT the service account's warehouse access
```

ABAC over subject, resource, action, environment — evaluated
**before context assembly**, not filtered after.

---

<!-- _class: lead -->

# Sandboxes Still Matter

## They solve one layer.

---

## Four Questions, Four Layers

```text
sandbox         where can this process execute?
policy layer    is this operation authorized?
context layer   what may this agent receive?
typed tools     which operations exist at all?
```

Isolation, restricted networking, minimal credentials, least-privilege
RBAC — keep all of it.

**Defense in depth means the layers are different, not redundant.**

---

<!-- _class: lead -->

# The Takeaway

## A sandbox controls where code runs.

## A guardrail controls which actions exist.

The agent will keep asking *"what can I do from here?"*

### Our architecture decides which answers are real.

---

<!-- _class: lead -->

# Thank You

**Sandboxes Are Not Guardrails**

Miriah Peterson · @Soypete
Haikai Labs

---

## Sources

**Hugging Face** — Anatomy of a Frontier Lab Agent Intrusion:
A Technical Timeline of the July 2026 Incident

**Hugging Face** — Security Incident Disclosure, July 2026

**Forge** — structured agent middleware
[github.com/antoinezambelli/forge](https://github.com/antoinezambelli/forge)

**Agentware** — policy enforcement and audit middleware
[github.com/HaikeiLabs/Agentware](https://github.com/HaikeiLabs/Agentware)

---

<!-- _class: lead -->

# Bonus

## Questions this gets

---

## "So no shell access ever?"

Not quite. **Scope it like any other capability.**

```text
exploratory / dev      shell is fine, blast radius is you
bounded task           typed tools, no shell
production autonomy    typed tools + policy + audit
```

The problem is not that shells exist. It is that a shell in an
autonomous loop makes the set of possible actions unknowable —
and you cannot write policy about a set you cannot enumerate.

---

## "Isn't this just least privilege?"

Yes — and that is the point.

```text
nothing here is new security thinking
```

Authentication, API contracts, type systems, schemas, policy engines,
RBAC, ABAC, service boundaries, validation.

**None of it became obsolete when an LLM entered the architecture.**

Agents make it more important, because the caller now constructs
requests no engineer wrote.

---

## "Won't better models fix this?"

The opposite.

```text
more capable model
      ↓
discovers more options · traverses more systems
      ↓
larger space of reachable actions
```

**Greater reasoning ability expands the attack surface.**

The smartest possible model still should not reason its way into
permissions it does not have.
