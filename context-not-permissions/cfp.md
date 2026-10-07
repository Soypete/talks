# AgenticCon — CFP Submission

**Event:** AgenticCon, San Francisco
**Submit:** https://agenticcon.com/cfp
**CFP close date:** [Confirm on the site before submitting]

---

## Session Title

Agents Need Context, Not Permissions

## Session Description

When an agent picks the wrong source of truth, misreads a business term, or takes
an action nobody intended, the reflex is to conclude the model is not capable
enough and go shopping for a better one.

But what would more intelligence actually fix? A smarter model still cannot know
that Finance means the billing entity while Product means the person using the
software, unless that distinction exists somewhere the system can reach. It cannot
know that one database is authoritative and another holds stale copies, because
both contain plausible records. It cannot know that a technically valid join
violates a business rule that was never represented anywhere.

We call that gap the Context Void: the distance between the context an agent
receives and the context required to do the task correctly. It is not always
starvation. An agent can sit inside an enormous data estate and still lack the
structure that says which information governs the decision in front of it.

This talk gives you three questions, borrowed from computational linguistics, for
locating the void. Lexicon: what information belongs in this task, and is its
source, authority, and access condition known? Semantics: what does that
information mean, and how do the entities relate? Pragmatics: how may that meaning
be used here, by this person, against this resource?

The "not permissions" half is the practical payoff. Teams usually grant broad
access, discover something alarming, bolt on permissions, find those permissions
block useful work, and widen them again. That loop exists because the scope was
guessed rather than derived. Once you know what information a task requires and who
is asking, the permission boundary falls out of the design instead of being
retrofitted after an incident.

## What attendees will learn

- A diagnostic sequence for agent failures that separates reasoning problems from
  unrepresented-decision problems.
- Why retrieval solves an access problem without solving the interpretation
  problem, and why embedding proximity is not organizational truth.
- Why persistence without authority produces confident stale context, and how
  governed context differs from memory.
- How to test a context fix: add the missing definition, introduce conflicting
  records, remove necessary information, change a semantic relationship.
- Why permission scope should be derived from task context rather than guessed and
  tightened after incidents.

## Key takeaway

The next time an agent is confidently wrong, do not ask which model to swap in. Ask
what it was equipped to understand. If the information was missing, the meaning was
unrepresented, or the rules of use were never stated, you have not found a model
problem.

## Audience level

Intermediate. For engineers building agents against real organizational data. No
specific framework or ontology tooling assumed.

## Speaker

- **Name:** Miriah Peterson
- **Title:** CEO, Haikai Labs
- **Email:** captainnobody1@gmail.com
- **Twitter/X:** @Soypete
- **Website:** https://soypete.tech/

## Speaker bio

Miriah Peterson is CEO of Haikai Labs, where she is building a Sovereign Context
Layer for reliable AI. An engineer and educator focused on data engineering and AI
infrastructure, she has built production systems at SchoolAI, Agility Ads, Weave,
Tailscale, MX, and Nav. She created SoyPete Tech, teaches for Boot.dev and
O'Reilly, and hosts the Domesticating AI podcast.

## Notes for reviewers

Vendor-neutral. The framework is presented as an architectural pattern, with
published research cited throughout (RAG, Lost in the Middle, RULER, NoLiMa, ReAct,
CLAM). Haikai Labs' work informs the framing but there is no product demonstration.

## Related writing

- *Escaping the Context Void: Why Your Agents Suck and How to Make Them Better*
- *The Context Engineering Manifesto*
- *Your Context Window Is Not Your Effective Context Window*
