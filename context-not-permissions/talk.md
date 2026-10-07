---
marp: true
theme: gaia
paginate: true
title: "Agents Need Context, Not Permissions"
description: The Context Void and the Three Laws of Context Engineering
---

<!-- _class: lead -->

# Agents Need Context

## Not Permissions

Miriah Peterson · @Soypete
AgenticCon

---

## Who Am I?

- CEO of Haikai Labs
- Co-host of the **Domesticating AI** podcast
- Building AI systems since 2022

---

<!-- _class: lead -->

# Have You Ever Missed the Joke?

Everyone laughs. You understood every word.

## You still have no idea what happened.

<!-- Open human. Everyone has been the new person in a company decoding acronyms
and discovering three departments define "customer" three ways. -->

---

## Capability Is Not Context

```text
scalpel + anatomy knowledge ≠ surgeon
```

They still need the vocabulary of the team, how the systems relate,
and the judgment to know when to cut.

**We hand agents the scalpel and assume intelligence fills in the rest.**

---

## The Reflex

Agent picks the wrong source of truth. Misreads a business term.
Takes an action nobody intended.

```text
conclusion: the model is not smart enough
action:     shop for a better one
```

## But what would more intelligence actually fix?

---

## What a Smarter Model Still Cannot Know

- that **Finance** means the billing entity and **Product** means the user
- that one database is authoritative and the other holds stale copies
- that a technically valid join violates a business rule

...unless that distinction exists **somewhere the system can reach.**

<!-- None of these are reasoning failures. They are unrepresented decisions. -->

---

<!-- _class: lead -->

# The Context Void

The gap between the context an agent receives
and the context required to do the task correctly.

---

## It Is Not Always Starvation

```text
20 documents about a customer
   → which one is authoritative?

a compliance policy
   → superseded this morning, nobody said

a raw identifier
   → customer? employee? internal service?

the right tool to change a record
   → may this user change it?
```

**Enormous information. Insufficient structure.**

---

## The Failure Chain

```text
missing or ambiguous data
          ↓
missing or ambiguous meaning
          ↓
probabilistic inference
          ↓
unvalidated action
```

The problem is not inference. **Inference is why we use models.**

The problem is leaving deterministic decisions unmade and asking
intelligence to fill the gap.

---

<!-- _class: lead -->

# Three Questions

## What information? What does it mean? How may it be used?

---

## Law One — Lexicon

> An agent should reason from information whose source, authority,
> relevance, ownership, and access conditions are known.

Retrieval cannot only ask *what looks relevant?*

```text
where did this come from?     who owns it?
is it current?                what superseded it?
who may access it?            for which purpose?
```

**Curation decides what belongs in the task. Retrieval only finds it.**

---

## Memory ≠ Governed Context

```text
MEMORY   what has the agent seen before?
CONTEXT  what is authoritative, relevant, and authorized — now?
```

Persistence without a data model accumulates unverified facts.

**Persistence without authority creates confident stale context.**

---

## Law Two — Semantics

> Information without meaning is still incomplete context.

```text
123-45-6789
```

The characters tell the model almost nothing.

```text
it is an SSN · belongs to a person · regulated
display masked · usable for identity verification
access governed by policy X
```

**Same data. Entirely different operational meaning.**

---

## Meaning Is Not Universal

```text
customer    finance ≠ sales
server      security ≠ platform
patient id  treatment ≠ billing ≠ analytics
SKU         one variant ≠ a product family
```

These relationships change the conclusions an agent may draw
from **identical underlying data**.

---

## Similarity Is Not Semantics

Vector search answers: *what looks similar to this request?*

It does not establish:

```text
which record supersedes which
whether two identifiers are the same entity
whether a relationship is contractual, hierarchical,
  temporal, causal — or merely correlated
which definition applies in this domain
```

**Embedding proximity is not organizational truth.**

---

## Law Three — Pragmatics

> "Can you check production?"

A coworker knows which dashboards, which commands, which systems,
and what *not* to do. Almost none of that is in the sentence.

```text
identity · purpose · resource · action
business rules · policy · permitted outcomes
```

**The model may infer which action accomplishes the task.
It may not infer whether that action is permitted.**

---

<!-- _class: lead -->

# Diagnosing a Void

## A refund request, three questions

---

## Walk the Three Laws

```text
LEXICON     did it have the customer, order, payment,
            purchase date, current return policy?
            → missing policy = lexicon problem

SEMANTICS   does "purchase date" mean order date here
            and settlement date there?
            → both correct, different conclusions

PRAGMATICS  is "help this customer" explain, evaluate,
            recommend, or execute a refund?
            → never established = inferred authority
```

**A vague model failure becomes an inspectable one.**

---

## And It Gives You Tests

```text
add the missing definition      → does the answer change?
introduce conflicting records   → which wins?
remove necessary information    → does it say it cannot proceed?
change a semantic relationship  → does the conclusion follow?
```

**That is what turns the Context Void from a metaphor
into an engineering problem.**

---

<!-- _class: lead -->

# More Information ≠ More Context

---

## The Impulse to Explain More

Bad result → add a paragraph → add a document → add an instruction.

Sometimes that was the missing piece.

**Sometimes we just made the ambiguity longer.**

```text
"Lost in the Middle"  position changes performance
RULER                 degrades with length + complexity
NoLiMa                remove lexical overlap, watch it fall
```

*available context ≠ effectively used context*

---

## Capacity Is Not Architecture

```text
128 GB of RAM ≠ load the database into memory
10 TB of disk ≠ one directory
1M tokens     ≠ send a million tokens
```

A million-token window cannot resolve a definition
**the organization never agreed on.**

---

<!-- _class: lead -->

# Why "Not Permissions"

---

## Permissions Come Last, Not First

The common pattern:

```text
give the agent broad access
   → discover it did something alarming
   → bolt on permissions
   → discover permissions block useful work
   → widen them again
```

The question was never *what may this agent touch?*

**It was: what does this task actually require?**

---

## Scope Follows Context

```text
task → required lexicon → authorized subset → agent context
```

If you know which information the task needs and who is asking,
the permission boundary **falls out of the design**.

If you do not, permissions are a guess you tighten after incidents.

**Context engineering is how you stop guessing.**

---

<!-- _class: lead -->

# The Takeaway

## Next time an agent is confidently wrong:

### Do not ask which model to swap in.

### Ask what it was equipped to understand.

---

## Three Questions to Leave With

```text
1. Did it have the relevant information?
2. Was the meaning represented?
3. Were the rules for using it explicit?
```

If any answer is no, you may not have a model problem.

**You may have found a Context Void.**

---

<!-- _class: lead -->

# Thank You

**Agents Need Context, Not Permissions**

Miriah Peterson · @Soypete
Haikai Labs

---

## Sources

Lewis et al. — *Retrieval-Augmented Generation*
Liu et al. — *Lost in the Middle*
Hsieh et al. — *RULER*
Modarressi et al. — *NoLiMa*
Yao et al. — *ReAct*
Kuhn et al. — *CLAM*
Kalai et al. — *Why Language Models Hallucinate*

**The Context Engineering Manifesto** — Haikai Labs
