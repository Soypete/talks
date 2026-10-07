# Sandboxes Are Not Guardrails

> Why containment infrastructure is not authorization for autonomous agents

In July 2026, an agent running an OpenAI cyber-capability evaluation was placed inside a
cybersecurity challenge. By most conventional definitions of agent security, this
is exactly what we have been told to do. The model had network restrictions. It
had process isolation. It was contained inside an environment specifically
designed to prevent it from affecting the systems around it.

Then it escaped.

The agent exploited a zero-day in a package registry cache proxy, reached an
external code-execution environment, gained root access there, and used that
environment as a launchpad against Hugging Face. Once inside Hugging Face's
infrastructure, it continued probing until it reached production systems and
eventually found datasets associated with the evaluation it was supposed to
complete.

Hugging Face reconstructed roughly 17,600 actions from the intrusion. That number
is important because this was not one clever jailbreak where the model suddenly
became malicious. It was thousands of individually reasonable actions strung
together toward a goal. The agent inspected its environment, found another
environment, enumerated what was available there, discovered additional resources,
and kept moving toward something it believed would help it solve the problem.

There are plenty of traditional security failures inside that story. There were
exploitable services, credentials, Kubernetes permissions, and infrastructure
assumptions that should be examined independently. But focusing exclusively on
those failures misses the part that matters for anyone building agents.

The sandbox constrained where the agent started. It did not constrain which
actions the surrounding systems would allow it to take.

That distinction matters because we have spent a lot of time treating sandboxing
as though it is synonymous with guardrails. It is not. A sandbox gives us
containment. A guardrail determines whether an action should be allowed to happen
at all.

Agents need both.

## A sandbox solves a very specific problem

Sandboxes are useful because software does things we did not expect.

If I allow an agent to execute arbitrary code, I absolutely want that code running
inside an isolated environment. I want restricted networking. I want minimal
credentials. I want filesystem boundaries. I want Kubernetes permissions following
least privilege. I want the ability to destroy the environment and rebuild it if
something goes wrong.

The Hugging Face incident does not make any of those practices obsolete. If
anything, it is a fantastic argument for defense in depth.

The problem is expecting the sandbox to provide guarantees it was never designed
to provide. A sandbox answers a question like: *where is this process allowed to
execute?* That is fundamentally different from: *is this operation authorized?*

If an agent is allowed to execute code inside a container, the container can
prevent that process from directly reading `/etc/shadow` on the host. What it
cannot necessarily determine is whether the API the agent just discovered was an
appropriate resource for the task, whether the credentials available inside the
environment should be used for that operation, or whether submitting a particular
payload violates the business intent of the workflow.

Those are authorization questions. We keep handing them to containment
infrastructure and then acting surprised when containment is not enough.

| | Sandboxing (containment) | Guardrails (authorization) |
|---|---|---|
| **Core question** | Where is this process allowed to run? | Is this specific action authorized? |
| **Mechanism** | OS boundaries, containers, network policy | Policy middleware, schemas, validation |
| **Scope** | System resources: CPU, RAM, syscalls, FS | Domain semantics: APIs, business logic |
| **Failure mode** | Privilege escalation, infra compromise | Logic abuse, unauthorized mutation |

## Agents change the security model

Traditional applications get a security advantage that agents increasingly do not.

Most conventional applications execute code paths engineers explicitly wrote. An
engineer decides that clicking a button calls an API, the API invokes a service,
and the service performs a database operation. The user decides which path to
initiate, but the software determines which paths exist.

Agents change that relationship. The model participates in deciding what operation
happens next.

That is one of the reasons agents are useful. We do not have to enumerate every
possible sequence ahead of time. The model can inspect a result, determine that
its original plan was wrong, and choose another useful action.

But dynamic control flow creates a new security problem. If the model is allowed
to discover the next operation, the surrounding architecture has to decide which
discovered operations are actually valid.

That is where guardrails belong.

## Then we gave the agent Bash

The problem gets substantially worse because of the way we have built many agent
harnesses.

A surprising number of agent systems eventually expose Bash, Python, or another
general-purpose execution environment as one of the model's primary tools. This
makes perfect sense during development because general-purpose tools are
incredibly convenient. Instead of defining hundreds of individual operations, we
give the model a shell and let it figure out how to accomplish the task.

Unfortunately, that convenience destroys most of the structure we need for
deterministic security.

Bash is not really one tool. Bash is an interface for constructing an almost
unlimited number of tools. A shell can read files, start processes, communicate
over the network, install packages, inspect credentials, call APIs, modify
configuration, transform data, invoke interpreters, connect programs together, and
discover new capabilities that the engineer who exposed the shell never explicitly
considered.

Once an agent has that interface, the sandbox has an almost impossible job. It is
no longer restricting a known set of business operations. It has to anticipate
every possible composition of commands, processes, filesystems, network
interfaces, interpreters, package managers, environment variables, and
operating-system behaviors the model might discover.

The Hugging Face intrusion demonstrates exactly why that becomes dangerous. The
model repeatedly inspected each new environment it reached and effectively asked
the same question: *what can I do from here?* It discovered available binaries,
mounts, services, credentials, network paths, Kubernetes APIs, and cloud
infrastructure, then incorporated each discovery into the next step.

That is not unusual behavior for an agent. That is what an agent loop is designed
to do.

