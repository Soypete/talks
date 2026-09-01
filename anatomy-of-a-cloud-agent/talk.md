---
marp: true
theme: gaia
paginate: true
title: "Anatomy of a Cloud-Native Agent Harness"
description: "What happens when the harness leaves your laptop?"
---

<!-- _class: lead -->

# Anatomy of a Cloud-Native Agent Harness

## What happens when the harness leaves your laptop?

Miriah Peterson · @Soypete

KubeCon + CloudNativeCon Europe 2027

---

## Who Am I?

- Independent engineer and educator
- Co-host of the **Domesticating AI** podcast
- Building local and cloud-native agent harnesses
- Building AI systems since 2022

---

<!-- _class: lead -->

# We Love Agents

Since Claude Code's release in February 2025, developers have invested heavily in human-enabling agent harnesses.

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
  └── local or self-hosted model server
```

[github.com/IMJONEZZ/lo-agent](https://github.com/IMJONEZZ/lo-agent)

The question is not whether this works locally. It does. The question is what each component becomes in the cloud.

---

# The Next Evolution

One employee can run one harness on one laptop. A cloud-native system must support:

- multiple tasks at the same time
- compute that starts when work arrives
- coordination around shared files and resources
- connections to external systems
- work that continues while the user is away

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

# Agentic Middleware

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

Middleware is the translation layer between probabilistic decisions and the deterministic interfaces of the cloud.

---

<!-- _class: lead -->

# Because the Laptop Is Part of the Agent

```text
User
  ↓
Agent Harness
  ↓
Operating System
  ↓
Filesystem + Processes + Credentials + Network
```

**The machine is doing far more work than we give it credit for.**

---

# Anatomy of a Local Agent Harness

The harness gets:

- an identity
- a filesystem
- environment variables and credentials
- processes and shell access
- network access
- persistent state
- user-installed tools

---

# Lo Agent: A Bare-Metal Harness

Lo Agent is a concrete example of the local model:

```text
User
  ↓
Lo Agent
  ├── prompt and skills
  ├── local files
  ├── processes and shell
  ├── credentials
  └── model provider
```

The harness is powerful because the machine provides the workspace. The challenge is preserving useful capabilities when that workspace becomes a distributed cloud workload.

[Lo Agent](https://github.com/IMJONEZZ/lo-agent)

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

# The Agent Should Be Ephemeral

The **authority** should be durable.

The **state** should be external.

The **credentials** should be renewable.

The **actions** should be auditable.

The **compute** should be disposable.

## Sound familiar?

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

# Anatomy of the Cloud-Native Agent

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

# What's Next?

These are the problems agentic middleware—or Agentware—must solve:

**identity, authorization, context, and policy for autonomous agents.**

If you're building agents that need to operate safely across real enterprise systems:

## I'd love to talk.

---

<!-- _class: lead -->

# Thank You

## Anatomy of a Cloud-Native Agent

**What happens when the harness leaves your laptop?**

Miriah Peterson · @Soypete
