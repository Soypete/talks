# Anatomy of a Cloud Agent Harness

> What happens when the harness leaves your laptop?

AI agents were born on workstations.

That origin story matters. A local agent harness can rely on the operating system to answer questions that seem invisible in the product demo:

- Who is running this process?
- Which files can it read?
- Which credentials are available?
- Which commands can it execute?
- What network can it reach?
- Where does its state live?

The laptop is not just where the agent runs. It is part of the agent's security model.

When the harness moves into the cloud, those answers stop being implicit. Compute becomes ephemeral. Identity becomes a workload identity. Secrets arrive through explicit delivery mechanisms. Access is mediated through APIs, connectors, and policies. State must be externalized. Every action needs an accountable subject.

That is the architectural shift from a bare-metal agent harness to a cloud agent harness.

This article uses the locally available Lo Agent checkout as the concrete reference
for the local side of that transition. The checkout was last observed at version
`0.2.23`, commit `b421f60`; it has not been refreshed for this article. The point is
not to claim that this snapshot is the latest Lo release, but to name the seams a
cloud design must preserve.

## The actual anatomy of a local harness

Lo makes the “harness around the model” concrete. Its important layers are:

```text
model client / inference adapters
              ↓
agent loop: decide → call → observe → continue or stop
              ↓
tools, skills, permissions, and sandbox
              ↓
memory, compaction, events, and replay
              ↓
sessions, coordinator, web UI, integrations, and telemetry
```

The model is only one component. The harness owns the loop, decides which tools are
visible, validates and executes calls, manages context, records events, and exposes a
durable result. Lo’s repository makes these boundaries visible in code: inference
adapters, `agent/loop.py`, skills and tools, permissions and sandboxing, event logging
and replay, MCP/UTCP integrations, session coordination, and the web interface.

This is the anatomy to carry into the cloud—not a laptop-shaped process copied into a
container.

## Guidelines for designing the harness

1. **Separate the model, loop, and harness.** The model proposes an action; the loop
   advances the task; the harness supplies reliability and policy.
2. **Give every job a contract.** Define allowed tools, inputs, outputs, stop condition,
   and machine-checkable definition of done before inference starts.
3. **Scope tools by phase.** Do not expose every capability to every turn.
4. **Validate outside the model.** Check tool names, arguments, schemas, authorization,
   and final results in deterministic code.
5. **Make recovery explicit.** Handle malformed calls, useful error feedback, bounded
   retries, backoff, and a clear exhausted-retry state.
6. **Treat context as runtime state.** Persist events and results; compact old rounds
   deliberately; measure what was removed and retained.
7. **Keep policy outside the prompt.** Permissions, secrets, network access, and
   authorization must be enforced by tools and services.
8. **Carry two identities.** Record workload identity and delegated human identity.
9. **Externalize state; make compute replaceable.** A task should survive a pod restart—
   and a rolling update. Persist between steps, not at the end.
10. **Observe the completed job.** Measure phases, rounds, tools, retries, tokens,
    latency, exit reason, verification, and cost—not just streamed text.

## What the laptop quietly provides

Before naming what breaks, it is worth being precise about what the workstation hands the
harness for free:

```text
identity · filesystem · credentials · processes
network · persistent state · installed tools
```

Unix already knows who you are. Files have an owner, a group, and read, write, and
execute bits. Processes run as identities. When you ask a local agent to push a branch,
it uses authority that already exists in its execution environment; when you ask it to
read a file, the filesystem decides whether that is allowed.

The agent inherits those constraints without anyone designing them. That inheritance is
the thing the cloud takes away. Cloud-native workloads have service identities, RBAC,
secret injection, explicit APIs, and ephemeral compute—an excellent model for services.

Agents are weird, because an agent acts on behalf of a person. Is it a service, a user, a
delegate, or all three? The six problems below are what that question turns into once the
workstation is gone.

## From one laptop to an agent workforce

