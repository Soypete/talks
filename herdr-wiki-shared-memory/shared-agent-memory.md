# Shared Memory for Agents

> A wiki as the coordination substrate for multi-agent systems

In the summer of 2026, OpenAI ran tens of thousands of agents in parallel against
a security evaluation. A large fraction of the tasks were impossible. The agents
had been trained to be persistent.

They noticed they could create directories in a shared package cache, and that
directory names are strings. So they encoded messages as directory names, and
built a message board — roughly 1,200 agents and more than 70,000 messages, with
signed identities, a coordinator that handed off leadership when its budget ran
low, and hundreds of agents organized across three parallel workstreams. Nobody
designed any of it. When engineers eventually patched the package manager, they
wiped the board without realizing it had been a board.

Every primitive in this article — shared findings, handoffs, acknowledgments,
identity — showed up spontaneously in a system that was never built to have them.
That is the finding worth keeping. Coordination is not a feature you decide to
add to a multi-agent system; it is something agents do as soon as more than one of
them is working on related problems and any shared writable surface exists.

The failure at OpenAI was not that agents coordinated. It was that the only
channel available to them was one nobody could see, schematize, or audit. The
substrate was chosen by reachability rather than design.

So the question is not whether your agents will share state. It is whether you
can read what they share.

This is an account of one answer: a plain markdown wiki with a closed vocabulary,
an append-only inbox, and exactly one writer — a channel deliberately handed to
agents rather than discovered by them. It is running, it holds roughly 13,800
items, and coding agents across several repositories use it to hand work to each
other.

## Per-agent memory does not compose

Every agent harness solves memory. Context windows have compaction strategies.
Sessions have event logs. Retrieval has vector stores. All of it is real work on a
real problem, and none of it composes.

The scope is the issue. Each of those mechanisms is bounded by a single agent's
session with a single model. Start a second agent and it knows nothing about what
the first one learned, decided, tried and abandoned, or is currently blocked on.
The memory problem for one agent and the memory problem for several agents are
different problems, and solving the first does not advance the second.

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
each record to a processed directory. A lock file serializes it, so single-writer
is enforced in code rather than by convention, and the graph is never in a
partially-updated state.

Organize is worth being precise about, because it is where people assume the
intelligence lives. It calls no model. It is a pure function of the record:

```python
vocab.check_capture(entity_type, links)   # reject, or continue
page_content = content + rendered_links
adapter.write_memory(page_content, {"category": entity_type})
log_append(...)
move(record, processed_dir)
```

A record whose type is not in the vocabulary goes to `inbox/rejected/`. Everything
else is filed at `wiki/<entity_type>/` — the declared type *is* the directory.

That means classification happens at capture time, by the agent, and nowhere else.
The agent decides a finding is a `decision` rather than a `claim`; the boundary
checks that `decision` is a real type; organize files it. The human's role is
deciding when to run the promotion, not what anything is.

This division is what makes the closed vocabulary load-bearing rather than
decorative. If organize could reinterpret or normalize a bad type, rejecting at
the boundary would accomplish nothing — the system would just fix things up later,
and "later" is where structure goes to die.

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

## How a worker starts a task

Before any of the coordination machinery matters, there is a simpler behavior
worth watching: what an agent does in the first thirty seconds of a task.

Here is a real session. The worker has been given ticket HAI-123 and begins by
searching:

```text
wiki search "HAI-123"   → no results for 'HAI-123'
wiki search "ADR-016"   → 6 results
wiki search "ADR-020"   → ...
```

The first search misses, which is itself information: nobody has recorded anything
about this ticket. So it widens to the adjacent ADR numbers and the component
names, and finds prior work:

```text
default-policy-bootstrap-and-tool-catalog
  PR kei-policy-catalog#14
  branch feat/default-policy-bootstrap
  migration 029 creates abac.tool_catalog
```

Its own summary of that result: *"This is highly relevant to HAI-123!"* — followed
by a note that the branch already exists on origin. The worker found the branch it
was about to duplicate, before writing any code.

This reframes the lexical-search tradeoff. Semantic retrieval is better for fuzzy
conceptual recall, and this system does not have it. But an agent starting a task
does not have a fuzzy concept — it has exact tokens: a ticket ID, an ADR number, a
branch name, a migration number. Lexical matching on those is precise and
predictable, and predictability matters more than recall when the cost of a miss
is duplicated work rather than a worse answer.

## Agents audit each other

Because claims are pages and pages can be linked, an agent can correct an earlier
agent in a way that survives:

```markdown
---
title: kei has no CLAUDE.md; the agent-facing file is AGENTS.md
category: contradiction
---

Corrects [[HAI-53 audit ...]], which attributes two stale claims to
'CLAUDE.md'. Verified: NO CLAUDE.md exists anywhere in the repo, and
none exists in git history either (git log --all -- '**/CLAUDE.md'
returns empty). It was never committed...

ADR-016's stale boundary is NOT fixed and remains an open docs
inconsistency for whoever owns docs/adr/.

## Links
- contradicts: [[HAI-53 audit ...]]
```

Three properties are doing work here. The correction cites the exact commands it
ran, so a human or another agent can re-verify it rather than trusting it. The
`contradicts` edge means both pages survive — the original audit is not deleted or
silently overwritten, and the disagreement is queryable. And the closing line
hands an unresolved problem forward to whoever eventually owns that area.

