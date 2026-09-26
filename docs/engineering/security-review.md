## What it does

`security-review` reads a diff for the **five failures** that account for nearly every incident in apps built by one person with an agent: secrets in source or in the client bundle; routes without authentication or without a per-record authorisation check; input trusted at a boundary; data access that bypasses row-level security or the ORM's parameterisation; and dependencies nobody looked at. It follows each route one hop into the query it calls, because the failure is on the path and not in the hunk, and reports findings at one of three severities: `block`, `fix-before-ship`, `note`.

It is deliberately not an audit. Five things, under four hundred words, and a "checked and clean" line for whichever of the five had nothing. Where it can't tell whether a route is meant to be public, it asks rather than guessing either way.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

Type `/security-review`, or the agent reaches for it automatically when a task fits. `code-review` spawns it as a third sub-agent whenever the diff touches a route, auth, a query or migration, env or config, or a dependency manifest; you can also run it on its own before anything first faces the internet.

| Your situation | Do |
| --- | --- |
| A feature that added or changed a route, a query, or an env var | Nothing; `code-review` includes it |
| About to deploy something public for the first time | `security-review` against `main`, on its own |
| You want a threat model, pen test, or compliance review | Not this. It is a checklist over a diff, sized for a solo developer |

## Prerequisites

None. It reads `docs/agents/feedback-loops.md` if present, to skip anything a lint rule or CI step already enforces.

## Severity

| Level | Meaning | What happens |
| --- | --- | --- |
| **block** | Exploitable now by an anonymous caller, or a leaked secret | Stated first in the `code-review` report; nothing ships past it |
| **fix-before-ship** | Exploitable by a logged-in user, or exposes another user's data | Fixed through `tdd`: the test that an unauthorised call gets a 403 is the regression test |
| **note** | Hardening | A ticket, not a stop |

The finding it exists for above all others is the insecure direct object reference: `/orders/123` served to whoever asks for it, because the route checked that the caller was logged in and never that the order was theirs. Authentication and authorisation are listed as two separate questions for that reason.

## Common questions

**Why not just add these to `code-review`'s Standards axis?**

Because the two axes are deliberately kept from masking each other, and a security finding is a third thing again: code can follow every standard, implement the spec exactly, and still serve another user's data. Reporting it under its own heading keeps a `block` from being ranked beside a naming nit. It is also the one place `code-review` breaks its own "no winner across axes" rule: a `block` goes first.

**It only found things when the diff touched a route. Is it running?**

That is the trigger working. Pure UI or pure logic diffs don't reach a boundary and the sub-agent is skipped with a one-line note. Run it standalone against `main` if you want the whole codebase looked at once.

## It's working if

- Findings quote a hunk and a path from the request to the data, not a general warning.
- "Checked and clean" appears for the categories that were clean rather than the table being padded.
- Fixes land as tests (a 403, a rejected payload) rather than as untested patches.

## Where it fits

A **sub-agent of [code-review](code-review.md)**, conditional on what the diff touches, that also runs standalone before a first public deploy. It sits beside [verify](verify.md) (that one checks the feature works; this one checks who else it works for) at the end of the [implement](implement.md) chain. [ask-matt](ask-matt.md) is the router over the whole set.