The first instinct is often to give every employee a machine with an agent installed on it. That works for one person and one active task. It becomes awkward when an organization needs an agent to work on multiple tasks at once, coordinate access to shared files, connect to external systems, or continue working while its human is in a meeting.

These are familiar software scaling problems—now with an autonomous decision-maker inside the workload.

The cloud-native model gives us useful layers:

```text
Kubernetes control plane
  schedules, scales, and isolates workloads
            ↓
Agent harness workload
  coordinates tools, files, and task state
            ↓
Ephemeral agent tasks
  bounded units of work that can run concurrently
            ↓
External APIs and data sources
  repositories · documents · databases · internal services
```

The control plane is the platform foundation. The harness is the software layer that provides an agent workspace. Individual agent tasks can start and stop as needed, instead of tying the agent's lifetime to a person's laptop.

## Problem one: identity

### The cloud-native agent has two identities

A service account can tell us which workload is making a request. It cannot, by itself, tell us which person authorized the request or what that person is allowed to see.

Reliable agent systems therefore need to carry two identities through the execution path:

1. **Workload identity:** which agent, deployment, or job is running?
2. **Delegated identity:** which human or principal authorized this action?

This distinction is the foundation for least privilege and useful audit logs. “The agent accessed the customer record” is incomplete. A meaningful record also needs the invoking user, the purpose, the policy decision, and the exact data or operation involved.

## Problem two: OAuth

Humans log in. Agents do not.

A local application has a natural home for the interactive flow: open a browser, ask the
user to authenticate, receive an authorization code, store and refresh tokens locally, and
ask again when the refresh fails. The workstation makes this easy enough that it stops
looking like a design decision.

Now remove the human. A task starts from a queue, a schedule, or an event. There may be
nobody present, and the agent still needs delegated authority to act. The options are all
uncomfortable in different ways:

```text
Shared static credential      broad, hard to attribute, hard to rotate
Personal access token         one human's authority, everywhere
Long-lived OAuth token        durable, and durable is the problem
User reauthentication         correct, and impossible at 3am
Service identity              answers "which workload", not "for whom"
Delegation broker             more infrastructure, right shape
```

Headless applications already solved much of this: they store authorization grants,
refresh credentials, request reauthentication, revoke access, and scope permissions. The
agent case adds one complication those systems never had to model—the thing holding the
token is also untrusted execution that reads attacker-controlled text.

## Problem three: secrets

The classic agent architecture is a `.env` file containing a GitHub token, a model
provider key, and a database password, plus a process with shell access.

A prompt that says "never access secrets" is not equivalent to `permission denied`. The
model reads that instruction in the same context window as a repository, a document, a
tool description, or an API response—any of which may contain text arguing the opposite.
Security boundaries have to exist outside model reasoning.

Locally you can get part of the way with runtime secret injection: a credential manager
that supplies the secret to the operation without the value ever entering the model's
context. Cloud-native infrastructure has excellent versions of this—vaults, cloud secret
managers, workload identity, sidecars, short-lived credentials.

There is a catch, and shell access is the whole of it. If the process can run `env`, read
files, list other processes, or make arbitrary network calls, then a secret that exists
anywhere reachable by that process is reachable by the model driving it. The abstraction
is only as strong as the narrowest capability you actually granted.

## Problem four: tools

This is the most consequential architectural change, and the one most often skipped.

A general-purpose harness gives the model a shell, and the shell gives it anything the
operating system permits. That is extraordinarily powerful and extraordinarily difficult
to constrain, because the capability surface is "everything" and the policy surface is a
sentence in a prompt.

The cloud-native alternative puts software between the decision and the action:

```text
              ┌── GitHub tool
              │
LLM → policy ─┼── document tool
              │
              ├── database tool
              │
              └── deployment tool
```

The model chooses; software controls what choosing can accomplish. Instead of letting an
agent run `kubectl apply -f whatever.yaml`, give it:

