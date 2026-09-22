# Shared Memory for Agents

> A wiki as the coordination substrate for multi-agent systems

Every agent harness solves memory. Context windows have compaction strategies.
Sessions have event logs. Retrieval has vector stores. All of it is real work on a
real problem, and none of it composes.

The scope is the issue. Each of those mechanisms is bounded by a single agent's
session with a single model. Start a second agent and it knows nothing about what
the first one learned, decided, tried and abandoned, or is currently blocked on.
The memory problem for one agent and the memory problem for several agents are
different problems, and solving the first does not advance the second.

This is an account of one answer: a plain markdown wiki with a closed vocabulary,
an append-only inbox, and exactly one writer. It is running, it holds roughly
13,800 items, and coding agents across several repositories use it to hand work to
each other.

## Why the usual substrates fall short

The reflex is to reach for a vector store, because retrieval is the visible part
of the problem and vector stores are the available answer. They are a good index
and a poor system of record. You cannot diff one. You cannot review a change to
one. When two agents write conflicting information, nothing marks the conflict —
both embeddings simply exist, and retrieval returns whichever is closer to the
query. Attribution, if present at all, lives in metadata nobody reads.

A shared chat channel has the opposite problem. Provenance is excellent: every
message has an author and a timestamp. Structure is absent by construction. You
cannot ask "what decisions are still open" of a channel, because a decision is not
a thing in a channel — it is prose that a human recognizes as a decision.

Shared files without writer discipline give you neither. Two agents editing the
same file is a lost update waiting to happen, and the usual fix — a lock — turns
every capture into a coordination problem.

A purpose-built database would work. It also costs more than the problem is worth
before you know what the schema should be, and it puts the memory somewhere a
human cannot casually open.

## The shape of the system

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

Three properties do most of the work.

**Capture never touches the graph.** An agent capturing a finding writes one
atomic JSON file to an inbox directory and appends one line to a log. That is the
entire write path. There is no read-modify-write anywhere in it, so two agents
capturing simultaneously cannot collide, and no locking is required. This is a
spool directory, which is not a new idea; it is just rarely applied to agent
memory.

**Exactly one operation writes the graph.** A separate `organize` step promotes
inbox records into typed pages, updates the index, appends to the log, and moves
each record to a processed directory. Because there is one writer, the graph is
never in a partially-updated state, and every change is a reviewable batch.

**Reads see pending writes.** Search reads the graph *and* the inbox, marking
pending records. An agent that captures at 10:00 is visible to an agent searching
at 10:01, long before anyone runs `organize`. This is what keeps the single-writer
design from introducing staleness: the graph is the settled record, the inbox is
the working set, and search covers both.

## The vocabulary is closed

A capture declares an entity type and optional typed links. Both come from a fixed
list:

```toml
[entity_types]
claim         = "A discrete assertion."
decision      = "A decision with context and rationale."
contradiction = "A recorded conflict between two claims."
entity        = "A named thing worth its own page."
source        = "An immutable ingested document."
```

A capture whose type is not in the list is **rejected**. Nothing is coerced to a
default, and the plugin does not invent terms — changing the schema means a human
editing a config file.

This is the decision most likely to feel wrong, and it is the one holding the rest
up. The tempting alternative is to accept anything and normalize later, which
reliably produces a pile nobody can query. Rejecting at the write boundary means
the graph is well-typed at all times, which is what makes questions like "what
decisions were recorded this month" answerable with a directory listing.

Link predicates are closed the same way — `derived_from`, `contradicts`,
`supports`, `about`, `relates_to` — which turns the wiki into a graph rather than
a pile of documents. A claim that contradicts another claim is a queryable fact,
not a remark.

## Then agents started coordinating

The interesting part was not planned. The vocabulary grew a second cluster of
types, added because the pattern kept appearing in practice:

```toml
blocker         = "A blocking issue that stalls the dependent task."
handoff         = "A task passed from one agent or context to another."
ack             = "An acknowledgment that a handoff was received."
release         = "A declared release of a resource, lock, or responsibility."
contract_change = "A change to an inter-agent contract."
```

with predicates `answers`, `acknowledges`, and `blocks`.

A knowledge base had become a place where agents hand work to each other. Here is
a real handoff page, lightly trimmed:

