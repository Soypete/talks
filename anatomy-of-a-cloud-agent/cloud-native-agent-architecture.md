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
9. **Externalize state; make compute replaceable.** A task should survive a pod restart.
10. **Observe the completed job.** Measure phases, rounds, tools, retries, tokens,
    latency, exit reason, verification, and cost—not just streamed text.

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

## The cloud-native agent has two identities

A service account can tell us which workload is making a request. It cannot, by itself, tell us which person authorized the request or what that person is allowed to see.

Reliable agent systems therefore need to carry two identities through the execution path:

1. **Workload identity:** which agent, deployment, or job is running?
2. **Delegated identity:** which human or principal authorized this action?

This distinction is the foundation for least privilege and useful audit logs. “The agent accessed the customer record” is incomplete. A meaningful record also needs the invoking user, the purpose, the policy decision, and the exact data or operation involved.

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

The open source [Lo Agent](https://github.com/IMJONEZZ/lo-agent) repository provides a concrete starting point for examining the bare-metal harness model and asking what must change when its workspace becomes a cloud-native workload. Use the locally pinned checkout as a snapshot for discussion, not as a substitute for checking the current upstream implementation.

## From model capability to governed velocity

The architecture question is no longer simply, “Which model is smartest?” It is also:

> Can this agent act quickly without becoming an unaccountable pathway into the business?

The answer depends on architecture. Compute should be replaceable. Credentials should be short-lived and scoped. Connectors should be controlled. Policies should be enforced outside the model. Context should remain under the organization's control. Actions should be attributable to a human request and a specific workload.

That is how agents move from impressive demonstrations to dependable infrastructure.

The goal is to make the path from a local, filesystem-oriented harness to a scalable, API-oriented cloud agent understandable and buildable. Agentware is the next step: the middleware and runtime that turns the local harness pattern into elastic, concurrent cloud workloads.
