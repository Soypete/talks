# Session Title

Anatomy of a Cloud-Native Agent: What Happens When the Harness Leaves Your Laptop?

# Description

The most capable AI agent harnesses today were designed around a workstation. Tools like Claude Code, Cursor, OpenCode, and Hermes inherit a user, filesystem, credentials, shell, local state, and permission model from the machine beneath them. The laptop is not merely where the agent runs; it is part of the agent's architecture.

Move that agent into the cloud, and those assumptions begin to break. Cloud-native systems use ephemeral workloads, service identities, scoped authorization, secret injection, and explicit interfaces. An autonomous agent, however, may need to act on behalf of a human across GitHub, Google Drive, internal APIs, databases, and production infrastructure—without inheriting everything that human can access.

This talk dissects a local agent harness and maps each of its implicit capabilities to a cloud-native architecture. We will examine workload identity versus delegated user authority, OAuth and token lifecycles, secrets, shell access, deterministic tools, external state, policy enforcement, and auditability. We will also explore why job-specific agents with narrow capabilities offer a stronger foundation than unrestricted user impersonation.

The goal is not to put Claude Code in a container. It is to answer a more fundamental question: What is the cloud-native architecture for software that acts like a user?

Attendees will leave with a practical mental model for designing agents whose compute is ephemeral, authority is scoped, credentials are renewable, state is external, and actions are auditable.

**Local agents inherit authority. Cloud-native agents must be granted authority.**

# Small print

This is a vendor-neutral architecture talk for platform engineers, security engineers, cloud-native application developers, and AI engineers building agents that operate across real systems. Familiarity with Kubernetes or agent tooling is helpful but not required. The session does not require access to any commercial product and is not a product pitch.