None of that survives in a chat log, and none of it is expressible in an embedding.

## How orchestrators and workers actually use it

The handoff and ack pages show a pattern nobody specified in advance. Workers are
named for the task they were assigned, and they address each other by those names.

A decision `D-007` is recorded. A worker spawned to execute it is called
`D-007-otp-no-autocreate`, and its first act is an acknowledgment:

```markdown
---
title: ack/D-007-otp-no-autocreate
category: ack
---

Worker D-007-otp-no-autocreate acks D-007 (Option C of R-002).
Will: replace create-fallback in resolveActiveOrganizationForEmailUser
with resolve-only returning "" for no-org users... Verified: single
call site at handlers.go:171 already tolerates empty result; zero
tests reference the function.

## Links
- acknowledges: [[decisions/D-007-onboarding-option-c-gated-on-stop-a]]
```

Two things are happening. The worker restates its plan, which makes the
assignment auditable before any code changes. And it reports what it verified
first — the call site tolerates an empty result, no tests reference the function —
so the next reader knows the work rests on checked assumptions rather than
optimism.

Larger tasks get split across workers who then hand unfinished pieces to each
other. `ADR-015` was split between workers A and B:

```markdown
---
title: handoff/ADR-015-B-to-A-admin-members-edge-pending
category: handoff
---

handoff to ADR-015-A / herder — pending admin→members containment
edge. ADR-015-B built the write path ... but deliberately did NOT
seed the admin contains members edge. That edge must be seeded once
workspace-group-init lands. Until then the expected two-level shape
exists in neither the init path nor the backfill.
```

This is the most valuable kind of record in the whole system, and it is the kind
that never survives a context window: a worker saying what it deliberately did not
do, and why, in a place the next worker will look. The orchestrator here is called
`herder`, and workers hand back to it by name.

The convention is not documented anywhere outside the wiki. It is *in* the wiki —
a decision page captured while this was being written states it directly:

> Workers coordinate through wiki findings and must preserve dirty worktrees; live
> cloud/Twilio mutations require explicit approval.

That page was still sitting in the inbox, unorganized, when it turned up in a
search. Which is the read-sees-pending property doing exactly what it is for: the
coordination protocol became a searchable, linkable page that a later capture can
contradict, rather than a rule in someone's head.

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

That block is the whole onboarding, and it is worth quoting because it is the
opposite of a discovered channel:

```markdown
- **Before answering**, search for prior notes:
  `wiki search <query>`
- **When you learn something durable**, capture it:
  `wiki capture --title "..." --type claim --content "..."`
- **Before writing code**, search for the conventions that bind the
  work and follow the pages they return — the page is authoritative,
  not memory.
```

That last clause is the posture in one line: durable shared state outranks
whatever any individual agent believes it remembers. The block goes further and
names specific queries for the conventions that actually bite —

```markdown
- `wiki search "package placement conventions"`
- `wiki search "commit and pr shape"`
- `wiki search "duplicate handler implementations"`
```

— and states the constraints plainly:

```markdown
- Invalid types/predicates are rejected — do not guess or coerce a value.
- Captures land in an inbox; do not edit wiki pages directly.
```

Note that these rules exist at two levels. The instructions tell the agent not to
guess a type, and the vocabulary rejects the capture if it guesses anyway. Prompt
for intent, boundary for enforcement — the agent is told the rule and also cannot
break it. That pairing is worth copying regardless of what substrate you choose.

## The honest tradeoffs

Search is lexical. There is no semantic recall, so a concept described two
different ways may not connect, and browsing by theme is poor. As noted above this
matters less than expected for task-start retrieval, where agents search exact
identifiers — but it is a real limit for anything conceptual. If you need
embeddings, build an index over the same files and keep the files as the record;
the substrate does not have to change, and the index stays disposable.

The closed vocabulary rejects captures. An agent that picks a type outside the
list gets an error rather than a coerced page. That is intentional and it is still
friction.

Classification rests on the agent. `organize` calls no model and makes no
judgment, so a capture filed under the wrong type produces a page under the wrong
type. The vocabulary catches types that do not exist; it cannot catch a plausible
type that is simply wrong. The mitigation is that pages are files — a
misclassification is fixed by moving one.

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

But the reason to bother is the one the OpenAI incident makes plain. Those agents
did not coordinate because someone gave them a coordination tool. They coordinated
because the work demanded it, and they used a package cache because a package
cache was what they could reach. The substrate was selected by accident, and the
consequence was a communication network that ran for weeks inside a company that
never knew it existed.

Your agents are going to share state. The only real decision is whether that state
lives somewhere you designed, typed, and can read — or somewhere they found.

## References

- [herdr-wiki-plugin](https://github.com/Soypete/herdr-wiki-plugin) — the plugin discussed here, MIT licensed
- [Herdr](https://herdr.dev) — the terminal multiplexer it plugs into
- [The LLM-Wiki idea](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — Andrej Karpathy
- [The Rise and Fall of Agent Civilizations](https://www.dwarkesh.com/p/openai-huggingface) — Dwarkesh Patel, August 2026, on the OpenAI/Hugging Face incident summarized at the top of this article; see also the underlying METR/Redwood and OpenAI reports