```markdown
---
title: "AGENTS-1 handoff: workflow registry + Notion schemas"
category: handoff
created: 2026-09-17T16:06:15
---

Implemented AGENTS-1: added harness-neutral WorkflowManifest/
WorkflowRegistry with register, get, list_workflows,
discover_by_tool, discover_by_connector, and validate methods...
47/47 tests pass, mypy clean, ruff clean. PR: .../pull/14

## Links
- about: [[workflow_registry]]
```

Note what it carries: what was done, evidence that it works, a link to the pull
request, and a typed edge to the entity it concerns. The next agent searching for
that entity finds this page.

And a blocker:

```markdown
---
title: "blocker: S3 release bucket not provisioned"
category: blocker
---

PR #10 and the stacked release workflow PR both depend on an S3
bucket and an OIDC IAM role that do not yet exist... The companion
Terraform PR must be applied before any release can be published.

## Links
- blocks: [[release-pipeline]]
```

`blocks:` is an edge, so "what is currently blocking the release pipeline" is a
query rather than an archaeology exercise.

This is worth distinguishing from a message queue. A handoff is a durable page
with links, findable months later, not an event that is consumed and disappears.
The coordination record and the knowledge record are the same artifact.

## What is actually in there

| | |
|---|---:|
| total items | ~13,800 |
| claims | 155 |
| decisions | 125 |
| contradictions | 34 |
| blockers | 19 |
| handoffs | 18 |
| releases, acks, contract changes | 8 |

The headline number is misleading and worth deflating: the bulk is imported
reference material and test fixtures. The number that matters is the small one —
19 blockers and 18 handoffs, written by agents doing real work across
repositories, without anyone designing a coordination protocol for them to follow.

## The agent-facing surface

There is none to speak of, which is the point:

```bash
wiki search <query> [--top-k N] [--json]
wiki capture --title "..." --type claim --content "..." \
  --link derived_from:some-page
wiki organize
wiki audit [--stale-days N]
```

A command and standard output. Any agent that can run a shell command can
participate, which is why this works across Claude Code, opencode, and codex with
no per-harness integration. Per-agent skills exist, but a block of instructions in
`CLAUDE.md` or `AGENTS.md` is enough — the agent reads it at session start and
uses the commands.

## The honest tradeoffs

Search is lexical. There is no semantic recall, so phrasing matters, and a concept
described two different ways may not connect. If you need embeddings, build an
index over the same files and keep the files as the record — the substrate does
not have to change, and the index stays disposable.

The closed vocabulary rejects captures. An agent that picks a type outside the
list gets an error rather than a coerced page. That is intentional and it is still
friction.

Reconciliation needs a human. `organize` is not automatic, by design, because it
is the step where judgment applies. The mitigation is that search reads the inbox,
so a delayed organize costs tidiness rather than visibility — it behaves more like
a garbage collector than a lock.

Markdown on disk means no transactions and no queries beyond grep and directory
structure. In exchange:

```bash
grep -r "release pipeline" ~/code/wiki
git diff HEAD~1 -- wiki/decision/
wiki audit --stale-days 14
```

Every memory is a file you can read. Every change is a diff you can review. Every
claim has a page you can edit or delete. `wiki audit` finds orphans, broken
wikilinks, unindexed pages, and stale inbox records, and it is read-only.

## What generalizes

The storage was never the hard part. Five ideas carry over to any shared agent
memory, whatever it is built on:

1. **Put the vocabulary at the write boundary.** Reject, do not normalize.
2. **Separate capture from reconciliation.** One writer, an inbox between them.
3. **Make links typed.** A graph you can query beats prose you can search.
4. **Let reads see pending writes.** Visibility now, commitment later.
5. **Store it in something a human can open.** You will need to.

None of this requires a vector database, and the whole thing runs on a filesystem
and a CLI — which means you can try the design this afternoon and find out whether
it survives contact with your agents.

## References

- [herdr-wiki-plugin](https://github.com/Soypete/herdr-wiki-plugin) — the plugin discussed here, MIT licensed
- [Herdr](https://herdr.dev) — the terminal multiplexer it plugs into
- [The LLM-Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Andrej Karpathy
