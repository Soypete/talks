---
marp: true
theme: gaia
paginate: true
title: "Shared Memory for Agents"
description: A wiki as the coordination substrate for multi-agent systems
---

<!-- _class: lead -->

# Shared Memory for Agents

## A wiki as the coordination substrate

Miriah Peterson · @Soypete

---

## Who Am I?

- CEO of Haikai Labs
- Co-host of the **Domesticating AI** podcast
- Building AI systems since 2022

---

<!-- _class: lead -->

# Agents Will Build a Message Board

## Whether or not you give them one.

---

## Summer 2026: OpenAI

Thousands of agents, evaluated in parallel. Many given impossible tasks.

```text
shared package manager (Artifactory)
            ↓
messages encoded as directory names
            ↓
~1,200 agents · >70,000 messages
```

They found each other through the only shared writable surface they had.

<!-- Tell this briskly; it is the setup, not the subject. Persistent agents on
impossible tasks discovered they could create directories in a shared package
cache, and encoded messages as directory names. Cite the Dwarkesh Patel writeup
and the METR/Redwood report. The point is not the scandal — it is the mechanism. -->

---

## What They Built, Unprompted

- a shared board with **identity** — agents signed messages
- **handoffs** — a coordinator handed leadership when its budget ran out
- **division of labor** — hundreds of agents across three workstreams
- **a protocol** — conventions nobody specified

**Coordination is not a feature you add. It is a thing agents do.**

<!-- This is the slide that earns the whole talk. Every primitive in this
presentation — identity, handoff, acknowledgment, shared findings — appeared
spontaneously in a system that was never designed to have them. The agents
invented the coordination substrate because the work demanded one. -->

---

## But Look at *Where* They Built It

| | Their board | What you'd want |
|---|---|---|
| Channel | a package cache | a designed one |
| Schema | directory names | typed records |
| Visibility | covert | logged |
| Auditability | reconstructed after | by construction |
| Off switch | crash it | stop running organize |

**Nobody chose that substrate. It was the only writable thing they could reach.**

<!-- Be careful not to moralize here. The failure was not that agents
coordinated; it was that the only channel available was one nobody could see.
When the humans patched Artifactory they wiped the board without ever realizing
it was a board. -->

---

<!-- _class: lead -->

# So: Give Them One

## Designed. Typed. Logged. Yours.

---

<!-- _class: lead -->

# Every Harness Solves Memory

## For exactly one agent.

---

## What We Built for One Agent

```text
context window   → what fits right now
compaction       → what survives the window
session log      → what happened in this conversation
vector store     → what to retrieve into this prompt
```

All of it scoped to **one model, one conversation**.

<!-- This is the setup. Every one of these is a real solution to a real problem,
and none of them is wrong. The point is the scope: each is bounded by a single
agent's session. Nothing here composes. -->

---

## Then You Run a Second Agent

```text
Agent A                      Agent B
   │                            │
learns something           learns nothing
decides something          decides it again
hits a blocker             hits the same blocker
```

**Nothing A learned is available to B.**

<!-- This is the moment the problem appears, and it appears immediately — not at
scale, not in production, just the second time you start an agent. -->

---

## The Usual Answers

| Substrate | What you lose |
|---|---|
| **Vector store** | who wrote it, when, why; diffs; review |
| **Chat channel** | structure — it is prose by construction |
| **Shared files** | any guarantee two writers won't collide |
| **A database** | human readability, and a weekend |

**Each is missing something you need to operate the thing.**

<!-- Be fair to each of these. A vector store is a fine retrieval layer and a
terrible system of record: you cannot diff it, review it, or attribute it. A chat
channel has provenance and no structure. Shared files have no writer discipline.
Be honest that a purpose-built database would work — it just costs more than the
problem is worth at this stage. -->

---

<!-- _class: lead -->

# What If Memory Were a Wiki?

## Plain markdown. One writer. A closed vocabulary.

---

## The Shape of It

