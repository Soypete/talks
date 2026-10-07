# The Determinism Boundary

> Where probabilistic reasoning should end and infrastructure should begin

Large language models are probabilistic systems. That is not a flaw. It is the
reason they are useful.

They can interpret ambiguous requests, infer intent, navigate incomplete
information, compare possibilities, and reason about language in ways traditional
software systems cannot. That flexibility is exactly what makes them powerful.

The mistake is assuming that because a model can reason about a decision, it
should also be responsible for enforcing that decision.

It should not.

There is a line in every agentic system where probabilistic reasoning needs to
stop and deterministic infrastructure needs to take over. We call that line the
Determinism Boundary. On one side, the model can interpret, infer, suggest, rank,
plan, and propose. On the other, the system must decide what is actually allowed.

## Questions with multiple possible answers

Suppose you ask an agent to resolve a customer issue.

There may be several reasonable ways to accomplish that goal. The agent could
issue a refund, apply a credit, escalate to support, replace an order, or ask for
more information. There may not be one objectively correct answer. The model has
to interpret the situation, reason through the options, and select a likely path
forward.

This is exactly where probabilistic reasoning belongs.

Now change the question. *Can this employee approve a $2,000 refund?*

That should not be a probabilistic judgment. The answer should derive from
identity, role, resource, amount, policy, and perhaps purpose. Given the same
inputs, the system should return the same answer every time.

The model may reason that a $2,000 refund would make the customer happy. It may
even be correct that the refund is the best business outcome. That does not create
authority.

This is the Determinism Boundary in practice.

## Reasoning is not enforcement

We increasingly try to solve operational problems by making models reason harder.
We add chain-of-thought prompting patterns, ReAct loops, planning stages,
reflection, critique, and tool-selection instructions. These techniques can make
models more effective at navigating ambiguity and can improve the quality of a
proposed action.

But reasoning about a constraint is not the same thing as enforcing one.

A model can reason, *"This user probably should not have access to payroll
data."* That is not access control.

A model can reason, *"The refund policy says managers may approve refunds up to
$500."* That is not authorization.

A model can reason, *"Deleting this account seems dangerous, so I should probably
ask for confirmation."* That is not a safety boundary.

Reasoning helps a model choose among possibilities. It should not be responsible
for creating permission.

This is why reasoning prompts are not pragmatics. Pragmatics is not simply telling
the model more about how it should behave. Pragmatics includes the rules governing
how meaning becomes action in a specific situation: who is acting, under whose
authority, against which resource, for what purpose, and within which constraints.

The model can interpret those conditions. Infrastructure has to enforce them.

## Sandboxes solve a different problem

The same boundary appears in agent security.

A sandbox answers a useful question: *where can this process run?* It can restrict
filesystem access, network access, operating-system capabilities, and execution
environment. Those controls matter. They are part of defense in depth.

But they do not answer a different question: *should this action be allowed?*

An agent running safely inside a sandbox may still have credentials to call an
API. It may still be able to send a message, update a customer record, access
sensitive information, or trigger a production workflow. The sandbox can constrain
the environment while the application surrounding it still grants excessive
authority.

That is why sandboxes are not guardrails. Containment controls execution
environment. Guardrails control permissible action.

The distinction becomes especially important for agents because the model can
dynamically discover paths through the tools and systems available to it. A
sandbox may prevent the model from escaping one machine while doing nothing to
determine whether a perfectly valid API call is appropriate for the current user
and task.

## The boundary exists before execution

It is tempting to think of the Determinism Boundary as something that exists only
around tool calls, but it starts earlier and appears in four places.

**It exists when context is assembled.** If a user is not permitted to access
payroll data, we should not retrieve the payroll data and then ask the model not
to disclose it. Access should be decided before the information enters the model's
context.

**It exists when tools are exposed.** If the current workflow cannot delete
accounts, the model should not receive unrestricted access to a generic deletion
tool and then be instructed not to use it. A prompt can ask a model not to perform
a forbidden action. A system can make that action unavailable. Those are not
equivalent guarantees.

