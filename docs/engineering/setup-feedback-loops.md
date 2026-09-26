## What it does

`setup-feedback-loops` wires the checks every other skill spends and nobody else installs: a typecheck, a linter, a test runner with a fast single-file invocation, a formatter in check mode, a smoke test, dev-server logs the agent can read, a headless browser for web apps, and a pre-commit guardrail. It audits what the repo already has, proposes the gaps in one table, wires them with the stack's conventional defaults, and writes the exact commands and their timings to `docs/agents/feedback-loops.md`, where `implement`, `tdd`, `diagnosing-bugs` and `verify` read them.

It refuses to call a loop wired until it has seen it go red. Every check gets a deliberate fault introduced, the red output shown, the fault reverted, and the green shown again. A present-but-silent check (a test script that finds zero tests, a typecheck with `strict` off) is treated as worse than a missing one, because the agent trusts it.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

You invoke this by typing `/setup-feedback-loops`; the agent won't reach for it on its own.

| Your situation | Do |
| --- | --- |
| A fresh repo, right after `/setup-matt-pocock-skills` | Run it before the first feature. The wiring commit lands ahead of any code |
| An existing project where `tdd` keeps stalling on "no test runner" or `implement` never runs a typecheck | Run it; the audit table will say which loops are missing or silent |
| The stack changed (new framework, added a web front end to a CLI) | Run it again, naming the loop: `/setup-feedback-loops browser` |
| You want to tune lint rules | Not this. Rules accrete through review; this installs defaults and moves on |

## Prerequisites

None. It detects the stack from the lockfile and existing scripts. On Node it borrows the `setup-pre-commit` shape for the guardrail.

## Red before green

The skill's word is **prove red**. A green run says nothing about whether a check can catch anything; only a red run does. That is why the process has a whole step where the agent breaks each loop on purpose, and why `docs/agents/feedback-loops.md` opens with the line that every command listed there has been seen failing.

The other thing it insists on is **speed**. A two-second typecheck the agent runs after every edit is worth more than a three-minute one it learns to skip, so the file records durations, and a slow suite gets a note and the fastest single-file command the agent could find, because that is what `tdd` actually runs.

## Common questions

**Why isn't this part of `setup-matt-pocock-skills`?**

Different concerns and different lifetimes. `setup-matt-pocock-skills` configures where issues and domain docs live and is a one-time answer. Feedback loops depend on the stack and change with it, and proving them red is a real session of work rather than three questions. Keeping them apart also means an existing repo with a tracker already configured can add loops without re-answering the tracker questions.

**It wants to turn `strict` on and that surfaces forty errors.**

That is the audit working. The recommendation is still on, fixed in one commit before feature work, because every future `tdd` cycle will lean on the typecheck and a lenient one lets the agent ship what it should have caught. If forty is genuinely too many today, the honest fallback is `strict` on with a short, listed set of file-level exceptions, never `strict` off.

## It's working if

- `docs/agents/feedback-loops.md` exists, and every command in it has a duration beside it.
- You saw each loop go red in the transcript before it was declared done.
- `tdd` sessions afterwards run a single test file in seconds rather than the whole suite.
- A commit with a failing test is rejected by the hook rather than discovered later.

## Where it fits

A **run-once setup**, second in the sequence after [setup-matt-pocock-skills](setup-matt-pocock-skills.md) and before any Build or Fix work, re-run when the stack changes. [tdd](tdd.md), [implement](implement.md), [diagnosing-bugs](diagnosing-bugs.md) and [verify](verify.md) all read the file it writes. [ask-matt](ask-matt.md) is the router over the whole set.
