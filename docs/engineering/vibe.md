## What it does

`vibe` is a dispatcher for one developer working alone. You tell it what you are trying to do (or nothing, and it asks), and it hands back a **route card**: which of four lanes you are on (Build, Fix, Review, Tidy), how big the work is, the exact next command to type, the two or three steps after that, and what to do with your [context](https://www.aihero.dev/ai-coding-dictionary/context) between them.

It gives a short, considerate explanation and a route card, then stops. It does not tell the product story, grill, write a [spec](https://www.aihero.dev/ai-coding-dictionary/spec), or start coding; where a lane's first step is a model-invoked skill (`tdd`, `diagnosing-bugs`, `code-review`) it offers to fire that one on a "go", and otherwise you type what the card names.

It is a curated subset, not the full map. The kit is twenty-six skills chosen for solo work; `wayfinder`, `triage`, `to-questionnaire` and the rest are named as deliberately out, each with the moment to bring it back. The full map stays [ask-matt](ask-matt.md).

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

You invoke this by typing `/vibe`; the agent won't reach for it on its own.

| Your situation | What the card gives back |
| --- | --- |
| You can picture using the product but cannot write its requirements, or want to hear a user journey from the workspace | [tell-a-story](./tell-a-story.md), before setup or sizing if needed; the card names it and stops |
| You want a guide to the commands you have | [askcat](../productivity/askcat.md), without a setup detour |
| You need proof cases, running evidence, or an audit of existing tests | [cattytest](./cattytest.md), [verify](./verify.md), or [test-audit](./test-audit.md), selected by what is missing rather than overlapping keywords |
| A library or API fact needs checking | [research](./research.md), which is part of the solo kit |
| An idea, and you don't want to think about process | Build lane, sized S, M or L: just say it, grill then implement, or grill → spec → tickets → implement per ticket |
| Something broke, flaky, or slow | Fix lane, split on whether you already know the cause: `tdd` straight in, or the gated `diagnosing-bugs` loop |
| A branch you want checked | `/code-review main`, and what to do with each axis of findings |
| The codebase feels harder to change than it should | `/improve-codebase-architecture`, and how the idea it produces goes back onto Build |
| You've asked for the same change three times and it's still wrong | Not a fifth attempt. Discard, clear, write one input / expected / actual example; whether you can write it picks the lane |
| The session drifted, is about to move, or died on you | One of the three seam moves: [refocus](refocus.md) to stay, [handoff](../productivity/handoff.md) to leave on purpose, [takeover](../productivity/takeover.md) in the new window when the old one is gone |
| A grill question only running code can settle | The prototype detour: `/handoff` the question, [prototype](prototype.md) in a fresh session, the decision comes back to the grill |
| A greenfield product with decisions spanning several sessions | [wayfinder](./wayfinder.md), with story alignment first if the destination is still unclear |
| A team or outside stakeholders | [ask-matt](./ask-matt.md), the broader map |

## Prerequisites

Building and publishing work assume [setup-matt-pocock-skills](setup-matt-pocock-skills.md) has configured the tracker. Stories, the Askcat guide, clarifications, and session care are routed before setup checks. Evidence and research skills retain their own prerequisites instead of acquiring a tracker dependency from the router. An explicit command wins over a generic setup suggestion.

For other requests, a repo with no tracker, feedback-loop record, or glossary gets the first-run card. A missing tracker in an otherwise configured repo routes to setup. Local markdown is the solo default; GitHub works the same way with issues in place of files.

## Nothing silently falls off the map

The dispatcher has an explicit coverage table for every promoted skill: in the daily kit, a situational detour, or outside the kit with a named route. The repository check compares that table with the actual skill directories and invocation metadata. A new promoted skill with no guidance fails the check.

User-invoked commands remain yours to type. A missing entry in the model's automatic-skill list is not enough to call one uninstalled; the dispatcher checks accessible files or a manifest. Beta skills remain opt-in rather than being mistaken for shipped commands.

## Lanes and size

The word to think with is **lane**. You are always in exactly one, and each has one decision inside it:

| Lane | The one decision | Why it matters |
| --- | --- | --- |
| **Build** | Align the product first if needed, then size: S, M or L | Size decides how much ceremony you pay. S is a sentence; M is a grill and an implement in one window; L is grill, spec, tickets, and a fresh window per ticket |
| **Fix** | Do you know the cause? | Yes goes straight to a failing test. No goes to a loop that refuses to theorise until one command goes red on the bug |
| **Review** | None | Two axes, Standards and Spec, never merged into one score |
| **Tidy** | Which candidate | The survey produces an idea; the idea goes back onto Build |

The sizing question is asked in order and the first yes wins: can you write it as one sentence with no open questions (S); does it fit one sitting but you have questions first (M); neither (L). Most solo work is S or M, and the card recommends against L until you have caught yourself re-explaining a decision in a second session.

## Common questions

**How is this different from `ask-matt`?**

`ask-matt` is the map of everything, written as prose so it can carry the branches. `vibe` is a fixed subset with the branches pre-decided for one person working alone, and it hands back a fill-in-the-blanks card rather than a paragraph. If your situation involves other people (incoming bug reports, a stakeholder, a colleague picking up the work) you have left the subset, and it says so.

**Can I skip it and just type the skills?**

Yes, and after a week you will. The card exists for the first few sessions, and for the moments where you have a bug and can't tell whether it is a `tdd` bug or a `diagnosing-bugs` bug. The cheatsheet at the bottom of the skill's `WORKFLOW.md` is the same information as a table, and [the poster](https://github.com/awangs1986/popcodeskills/blob/main/docs/engineering/vibe-workflow-poster.png) is the same information as one picture.

**It offered to start `tdd` for me. Is that safe?**

It only fires model-invoked skills, and only after you say go. Every user-invoked step (`tell-a-story`, `grill-with-docs`, `to-spec`, `to-tickets`, `implement`, `improve-codebase-architecture`, `refocus`, `handoff`, `takeover`) stays yours to type; no skill in this repo can fire those for you.

## It's working if

- A warm, brief explanation leads to one next command, then the router stops instead of starting the work.
- When the product picture is missing, the next step is a story rather than a premature size or a setup questionnaire.
- Sizing lands on S or M most of the time, and you can say why the occasional L earned its spec.
- After an L build you notice you are no longer re-explaining decisions between sessions: they are in `CONTEXT.md`, an ADR, or the spec.
- A hard bug's fix commit names the hypothesis that turned out right, because the Fix lane went through the loop rather than around it.

## Where it fits

A **run-first dispatcher**: the thing you type when you don't yet know which chain step you're at. It offers [tell-a-story](./tell-a-story.md) when the product experience needs aligning, then hands off to the main chain ([grill-with-docs](grill-with-docs.md) → [to-spec](to-spec.md) → [to-tickets](to-tickets.md) → [implement](implement.md) → [code-review](code-review.md)) at whichever step the size calls for, to [diagnosing-bugs](diagnosing-bugs.md) for a hard bug, and to [improve-codebase-architecture](improve-codebase-architecture.md) for upkeep. [ask-matt](ask-matt.md) remains the router over the whole set, because it covers the situations this one deliberately leaves out.
