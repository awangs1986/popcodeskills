## What it does

`cattytest` designs the tests the agent cannot design for itself: the ones that check whether the software did what you *wanted*, not what it *understood*. The feature was "pick the apple off the tree"; the code is clean, the gates are green, the apple is still on the tree. Every gate the agent writes encodes its own understanding of the task, so when the understanding is the bug, every gate passes.

The skill is a grilling session from your side of the screen. One scope question (this feature, or the whole product), a silent read of the ticket, the entry points and the gates that already exist, then rounds along eight branches: the apple (what had to be true in the world afterwards), proxies (how every existing gate can be green while the apple is missing), the walk (what a person actually does, step by step), real data (which user, which record, which numbers), evidence (the artefact you would look at), the ways a real person breaks it, who runs each case, and the line before merge. It ends in a `test-cases.md`: numbered cases in your words, each with steps, data, the apple, the evidence, and whether `verify`, you, or an automated test runs it.

It designs cases. It does not run them (`verify` does), does not write code, and does not touch `tdd`'s gates, which stay the agent's inner loop.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

Type `/cattytest`. It is user-invoked; the agent never starts a case-design interview on its own.

| Your situation | Reach for |
| --- | --- |
| Everything is green and it still doesn't do what you asked | **`/cattytest`**: the proxies round names how, and each way becomes a case |
| A feature is half-built and you don't know how to check it works | **`/cattytest`**, then `verify` on the sheet |
| You want the agent to build a behaviour test-first | [tdd](tdd.md); that's a gate, not a case |
| You want to know whether the gates you have are real | [test-audit](test-audit.md); it judges gates, this skill designs outcomes |
| You have cases and want them walked with evidence | [verify](verify.md); it runs what this skill writes |

## Prerequisites

None hard. A ticket or spec gives it a first draft of the cases; `docs/agents/feedback-loops.md` tells it which cases `verify` can run and which only you can. Without either it still produces the sheet, with more in **Open**.

## Gates and apples

Two kinds of test, two loops, two owners:

| | Gates | Cases |
| --- | --- | --- |
| Written by | The agent, in `tdd` | You, through `cattytest` |
| Check | The code does what the agent understood | The software did what you wanted |
| Pass looks like | Green | The apple in the basket: a file that opens, an email that arrived, a page that shows the right thing |
| Fail is caught by | The suite | `verify`, or you, looking at the evidence |
| Audited by | `test-audit` | Reading the sheet: "can all of these pass and I still don't have what I wanted?" |

A case that turns out to be "this function returns X for Y" is a gate in disguise; the skill hands it to `tdd` and drops it from the sheet. A gate that is the only proof of an outcome goes in the sheet's *Gates that don't count as proof* section, with the apple it can't see.

## Common questions

**Why isn't this just better acceptance criteria?**

It produces them, in executable form, and it usually finds that the ones on the ticket were proxies ("the endpoint returns the rows" instead of "the user sees their notes"). The difference is the interview: the proxies round puts the existing gates next to the outcomes and asks how they can all be green while the outcome is missing. That question is where the cases come from, and nobody asks it of themselves.

**It marked half the cases "by hand". Isn't the point to automate?**

No. The point is to know. `verify` runs what it can observe; anything a human has to judge (arrived in the real inbox, looks right, reads right) stays by hand, and stays on the sheet so it isn't forgotten. Automation is offered only for the two or three cases you'd run on every merge, and only after they've passed once.

**Whole product scope gave me sixty cases.**

And a line. The ranking round says which apples you'd hear about first; the budget round draws the *before merge* line. Sixty is a description of the product; the ones above the line are this week.

## It's working if

- The proxies round names at least one way the current green build could still be wrong, and you recognise it.
- At least one acceptance criterion on the ticket gets rewritten from code words into an outcome.
- `verify` on the sheet fails at least once on a feature you thought was done.
- You stop saying "the tests pass" and start saying "case 3 passed, here's the screenshot".

## Where it fits

Upstream of [verify](verify.md), which walks the sheet's cases with evidence; each FAIL becomes a red test for [tdd](tdd.md), as it does today. Alongside, not inside, [tdd](tdd.md): gates are the agent's loop, cases are yours. Its counterpart on the gate side is [test-audit](test-audit.md). [vibe](vibe.md) routes "green but it doesn't do what I want" here; [ask-matt](ask-matt.md) is the router over the whole set.
