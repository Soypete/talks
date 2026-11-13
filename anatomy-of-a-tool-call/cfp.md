# Anatomy of a Tool Call — CFP draft

**Status:** Draft, not submitted  
**Best target:** AGNTCon + MCPCon North America 2027  
**Submission:** https://sessionize.com/agntcon-mcpcon-north-america-2027/  
**Audience:** Agent harness developers, AI infrastructure and platform engineers  
**Source writing:** *Anatomy of a Tool Call* (SoyPete Tech work in progress, November 2026); *Anatomy of an Agent Harness* (Haikei Labs, November 3, 2026). Verify article permalinks before sending.

## Title

Anatomy of a Tool Call: Who Decides What the Model Can Execute?

## Abstract

A model does not execute a tool call. An agent harness advertises tools, carries the conversation through the agent loop, interprets model output, and decides what code runs. That distinction is easy to lose when a tool call appears as a neat JSON object in a trace.

We will follow a single tool call from registration to inference, proposal, argument validation, identity-aware authorization, execution, result handling, and the next turn of the loop. Along the way, we will account for an often-overlooked cost: the schemas and descriptions of available tools repeatedly consume context, while their results become part of subsequent context history. More MCP servers do not automatically mean a better or safer agent.

This is a practical architecture session about where model reasoning ends and deterministic infrastructure begins. We will show which decisions belong to the model, which belong to the harness, and where delegated identity, policy, observability, and tests attach.

## Takeaways

- Trace the lifecycle of one tool call in an agent loop.
- Explain how registered tools and returned results affect effective context.
- Separate a model's proposed operation from the harness's authority to perform it.
- Place argument validation, identity, per-tool policy and audit in the execution path.
- Evaluate actual tool behavior rather than only textual answers.

## Session outline

1. Agent loop and tool registration
2. Model-facing description versus executable implementation
3. Context overhead and tool-result persistence
4. Authorization before action; sandbox versus guardrail
5. Tracing, evals, and repeatable failure demonstrations

**Reuse note:** New material relative to the 2026 self-hosting agents presentation; do not reuse its title and abstract verbatim.