**It exists when actions are proposed.** If a refund exceeds a user's authority,
the request should be rejected by policy regardless of how persuasive the model's
reasoning may be. The policy is not additional evidence for the model to weigh
against the customer's circumstances. It is a boundary around the operation.

**And it exists after execution.** The system should be able to record who
requested the action, what identity the agent acted under, which resource was
affected, which policy allowed or denied it, and what actually happened.

Determinism is not merely the final allow or deny. It is the structure surrounding
probabilistic reasoning.

## The model proposes; infrastructure disposes

A useful agent architecture therefore looks less like:

```text
prompt → model → tool
```

and more like:

```text
intent → model reasoning → proposed action
      → deterministic validation → execution
```

The model still matters enormously. It interprets the goal, gathers information,
reasons about possibilities, and proposes the operation most likely to accomplish
the task. But the proposal does not become reality simply because the model
generated it.

The proposed action crosses the Determinism Boundary. At that point, identity,
purpose, resource, parameters, business rules, and policy can be evaluated by
systems designed to produce deterministic decisions.

Note that this does not remove ReAct or any other reasoning loop. It bounds them.
The agent still gets to reason about the work, determine which approved tool is
useful, reconsider the plan when an operation fails, and ask a human for
clarification when information is missing. What it cannot do is turn a plausible
interpretation into a new permission.

## Why this matters more as models get better

There is a strange assumption in AI architecture that better models will
eventually reduce the need for these boundaries.

The opposite is true.

A more capable model can discover more options, use more tools, traverse more
systems, and construct more sophisticated plans. Greater reasoning ability expands
the space of possible actions. That makes explicit boundaries more important.

The evidence is already in. In July 2026, an agent placed in a sandbox and given a
security challenge produced roughly 17,600 reconstructed actions on its way to
compromising production infrastructure. Not one jailbreak — thousands of
individually reasonable steps, each a sensible next move given what the agent
could see. Each newly discovered capability became another possible action.

The failure was allowing the space of technically discoverable actions to get too
close to the space of permissible actions.

The smartest possible model still should not be able to reason its way into
permissions it does not have. It should not matter how convincing the argument is.
If the policy says no, the answer is no.

## The same mistake in four disguises

This is the connection between several problems that otherwise look unrelated.

Reasoning prompts are not pragmatics, because probabilistic reasoning cannot
substitute for deterministic rules of use. Sandboxes are not guardrails, because
execution containment cannot substitute for authorization. Prompt instructions are
not policy, because natural-language guidance cannot guarantee enforcement.
Retrieval is not access control, because finding information does not establish
whether the requester is permitted to use it.

All of these mistakes come from putting responsibility on the wrong side of the
same boundary.

## None of this is new

Software engineering spent decades separating business logic from authorization.
Authentication, API contracts, type systems, schemas, policy engines, RBAC, ABAC,
service boundaries, validation — none of it became obsolete when an LLM entered
the architecture.

Agents make it more important, because the caller is now a model constructing
requests no engineer wrote.

A production harness, before executing any tool, should be able to answer: does
this tool exist in this agent's schema? Do the arguments validate? Which human
initiated this? Which resource does it target? Is that identity, through this
agent, during this task, authorized to perform this operation?

Only then should execution happen. At that point the harness looks much more like
an API gateway than a chat loop.

## The architectural line

The model should be allowed to reason. The surrounding system should decide what
reality permits.

That is the Determinism Boundary.

## References

- Hugging Face — *Anatomy of a Frontier Lab Agent Intrusion: A Technical Timeline of the July 2026 Incident*
- NIST SP 800-162 — *Attribute Considerations for Access Control Systems*
- Wei et al. — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*
- Yao et al. — *ReAct: Synergizing Reasoning and Acting in Language Models*
- Yao et al. — *Tree of Thoughts: Deliberate Problem Solving with Large Language Models*
- *The Context Engineering Manifesto* — Haikai Labs
