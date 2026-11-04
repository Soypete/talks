# You Cannot Scale a Sandbox

> What UNIX time-sharing teaches us about governing agent fleets

The standard advice for running an AI agent safely is to put it in a sandbox. Give
it its own container, a throwaway filesystem, a restricted network, and a process
boundary. If something goes wrong, the damage stays in the box.

That advice is correct. It is also the advice for running *one* agent.

When a company goes from one coding agent on one laptop to hundreds of agents acting
for different users across Slack, a warehouse, a CRM, and a dozen internal APIs, the
instinct is to repeat what worked: more sandboxes, one per agent, one per task, one
per user. It feels like scaling. It isn't, because the questions that matter at
fleet scale aren't containment questions.

- Whose authority is this agent using?
- Which operations should exist for this identity, this task, and this resource?
- Which actions run automatically, which need approval, and which are forbidden?
- When something happens, can we tie it back to a principal and a policy?

A sandbox answers none of these. It answers "where can this process execute?" That
was a reasonable question when there was one agent and one human watching it. With
a fleet, it's the wrong question.

## We have solved this problem before

Computing has been here before. Early computers ran one job at a time: you
submitted your work and waited. Sharing a machine among many people safely meant
handing each of them the whole machine in turn. That is the sandbox model: isolation
by giving everyone their own environment.

Thompson and Ritchie's 1974 paper, *The UNIX Time-Sharing System*, describes the
alternative. Many users share one machine at the same time, safely. The paper is
usually read for pipes and "everything is a file," but its quieter lesson is how
UNIX made sharing safe without giving everyone their own computer. It came down to
three decisions.

**Identity travels with every process.** Every process runs as a user. The UID is
not something the program asserts about itself. The system assigns it, and it
follows the process into every system call. Delegation is explicit: the
set-user-ID bit lets a program run with its owner's authority, and the system
records that it does.

**Every resource goes through one mediated interface.** Files, devices, and pipes
are all reached through the same handful of calls, and the kernel sits behind all
of them. No process can reach a resource without passing through the kernel.
That makes the kernel what security people call a reference monitor: one place
where every access decision happens.

**Permission is checked at `open()`, and you get back a handle.** A process asks to
open a file. The kernel checks the UID against the permission bits once. If it
succeeds, the process gets a file descriptor: a small integer that grants access to
that resource and nothing else. Reads and writes go through the descriptor. The
process never touches the disk directly, and it never holds anyone's password.

Isolation mattered too. Processes had separate address spaces, and a crash in one
didn't take down the others. But isolation was never the whole security model. The
kernel was. Identity plus a single point of mediation plus handles instead of raw
access is what let one machine serve many users.

## What agents lost

Look at a typical sandboxed agent through that lens.

**The resources left the kernel.** The things an agent acts on are a Salesforce
instance, a Slack workspace, a Snowflake warehouse, an LLM provider, and an internal
billing API. None of them are files the kernel mediates. They sit across the
network, and the sandbox's kernel has no idea what a "refund" or a "customer record"
is. The reference monitor that made UNIX safe can't see the actions that matter.

**The UID turned into a token in the environment.** Inside the sandbox, identity is
usually whatever credential someone put in an environment variable or a mounted
config file, often a service account shared by every agent and every user. The
original "process runs as a user" guarantee becomes "process runs as whoever owns
`OPENAI_API_KEY`." When fifty employees use the same agent, all fifty inherit the
same authority.

**`bash` made the action set unenumerable.** A general-purpose shell is the most
flexible tool you can give an agent and the least governable. With `curl` and a
token, the set of possible actions is every endpoint the token can reach, in any
order, with any arguments. You can't write policy against a set you can't
enumerate.

So the sandbox still does its job. It contains the process. But the process can
take perfectly valid, perfectly unauthorized actions over the network using
credentials the sandbox handed it. Containment worked, and nobody decided whether
those actions should exist.

Adding more sandboxes doesn't fix this. A hundred sandboxes give you a hundred
copies of the same gap, each with its own credential, its own drift, and its own
audit trail if you're lucky.

## Rebuilding the kernel one layer up