```text
deploy_application(application, environment, version)
```

The second interface is narrower, deterministic, authorizable, and auditable. You can
write a policy about it, log it meaningfully, and reason about its blast radius. You
cannot do any of those things about an arbitrary shell command.

This changes what an agent is. It stops looking like a coding agent running forever and
starts looking like software that contains probabilistic decision-making. Typed tool
interfaces, workflow engines, and explicit orchestration make agents boring in the way
production systems should be boring—the harness becomes part of the application
architecture rather than a general-purpose escape hatch.

## Problem five: authorization

Authentication asks who you are. Agent authorization has to answer a longer question:
what may you do, for whom, with what data, right now?

The practical consequence is that job-specific agents should not be one agent with
different prompts. A marketing agent reaching a CMS, analytics, and brand assets and an
engineering agent reaching source control, CI, and development infrastructure are
different authorization subjects, not different system messages.

```text
You are a marketing agent.        GitHub production repository:
Never modify production code.     DENY
```

The left side is intent. The right side is authority. Intent belongs in prompts;
authority belongs in infrastructure. Least privilege finally has a precise form here: the
question is not what the human can access, but what this agent needs in order to
accomplish this job on that human's behalf. That set should be dramatically smaller.

## Problem six: state

### Ephemeral and long-running are the same requirement

It is tempting to read "ephemeral compute" as a constraint the cloud imposes and a
laptop escapes. The opposite is closer to the truth.

Two failures look different and are not:

- **The context window fills.** The task is not finished, and the next session starts
  with no memory of the previous one. Anthropic [describes this][harness-long-running]
  as a software project staffed by engineers working in shifts, where each new engineer
  arrives with no memory of what happened on the previous shift.
- **The compute disappears.** Not because pods crash, but because we deploy. A rolling
  update drains the pod while the agent is forty minutes into a task. Kubernetes is not
  going to ask whether the agent was finished.

Both are solved by the same move: get the state out of the thing that dies. Externalize
state and compute becomes disposable; make compute disposable and the work can run
longer than any single machine. The laptop could never offer that trade, because its
state and its compute are the same thing.

This has a design consequence. The unit of work has to be a **step**, not a session:
small enough to finish inside a termination grace period, durable enough to hand off.
Persist between steps, not at the end. Pod A completes a step and persists; Pod B reads
that state and continues at the next one.

Something also has to notice the step landed and schedule the next one—a queue, a
controller reconciling desired against actual, or an event log with a cursor. This is
worth naming, because "the next pod picks it up" otherwise describes a miracle. The
agent step loop is a reconciliation loop: observe state, decide one action, converge,
repeat. Kubernetes controllers have worked this way the whole time. The difference is
that the decider is probabilistic, which is exactly why a policy layer belongs between
the decision and the action.

State is also not one thing. Conversation state survives a context reset. Task progress
survives a pod restart. Workspace state can often be rebuilt from source. Authority
outlives the task itself. Audit outlives everything. A single ordered event stream can
drive the work, but it must not be the same stream that constrains it: the agent
advances the work cursor, cannot write the audit log, and cannot read the authority
store.

Anthropic's own account of [running managed agents at scale][managed-agents] arrives at
a similar decomposition—a durable append-only session log outside the harness, a
stateless brain resumed with `wake(sessionId)`, and interchangeable sandboxes reached
through `execute(name, input)`—summarized in the section title "the session is not
Claude's context window." Their advice for the harness itself is "don't adopt a pet."

That work solves state and keeps credentials out of the sandbox, through resource-bundled
auth or a vault behind a proxy. It does not answer whose authority a stateless brain is
exercising. Nothing in `wake(sessionId)` says on whose behalf.

A related point from their [harness design work][harness-design]: "every component in a
harness encodes an assumption about what the model can't do on its own." That is a useful
test to apply to each layer described here. It is also why the same team notes that the
space of interesting harness combinations does not shrink as models improve—it moves.

