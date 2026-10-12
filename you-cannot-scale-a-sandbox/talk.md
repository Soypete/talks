---
marp: true
theme: gaia
paginate: true
title: "You Cannot Scale a Sandbox"
backgroundImage: url('../images/soypete_background.png')
description: What UNIX time-sharing teaches us about governing agent fleets
---

<!-- _class: lead -->

# You Cannot Scale a Sandbox

## What UNIX time-sharing teaches us about governing agent fleets

Miriah Peterson · @Soypete

---

## Who Am I?

- CEO of Haikei Labs: a governed context layer for AI agents
- Previously: SchoolAI, Weave, Tailscale, MX, Nav
- Co-host of the **Domesticating AI** podcast
- Writing a book on context engineering

<!-- Disclose Tailscale and Haikei up front. Both appear later as examples of
layers, not pitches. -->

---

<!-- _class: lead -->

# "Just put it in a sandbox."

## Correct advice. For one agent.

---

## What a sandbox gives you

```text
filesystem    → scoped
network       → restricted
process       → isolated
blast radius  → contained
```

It answers one question:

**Where can this process execute?**

---

## The questions a fleet asks

- **Whose authority** is this agent using?
- **Which operations** should exist for this identity, task, and resource?
- **Which actions** run automatically, which escalate, which are forbidden?
- **Can we trace** every consequential action to a principal and a policy?

A sandbox answers none of these.

<!-- One agent, one human watching: you can live with the gap. Five hundred
agents for two hundred users: you can't. -->

---

## More sandboxes ≠ scale

```text
1 agent   → 1 sandbox   → 1 token in env
100 agents → 100 sandboxes → 100 tokens in env
                           → 100 drift surfaces
                           → 0 shared policy
```

You multiplied the boundary. You did not add a decision.

---

<!-- _class: lead -->

# We've solved this before.

## 1974

---

## Before time-sharing

One machine. One job at a time.

Safe sharing = **give each user the whole machine, in turn.**

That's the sandbox model.

<!-- Batch processing and dedicated machines: isolation by separation. It works
and it doesn't scale. -->

---

## *The UNIX Time-Sharing System*

Ritchie & Thompson, CACM, 1974

Many users. **One machine. At the same time. Safely.**

Isolation helped. It wasn't the security model.

**The kernel was.**

---

## What made UNIX safe: 1. Identity on every process

- Every process runs **as a user**
- The UID is assigned by the system, not asserted by the program
- It follows the process into **every** system call
- Delegation is explicit: **set-user-ID**

---

## What made UNIX safe: 2. One reference monitor

```text
process ──▶ open/read/write/exec ──▶ KERNEL ──▶ file · device · pipe
```

Every resource behind the same small interface.

No path around the kernel.

---

## What made UNIX safe: 3. Check at `open()`, return a handle

```c
fd = open("/data/orders", O_RDONLY);   // permission checked here, once
read(fd, buf, n);                      // the handle IS the capability
```

- The process never touches the disk
- The process never holds anyone's password
- The descriptor grants **this resource, this mode**, nothing else

---

<!-- _class: lead -->

# Identity + mediation + handles

## That's what let one machine serve many users.

---

<!-- _class: lead -->

# What agents lost

---

## 1. The resources left the kernel

```text
agent ──▶ Salesforce
      ──▶ Slack
      ──▶ Snowflake
      ──▶ LLM provider
      ──▶ internal billing API
```

The sandbox's kernel doesn't know what a **refund** is.

The reference monitor can't see the actions that matter.

---

## 2. The UID became a token in the environment

```bash
export OPENAI_API_KEY=sk-...
export SALESFORCE_TOKEN=...
```

"Process runs as a user" →
**"process runs as whoever owns the key."**

Fifty employees, one agent, one service account: **fifty people with the same
authority.**

---

## 3. `bash` made the action set unenumerable

```bash
curl -X POST https://api.internal/$ANYTHING \
  -H "Authorization: Bearer $TOKEN" -d "$WHATEVER"
```

Possible actions = every endpoint × every argument × every order.

**You can't write policy against a set you can't enumerate.**

---

## The sandbox still worked

It contained the process.

The process then took **valid, unauthorized** actions over the network, using
credentials the sandbox handed it.

Containment succeeded. **No one decided whether the action should exist.**

---

<!-- _class: lead -->

# Rebuild the kernel one layer up

## At the network and the context

---

## Layer 1: Identity on every call

Every request carries the human or workload it acts for, **set by
infrastructure, not by the agent.**

```text
agent ──▶ identity-aware gateway ──▶ LLM provider / tool
              │
              ├─ who: alice@corp (from network identity)
              ├─ key: injected here, never in the sandbox
              └─ log: attributed request
```

---

## Example: Tailscale Aperture

- AI gateway between your org and LLM providers
- Inherits **user or workload identity** from the tailnet
- No API keys distributed to users or agents
- Holds provider keys centrally, attributes every request

**This is the UID, back on the wire.**

