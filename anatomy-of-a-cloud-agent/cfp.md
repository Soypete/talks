# Session Title

Anatomy of a Cloud-Native Agent: What Happens When the Harness Leaves Your Laptop?

# Session Description

We love agents. Since February 2025, developers have built harnesses that turn language models into tools for working with files, code, and computers.

These harnesses work because the laptop provides a user, filesystem, processes, credentials, network, and state. But what is the next step in their evolution? What would it take for an agent to escape one user's machine, scale across tasks, and keep working while its user is away?

Cloud-native infrastructure is fundamentally different: a control plane, ephemeral pods, explicit identities, external state, and services connected through APIs. Simply putting a local harness in a container does not bridge that mismatch.

This talk dissects a local harness and maps its components to a CNCF architecture. We confront the shift from filesystem-and-skill-oriented tools to API-based cloud services, then ask what agentic middleware—or Agentware—must provide for elastic, concurrent workloads. Lo Agent is the concrete local example.

## What attendees will learn

- How a local agent harness quietly depends on the operating system for identity, credentials, filesystem permissions, process isolation, networking, and state.
- How to separate workload identity from the human identity that authorizes an action, and when an agent needs to use each one.
- How to design delegated authorization, OAuth and token lifecycles, secret delivery, and external state for ephemeral agent workloads.
- Why cloud agents need API-based data access and agentic middleware instead of direct dependence on local files and skills.
- How to place policy enforcement and audit logging outside the model's context window.

## Who this talk is for

This is a beginner-friendly architecture talk for platform engineers, security engineers, cloud-native application developers, and AI engineers who are building or evaluating agents that operate across real systems. Familiarity with Kubernetes or agent tooling is helpful but not required.

## Key takeaways

Attendees will leave with a practical mental model for designing agents whose compute is ephemeral, authority is scoped, credentials are renewable, state is external, tools are narrow, and actions are attributable to both a workload and a human request.

## Small print

The session is vendor-neutral, does not require access to a commercial product, and is not a product pitch. Examples may reference common cloud-native patterns and open source components.

# Value to the community

AI agents are moving from local developer workstations into shared cloud environments, but many designs still assume that the operating system will provide a human user's identity, permissions, secrets, filesystem, and audit trail. Those assumptions do not transfer automatically to ephemeral workloads.

This talk gives the cloud-native community a concrete vocabulary and architecture for the transition: the control plane, harness workload, ephemeral agent task, workload identity, external state, API-based data access, and agentic middleware. It connects familiar platform primitives—containers, pods, service accounts, queues, and APIs—to the new problem of moving a filesystem-oriented agent into a distributed, cloud-native environment.

The topic is timely because teams are adopting agents faster than they are establishing safe boundaries. The session is useful even for teams that never deploy a general-purpose coding agent: the same design questions apply to support, operations, data, and internal automation agents.

# Case study?

No. This is a vendor-neutral architecture and design-pattern talk, with illustrative examples rather than a single end-user deployment case study.

# Talk presented before?

No. This is a new session for KubeCon + CloudNativeCon Europe 2027. [Confirm before submission.]

# Relevant CNCF / Open Source Projects

Kubernetes (control plane, service accounts, RBAC, scheduling, and ephemeral workloads); OCI containers; OpenTelemetry (agent tracing and audit signals); Envoy (service-to-service policy boundaries); Open Policy Agent (policy concepts and enforcement patterns); OAuth 2.0 and OpenID Connect (delegated identity and authorization flows); Model Context Protocol (tool and context interfaces). No project is presented as a product endorsement.

# Additional resources

- Talk source: `anatomy-of-a-cloud-agent/talk.md` in the speaker's public talks repository. [Add public URL before submission.]
- Speaker profile: https://soypete.tech/ [Confirm current URL.]
- Domesticating AI podcast: [Add public URL before submission.]

# Submission details

## Event and format

- Submitting for: KubeCon + CloudNativeCon Europe 2027
- Poster session: No
- Track: Agentic AI
- Session format: Session Presentation (30 minutes)
- Audience level: Beginner

## Speaker

- Speaker: Miriah Peterson
- Email: captainnobody1@gmail.com
- Speaker title: Independent Engineer and Educator
- Company: SoyPete Tech
- Company website: [Confirm and add URL]
- End-user organization?: No / [Confirm based on CFP definition]
- Country of residence: [Confirm]
- Spoken previously?: [Confirm]
- I am not speaking: No
- Co-speakers: None currently

## Speaker bio

Miriah Peterson is an engineer and educator focused on data engineering, AI infrastructure, and context engineering. She has built production data and AI systems at SchoolAI, Agility Ads, Weave, Tailscale, MX, and Nav. She created SoyPete Tech, teaches for Boot.dev and O'Reilly, hosts Domesticating AI, and organizes GoWest, Utah Data Engineering, and Machine Learning Utah. Her work helps teams build reliable AI systems.

## Optional diversity questions

- Person of color: [Optional — speaker to complete]
- Gender identity: [Optional — speaker to complete]
- Identify with other underrepresented group(s): [Optional — speaker to complete]

## Required acknowledgements

- Content Quality Agreement: Agree
- Code of Conduct: Agree
- Commitment to Inclusivity: Agree
- Speaker Gender Representation: Not applicable to one speaker; agree
- Speaker submission limit acknowledgement: Agree, provided this remains within the three-submission limit
- Consent to share session and personal data with the organizer: Agree
