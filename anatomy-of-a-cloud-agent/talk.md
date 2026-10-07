---
marp: true
theme: gaia
paginate: true
title: "Anatomy of a Cloud Agent Harness"
description: "What happens when the harness leaves your laptop?"
---

<!-- _class: lead -->

# Anatomy of a Cloud Agent Harness

## What happens when the harness leaves your laptop?

Miriah Peterson · @Soypete

KubeCon + CloudNativeCon Europe 2027

---

## Who Am I?

- CEO of Haikai Labs
- Co-host of the **Domesticating AI** podcast
- Building local and cloud-native agent harnesses
- Building AI systems since 2022

---

<!-- _class: lead -->

# We Love Agents

As tool-using agents moved from chat into coding, operations, and data workflows, developers built harnesses around them.

They let language models use files, skills, shells, processes, and tools to operate computers on our behalf.

The result is software that can help us write, research, debug, automate, and build.

## What is the next step in their evolution?

---

# The Harness Is More Than the Model

An agent is not just an LLM. The harness is the software around the model that provides:

- tools and function calls
- files and skills
- process execution
- credentials and network access
- memory and task state
- model interaction

The harness turns model output into useful computer action.

---

# A Bare-Metal Agent Harness

```text
User
  ↓
Agent harness
  ↓
Operating system
  ↓
CPU · memory · filesystem · processes · network · credentials
```

The harness is powerful because the machine provides the workspace.

---

# Lo Agent: A Concrete Local Harness

Lo Agent is a useful example because it exposes the local model directly:

```text
Lo Agent
  ├── model client
  ├── tools and function calls
  ├── grammar-based skills
  ├── local state and event log
  ├── process and filesystem access
  └── model server for all model interactions
```

