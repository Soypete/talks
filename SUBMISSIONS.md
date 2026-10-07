# Submission map — autumn 2026

Which talk goes to which event, and why. Update as CFPs close and results land.

## Submit this week

| Event | Date | CFP closes | Talk | Status |
|---|---|---|---|---|
| Agent Substrate Day, SLC | Nov 9 | **Sep 30** | `sandboxes-are-not-guardrails` | ready |
| AI Native DevCon, Brooklyn | Nov 3–4 | **Oct 1** | `agentcon-scoped-knowledge` | ready |
| AgenticCon, SF | — | confirm | `herdr-wiki-shared-memory` | ready |
| AI Software Factory Summit | — | confirm | `reviewing-agent-actions` | ready |

## Submit next

| Event | Talk | Notes |
|---|---|---|
| DPE Summit 2027 | `data-as-ai-guardrail` | ontologies + data engineering |
| AI & Platform Security Global Summit | `determinism-boundary` | security framing already fits |

## Why these pairings

**Agent Substrate Day → Sandboxes Are Not Guardrails.** Single-track Kubernetes
infrastructure audience, reviewed by maintainers. Their CFP asks for security and
reliability patterns and "honest accounts of what you got wrong." The talk is built
on the July 2026 incident with a published timeline, so every claim is checkable.
`anatomy-of-a-cloud-agent` is the other candidate here but needs cutting from 88
slides and a beginner framing.

**AI Native DevCon → Stop Giving Agents Permissions.** Their CFP explicitly wants
"what you tried, what worked, what failed." This talk has four working
implementations plus reliability tradeoffs, eval consistency results, and
patterns-to-avoid. Primary track Context Engineering, secondary Agent Enablement
Platform. The newer `determinism-boundary` is the backup if they want something more
architectural.

**AgenticCon → Shared Memory for Agents.** Real running system, evidence drawn from
its own history, and the agent-civilizations opening. `agentcon-scoped-knowledge`
also fits here if the wiki talk goes elsewhere.

**AI Software Factory → You Cannot Review Every Agent Action.** Factories are where
per-action review breaks. Nothing else in the repo covers audit, attribution, and
delegation at volume.

**DPE Summit → Data as an AI Guardrail.** A data engineering talk that happens to be
about agents. The right audience for ontologies-as-inference-models.

## Existing talks not currently placed

| Talk | Fit |
|---|---|
| `anatomy-of-a-cloud-agent` | KubeCon EU 2027 (its original target) |
| `agentcon-memory-talk` / `beyond-ai-memory` | MLOps World; near-duplicates, pick one |
| `agentcon-self-hosting` | AgentCon / MCP Con, Oct 23 — already scheduled |
| `determinism-boundary` | security-focused events; backup for DevCon |

## Before submitting anywhere

- Confirm close dates for AgenticCon and AI Software Factory Summit.
- Substrate Day (Nov 9, SLC) and DevCon (Nov 3–4, Brooklyn) are four days apart in
  different cities — confirm travel before submitting to both.
- DevCon's travel-support request deadline is also Oct 1.
- `beyond-ai-memory` and `agentcon-memory-talk` overlap heavily; do not submit both
  to the same event.