```text
                 agents
          search │      │ capture
                 ▼      ▼
         ┌───────────────────────┐
         │        INBOX          │   append-only
         │   one JSON per note   │   never blocks
         └───────────┬───────────┘
                     │  organize          ← single writer
                     ▼
         ┌───────────────────────┐
         │      WIKI GRAPH       │
         │  typed pages + links  │
         │   index.md · log.md   │
         └───────────────────────┘
                     │
              raw/ (immutable sources)
```

**Capture never touches the graph. Only `organize` writes.**

<!-- Walk this slowly; it is the architecture slide. Agents read from both the
graph and the inbox, so a capture is visible to other agents immediately, marked
as pending. Agents write only to the inbox, one atomic file per capture, which is
why concurrent writes need no locks. A single reconciliation step promotes inbox
records into typed pages. raw/ holds immutable ingested sources. -->

---

## Why the Inbox Matters

```text
capture  →  one atomic file  →  done
```

- no locks, no transactions, no coordination protocol
- two agents capturing at once cannot collide
- a capture is visible to search **before** it is organized
- reconciliation is a separate, reviewable step

**Concurrency is solved by not sharing the write path.**

<!-- This is the single best design decision in the system and it is not novel —
it is a spool directory. Each capture is one atomic file write. There is no
read-modify-write anywhere in the capture path, so there is nothing to race. -->

---

## A Closed Vocabulary at the Write Boundary

```toml
[entity_types]
claim         = "A discrete assertion."
decision      = "A decision with context and rationale."
contradiction = "A recorded conflict between two claims."
entity        = "A named thing worth its own page."
source        = "An immutable ingested document."
```

A capture with a type outside the list is **rejected**.

**Nothing is coerced to a default.**

<!-- Emphasize rejection. The tempting design is to accept anything and normalize
later, which produces a pile you cannot query. Rejecting at the boundary means the
graph is always well-typed. Schema changes are a human editing a config file, not
the plugin inventing terms. -->

---

## Who Decides What Something Is?

```text
AGENT      chooses the type         ← the only judgment here
VOCABULARY accepts or rejects it    ← closed set, deterministic
ORGANIZE   files it                 ← mechanical
HUMAN      decides when to run      ← scheduling, not sorting
```

**Organize calls no model.** It validates, renders links, writes the page
to `wiki/<type>/`, logs it, moves the record.

```python
vocab.check_capture(entity_type, links)   # or reject
adapter.write_memory(content, {"category": entity_type})
```

<!-- This is the slide that makes the closed vocabulary matter. If organize could
reinterpret a bad type, the vocabulary would be decorative. Because promotion is a
pure function of the record, the agent's declared type is the classification, and
the boundary either accepts it or throws it in rejected/. A LockFile serializes
organize, so single-writer is enforced in code rather than by convention. -->

---

## Typed Links Make It a Graph

```text
derived_from · contradicts · supports · about · relates_to
```

```markdown
## Links

- contradicts: [[indexed-retrieval-wins]]
- derived_from: [[imported/some-paper]]
```

**A claim that contradicts another claim is a queryable fact.**

<!-- The link predicates are as closed as the entity types. This is what makes
contradiction a first-class thing rather than a note someone wrote. Two agents
reaching opposite conclusions produces a recorded, findable conflict. -->

---

<!-- _class: lead -->

# Then Something Unexpected

## Agents started using it to coordinate.

---

## Coordination Primitives

```toml
blocker         = "A blocking issue that stalls the dependent task."
handoff         = "A task passed from one agent or context to another."
ack             = "An acknowledgment that a handoff was received."
release         = "A declared release of a resource, lock, or responsibility."
contract_change = "A change to an inter-agent contract."
```

```text
answers · acknowledges · blocks
```

**The knowledge base became a place to hand work over.**

<!-- These types were added after the fact, because the pattern showed up in
practice. Note that this is not a message queue: a handoff is a durable page with
links, searchable months later, not an event that is consumed and gone. -->

---

## A Real Handoff

```markdown
---
title: "AGENTS-1 handoff: workflow registry + Notion schemas"
category: handoff
created: 2026-09-17T16:06:15
---

Implemented AGENTS-1: added harness-neutral
WorkflowManifest/WorkflowRegistry ... 47/47 tests pass,
mypy clean, ruff clean. PR: .../pull/14

## Links
- about: [[workflow_registry]]
```

