# You Cannot Review Every Agent Action

> Attribution, delegation, and audit when agents outpace human review

In July 2026, a single agent working on a single evaluation task produced roughly
17,600 reconstructed actions.

Imagine that review queue. Now imagine a software factory running a hundred agents
continuously.

The software factory premise — more agents, more autonomy, more throughput — has a
review problem built into it, and the problem is structural rather than cultural.
Human review does not scale with the thing it is reviewing. With one agent you read
the diff. With ten you skim. With a hundred you approve. With a thousand you hope.

There are two common responses and both are bad.

Review everything, and the factory stops. You have built expensive autocomplete
with a human bottleneck attached, and you are paying for autonomy you refuse to
use.

Review nothing, and the factory runs, but nobody can say what it did. "The AI
decided" becomes an extremely convenient place for responsibility to disappear.

Neither is an architecture.

## Review is the wrong unit

The useful move is to stop asking "did a human see this action?" and start asking
three different questions, none of which requires a person at execution time.

1. Could this action have happened at all?
2. On whose authority did it happen?
3. Can we reconstruct it afterward?

The first is policy. The second is delegated identity. The third is audit.

## Could it have happened at all?

There is a difference between reviewing instances and constraining the set.

Reviewing instances means looking at every action, one at a time. It scales with
volume, which means it does not scale. Constraining the set means deciding in
advance which actions can exist. It scales with design, and costs nothing per
invocation.

You do not review each SQL query your web application issues. You constrained which
queries it can issue, once, when you wrote the data access layer.

This is exactly where a general-purpose shell breaks the model. A shell is not one
tool; it is an interface for constructing unlimited tools. You cannot write policy
about a set you cannot enumerate, and you cannot review a set you cannot enumerate
either. Typed tools are what make the set finite.

```text
kubectl apply -f whatever.yaml

deploy_application(app, environment, version)
```

The second interface you can reason about once, at design time, and then stop
reasoning about per invocation. Review the contract, not every call under it.

## On whose authority?

Attribution dies at the first delegation hop.

An agent spawns a subagent. The subagent runs as a service account. Every log
downstream says "the agent did it." Nobody can answer who authorized the action,
what data it touched, or what it cost.

That is not merely an observability gap. It is the mechanism by which
accountability evaporates from an autonomous system.

Fixing it requires carrying two identities rather than one. Workload identity tells
the platform which agent, deployment, or job is running. Delegated identity tells
the system which human or principal authorized the action. A service account can
only answer the first.

Both have to survive every hop:

```python
caller = CallerContext(
    user_id="user-123",
    invoking_subject="user-123",
)

child = caller.delegate(span="subagent-1")

# child.invoking_subject == "user-123"
# child.delegation_depth == 1
```

The subagent gets its own span and its own delegation depth. The human rides along
unchanged.

Scope should follow that human. If a junior analyst invokes a finance agent, the
agent should operate inside the analyst's authorization boundary — not inherit the
warehouse access its service account happens to hold. A delegated subtask should
carry a deliberately scoped version of the context required to complete it, not the
full surface available elsewhere in the organization.

## Can we reconstruct it?

The third question is answered by one append-only record per action, emitted
whether or not the call proceeded:

```text
invoking subject          who authorized this
delegation chain          parent span, delegation depth
originating framework     which harness made the call
argument digest           SHA-256, not the arguments
resources touched         what data was involved
policy decision + rule    why it was allowed or denied
tokens, latency           what it cost
```

Two details matter more than they look.

**Digest, not arguments.** Tool arguments routinely contain customer data, secrets,
PII, and proprietary content. An audit trail that copies all of that into a
long-lived log is a liability, not a control. A hash proves what was called without
retaining what was in it.

**One instrumentation path.** Metrics should be rollups over the audit records
rather than a second pipeline. If your dashboard and your audit log disagree, you
have two systems and zero answers.

## What humans should review instead

Human attention does not disappear. It moves to both ends.

Upstream, people review the tool contract, the policy, and the delegation model.
These are reviewed once and apply to everything afterward. This is where careful,
slow, expensive human judgment pays for itself, because a single decision governs
millions of invocations.

Downstream, people review denials, exceptions, anomalies in the audit stream, and
the first instance of any new pattern. These are reviewed by volume rather than by
default, and they are self-prioritizing: a denial is rare and informative by
construction.

The middle — routine, authorized, policy-compliant execution — is the part that
should not need a person. That is the whole point of building the factory.

A denial queue is a far better review artifact than an approval queue. "Policy
denied 47 actions this week, here is which rule, which agent, which human, and
which resource" is a document someone can actually read. Seventeen thousand
approvals is not.

## What this does not solve

Being honest about the limits matters, because the failure mode of governance
architecture is believing it covers more than it does.

A correctly authorized action can still be wrong. Policy said yes and the outcome
was bad anyway. No amount of attribution prevents that.

A policy that encodes a bad rule is enforced faithfully. Determinism is neutral
about whether the rule is correct; it only guarantees the rule is applied.

Drift between stated and actual authority is invisible to audit. If someone widened
a scope and nobody noticed, every subsequent action is legitimately authorized and
legitimately wrong.

Audit tells you what happened. It does not tell you it should have.

## What it does buy

The factory can run, and you can still answer the question afterward: who
authorized this, what did it touch, what did it cost, and which rule permitted it.

That is the difference between autonomy and abdication.

You cannot review every action. Constrain the set, carry the identity, record the
decision — then review the contract, the exceptions, and the anomalies rather than
the queue.

## References

- Hugging Face — *Anatomy of a Frontier Lab Agent Intrusion: A Technical Timeline of the July 2026 Incident*
- NIST SP 800-162 — *Attribute Considerations for Access Control Systems*
- [Agentware](https://github.com/HaikeiLabs/Agentware) — policy enforcement and audit middleware
- *The Context Engineering Manifesto* — Haikai Labs
