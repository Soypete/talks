# Enterprise agent authority — CFP and organizer pitch draft

**Status:** Draft, not submitted  
**Best targets:** Utah Cyber Alliance, Credo AI Virtual Trust Summit, AI Summit North America  
**Audience:** CIOs, CISOs, CTOs, enterprise architects, data governance and risk leaders  
**Related talk:** [You Cannot Review Every Agent Action](../reviewing-agent-actions/cfp.md) (accepted, AI Software Factory Summit 2027)  
**Related essay:** *You Cannot Review Every Agent Action* (Haikei Labs, October 26, 2026). Verify original Substack permalink before external submission.

## Title

Who Is Your AI Agent Acting For? Giving Agents Autonomy Without Unlimited Authority

## Abstract

Enterprises want agents that do useful work across internal systems, not another assistant that can only summarize a document. But the first question is not which model to choose. It is: who is the agent acting on behalf of?

That question changes the architecture. The agent might read customer records under an employee's identity, prepare a financial adjustment, create a ticket, or propose a production change. Each action has a different authority requirement. Some are routine, some need an explicit approval, and some must be impossible regardless of how convincingly the model asks.

We will walk through a realistic cross-system workflow and show how to define delegated identity, permission boundaries, approval points, and auditable action records. The lesson is that reviewing every agent decision does not scale. Organizations need to move governance into enforceable infrastructure: the model proposes a step, but the system determines whether the step is permitted.

## Audience takeaways

- Ask whose authority each agent action uses.
- Distinguish read access, execution rights, approval requirements, and prohibited actions.
- Establish policy at the tool/action boundary rather than treating prompts as controls.
- Build useful autonomy with attributable, auditable, and testable decisions.

## Enterprise adaptation

Avoid code-first or framework-specific implementation. Lead with operational accountability, risk ownership, and a diagram of one business workflow. Reserve harness implementation detail for technical Q&A.

## Short organizer pitch

I can offer a practitioner-led session on how enterprises give AI agents useful autonomy without giving them unlimited authority. It uses a concrete workflow to answer who an agent acts for, what data and tools it can access, which actions require approval, and which must be denied by policy. The session is vendor-neutral and adapts to either an executive governance audience or an enterprise architecture audience.