The fix isn't to give up on UNIX's model. It's to rebuild the parts agents lost at
the layer where their resources now live: the network and the context the model
reasons over.

### Identity on every call

The first missing piece is the UID. Every request an agent makes, whether to a model
provider or a tool, should carry the identity of the human or workload it acts for,
and that identity should come from infrastructure, not from the agent.

Identity-aware gateways do this at the network layer. Tailscale's Aperture is a good
worked example. It is an AI gateway that sits between an organization and its LLM
providers. Devices have already authenticated to join the tailnet, so Aperture
inherits that user or workload identity instead of asking for new logins or API
keys. The gateway holds the provider keys, attaches them on the way out, and
attributes every request to an identity.

That is the UNIX pattern almost exactly. The agent never holds the provider
credential, and the identity on the request comes from the system, not the
process.

### A reference monitor for context and actions

Identity on the wire tells you *who* is asking. It doesn't decide *what that
identity should be able to see or do* for this task. That's the kernel's other job,
and it's the one agents need most.

A governed context layer plays this role. It is the pattern we're building at
Haikei. Before the model sees anything, the context layer takes the principal, the
task, and the policy, and decides:

- which data is eligible to enter the context window,
- which tools exist for this agent in this task,
- which of those operations run automatically, which need escalation, and which
  are forbidden,
- and what gets written to the audit log when something happens.

The order matters: identity → context → policy → available actions → audit. Filtering a
model's output after it has already read data it shouldn't have is like checking
permissions after `read()`. UNIX checks at `open()`. Agents should be authorized
before context is assembled, not cleaned up after inference.

### Handles, not secrets

The last piece is the file descriptor. A typed tool such as
`refund_order(order_id, amount)`, with a schema, a resource scope, and a policy
decision attached, is a handle. It gives the agent access to one operation on
one kind of resource, checked once at the boundary, and the credentials stay in a
broker the model never reads.

Compare that to `bash` plus a token. One is a file descriptor; the other is the raw
disk. Typed tools turn an unenumerable action surface back into a finite set you
can write policy against, test, and audit.

## Two layers, not one product

These are two layers, and they do different jobs:

| UNIX | Agent fleet | Example |
|------|-------------|---------|
| UID on every process | Identity on every request | Identity-aware gateway (Tailscale Aperture) |
| Kernel as reference monitor | Policy over context and actions | Governed context layer (Haikei) |
| `open()` permission check | Authorize before context assembly | Policy decision point |
| File descriptor | Typed tool with brokered credentials | Tool schema + enforcement point |
| Process isolation | Sandbox | Containers, VMs, seccomp |

The sandbox stays in the table on purpose. You still want containment for code
execution. It just isn't the authorization model, and it never was, even in UNIX.

## The determinism boundary

None of this is about making agents less capable. The model should be free to
reason, plan, and propose. What changes is who decides whether a proposal becomes
real. The model proposes; infrastructure disposes.

A scalable agent control plane has to make a short list of things deterministic:

1. **Principal:** which human or workload this action is for.
2. **Task:** what job the agent was given, and by whom.
3. **Resource:** exactly which object the action touches.
4. **Operation:** a typed, enumerable action, not a shell string.
5. **Decision:** allow, deny, or escalate, made by policy and not by the model.
6. **Record:** an audit entry tying all five together.

If your architecture can't produce those six things for every consequential action,
adding another sandbox won't help. You need what UNIX had: identity everywhere, one
place where decisions happen, and handles instead of raw access.

## A first step

Pick one general-purpose tool your agents use today, such as a shell, a generic HTTP
client, or a broad SQL connection. Replace one thing it's used for with a typed
operation that has an explicit principal, resource scope, policy decision, and audit
record. Route the agent's model traffic through a gateway that knows who the
request is for.

That's one file descriptor and one UID. That's how UNIX started too.

---

*References: Ritchie & Thompson, "The UNIX Time-Sharing System," CACM 17(7), 1974.
Saltzer, Reed & Clark, "End-to-End Arguments in System Design," ACM TOCS, 1984.
Tailscale, "What is Aperture?" (tailscale.com/docs/aperture). Related: "Sandboxes
Are Not Guardrails," "The Determinism Boundary."*
