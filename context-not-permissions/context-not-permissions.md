# Agents Need Context, Not Permissions

> Why permission scope should be derived from task context rather than guessed

Most teams arrive at agent permissions the same way.

Give the agent broad access so it can actually do the job. Discover it did
something alarming. Bolt on permissions. Discover those permissions block useful
work. Widen them again. Repeat until either the agent is useless or nobody is
comfortable with what it can reach.

That loop is not a failure of discipline. It happens because the scope was guessed
rather than derived. Nobody ever established what the task actually required, so
the permission boundary had nothing to follow.

The fix is upstream of permissions entirely. If you know which information a task
needs and who is asking for it, the boundary falls out of the design.

## The reflex to blame the model

When an agent picks the wrong source of truth, misreads a business term, or takes
an action nobody intended, the usual conclusion is that the model is not capable
enough, and the usual next step is shopping for a better one.

But what would more intelligence actually fix?

A smarter model still cannot know that Finance defines a customer as the billing
entity while Product means the person using the software — unless that distinction
exists somewhere the system can reach. It cannot know that one database is
authoritative while another holds stale copies, because both contain plausible
records. It cannot know that a technically valid join violates a business rule that
was never represented anywhere.

An agent can sit in the middle of an enormous enterprise data estate — databases,
documents, APIs, messages, retrieval systems — and still lack the information
required to understand any of it correctly. It is not necessarily starved for data.
It may be missing the structure that says what matters.

We call that gap the Context Void: the distance between the context an agent
receives and the context required to complete its task correctly.

## Three questions, borrowed from linguistics

Computational linguistics gives three useful categories for locating the void.

**Lexicon: what information belongs in this task?** Retrieval cannot only answer
*what looks relevant?* It also has to establish where information came from, who
owns it, whether it is authoritative and current, what supersedes it, who may
access it, and under which purpose it may be used. Retrieval finds candidates.
Curation decides what belongs.

This is also where memory and governed context separate. Memory asks what the agent
has seen before. Governed context asks what is authoritative, relevant, and
authorized *now*. Persistence without a data model accumulates unverified facts —
persistence without authority creates confident stale context.

**Semantics: what does that information mean?** Consider the string `123-45-6789`.
The characters tell the model very little. The operational meaning appears when the
system can establish that it is an SSN, that it belongs to a person, that it is a
regulated identifier, that it should be displayed masked, that it may be used for
identity verification, and that access is governed by a specific policy.

Meaning is not universal either. A customer means something different to finance
than to sales. A server means something different to security than to platform
engineering. A SKU may be a product variation in one system and a product family in
another. These relationships change the conclusions an agent may draw from
identical underlying data.

This is why similarity is not semantics. Vector search answers *what looks similar
to this request?* It does not establish whether one record supersedes another,
whether two identifiers refer to the same entity, whether a relationship is
contractual or hierarchical or merely correlated, or which definition applies in
the current domain. Embedding proximity is not organizational truth.

**Pragmatics: how may that meaning be used?** If I ask a coworker to check
production, they know which dashboards they may inspect, which commands they may
run, and what they should not touch. Almost none of that is in the sentence. Agents
need the same background supplied explicitly: identity, purpose, resource, action,
business rules, policy, permitted outcomes.

The model may infer which action would accomplish the task. It should not infer
whether that action is permitted.

## Using the three laws as a diagnostic

The value of these categories is not vocabulary. It is a repeatable way to
investigate why an agent misunderstood a task.

Take an agent handling a customer refund.

The lexicon question is whether the agent received the relevant information —
customer, order, payment, purchase date, the applicable return policy. If the
current policy never entered the working context, that is a lexicon problem, and no
larger model can reason over information it never received.

The semantics question is whether the system represented what those records mean.
Perhaps the order belongs to a subsidiary while the contract belongs to the parent.
Perhaps "purchase date" means submission date in one system and settlement date in
another. Both records are correct and they support different conclusions.

The pragmatics question is what the agent was expected to do. "Help this customer"
could mean explain the policy, determine eligibility, recommend an exception,
initiate a refund, or complete one. If that was never established, the agent is
inferring an organizational intention that should have been part of its context.

This also gives you tests. Add the missing definition and see whether the answer
changes. Introduce conflicting records and verify which source wins. Remove
necessary information and check whether the agent recognizes it cannot proceed.
Change a semantic relationship and confirm the conclusion follows.

That is what turns the Context Void from a metaphor into an engineering problem you
can locate, test, and correct.

## More information is not more context

When an agent misunderstands, the instinct is to explain more. Add a paragraph, a
document, another instruction. Sometimes that supplies exactly what was missing.
Sometimes it just makes the ambiguity longer.

The long-context research is relevant here. *Lost in the Middle* showed that
performance varies with where relevant information sits in the context. RULER
showed degradation as both length and task complexity increase. NoLiMa removed
lexical overlap between query and evidence and watched performance fall sharply
well before the advertised context limit.

Available context and effectively used context are not the same thing. Capacity is
not architecture. Having 128 GB of RAM does not mean loading the database into
memory, and a million-token context window cannot resolve a definition the
organization never agreed on.

## Why the permission boundary follows

Return to the loop at the top. Broad access, alarming incident, bolted-on
permissions, blocked work, widened permissions.

That loop runs because the question being asked is *what may this agent touch?* —
which has no principled answer. There is no natural stopping point between "enough
to work" and "everything."

The better question is *what does this task actually require?* That one has an
answer, and the answer is exactly the lexicon: the information relevant to this
decision, from appropriate sources, for this purpose.

```text
task → required lexicon → authorized subset → agent context
```

Once that chain exists, the permission boundary is not a guess you tighten after
incidents. It is a consequence of having established what the task needs and who is
asking.

And the same evaluation improves security rather than trading against it. If the
user is not authorized to access payroll data, the answer is not to retrieve it and
instruct the model not to mention it. The information should never enter that
agent's context in the first place.

## The question to ask

The next time an agent produces a confidently wrong answer, do not start by asking
which model to swap in. Ask what it was equipped to understand.

Did it have the relevant information? Were the business definitions explicit? Were
the important relationships represented? Did it understand how that meaning should
be used in this task?

If the answer to any of those is no, you may not have found a model problem at all.
You may have found a Context Void — and no amount of permission tuning will close
it.

## References

- Lewis et al. — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*
- Liu et al. — *Lost in the Middle: How Language Models Use Long Contexts*
- Hsieh et al. — *RULER: What's the Real Context Size of Your Long-Context Language Models?*
- Modarressi et al. — *NoLiMa: Long-Context Evaluation Beyond Literal Matching*
- Yao et al. — *ReAct: Synergizing Reasoning and Acting in Language Models*
- Kuhn et al. — *CLAM: Selective Clarification for Ambiguous Questions*
- Kalai et al. — *Why Language Models Hallucinate*
- NIST SP 800-162 — *Attribute Considerations for Access Control Systems*
- *The Context Engineering Manifesto* — Haikai Labs
