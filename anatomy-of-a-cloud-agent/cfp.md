# Session Title

Anatomy of a Cloud-Native Agent: What Happens When the Harness Leaves Your Laptop?

# Session Description

AI agent harnesses were designed around workstations, where the operating system supplies identity, filesystem permissions, credentials, shell access, networking, and state. Move the harness into the cloud and those assumptions break.

This talk maps a local agent's implicit capabilities to a cloud-native architecture. We examine workload identity versus delegated user authority, OAuth and token lifecycles, secrets, shell access, typed tools, external state, policy enforcement, and auditability. We ask why a job-specific agent with narrow capabilities is a stronger foundation than unrestricted user impersonation.

The goal is not to put Claude Code in a container. It is to understand the architecture for software that acts like a user—and how to make that action scoped, explicit, and auditable.

## What attendees will learn

- How a local agent harness quietly depends on the operating system for identity, credentials, filesystem permissions, process isolation, networking, and state.
- How to separate workload identity from the human identity that authorizes an action.
- How to design delegated authorization, OAuth and token lifecycles, secret delivery, and external state for ephemeral agent workloads.
- Why typed, purpose-built tools are safer and more auditable than unrestricted shell access.
- How to place policy enforcement and audit logging outside the model's context window.

## Who this talk is for

This is a beginner-friendly architecture talk for platform engineers, security engineers, cloud-native application developers, and AI engineers who are building or evaluating agents that operate across real systems. Familiarity with Kubernetes or agent tooling is helpful but not required.

## Key takeaways

Attendees will leave with a practical mental model for designing agents whose compute is ephemeral, authority is scoped, credentials are renewable, state is external, tools are narrow, and actions are attributable to both a workload and a human request.

## Small print

The session is vendor-neutral, does not require access to a commercial product, and is not a product pitch. Examples may reference common cloud-native patterns and open source components.

# Value to the community

AI agents are moving from local developer workstations into shared cloud environments, but many designs still assume that the operating system will provide a human user's identity, permissions, secrets, filesystem, and audit trail. Those assumptions do not transfer automatically to ephemeral workloads.

This talk gives the cloud-native community a concrete vocabulary and architecture for the transition: workload identity plus delegated authority, short-lived credentials, explicit tools, external state, policy enforcement outside the model, and end-to-end auditability. It connects familiar platform primitives—service accounts, RBAC, secret managers, queues, and APIs—to the new problem of software acting on behalf of a person.

The topic is timely because teams are adopting agents faster than they are establishing safe boundaries. The session is useful even for teams that never deploy a general-purpose coding agent: the same design questions apply to support, operations, data, and internal automation agents.

# Case study?

No. This is a vendor-neutral architecture and design-pattern talk, with illustrative examples rather than a single end-user deployment case study.

# Talk presented before?

No. This is a new session for KubeCon + CloudNativeCon Europe 2027. [Confirm before submission.]

# Relevant CNCF / Open Source Projects

Kubernetes (workload identity, service accounts, RBAC, and ephemeral workloads); Open Policy Agent (policy concepts and enforcement patterns); OAuth 2.0 and OpenID Connect (delegated identity and authorization flows). No CNCF project is presented as a product endorsement.

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
- Speaker title: CEO and Founder
- Company: Haikai Labs
- Company website: [Confirm and add URL]
- End-user organization?: No / [Confirm based on CFP definition]
- Country of residence: [Confirm]
- Spoken previously?: [Confirm]
- I am not speaking: No
- Co-speakers: None currently

## Speaker bio

Miriah Peterson is the CEO and founder of Haikai Labs, where she builds data governance, context engineering, and secure AI infrastructure for reliable agentic systems. She has built production data platforms and AI systems at SchoolAI, Agility Ads, Weave, Tailscale, MX, and Nav. Miriah is the creator of SoyPete Tech, a Boot.dev and O'Reilly instructor, co-host of Domesticating AI, and organizer of GoWest Conference and Utah technology meetups.

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

# Positioning notes for Haikai Labs

Haikai Labs should be named as the speaker's current company by the time of the conference. The talk itself should remain vendor-neutral and should not present Kei, the Haikai middleware, or the Sovereign Context Layer as required solutions. If a brief company disclosure is useful, use: “I’m the CEO and founder of Haikai Labs, a company working on governed context infrastructure for reliable AI systems.”