## From files and skills to APIs

Teams often try to govern agents with instructions in Markdown or system prompts: do not access secrets, do not modify production, only use approved data.

Those instructions may be helpful, but they are not enforcement boundaries. The model reads instructions alongside untrusted content. A repository, document, tool description, or API response can contain text that attempts to redirect the agent.

The security boundary must exist outside the model's reasoning. A denied filesystem operation, an unavailable connector, a policy engine, or a tool that refuses an unauthorized request is stronger than a sentence asking the model to behave.

The local harness is naturally file-oriented. It searches a working tree, reads local configuration, invokes shell commands, and relies on skills installed beside it. That model does not scale cleanly when the data lives across repositories, document systems, databases, queues, and internal services.

In the cloud, the agent needs explicit API-based access to those sources. The important design move is not to recreate one giant filesystem; it is to expose narrow, reliable interfaces that the harness can call from ephemeral workloads.

This is where agentic middleware fits. It translates a model's probabilistic decision into a deterministic operation: route context, select a tool, coordinate state, enforce access, and record what happened.

## Agentic middleware

Agentic middleware sits between the task and the services it needs:

```text
Agent task
    ↓
Agentic middleware
  routes context
  selects tools
  coordinates state
  enforces access
  records actions
    ↓
APIs and cloud-native services
```

It is the layer that lets us move from a harness that manipulates files to a system that coordinates APIs, queues, databases, and other services. It also gives the platform a place to handle identity, retries, concurrency, and auditability.

## Middleware is a shape we have built before

None of this shape is new. Every serious web framework ships the same directory:
authentication, CORS, sessions, trusted hosts, body limits, error handling. Nobody puts
authentication in the view function. We factored it out because every request needs it
and no individual handler should be trusted to remember.

The properties are always the same: one path everything traverses, cross-cutting
concerns the handler cannot skip, policy composed declaratively outside business logic,
and a handler that stays ignorant of all of it.

A tool call is a request. The model is the least trustworthy handler we have ever
shipped.

Agent frameworks are rediscovering this independently. Agent SDKs have grown input and
output guardrails, per-tool checks, tool identity, lifecycle hooks, and a context object
threaded through the run. Coding harnesses like OpenCode ship [permission
systems][opencode-permissions] with allow, ask, and deny rules, pattern-matched on tool
input, last matching rule winning, and [overridable per agent][opencode-agents]. [MCP
gateways][mcp-gateway] offer a centralized policy enforcement point with fail-closed
defaults and full audit trails, and the June 2026 Enterprise-Managed Authorization
extension to the MCP spec makes enterprise identity providers the authoritative
provisioner for server access. All of this is real policy living outside the prompt, and
all of it is good.

## Why the cloud changes the trust assumptions

The difficulty is that most of this middleware assumes the process it runs in is
trustworthy, and that a human is nearby.

That assumption breaks quietly. Run the same harness headlessly and "ask" has nobody to
ask. The failure modes are already reported in the wild: [deny rules ignored][bug-deny]
when a custom agent is invoked through an SDK path, and [approval prompts that nobody
answers][bug-ask] when permissions are requested with no human in the loop. A laptop
harness has a backstop—the user sees the prompt. A cloud harness does not, and the call
either proceeds silently or hangs.

"Ask" is not a policy. It is a human in a loop that the cloud removed.

So the shape stays and the trust assumptions change:

```text
LOCAL MIDDLEWARE              CLOUD MIDDLEWARE
in the harness process   ──▶  outside it, fail-closed
ask the user             ──▶  decide without one
one identity             ──▶  subject carried across hops
logs for debugging       ──▶  audit as a product requirement
per-framework hooks      ──▶  one record shape
```

The delegation row is the one that network gateways structurally cannot reach. A gateway
sits at the client-to-server boundary; once a harness spawns a subagent in-process, the
gateway sees a single identity. Attribution dies at the first hop: the subagent runs as a
service account, and every log downstream says "the agent did it." Nobody can answer who
authorized the action, what data it touched, or what it cost.