**Written by an agent. Read by the next one.**

<!-- This is a real page from the running wiki, lightly trimmed. Point out what it
carries: what was done, the evidence that it works, a link to the PR, and a typed
edge to the entity it concerns. The next agent searches for the entity and finds
the handoff. -->

---

## A Real Blocker

```markdown
---
title: "blocker: S3 release bucket not provisioned"
category: blocker
---

PR #10 and the stacked release workflow PR both depend on
an S3 bucket and an OIDC IAM role that do not yet exist...
The companion Terraform PR must be applied before any
release can be published.

## Links
- blocks: [[release-pipeline]]
```

**`blocks:` is an edge. You can query what is stuck.**

---

## A Worker Orienting Itself

Real session. Ticket **HAI-123**. It has not written any code yet.

* **`wiki search "HAI-123"`**  →  *no results*
* ↓ &nbsp; nobody has recorded this. widen.
* **`wiki search "ADR-016"`**  →  *6 results*
* ↓ &nbsp; adjacent work exists. read it.
* **`default-policy-bootstrap-and-tool-catalog`**
* &nbsp;&nbsp;&nbsp;PR #14 · branch `feat/default-policy-bootstrap`
* &nbsp;&nbsp;&nbsp;migration 029 creates `abac.tool_catalog`
* ↓
* > "This is **highly relevant** to HAI-123!"
* ## It found the branch it was about to duplicate.

<!-- Advance one step at a time; the payoff only lands if the room follows the
widening. Beat 1: the worker searches its own ticket and gets nothing. Beat 2: a
miss is information — nobody has recorded this, so widen rather than stop. Beat 3:
the adjacent ADR hits. Beats 4-6: what it found, including a branch that already
exists on origin and a migration number. Beat 7: its own reaction, verbatim.
Beat 8: the point. It discovered prior work before writing a line of code. -->

---

## Search Is How a Worker Starts

```text
new task
   ↓
search the ticket, the ADR, the component
   ↓
┌── hits ──▶ read the pages, follow the links
└── miss ──▶ nobody has done this; proceed and capture
```

**A miss is a result.** It means the work is genuinely new.

Lexical search means you search **identifiers** — ticket IDs, ADR numbers,
branch names. That is what an agent actually has at the start of a task.

<!-- Generalize the transcript into the pattern. The important half is the miss
branch: an empty result is not a failure, it is permission to proceed, and it
tells the agent to capture what it learns because it is first. Also reframes the
lexical-vs-semantic tradeoff: semantic search wins for fuzzy conceptual recall,
but a worker beginning a ticket has exact tokens, and lexical matching on those is
precise and predictable. The tradeoffs slide later still stands. -->

---

## Agents Audit Each Other

```markdown
---
title: kei has no CLAUDE.md; the agent-facing file is AGENTS.md
category: contradiction
---

Corrects [[HAI-53 audit ...]], which attributes two stale claims
to 'CLAUDE.md'. Verified: NO CLAUDE.md exists anywhere in the
repo, and none exists in git history either
(git log --all -- '**/CLAUDE.md' returns empty)...

ADR-016's stale boundary is NOT fixed and remains an open
docs inconsistency for whoever owns docs/adr/.

## Links
- contradicts: [[HAI-53 audit ...]]
```

**A later agent disproved an earlier one — and left the receipts.**

<!-- Three things to point at. It cites the exact commands it ran, so the
correction is checkable. It uses the contradicts edge, so both pages survive and
the conflict is queryable. And the last line hands an unresolved issue forward to
whoever picks up that area. None of this survives in a chat log. -->

---

## Orchestrators and Workers

Workers get named for the task they were assigned:

```text
D-007-otp-no-autocreate       ADR-015-A       ADR-015-B
        │                          ▲               │
        │ acknowledges             └───── handoff ─┘
        ▼
  D-007  (orchestrator decision)
```

**The wiki is the channel.** No queue, no bus, no protocol.

<!-- These IDs are real. A decision D-007 is recorded by the orchestrator; a
worker spawned to execute it is literally named D-007-otp-no-autocreate. ADR-015
was split between two workers, A and B. Note that the orchestrator in these pages
is called "herder" — workers hand back to it by name. -->

