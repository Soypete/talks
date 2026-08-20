---
marp: true
theme: gaia
paginate: true
title: "Beyond AI Memory: Why Semantic Context Is the Missing Layer in Agentic Infrastructure"
backgroundImage: url('../images/soypete_background.png')
description: Why production agents need engineered context, not more memory
---

<!-- _class: lead -->

# Beyond AI Memory

## Why Agents Need Engineered Context

Miriah Peterson · @Soypete

---

## Who Am I?

- AI/ML infrastructure engineer
- Builder of production agent systems
- Creator of open-source context and ontology tools
- Organizer: Utah Data Engineering & MLOps Meetups

![bg right:40%](../images/SP_Logo-02.png)

---

<!-- _class: lead -->

# Raise your hand if an agent has ever…

## deleted code you needed

## reverted the wrong changes

## updated the wrong file

---

<!-- _class: lead -->

# Agents do not need more memory.

## They need the right context.

---

## Memory Is Stored History

- Past messages
- Previous actions
- Saved preferences
- Summaries
- Retrieved documents

Memory tells us **what happened before**.

---

## Context Is What This Task Requires

> The minimum information, meaning, state, and authority needed to handle one request.

Context tells the agent **what matters now**.

---

## Same Memory. Different Context.

> “Clean this up.”

| Situation | Required context |
|---|---|
| Code review | Explain problems; change nothing |
| Working branch | Edit only the selected file |
| Production incident | Preserve state; collect evidence |

History alone cannot choose the right action.

---

## Context Is a Query

```text
request + user + task + current state + policy
                         ↓
                 context for now
```

It is assembled for a purpose.

It is not a transcript we keep appending to.

---

<!-- _class: lead -->

# Why must context be engineered?

---

## Because It Changes Every Time

- **User:** Who is asking?
- **Task:** What are they trying to accomplish?
- **State:** What is true right now?
- **Meaning:** What do these entities mean here?
- **Authority:** What may happen next?

The right context is conditional—not universal.

---

## What Most Harnesses Do

```text
request
   ↓
retrieve similar text
   ↓
ask the model what it means
   ↓
let the model choose a tool
```

Each arrow adds an inference.

---

## Inference Becomes Action

```text
the user said X
      ↓
the model inferred Y
      ↓
the harness treated Y as permission
      ↓
the tool made Y real
```

**Plausible is not authorized.**

---

<!-- _class: lead -->

# What happens when context is not engineered?

---

## 1. The Wrong File

> “Remove the old handler.”

The agent finds two similar handlers.

It edits the deprecated example instead of the live implementation.

**Missing context:** identity and scope.

---

## 2. The Wrong Data

> “Summarize the patient history.”

Retrieval finds a semantically related note from another care team.

The note is relevant—but not permitted for this purpose.

**Missing context:** provenance and authority.

---

## 3. The Wrong Action

> “That felt like a nine. Add weight.”

The agent remembers the athlete’s strength goal.

It misses the live form-breakdown signal.

**Missing context:** current state and action boundaries.

---

## The Pattern

| Missing | Agent must guess |
|---|---|
| Reference | Which thing? |
| Meaning | What does it mean here? |
| State | What is true now? |
| Authority | May I access or change it? |
| Intent | Is this a question, request, or action? |

---

<!-- _class: lead -->

# Context Engineering

## Make the required context explicit before action.

---

## The Context Assembly Pipeline

```text
classify
   → retrieve
      → resolve meaning
         → authorize
            → assemble
               → validate
                  → act
```

Each stage has an owner, a contract, and a test.

---

## 1. Classify the Task

> “Can you clean this up?”

```yaml
speech_act: ambiguous_request
target: unresolved
requested_effect: unclear
safe_next_step: ask_for_scope
```

Do not hide uncertainty behind a confident tool call.

---

## 2. Retrieve by Scope

```text
identity + purpose + entity + time
                  ↓
       authoritative source
                  ↓
          minimum result
```

Similarity can help find candidates.

Scope decides what may enter context.

---

## 3. Resolve Meaning

```text
RPE 9
  ├─ reported_by → athlete_42
  ├─ observed_during → current_set
  └─ combined_with → form_breakdown
```

Relationships make domain meaning explicit.

---

## 4. Bound the Action

```yaml
tool: set_next_weight
requires:
  - active_session
  - safe_form
  - progression_allowed
  - user_confirmation
```

The model proposes an action.

Infrastructure validates it.

---

## The Coaching Request—Engineered

> “That felt like a nine. Add weight.”

```yaml
intent: increase_next_set
current_state: form_breakdown_detected
governing_rule: stop_and_reassess
allowed_actions: [explain, request_review]
denied_actions: [increase_weight]
```

The answer is safer because the context is better.

---

## Test the Pipeline, Not Just the Answer

| Stage | Question |
|---|---|
| Classify | Did we understand the request? |
| Retrieve | Did we use the right source? |
| Resolve | Did we identify the right entities? |
| Authorize | Was access purpose-scoped? |
| Validate | Was the action allowed? |

---

## This Is Bigger Than RAG

RAG asks:

> What content is relevant?

Context engineering also asks:

> What does it mean, who may use it, and what may happen next?

RAG is one stage in the pipeline.

---

## The Infrastructure Boundary

```text
agent / model
      │ proposal
      ▼
┌──────────────────────────────┐
│ classify · retrieve · resolve│
│ authorize · validate · audit │
└──────────────┬───────────────┘
               ▼
       data · APIs · tools
```

The model reasons. The boundary governs.

---

## Models Can Change. Authority Should Not.

- Swap GPT for Claude or Llama
- Swap LangChain for PydanticAI or custom code
- Swap vector search for SQL or graph traversal

The context contracts remain.

The security boundary remains.

---

## Start With One Action

1. Name the action that can cause harm.
2. List the context required to perform it safely.
3. Identify the authoritative source for each item.
4. Make uncertainty and permission explicit.
5. Validate outside the model.

---

<!-- _class: lead -->

# Memory tells an agent what happened.

# Context tells it what matters now.

## Engineer the context before you trust the action.

---

<!-- _class: lead -->

# Questions?

## Miriah Peterson

### @Soypete
