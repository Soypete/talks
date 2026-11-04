# Plan: progress-aware workflow support in Agentware

## Goal

Help a harness determine whether a workflow is advancing, recover from an out-of-order action, and request an explicit finish when the work is verified. The harness continues to own the agent loop. Agentware supplies reusable response-quality components; these components do not authorize tool calls or replace the policy boundary.

The [connector experiment](head-to-head.png) is an early motivating example, not proof that the design generalizes. The current [prototype](enhanced.py) hard-codes one task and is not an SDK API.

## What Forge already does

[Forge's user guide](https://github.com/antoinezambelli/forge/blob/main/docs/USER_GUIDE.md) documents validation and rescue, retry nudges, required steps, tool prerequisites, error recovery, and context compaction in `WorkflowRunner`. Middleware callers wire some components themselves; its proxy does not have workflow-level prerequisite enforcement or compaction. Its prerequisite handling documents a limit on consecutive violations. This is substantial prior work: compare behavior and credit Forge before designing another version.

The guide does not establish that Forge implements the exact task-specific, observed-outcome checklist and finish-line handling used in our prototype. Inspect Forge source and tests at a pinned commit before claiming feature equivalence, copying behavior, or choosing an API. Agentware's [third-party notice](https://github.com/HaikeiLabs/Agentware/blob/main/python/THIRD_PARTY_NOTICES.md) attributes its guardrails facade design to Forge; the Python package does not declare Forge as a runtime dependency.

## Design boundaries

- Keep response quality, workflow progress, and authorization separate. A progress decision never grants tool access or bypasses a fail-closed policy decision.
- Build progress from validated, successful tool outcomes and explicit application-defined checks, not the model's assertion that a step worked. A successful API response alone need not mean the desired postcondition holds.
- Expose generic workflow definitions and events. Resource identities, task criteria, and domain-specific checks remain supplied by the application. Do not bake CRM, users, provider payloads, or benchmark scoring into Agentware.
- Permit independent steps in any order. Enforce only actual dependencies; a declared prerequisite is not an implicit total ordering. Match resources when required.
- Keep mutable workflow state scoped to a run. Define serialization and versioning before resuming, and reject malformed state. Record observations after execution and validate them before marking progress.
- Prompt the model to finish only after configured completion predicates are satisfied; the harness must not fabricate a successful `done` call or silently perform the action. Distinguish correct state, verified state, and accepted completion.
- Traces are opt-in and bounded. Default telemetry records safe metadata and digests, not raw tool arguments, results, credentials, or hidden reasoning. Raw synthetic traces in this talk repository are for the local demo only.

## Work packages

### 1. Specify and compare behavior

Pin Forge and Agentware revisions. Build a behavior matrix using their source and tests: retry reset, prerequisites, tool-error routing, rescue, state persistence, and compaction. Identify what Agentware already has and the exact gap. Resolve whether the SDK should expose a standalone `ProgressTracker`-style component or extend its existing facade; names here are proposals, not existing APIs.

Deliverable: a short ADR and versioned shared fixtures defining successful actions, progress observations, dependencies, verification invalidation, retry exhaustion, and finalization. Record whether fixtures are shared with or derived from Forge and preserve attribution and licensing.

### 2. Define a generic progress contract

Model a run as explicit, application-provided requirements and evidence: identifiers for steps and resources, dependencies, accepted observations, invalidation rules, and completion predicates. Require a caller-supplied predicate or trusted observation for domain correctness. Define typed results for progress, missing work, recoverable rejection, terminal failure, and finish readiness. Keep model-facing nudges separate from state and bounded in size. Avoid storing raw payloads in durable state by default.

Acceptance: independent steps may complete in either order; duplicate events are idempotent where possible; state changes invalidate only affected evidence; failed or merely attempted actions do not satisfy requirements; unrelated tasks cannot share progress.

### 3. Improve recovery and compaction

Separate consecutive no-progress attempts from the overall turn, time, and cost budgets. A verified state transition can reset a consecutive no-progress counter; never allow an unlimited loop. Return actionable, bounded reasons for blocked prerequisites, failed executions, and stale checks. When the workflow is ready but the model stops without its terminal call, issue a bounded finish nudge.

Integrate with each existing context strategy rather than discarding conversation history blindly. Preserve the system instruction, task, recent relevant observations, and complete tool-call/result pairs. Define what happens when the protected content alone exceeds the budget; never claim compaction guarantees a hard limit unless it does.

### 4. Implement ports in stages

1. **Go reference:** design the public contract and deterministic engine with shared fixtures.
2. **Python and TypeScript:** implement the same semantics and replay the same fixtures; expose language-idiomatic APIs without claiming signatures in advance.
3. **Rust:** first scope its smaller existing SDK surface and decide whether a guardrails/context module belongs there. If accepted, implement the contract and fixture replay; do not assume feature parity exists today.
4. Wire optional integrations in the inference/harness layer. Middleware does not own the agent loop, and existing integrations retain their current behavior by default.

### 5. Validate before publishing

- Unit and shared-contract tests: independent order, duplicate observations, failed actions, retry reset on real progress, stale verification, terminal handling, state isolation, serialization, budgets, and model responses that omit or malform tool calls.
- Context tests: paired tool messages remain valid, critical observations survive, compaction is repeatable, and an over-budget protected context is surfaced explicitly.
- Security tests: progress and completion cannot override authorization; deny, unknown caller, policy failure, and downstream error remain distinct; logs and persisted state redact sensitive values.
- Benchmark ablations: bare, existing guardrails, flexible prerequisites, progress-aware retry, checklist, finish nudge, and combined mode. Run the same task definitions and seeds across variants; report full completion and partial-state metrics, sample sizes, failures, model configuration, and latency separately. Include multiple tasks and models, not just the connector scenario.
- Run the repository's Go, Python, TypeScript, and, if implemented, Rust checks. Verify downstream failure behavior against each port's source and tests.

## Rollout and decisions

Ship behind an explicit opt-in, document migration and limitations, then stabilize only after shared fixtures and multi-task ablations pass. Decide the owner and lifecycle of persisted workflow state, how applications supply trustworthy evidence, and what can safely be summarized across restarts before enabling durable workflows. No production authorization behavior should change as a side effect of enabling progress guidance.