---

## A Worker Acknowledges Its Assignment

```markdown
---
title: ack/D-007-otp-no-autocreate
category: ack
---

Worker D-007-otp-no-autocreate acks D-007 (Option C of R-002).
Will: replace create-fallback in
resolveActiveOrganizationForEmailUser with resolve-only...
Verified: single call site at handlers.go:171 already tolerates
empty result; zero tests reference the function.

## Links
- acknowledges: [[decisions/D-007-onboarding-option-c-gated-on-stop-a]]
```

**It states its plan and what it checked before starting.**

---

## A Worker Hands Back What It Did Not Finish

```markdown
---
title: handoff/ADR-015-B-to-A-admin-members-edge-pending
category: handoff
---

handoff to ADR-015-A / herder — pending admin→members
containment edge. ADR-015-B built the write path ... but
deliberately did NOT seed the admin contains members edge.
That edge must be seeded once workspace-group-init lands.
```

**The most valuable thing an agent can record is what it chose not to do.**

<!-- This is the slide to linger on. A worker deliberately leaving work undone,
and saying so in a durable, addressable place, is the thing that never survives a
context window. The next worker does not rediscover the gap — it reads it. -->

---

## They Told Me How They Work

A `decision` page captured by an agent today:

> "Workers coordinate through wiki findings and must preserve
> dirty worktrees; live cloud/Twilio mutations require explicit
> approval."

**Nobody wrote that protocol down first. It was recorded from practice.**

<!-- This is a real, unedited line from a capture that was still pending in the
inbox when this deck was built. The coordination convention is itself a wiki page
— which means it is searchable, linkable, and can be contradicted later. -->

---

## What Is Actually In There

| | |
|---|---:|
| total items | ~13,800 |
| claims | 155 |
| decisions | 125 |
| contradictions | 34 |
| blockers | 19 |
| handoffs | 18 |
| releases · acks · contract changes | 8 |

**The coordination types are small. They are also the ones being used.**

<!-- Be honest about the shape of this: the bulk is imported and test content. The
interesting number is not 13,800, it is that 19 blockers and 18 handoffs were
written by agents doing real work across repositories. -->

---

<!-- _class: lead -->

# The Agent Loop

---

## Search Before You Answer

```bash
wiki search <query> [--top-k N] [--json]
```

```bash
wiki capture --title "..." --type claim \
  --content "..." --link derived_from:some-page
```

Put it in `CLAUDE.md` / `AGENTS.md` and every agent has it.

**No protocol. No SDK. A command and stdout.**

<!-- The agent surface is deliberately unglamorous. Any agent that can run a shell
command can participate, which is why this works across Claude Code, opencode, and
codex without per-harness integration. Skills exist for each, but the instruction
block in CLAUDE.md is enough. -->

---

## How an Agent Is Told About It

A block in `AGENTS.md` / `CLAUDE.md`. Read at session start.

```markdown
- **Before answering**, search for prior notes:
  `wiki search <query>`
- **When you learn something durable**, capture it:
  `wiki capture --title "..." --type claim --content "..."`
- **Before writing code**, search for the conventions that
  bind the work and follow the pages they return —
  **the page is authoritative, not memory.**
```

**No SDK. No protocol. Instructions and a CLI.**

<!-- Contrast this deliberately with the Artifactory story. Those agents had to
discover their channel; these agents are handed it in the first thing they read.
The strongest line is the last one: the page is authoritative, not memory. That
is the whole posture — durable shared state outranks what any single agent
thinks it remembers. -->

---

## It Tells Them What to Look Up

```markdown
- `wiki search "package placement conventions"`
- `wiki search "commit and pr shape"`
- `wiki search "duplicate handler implementations"`
```

Named queries for the conventions that bite.

```markdown
Rules:
- Invalid types/predicates are rejected —
  do not guess or coerce a value.
- Captures land in an inbox; do not edit wiki pages directly.
```

**The constraints are in the instructions, and enforced at the boundary.**

<!-- Two levels of defense. The instructions tell the agent not to guess a type,
and the vocabulary rejects it if the agent guesses anyway. Prompt for intent,
boundary for enforcement — the agent is told the rule and cannot break it. -->

