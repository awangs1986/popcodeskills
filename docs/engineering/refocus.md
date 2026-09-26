## What it does

`refocus` is for the long [session](https://www.aihero.dev/ai-coding-dictionary/session) where the agent has started to drift: it forgets a decision you made an hour ago, quietly widens the scope, or works on the wrong criterion. You type it, and the agent re-reads the requirements from their [primary sources](https://www.aihero.dev/ai-coding-dictionary/primary-source) on disk (the spec or ticket, `CONTEXT.md`, the ADRs in the area), scrolls back for every decision you made in the conversation that never reached a file, diffs all of that against what has actually been built, and hands back a one-screen brief: goal, binding decisions, done, remaining, **drift** (dropped, drifted, contradicted, leftovers), next step. Where the sources leave something genuinely ambiguous (a criterion the diff could satisfy two ways, a spec line and a mid-session decision that disagree, an unrequested change it can't tell whether to keep), it doesn't guess: it asks **one round** of numbered questions, each with a recommended answer, and writes your answers back to the spec or ticket so they survive the session. Then it stops until you confirm.

It reads files rather than recalling them. The requirements sit at the start of the [context window](https://www.aihero.dev/ai-coding-dictionary/context-window), where attention is weakest by the time you need this; the code just written sits at the end, where attention is strongest. Re-reading moves the requirements to the end. That mechanism is why the skill forbids summarising from memory: memory is what drifted.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

You invoke this by typing `/refocus`; the agent won't reach for it on its own.

| Your situation | Reach for |
| --- | --- |
| Long session, the agent seems to have lost the thread, and you want to stay in this window | **`/refocus`** |
| One message didn't land and you want it re-explained | [wait-what](../productivity/wait-what.md) |
| The work is moving to another directory, harness, or person | [handoff](../productivity/handoff.md) |
| The window is nearly full and you need to compress | `/compact`, seeded with the brief `refocus` just wrote |
| You want the diff judged against standards and spec | [code-review](code-review.md). `refocus` checks *alignment mid-build*; `code-review` checks *quality at the end* |

## Prerequisites

Nothing to install. It is sharpest when there is a spec or ticket on disk to anchor on ([to-spec](to-spec.md), [to-tickets](to-tickets.md)) and a `CONTEXT.md` to speak in; without them the conversation is the only primary source, and the brief says so.

## Drift

The word the skill gives you is **drift**, in three kinds, each answered by pointing at a source line and a diff hunk:

| Kind | Meaning |
| --- | --- |
| **Dropped** | A criterion or a decision you made in conversation with nothing in the diff and nothing in the remaining work |
| **Drifted** | Something in the diff no source asked for: scope creep, an unrequested refactor, speculative generality |
| **Contradicted** | A hunk that goes against a decision, an ADR, or an out-of-scope line |

The conversation-only decisions ("don't touch the auth module") are the ones to watch. They exist nowhere but the context, which is exactly what a long session degrades and a `/compact` flattens, so the brief quotes each one rather than paraphrasing it.

## One round, then escalate

The questions are bounded on purpose: at most five, one round, only what blocks the next step or would change a drift verdict. Anything the agent could settle by reading more of the repo is not allowed to become a question. Each carries a recommended answer, so the usual reply is a word per question.

| What comes back | What happens to it |
| --- | --- |
| An answer that clarifies a criterion | Appended to the spec or ticket (local `## Comments`, or a GitHub issue comment) |
| An answer that sharpens a term | Written into `CONTEXT.md` |
| A hard-to-reverse choice | Offered as an ADR |
| A second round of questions, or a source that turns out to be wrong | Not handled here. The brief says the spec is under-specified and points you at [grill-with-docs](grill-with-docs.md) and [to-spec](to-spec.md) |

## Common questions

**Isn't this just `/compact`?**

No, and the order matters. `/compact` is lossy: it summarises the session, and a decision it judged minor is gone. `refocus` re-reads the sources, so nothing is summarised, and it produces the brief a compact should be seeded with. If you are going to compact, refocus first and hand the compact the brief's path.

**Why does it make me confirm before continuing?**

Because a correction you make to the brief is the highest-value line in the session: it is a binding decision, stated at the end of the window where the agent will actually honour it. Resuming without that step would put the agent back on the same drifted course with a nicer summary.

**How is the question round different from `grill-with-docs`?**

Scope. `grill-with-docs` interviews until every branch of a design is settled and is where a spec comes from. The round here is a repair to an existing spec: a handful of questions about the specific places the diff and the sources disagree, each with a recommended answer. If it can't be done in one round, that is the signal the spec needs the full interview again, and the skill says so rather than becoming one.

**Can the agent run it on its own when it notices it is drifting?**

It doesn't notice. Drift is invisible from inside; you see it, so you fire it. That is why it is user-invoked.

## It's working if

- The brief fits on one screen and every **Drift** line points at a specific hunk and a specific source line.
- At least once, it surfaces a decision you made mid-session that you had assumed the agent still held.
- The questions it asks are ones you actually have to think about; a question you could have answered with "read the file" means it skipped step one.
- Your answers show up in the spec's comments afterwards, so the next session doesn't ask them again.
- After you confirm, the next thing the agent does is the **Next** line, not the thing it was doing before you typed `/refocus`.
- Your `/compact` instructions get shorter, because you paste the brief's path instead of re-explaining the feature.

## Where it fits

A **reach-for-it-anytime standalone** inside a build: the mid-phase corrective the [phase boundary](ask-matt.md) tree doesn't otherwise have. It sits beside [wait-what](../productivity/wait-what.md) (that one re-pitches a single message; this one re-anchors the whole session) and ahead of [handoff](../productivity/handoff.md) and `/compact` (both of which it can seed). [ask-matt](ask-matt.md) is the router over the whole set.