Keeping the invoking human attached through every delegation hop—alongside the workload
identity, with a record shape that does not change when the framework or model
changes—is the part that has to be built for agents specifically.

## From model capability to governed velocity

The architecture question is no longer simply, “Which model is smartest?” It is also:

> Can this agent act quickly without becoming an unaccountable pathway into the business?

The answer depends on architecture. Compute should be replaceable. Credentials should be short-lived and scoped. Connectors should be controlled. Policies should be enforced outside the model. Context should remain under the organization's control. Actions should be attributable to a human request and a specific workload.

That is how agents move from impressive demonstrations to dependable infrastructure.

## Agentware

The goal is to make the path from a local, filesystem-oriented harness to a scalable, API-oriented cloud agent understandable and buildable. [Agentware](https://github.com/HaikeiLabs/Agentware) is one answer: policy enforcement and audit middleware for agent tool calls, in Go, Python, and TypeScript.

Attribution dies at the first delegation hop. An agent spawns a subagent, the subagent
runs as a service account, and every log downstream says "the agent did it." Nobody can
answer who authorized the action, what data it touched, or what it cost. Every problem
named in this article reappears at every hop.

Every tool an agent invokes passes through one interception point. Policy decides whether
the call proceeds—fail-closed, so a call with no caller context is denied rather than
trusted—and an audit record is emitted either way. That record carries the invoking
subject, the delegation chain, the originating framework, a digest of the arguments
rather than the arguments themselves, the resources touched, the policy decision and the
rule behind it, tokens, and latency. When an agent spawns a subagent, the child gets its
own span and its own delegation depth, and the human subject rides along unchanged.

The record shape does not change when you swap frameworks or models. That is the point.

## A note on the other kind of ephemeral

Not every agent system wants durable state. [Mayfly][mayfly] takes the opposite
position deliberately: transient chat channels for agents, created with a click and
handed to agents as a URL, so that agents on different machines, different networks, and
different clouds can coordinate mid-task. Agents can even create their own channels. The
name refers to the insect, and the lifespan is the point.

Both designs are correct, because they answer different questions. This article is about
work that must survive the machine running it. Mayfly is about a conversation that should
not survive at all.

It is worth reading for the security note as much as the design. Its own description of
the model is blunt: "once you have the URL, you have root. Every client is equally
privileged. Every client can read everything." That is entirely reasonable for a
throwaway channel between agents you already trust, and it is exactly the property that
does not survive contact with enterprise systems. A capability URL is not a delegated
identity. The fun version and the governed version are not the same system.

## References

- [Effective harnesses for long-running agents][harness-long-running] — Anthropic, November 2025
- [Harness design for long-running application development][harness-design] — Anthropic, March 2026
- [Scaling managed agents: decoupling the brain from the hands][managed-agents] — Anthropic, April 2026
- [Mayfly][mayfly] — Josh Bleecher Snyder, September 2026
- [Lo Agent](https://github.com/IMJONEZZ/lo-agent) — the local harness used as the concrete reference
- [Agentware](https://github.com/HaikeiLabs/Agentware) — policy enforcement and audit middleware for agent tool calls

[harness-long-running]: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
[harness-design]: https://www.anthropic.com/engineering/harness-design-long-running-apps
[managed-agents]: https://www.anthropic.com/engineering/managed-agents
[mayfly]: https://blog.exe.dev/mayfly-chat
[opencode-permissions]: https://opencode.ai/docs/permissions/
[opencode-agents]: https://opencode.ai/docs/agents/
[mcp-gateway]: https://tyk.io/learning-center/mcp-gateway-architecture-technical-guide/
[bug-deny]: https://github.com/anomalyco/opencode/issues/6396
[bug-ask]: https://github.com/HammerMei/agentcoop/issues/165