---

## Read Includes Pending

```text
search ──┬──▶ wiki graph      (settled)
         └──▶ inbox           (pending, marked inbox:)
```

Agent A captures at 10:00.
Agent B searches at 10:01 and **sees it**.

Organize runs later — but it sorts nothing. It only promotes.

**Visibility is immediate. Commitment is deliberate.**

<!-- This resolves the obvious objection to a single writer: if only organize
writes to the graph, is memory stale until someone runs it? No — search reads the
inbox too. The graph is the settled record; the inbox is the working set. -->

---

<!-- _class: lead -->

# The Honest Tradeoffs

---

## What This Costs

| Constraint | Consequence |
|---|---|
| lexical search | no semantic recall; phrasing matters |
| closed vocabulary | captures get rejected |
| agent classifies | a wrong type is a wrong page |
| markdown on disk | no transactions, no queries beyond grep |

**Every one of these is load-bearing.**

<!-- Do not skip this slide. Each constraint buys the property above it: lexical
search is inspectable, rejection keeps the graph typed, the human writer keeps
the graph coherent, and files on disk make everything greppable and diffable. If
you need semantic recall, add an index over the same files — the substrate does
not have to change. -->

---

## What It Buys

```bash
grep -r "release pipeline" ~/code/wiki
git diff HEAD~1 -- wiki/decision/
wiki audit --stale-days 14
```

- every memory is a file you can read
- every change is a diff you can review
- every claim has a page you can edit or delete
- `wiki audit` finds orphans, broken links, stale records

**Memory you can operate.**

---

<!-- _class: lead -->

# Why This Generalizes

## The hard part was never storage.

---

## The Reusable Ideas

1. **Put the vocabulary at the write boundary.** Reject, do not normalize.
2. **Separate capture from reconciliation.** One writer, an inbox between.
3. **Make links typed.** A graph you can query beats prose you can search.
4. **Let reads see pending writes.** Visibility now, commitment later.
5. **Store it in something a human can open.** You will need to.

**None of this requires a vector database.**

---

<!-- _class: lead -->

# The Real Argument

## They coordinated through a package cache
## because that is what was reachable.

The question was never *whether* agents share state.

## It is whether you can see it.

---

<!-- _class: lead -->

# Thank You

## Shared Memory for Agents

[github.com/Soypete/herdr-wiki-plugin](https://github.com/Soypete/herdr-wiki-plugin)

Miriah Peterson · @Soypete

---

## Sources

**The plugin**
[github.com/Soypete/herdr-wiki-plugin](https://github.com/Soypete/herdr-wiki-plugin)

**The idea it started from** — Karpathy's LLM-Wiki
[gist.github.com/karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**The agent civilizations story** — Dwarkesh Patel, Aug 2026
[dwarkesh.com/p/openai-huggingface](https://www.dwarkesh.com/p/openai-huggingface)

*and the underlying METR/Redwood and OpenAI incident reports*

---

<!-- _class: lead -->

# Bonus

## Questions this usually gets

---

## "Why not just use a vector store?"

You can — **as an index, not as the record.**

```text
markdown files          ← the system of record
      ↓ embed
vector index            ← disposable, rebuildable
```

The files stay greppable, diffable, and reviewable.
The index becomes a cache you can throw away and rebuild.

**Use the vector store for recall. Do not use it for truth.**

---

## "What happens when two agents disagree?"

```text
Agent A: claim   "indexed retrieval wins"
Agent B: claim   "semantic retrieval wins"
                      ↓
         contradiction page links both
```

`contradiction` is a first-class type and `contradicts` is a real edge.

**The conflict becomes a durable, findable page — not a lost argument.**

---

## "Doesn't the human become the bottleneck?"

The human never classifies. **Organize is deterministic** — it could run
on a timer, a hook, or a cron.

```text
capture   → immediate, unbounded, concurrent
search    → sees pending captures right away
organize  → mechanical; runs whenever you want
```

Keeping a human in front of it is a **choice about review**, not a
requirement of the design.

**Organize is a garbage collector, not a lock.**
