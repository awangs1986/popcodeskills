## What it does

`test-audit` answers a question `tdd` cannot answer about itself: do these green tests protect the business logic, or do they just pass? It reads every test behind a change and does three things. It translates each test into a one-sentence **claim** in the project's own vocabulary ("a highlight reviewed today is not due again tomorrow") so the domain expert can read the suite as a list of business rules and spot the wrong one. It maps those claims to the acceptance criteria and user stories in both directions, so uncovered rules and untested wrong paths show up as rows. And it runs a **mutation probe**: it breaks the logic on purpose, one site at a time (`<=` to `<`, a removed early return, a dropped normalisation), runs the tests, and records whether anything died. A mutant that survives is a rule no test protects.

It audits and does not fix. Every gap becomes a named red test handed back to `tdd`. The claims list is left in the transcript for a human to read; a claim the human marks wrong is the finding that matters most, because it is the error a green suite would have carried into production.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

Type `/test-audit`, or the agent reaches for it automatically when a task fits. `implement` calls it after `verify` and before `code-review`.

| Your situation | Reach for |
| --- | --- |
| You use `tdd` and don't know what the tests actually check | **`test-audit`**: read the claims |
| Green suites keep hiding logic errors you find weeks later | **`test-audit`** on the feature before merge; the survivors and the wrong claims are where those errors live |
| You want to write the tests | [tdd](tdd.md); this skill only judges the ones that exist |
| You want the feature seen working end to end | [verify](verify.md); that one drives the app, this one interrogates the suite |
| You want full mutation testing with a score | A tool (`stryker`, `mutmut`, `cargo-mutants`) via [setup-feedback-loops](setup-feedback-loops.md). This is a ten-to-fifteen-mutant probe aimed at business weight, not a run |

## Prerequisites

A fast single-file test command, which it reads from `docs/agents/feedback-loops.md`; the probe runs it once per mutant and time-boxes itself by the duration listed there. It needs the ticket's criteria or the spec's user stories to map claims against.

## Two kinds of false green

The reason the skill has both a claims list and a mutation probe is that green tests hide logic errors in two different ways, and each check catches one:

| False green | What it looks like | Caught by |
| --- | --- | --- |
| **The test doesn't constrain the code** | Break the rule; the test stays green. Tautological assertions, mocked seams, `toBeTruthy()` on the load-bearing line | The mutation probe, mechanically |
| **The test constrains the wrong rule** | Test and code encode the same misunderstanding. Both green, both wrong | The claims list, read by a human. No tool finds this |

The second is the one that surfaces weeks later, and it is why the claims are written for the user rather than for the agent: if a claim needs a variable name to make sense, the skill rewrites it.

## Common questions

**Isn't this what `code-review` does?**

`code-review` reads the diff for standards and for fidelity to the spec, and treats test files as more code. It doesn't run mutants, and it doesn't render the suite as rules for a human. The two are adjacent in the `implement` chain on purpose: this one first, so its red tests are written before review sees the branch.

**The probe said everything was killed. Is it lying to look good?**

"All killed, all covered" is a permitted verdict and the skill is told not to invent survivors. Check the claims list instead: the second kind of false green passes every mutant.

**It left a broken line in my code.**

It shouldn't: the discipline is apply, run, revert, `git diff` clean, next mutant, and a clean tree at the end. If it happened, the file to check is the one the last mutant row names, and `git checkout` that file. Report it; that is a bug in the skill's discipline, not an accepted outcome.

## It's working if

- You can read the claims list without opening a test file and say "number 3 is wrong" when it is.
- At least occasionally a mutant survives on a rule you cared about, and the next `tdd` cycle kills it.
- The **Checks run** block at the end of `implement` shows the claim count and survivor count, so you know what was checked rather than trusting that it was.
- The logic errors you find in production get rarer, and the ones you do find trace to a claim that was wrong rather than to a rule nobody tested.

## Where it fits

A **chain step** inside [implement](implement.md) (`tdd` → `verify` → `test-audit` → `code-review` → commit), also run standalone across a whole feature before merge. It closes the loop `tdd` opens: [tdd](tdd.md) writes tests at agreed seams; this skill checks that what got written constrains the logic and says something the domain expert recognises. [ask-matt](ask-matt.md) is the router over the whole set.