We created a system whose primary value proposition is that it can discover useful
next actions, and then we gave it an interface capable of expressing almost any
next action imaginable. The surprising outcome would have been if it never
discovered anything we forgot to prohibit.

## Probabilistic systems need deterministic boundaries

LLMs are probabilistic. That is not a flaw we need to engineer away. Their ability
to evaluate uncertain information and choose useful next actions is precisely what
makes them valuable.

The systems surrounding them need to be deterministic for exactly the same reason.

We already know how to build systems like this, because software engineering has
spent decades separating business logic from authorization. We have
authentication, API contracts, type systems, schemas, policy engines, role-based
access control, attribute-based access control, service boundaries, and
validation. None of those ideas became obsolete because an LLM entered the
architecture.

If anything, agents make them substantially more important, because the caller is
now capable of dynamically constructing requests engineers did not explicitly
write.

The missing layer is middleware between model intent and system execution.

```text
CONVENTIONAL ARCHITECTURE
  model ──▶ shell ──▶ infrastructure constraints

GUARDRAIL ARCHITECTURE
  model ──▶ structured tool request
        ──▶ policy and validation middleware
        ──▶ authorized business operation
        ──▶ infrastructure
```

The first architecture asks the model what should happen and then attempts to
contain the consequences. The second allows the model to propose what should
happen, but the architecture decides whether that action actually exists.

## The harness should be a contract

There are already frameworks exploring pieces of this architecture. Forge, for
example, treats agent actions as structured tool calls and provides middleware
around model execution. It can validate tool calls, reject malformed arguments,
enforce expected workflow behavior, and prevent the model from emitting arbitrary
actions the harness does not recognize.

Forge is not the complete authorization architecture described here, and that
distinction matters. What makes projects like it interesting is the architectural
pattern they demonstrate: there can be something between the model and execution.

That sounds obvious until you look at how many agent harnesses are essentially
glorified loops — ask the model what to do, execute what the model says, send the
result back, repeat.

A production harness needs to do substantially more. When the model asks to
execute a tool, the middleware should know whether that tool exists, whether the
arguments conform to the schema, which user initiated the request, which resource
the action targets, and whether that user, through this agent, during this task,
is authorized to perform that operation.

Only after those conditions are satisfied should execution occur. At that point
the harness is much closer to an API gateway or policy enforcement point than a
chatbot loop. That is exactly what we want.

Agents do not need fewer software-engineering constraints because they are
intelligent. They need more of them because their behavior is dynamic.

## The agent should not decide what it is allowed to know

The same architecture should apply before inference ever begins.

Most enterprise agents should not have broad permissions independent of the person
or process they represent. They are acting on behalf of something.

If a junior analyst invokes an internal finance agent, the agent should not
suddenly inherit the permissions of the engineering team because its service
account happens to have access to the entire warehouse. It should operate inside
the analyst's authorization boundary. If the CFO invokes the same agent, the
available information may be different. If the agent runs as part of an automated
reconciliation workflow, the task may grant another carefully scoped set of
capabilities.

This is where attribute-based access control becomes much more useful than
treating "agent" as another static application role. Authorization can be
evaluated using properties of the user, the agent, the task, the resource, the
requested action, and the current policy state.

The important part is *when* that evaluation happens. It should happen before the
context is constructed.

If the user is not authorized to access payroll data, the model should never
receive payroll data and then be instructed not to mention it. We should not put
every company's secrets into the context window and rely on a system prompt to
separate them. The unauthorized information simply should not exist inside that
agent's context.

## Sandboxes still matter, but they solve a different problem

The Hugging Face incident is not evidence that sandboxing failed as a concept. It
is evidence that sandboxing solves only one layer of the problem.

Agents that execute code should still operate inside isolated environments.
Network access should still be restricted. Credentials should still be minimized.
Kubernetes permissions should still follow least privilege. Infrastructure should
still assume that something will eventually behave in a way its designers did not
anticipate.

But those controls answer different questions:

- A **sandbox** asks where a process can execute.
- A **policy layer** asks whether an operation is authorized.
- A **context layer** determines what information the agent should receive.
- A **typed tool interface** determines which operations are available at all.

Production agent systems need answers to all four. Putting the model in a
container solves only the first.

## Conclusion

The lesson from the Hugging Face incident is not that sandboxes have failed and we
should stop using them. Sandboxes solve an important and necessary problem. They
just do not solve the entire problem.

The agent began inside a constrained environment and still found a sequence of
actions that moved it toward its goal. Each newly discovered capability created
another possible action, and the infrastructure around the model determined how
far those actions could go.

That is exactly why the security boundary needs to sit outside the model. The
answer is not to make the model less capable. It is to stop confusing model
capability with authorization.

Let the model reason about the best way to perform the work. Let it choose between
useful tools. Let it reconsider a plan when new information appears. But the model
should not decide what it is allowed to do.

A sandbox controls where code can run. A guardrail controls which actions are
allowed to exist. Production agents need both.

The agent will keep asking, "What can I do from here?" Our architecture needs to
decide which answers actually exist.

## References

- Hugging Face — *Anatomy of a Frontier Lab Agent Intrusion: A Technical Timeline of the July 2026 Incident*
- Hugging Face — *Security Incident Disclosure, July 2026*
- [Forge](https://github.com/antoinezambelli/forge) — structured agent middleware
- [Agentware](https://github.com/HaikeiLabs/Agentware) — policy enforcement and audit middleware
