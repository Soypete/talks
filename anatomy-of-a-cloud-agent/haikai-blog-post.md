# When the Agent Leaves the Laptop, Context Becomes Infrastructure

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

That is the architectural shift behind governed, cloud-native agents.

## The cloud-native agent has two identities

A service account can tell us which workload is making a request. It cannot, by itself, tell us which person authorized the request or what that person is allowed to see.

Reliable agent systems therefore need to carry two identities through the execution path:

1. **Workload identity:** which agent, deployment, or job is running?
2. **Delegated identity:** which human or principal authorized this action?

This distinction is the foundation for least privilege and useful audit logs. “The agent accessed the customer record” is incomplete. A meaningful record also needs the invoking user, the purpose, the policy decision, and the exact data or operation involved.

## Context is not a prompt

Teams often try to govern agents with instructions in Markdown or system prompts: do not access secrets, do not modify production, only use approved data.

Those instructions may be helpful, but they are not enforcement boundaries. The model reads instructions alongside untrusted content. A repository, document, tool description, or API response can contain text that attempts to redirect the agent.

The security boundary must exist outside the model's reasoning. A denied filesystem operation, an unavailable connector, a policy engine, or a tool that refuses an unauthorized request is stronger than a sentence asking the model to behave.

This is why we describe the governance layer as a **Sovereign Context Layer**. It is the place where an organization defines which context an agent may receive, which actions it may take, and which user permissions it must respect. Context is not only information supplied to a model; it is the controlled environment in which intelligent action becomes possible.

## Three boundaries every agent needs

### 1. Data sovereignty

Organizations need to control where proprietary context resides and where it can flow. A zero-egress-by-default design keeps sensitive data within the organization's infrastructure unless an explicitly governed path allows otherwise.

This reduces the risk of turning corporate memory into an uncontrolled input to third-party systems. It also gives security and compliance teams a concrete boundary to inspect.

### 2. Dynamic authorization

Agents should not receive a permanent superuser credential simply because they are convenient to deploy. They should receive the narrow authority required for the job, evaluated in the context of the invoking user, resource, purpose, and current policy.

If a user cannot see a file, the agent acting for that user should not be able to see it either. If a support agent needs customer records but not payroll data, those scopes should be enforced by the data and tool layers—not merely described in its prompt.

### 3. Purpose-driven auditability

An audit trail should make agent activity understandable after the fact: who invoked the agent, which agent version ran, what tools were called, what context was accessed, what policy decision was made, and whether the operation succeeded.

Without this information, an organization cannot reliably investigate incidents or demonstrate that an automated action was authorized.

## Why tools are part of the policy surface

Tool descriptions are loaded into the model's context, which makes connector management a security-sensitive capability. Arbitrary users should not be able to add connectors or expand the agent's action surface without review.

The same principle applies to tool design. A narrow operation such as `deploy_application(application, environment, version)` is easier to authorize and audit than unrestricted shell access with `kubectl`, `curl`, and access to every environment.

General-purpose harnesses are powerful because they inherit the operating system's capabilities. Cloud-native agents become trustworthy when their capabilities are explicit, purpose-built, and enforced by software.

## The Haikai approach

Haikai Labs is building middleware for this transition. Kei places a governed execution layer between an agent and the systems it can affect. The goal is to help organizations deploy specialized agents for support, RevOps, development, and other workflows while retaining control of context, authorization, and auditability.

The platform vision has two complementary parts:

- **Kei Chat Harness:** a workspace for invoking agents from collaboration tools such as Slack, Teams, or Discord.
- **Sovereign Context Layer:** the policy and context infrastructure where organizations connect data sources, define permissions, constrain agent capabilities, and record actions.

The product is a practical expression of a broader idea: sovereignty is not opposed to intelligence. It is what makes intelligent action safe to use in environments where data, identity, and accountability matter.

## From model capability to governed velocity

The enterprise question is no longer simply, “Which model is smartest?” It is also:

> Can this agent act quickly without becoming an unaccountable pathway into the business?

The answer depends on architecture. Compute should be replaceable. Credentials should be short-lived and scoped. Connectors should be controlled. Policies should be enforced outside the model. Context should remain under the organization's control. Actions should be attributable to a human request and a specific workload.

That is how agents move from impressive demonstrations to dependable infrastructure.

Haikai Labs exists to make that governed path easier to build.