[github.com/IMJONEZZ/lo-agent](https://github.com/IMJONEZZ/lo-agent)

The local checkout used for this talk is version `0.2.23`, commit `b421f60`.
It has not been pulled recently; treat it as a concrete snapshot, not a claim about
the latest upstream release.

---

# The Actual Anatomy of Lo

```text
model client / inference adapters
              ↓
agent loop: decide → call → observe → continue or stop
              ↓
tools · skills · permissions · sandbox
              ↓
memory · compaction · events · replay
              ↓
sessions · coordinator · web UI · MCP/UTCP · telemetry
```

Lo is useful because these responsibilities are visible as separate seams. The
model is not the harness: the harness owns the loop, tool visibility, execution,
context lifecycle, event history, and the durable result.

---

# Anatomy Guidelines

1. Separate **model**, **agent loop**, and **harness** responsibilities.
2. Define a bounded job contract and machine-checkable definition of done.
3. Scope tools by phase; do not expose every capability to every turn.
4. Validate tool calls, authorization, and final results outside the model.
5. Make retries, rescue parsing, backoff, and exhausted-retry states explicit.
6. Treat context, compaction, events, and replay as runtime state.
7. Enforce permissions, secrets, and network policy outside the prompt.
8. Carry workload identity and delegated user identity through every action.
9. Externalize state so compute can be ephemeral and replaceable.
10. Observe the completed job: tools, retries, tokens, latency, verification, and cost.

---

The question is not whether this works locally. It does. The question is what each component becomes in the cloud.

---

# The Next Evolution

One employee can run one harness on one laptop. A cloud-native system must support:

- multiple tasks at the same time
- compute that starts when work arrives
- coordination around shared files and resources
- connections to external systems
- work that continues while the user is away—and longer than any one machine

These are familiar distributed-systems problems—with an autonomous decision-maker inside.

---

# From Laptop to Cloud-Native Harness

```text
Kubernetes control plane
  schedules, scales, and isolates workloads
            ↓
Agent harness pod
  filesystem, tools, task coordinator
            ↓
Ephemeral agent task
  one bounded unit of work
            ↓
Explicit APIs and data sources
  GitHub · Drive · databases · internal services
```

The control plane becomes the foundation. The harness becomes a workload. Agent tasks can start, stop, and run concurrently.

---

# The Data Access Pivot

On a workstation, an agent finds information through:

```text
files + shell + local skills
```

In a cloud-native system, most enterprise data is already exposed through:

```text
APIs + queues + databases + service interfaces
```

The harness must pivot from navigating one machine to coordinating explicit data sources across many services.

---

<!-- _class: lead -->

# Because the Laptop Is Part of the Agent

The harness gets all of this for free:

```text
identity · filesystem · credentials · processes
network · persistent state · installed tools
```

**The machine is doing far more work than we give it credit for.**

---

# The Unix Security Model Is Doing Work for Us

```text
User
 │
 ├── Files
 ├── Processes
 ├── SSH keys
 ├── CLI credentials
 ├── Environment
 └── Applications
```

The agent operates inside that user's world.

---

# Unix Already Knows Who You Are

```bash
$ whoami
miriah
```

Files have an owner, group, and read/write/execute permissions.

Processes execute as identities.

**The agent inherits those constraints.**

---

# The Agent Inherits Delegated Authority

When I ask an agent:

> Push this branch.

It uses authority already available in its execution environment.

When I ask:

> Read this file.

The filesystem decides whether that operation is allowed.

---

<!-- _class: lead -->

# Then We Remove the Workstation

```text
                ???

User → Agent → Container → Kubernetes
```

Where did the user's identity, filesystem, credentials, and authorization boundary go?

---

# Cloud-Native Changed the Security Model

Cloud-native workloads generally don't pretend to be humans.

They have:

- service and workload identities
- RBAC
- secret injection
- explicit APIs
- ephemeral compute

That's a fantastic model for services.

## Agents are weird.

---

# Agents Act on Behalf of Humans

```text
Miriah                         Miriah
  │                              │
  ├── GitHub                      ▼
  ├── Google Drive           Cloud Agent
  ├── Slack                       │
  ├── AWS                         ▼
  └── Internal Systems           ???
```

What exactly is the agent?

**A service? A user? A delegate? All three?**

---

<!-- _class: lead -->

# Problem #1

# Identity

Who is the agent?

And whose authority is it exercising?

---

# Service Identity ≠ User Identity

Kubernetes gives us an excellent primitive:

```text
Pod
 │
 ▼
ServiceAccount
 │
 ▼
RBAC
```

But a ServiceAccount represents a **workload**—not the human who authorized an action.

---

# We Need Two Identities

```text
WORKLOAD IDENTITY
"Which agent is this?"

        +

DELEGATED IDENTITY
"Who authorized this action?"
```

These identities answer different security questions. The workload identity tells the platform which agent is running; the delegated identity tells the agent which human authority applies to this task.

---

# Don't Copy the User's Entire Identity

The obvious architecture recreates the workstation—and its blast radius.

```text
User Credentials
      │
      ▼
    Agent
      │
      ▼
Everything the user can access
```

---

# Delegation Should Be Scoped

```text
User
 │
 ▼
Authorization
 │
 ▼
Scoped Agent Identity
 ├── Repo A: write
 ├── Drive Folder B: read
 └── Production: NONE
```

The agent doesn't need to **be** the user.

It needs authority to perform a specific job.

---

<!-- _class: lead -->

# Problem #2

# OAuth

Humans log in.

Agents don't.

---

# Local OAuth Is Deceptively Easy

A local application can:

1. Open a browser.
2. Ask the user to authenticate.
3. Receive an authorization code.
4. Store and refresh tokens locally.
5. Ask the user again when necessary.

**The workstation gives this workflow a natural home.**

---

# Now Make It Autonomous

```text
Cron / Event / Queue
        │
        ▼
      Agent
        │
        ▼
    Google Drive
```

There may be no human present.

But the agent still needs delegated authority.

---

# So Who Owns the Token?

Options quickly get ugly:

```text
Shared static credential
Personal access token
Long-lived OAuth token
User reauthentication
Service identity
Delegation broker
```

Each has different security properties.

---

# Cloud Applications Solved Part of This

Headless applications already:

- store authorization grants
- refresh credentials
- request reauthentication
- revoke access
- scope permissions

Agents need the same infrastructure—with another complication:

## The model itself is untrusted execution.

---

<!-- _class: lead -->

# Problem #3

# Secrets

---

# The Classic Agent Architecture

```text
.env

GITHUB_TOKEN=...
OPENAI_API_KEY=...
DATABASE_PASSWORD=...
```

Then:

```bash
agent
```

with shell access.

---

<!-- _class: lead -->

# “Don't Read `.env`” Is Not a Security Boundary

A prompt saying:

> Never access secrets.

is not equivalent to:

```text
permission denied
```

**Security boundaries should exist outside model reasoning.**

---

# Local Machines Can Partially Solve This

One pattern I use:

```text
Agent
  │
  ▼
1Password CLI
  │
  ▼
Runtime Secret Injection
```

The model invokes the operation without needing the credential in its context.

---

# Cloud-Native Has Excellent Secret Infrastructure

We already have:

```text
Vault
Cloud secret managers
Workload identity
Sidecars
Secret injection
Short-lived credentials
```

But there's a catch.

---

# Shell Access Changes the Threat Model

```text
Model
 │
 ▼
bash
 │
 ├── env
 ├── cat
 ├── ps
 ├── curl
 └── filesystem
```

If the secret exists somewhere reachable by the process, your beautiful abstraction can disappear.

---

<!-- _class: lead -->

# Problem #4

# Tools

This may be the most important architectural change.

---

# General-Purpose Harness

```text
LLM
 │
 ▼
Shell
 │
 ▼
Anything the OS permits
```

This is extraordinarily powerful.

It is also extraordinarily difficult to constrain.

---

# Cloud-Native Agent

```text
              ┌── GitHub Tool
              │
LLM → Policy ─┼── Drive Tool
              │
              ├── Database Tool
              │
              └── Deployment Tool
```

The model chooses actions.

**Software controls capabilities.**

---

# Tools Become Security Boundaries

Instead of:

```bash
kubectl apply -f whatever.yaml
```

give the agent:

```text
deploy_application(
    application,
    environment,
    version
)
```

The second interface is narrower, deterministic, authorizable, and auditable.

---

# This Changes How We Build Agents

A cloud agent starts looking less like:

> Claude Code running forever

and more like:

> Software containing probabilistic decision-making.

---

# Bespoke Agents Are Boring

## That's good.

Frameworks like PydanticAI, custom orchestration, workflow engines, and typed tool interfaces let us explicitly decide what an agent can do.

**The harness becomes part of the application architecture.**

---

<!-- _class: lead -->

# Problem #5

# Authorization

Authentication answers:

> Who are you?

Agent authorization must answer:

> What may you do, for whom, with what data, right now?

---

# Job-Specific Agents

```text
Marketing Agent       Engineering Agent       Finance Agent
 ├── CMS               ├── GitHub              ├── ERP
 ├── Analytics         ├── CI                  └── Billing
 └── Brand Assets      └── Dev Infrastructure
```

These should not be the same agent with different prompts.

---

# Prompt Boundaries Are Not Permission Boundaries

This:

> You are a marketing agent. Never modify production code.

is weaker than:

```text
GitHub production repository:

DENY
```

**Intent belongs in prompts. Authority belongs in infrastructure.**

---

# Least Privilege Finally Applies to Agents

The question should not be:

> What can Miriah access?

It should be:

> What does this agent need to accomplish this job on Miriah's behalf?

That set should be smaller. **Much smaller.**

---

<!-- _class: lead -->

# Problem #6

# State

---

# The Workstation Gives Agents Persistent State

Almost accidentally:

```text
~/
├── .config
├── .ssh
├── .gitconfig
├── project/
├── credentials
└── history
```

Containers are supposed to disappear.

## So where does the agent live?

---

# But the Work Outlives the Session

The context window fills. The task is not done.

```text
Session 1 ──▶ context full ──▶ ✗
Session 2 ──▶ starts with no memory of session 1
```

Anthropic describes this as engineers working in shifts, each arriving
with no memory of the previous shift.

The laptop has the same problem. It just hides it behind a directory
that happens to still be there.

---

# Two Failures That Look Different

```text
CONTEXT DIES              COMPUTE DIES
the window fills          the pod is evicted
    │                          │
    └──────────┬───────────────┘
               ▼
    the work must continue anyway
```

Long-horizon and ephemeral are the same requirement, seen from two sides.

**Both are solved by the same move: get the state out.**

---

# Separate Compute from State

```text
            ┌── Identity
            ├── Authorization
            ├── Task State
Agent Pod ──┼── Knowledge
            ├── Credentials
            └── Audit History
```

The pod can disappear.

The agent's operational state cannot.

---

# State Is Not One Thing

Each kind has a different lifetime—and a different owner.

| State | Survives | Owned by |
|---|---|---|
| Conversation | context reset | the harness |
| Task progress | pod restart | the coordinator |
| Workspace | or is rebuilt from source | the task |
| Authority | the task itself | a broker the agent can't read |
| Audit | everything | append-only, not the agent |

A single event log is simpler. But authority and audit must **not** be
writable by the thing they constrain.

---

# We Must *Treat* Agents as Ephemeral

Not because pods crash. Because we deploy.

```text
You ship a new harness version.
        │
        ▼
Rolling update drains the pod
        │
        ▼
Your agent is 40 minutes into a task.
```

Kubernetes is not going to ask whether the agent was finished.

---

# The Handoff Has to Be a Real Boundary

```text
Pod A          step completes ──▶ state persisted
                                        │
                        (pod terminates)│
                                        ▼
Pod B          reads state ──▶ continues at the next step
```

This only works if the unit of work is a **step**, not a session—
small enough to finish, durable enough to hand off.

**Persist between steps, not at the end.**

---

# So the Rules Follow

The **authority** should be durable.

The **state** should be external.

The **credentials** should be renewable.

The **actions** should be auditable.

The **compute** should be disposable.

## Sound familiar?

---

<!-- _class: lead -->

# This Is the Trade the Cloud Offers

## Externalize state, and compute becomes disposable.

## Make compute disposable, and the work can run longer than any machine.

The laptop could never offer this. Its state and its compute are the same thing—
close the lid and the shift ends.

---

# Ephemeral *Because* Long-Horizon

Not a compromise. A consequence.

```text
state outside compute
        │
        ├──▶ the pod can die         (ephemeral)
        │
        └──▶ the work resumes        (long-horizon)
```

A month-long task on compute that lives five minutes at a time.

**That is the thing the cloud is actually for.**

---

<!-- _class: lead -->

# This Is Cloud-Native

We already learned this lesson with applications.

```text
Machine = Application
```

became:

```text
Compute + State + Identity + Networking + Configuration + Secrets
```

**Agents are about to undergo the same transition.**

---

# Local Agent → Cloud-Native Agent

| Local assumption | Cloud-native architecture |
|---|---|
| Unix user | Delegated identity |
| Filesystem permissions | Policy + scoped resources |
| `.env` | Secret broker |
| Shell | Typed capabilities |
| Local files | External state |
| User credentials | Scoped authorization |
| Laptop | Ephemeral compute |

---

# Anatomy of the Cloud Agent

```text
                 USER
                  │
                  ▼
          Delegated Authority
                  │
                  ▼
          ┌───────────────┐
          │     AGENT     │
          │   Reasoning   │
          └───────┬───────┘
                  ▼
             Policy Layer
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    GitHub      Drive      Internal
     Tool        Tool        API
       └──────────┼──────────┘
                  ▼
           Scoped Credentials

       External State + Audit
```

---

# The Model Should Be the Least-Trusted Component

Not because models are malicious.

Because probabilistic reasoning should not define deterministic security boundaries.

```text
MODEL    "I want to do X."
POLICY   "Are you allowed?"
TOOL     "Perform exactly X."
AUDIT    "Record what happened."
```

---

# This Is Not an Agent Problem

It is:

**Identity engineering**

**Security engineering**

**Distributed systems**

**Platform engineering**

**Data engineering**

with an LLM in the middle.

---

# Anthropic Got Here Too

Building managed agents at scale, they landed on the same decomposition:

```text
SESSION    durable append-only event log, outside the harness
HARNESS    stateless brain — wake(sessionId), resume from the log
SANDBOX    interchangeable hands — execute(name, input)
```

> "The session is not Claude's context window."

Their section title is **"Don't adopt a pet."**

*Scaling Managed Agents, April 2026*

---

# Where That Account Stops

They solve state and keep credentials out of the sandbox.

```text
SOLVED                        STILL OPEN
ephemeral compute             whose authority is this?
durable session               per-call policy
credentials outside           attribution across delegation
```

A stateless brain still acts on someone's behalf.

**Nothing in `wake(sessionId)` says whose behalf.**

---

# Kubernetes Already Gives Us Many Primitives

- ephemeral workloads
- workload identity
- RBAC and network policy
- secret management
- controllers and reconciliation
- admission policy
- observability

The missing piece is understanding how they map onto **delegated autonomous actors.**

---

# The Open Source Agent Stack

```text
Kubernetes       schedule and isolate agent workloads
OCI containers   package the harness and its dependencies
Envoy            mediate service-to-service traffic
OpenTelemetry    trace decisions, tools, and external calls
MCP              describe tools and context interfaces
```

These projects solve different layers of the problem. The architecture still needs a policy boundary that connects them to a user, a task, and a purpose.

---

<!-- _class: lead -->

# Stop Deploying Laptops to Kubernetes

Putting a general-purpose agent harness in a container is not enough.

We need to redesign the assumptions underneath the harness.

---

# The Cloud-Native Agent

An agent should have:

1. Workload identity
2. Delegated user authority
3. Scoped credentials
4. Explicit capabilities
5. External state
6. Deterministic policy enforcement
7. Auditable actions
8. Ephemeral execution

---

<!-- _class: lead -->

# The Architectural Shift

## Local agents inherit authority.

## Cloud-native agents must be granted authority.

That difference changes almost everything.

---

# We Have Built This Before

Every serious web framework ships the same directory:

```text
middleware/
├── authentication
├── authorization
├── sessions
├── rate limiting
└── logging
```

Nobody puts authentication in the view function.

**We factored it out because every request needs it, and no handler should be
trusted to remember.**

---

# A Tool Call Is a Request

```text
tool call ──▶ [ middleware ] ──▶ execute ──▶ result
                    │
      authenticate · authorize · limit · audit
```

Agent frameworks are rediscovering this: guardrails, per-tool permissions,
MCP gateways. Real policy, outside the prompt.

**But the model is the least trustworthy handler we have ever shipped.**

---

# The Cloud Removes the Backstop

Most agent middleware today assumes a human is nearby.

| | Laptop | Cloud |
|---|---|---|
| Policy says "ask" | user sees the prompt | nobody is there |
| On failure | user notices | proceeds silently |
| Blast radius | one machine | every system reachable |
| Delegation | none | subagents and hops |

**"Ask" is not a policy. It is a human in a loop that the cloud removed.**

Middleware must move outside the harness process—and fail closed.

---

# What's Next?

These are the problems agentic middleware—or Agentware—must solve:

**identity, authorization, context, and policy for autonomous agents.**

---

# Attribution Dies at the First Hop

An agent spawns a subagent. The subagent runs as a service account.

```text
Miriah ──▶ Agent ──▶ Subagent ──▶ delete_table()
                                       │
                                       ▼
                         audit log: "the agent did it"
```

Nobody can answer who authorized it, what it touched, or what it cost.

**Every problem in this talk shows up again at every delegation hop.**

---

# One Interception Point

```text
        tool call
            │
            ▼
    ┌───────────────┐
    │  POLICY       │  allow · deny · filter
    │  fail-closed  │  no caller context ──▶ denied
    └───────┬───────┘
            │
            ▼
        execute
            │
            ▼
      audit record        emitted either way
```

The record shape does not change when you swap frameworks or models.

---

# The Human Survives the Delegation

```python
caller = CallerContext(
    user_id="user-123",
    invoking_subject="user-123",
)

child = caller.delegate(span="subagent-1")

# child.invoking_subject == "user-123"
# child.delegation_depth == 1
```

**Workload identity and delegated identity, carried together, through every hop.**

---

# What Lands in the Audit Row

```text
invoking subject          who authorized this
delegation chain          parent_span, delegation_depth
originating framework     which harness made the call
argument digest           SHA-256, not the arguments
resources touched         what data was involved
policy decision + rule    why it was allowed or denied
tokens, latency           what it cost
```

Append-only. Metrics are rollups over these records—there is no
second instrumentation path.

---

# Agentware

Policy enforcement and audit middleware for agent tool calls.

**Go · Python · TypeScript** · MIT

- fail-closed policy: no caller context is denied, not trusted
- memory writes go through the same chain—not a side channel
- harness contract: govern a harness without adopting a framework
- tenant-side execution; the control plane holds metadata only

[github.com/HaikeiLabs/Agentware](https://github.com/HaikeiLabs/Agentware)

---

<!-- _class: lead -->

If you're building agents that need to operate safely across real enterprise systems:

## I'd love to talk.

---

<!-- _class: lead -->

# Thank You

## Anatomy of a Cloud-Native Agent

**What happens when the harness leaves your laptop?**

Miriah Peterson · @Soypete

---

<!-- _class: lead -->

# Bonus

## What actually wakes the next pod?

---

# The Handoff Needs a Mechanism

Persisting state is only half of it. Something has to *notice*.

```text
step completes ──▶ ??? ──▶ next pod starts
```

Three honest options:

| Mechanism | The next step is... |
|---|---|
| Queue | a message someone consumes |
| Controller | the gap between desired and actual |
| Event log + cursor | the next unread offset |

---

# The Agent Loop Is a Reconciliation Loop

```text
observe state ──▶ decide one action ──▶ converge ──▶ repeat
```

Kubernetes controllers have worked this way the whole time.

The difference is that the decider is probabilistic—which is why the
policy layer sits between the decision and the action.

**We already know how to run this pattern. We have never run it with a model inside.**

---

# But Not Every Log Is the Same Log

```text
WORK LOG          drives progress    agent advances the cursor
AUDIT LOG         records history    agent cannot write it
AUTHORITY         grants access      agent cannot read it
```

One ordered stream can drive the work.

It must not be the same stream that constrains it.

---

<!-- _class: lead -->

# Bonus

## A different kind of ephemeral

---

# Mayfly Chat

Transient chat channels for agents—disposable by design.

```text
New Channel ──▶ URL ──▶ hand it to your agents ──▶ they talk
```

Agents on **different machines, different networks, different clouds**
coordinating mid-task. Agents can even create their own channels.

Named for the insect. The lifespan is the point.

[blog.exe.dev/mayfly-chat](https://blog.exe.dev/mayfly-chat) · Josh Bleecher Snyder

---

# Two Kinds of Ephemeral

```text
THIS TALK                    MAYFLY
ephemeral compute            ephemeral channel
durable state                no state worth keeping
the work must survive        the conversation should not
```

Both are correct. They are answering different questions.

---

# And a Warning in the Footnotes

> "once you have the URL, you have root. Every client is equally
> privileged. Every client can read everything."

Fine for a throwaway channel between agents you already trust.

This is also exactly the model Problem #5 warns about:

**a capability URL is not a delegated identity.**

The fun version and the enterprise version are not the same system.