<!-- Use this as an example of the layer. Any identity-aware proxy that binds
requests to a principal from infra fills the same slot. -->

---

## Identity isn't authorization

The gateway knows **who** is asking.

It doesn't decide **what this identity should see or do for this task.**

That was the kernel's other job.

---

## Layer 2: A reference monitor for context

```text
principal + task
      ↓
  eligible context      ← what data may enter the window
      ↓
  policy                ← allow · escalate · deny
      ↓
  available actions     ← which typed tools exist
      ↓
  audit
```

---

## Example: a governed context layer (Haikei)

Before the model sees anything:

- **Data**: only what this principal may see for this task
- **Tools**: only operations this task needs
- **Approval**: autonomous, escalated, or forbidden, decided by policy
- **Audit**: every decision tied to principal + policy version

<!-- Disclose: this is what my company builds. The point is the layer and its
order of operations, not the vendor. -->

---

## Check at `open()`, not after `read()`

| Filter output | Authorize context |
|---|---|
| Model already read it | Model never sees it |
| Leak via summary, tool args, memory | Nothing to leak |
| Probabilistic cleanup | Deterministic decision |

**Authorization before context assembly.**

---

## Layer 3: Handles, not secrets

```python
# raw disk
bash("curl ... -H 'Authorization: Bearer $TOKEN'")

# file descriptor
refund_order(order_id="ord_123", amount_cents=4200)
```

- Schema: enumerable
- Scope: one resource
- Credentials: in a broker the model never reads
- Policy decision + enforcement point at the boundary

---

## Layer 4: Approval boundaries

Every typed operation lands in one of three tiers, decided by policy:

| Tier | Example | What happens |
|---|---|---|
| **Autonomous** | `read_order`, `draft_reply` | Runs. Logged. |
| **Escalated** | `refund_order > $500`, `send_external_email` | Pauses for an approver. |
| **Forbidden** | `delete_customer`, `export_all_pii` | Never offered to the model. |

The tier depends on **principal × task × resource × operation**, not the tool name.

<!-- Same refund_order call: autonomous for a support lead under $50, escalated
for a contractor, forbidden for an agent acting for nobody. -->

---

## UNIX had this too: `sudo`

```bash
$ sudo systemctl restart billing
[sudo] password for alice:
```

- Elevation is **explicit**, per command, not ambient
- Policy (`sudoers`) says **who** may do **what**
- Every use is **logged** to a principal

Escalation is a policy decision with a record, not a vibe check.

<!-- sudo is from 1980, not the 1974 paper. Same lineage: setuid made
delegation explicit; sudo made elevation explicit and audited. -->

---

## You cannot review every agent action

```text
1 agent  × 20 actions/task    → a human can watch
500 agents × 2,000 actions/day → approval fatigue → rubber stamp
```

- Approve-everything becomes approve-**anything**
- Escalation only works if it is **rare and meaningful**
- So most actions must be **deterministically** autonomous or forbidden

**Policy decides the boring 99%. Humans decide the 1% that matters.**

<!-- Tie back to "You Cannot Review Every Agent Action." The approval tier is
only trustworthy because the other two tiers keep it small. -->

---

## What an escalation must carry

An approver needs the same six facts the control plane does:

- **who**: principal the agent acts for
- **what**: typed operation + exact resource
- **why**: task and agent's stated reason
- **policy**: which rule escalated it
- **decision**: approved / denied, by whom, when → **audit record**

An approval without these is a click, not a control.

---

## The full map

| UNIX | Agent fleet | Example |
|------|-------------|---------|
| UID per process | Identity per request | Tailscale Aperture |
| Kernel | Policy over context + actions | Haikei |
| `open()` check | Authorize before assembly | PDP |
| File descriptor | Typed tool, brokered creds | Tool schema + PEP |
| `sudo` / `sudoers` | Approval tiers | Escalation policy + audit |
| Process isolation | **Sandbox** | containers, VMs, seccomp |

<!-- The sandbox stays on the map. It's a row, not the table. -->

---

<!-- _class: lead -->

# Model proposes.
# Infrastructure disposes.

---

## What your control plane must make deterministic

1. **Principal**: who this action is for
2. **Task**: what job, assigned by whom
3. **Resource**: exactly which object
4. **Operation**: typed, enumerable
5. **Decision**: allow / escalate / deny, by policy
6. **Record**: audit tying all five together

No six? Another sandbox won't help.

---

## A first step on Monday

1. Pick **one** general-purpose tool: shell, HTTP client, broad SQL
2. Replace **one** use of it with a typed operation:
   principal · resource scope · policy decision · audit record
3. Route model traffic through a gateway that knows **who** it's for

One file descriptor. One UID.

**That's how UNIX started too.**

---

<!-- _class: lead -->

# Thank You

Miriah Peterson · @Soypete · soypete.tech

*Further reading:* Ritchie & Thompson, *The UNIX Time-Sharing System* (1974) ·
*Sandboxes Are Not Guardrails* · *The Determinism Boundary*
