## What it does

`verify` starts the thing that was just built and walks its acceptance criteria and user stories the way a user would: a headless browser for a web UI, `curl` for an API, the command itself for a CLI, a direct trigger for a job. Each criterion comes back as PASS, FAIL or UNVERIFIABLE with a piece of **evidence** attached: a screenshot, a captured response, a transcript. It also tries one obvious wrong path per criterion (empty input, the second click, someone else's record) to catch a happy-path-only implementation.

It observes and does not fix. A FAIL is handed back to whoever called it, usually `implement`, which turns it into the next red test. "The tests pass" is not treated as evidence that the feature works; only something the skill saw is.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

Type `/verify`, or the agent reaches for it automatically when a task fits. `implement` calls it after the suite goes green and before `code-review`; you can also say "does it actually work", "try it", or "show me" at any point.

| Your situation | Reach for |
| --- | --- |
| Work is claimed done and you want to see it work, not hear that it does | **`verify`** |
| You want the logic at a seam proven | [tdd](tdd.md); `verify` goes through the interface, never the code |
| You want the diff judged against standards and the spec | [code-review](code-review.md), which reads the diff and never boots the app |
| It failed and you don't know why | [diagnosing-bugs](diagnosing-bugs.md), handed the repro `verify` just ran |

## Prerequisites

It boots the app the way `docs/agents/feedback-loops.md` says, and drives a web UI with whatever browser that file names. Without the file it falls back to the package scripts and says so; [setup-feedback-loops](setup-feedback-loops.md) is what writes it. It needs the acceptance criteria to walk: the ticket or spec, in context or passed in.

## Evidence

The skill's word is **evidence**, and it means a file: a screenshot per step, the captured body, the stdout and exit code, saved under a `verify-<timestamp>/` directory in the temp dir and linked from the report. A description of a screenshot is not one. The third verdict, **UNVERIFIABLE**, exists so the agent has an honest thing to say when the only way to check would be to read the implementation or to use credentials it doesn't have; "probably works" is not on the list.

## Common questions

**How is this different from the old `qa` skill?**

`qa` turned the findings of a testing session into tickets and was absorbed into [triage](triage.md) and [to-tickets](to-tickets.md). `verify` is the testing session itself, scoped to one ticket's criteria, run by the agent, with evidence per row. Its FAILs go to `tdd` rather than to the tracker.

**Doesn't this make every ticket slower?**

By a few minutes, spent booting and clicking. It replaces the minutes you spent doing the same thing by hand after the agent said "done", and the hour you spent when you didn't.

**It said UNVERIFIABLE for half the rows.**

Usually one of two things. The app needs something the agent can't reach (a login, a third-party account, production data), which is a question for you and the report names it. Or the criteria are written in terms of internals rather than behaviour, which is a spec problem: a criterion `verify` can't check through the interface is one a user can't either.

## It's working if

- Every row in the report has a path to a file, and opening the file shows what the row claims.
- The wrong-path column catches something at least occasionally: a 500 on empty input, a second submit creating a duplicate.
- `implement` sessions end with a screenshot you can look at rather than a sentence you have to trust.

## Where it fits

A **chain step** inside [implement](implement.md) (`tdd` → `verify` → `code-review` → commit) that also works as a reach-for-it-anytime standalone. It is the bridge between the spec's user stories and the running application that [tdd](tdd.md) and [code-review](code-review.md) both stop short of. [ask-matt](ask-matt.md) is the router over the whole set.
