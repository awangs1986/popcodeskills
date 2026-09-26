---
name: cattytest
description: "Design the test cases that prove the software does what the user actually wanted, from the user's side of the screen: what they do, with what, and what must be true in the world afterwards. Not the agent's own gates. A grilling session that ends in a test-cases sheet verify can walk and the user can run by hand. Use when the user says \"the tests are green but it doesn't do what I want\", \"how do I know it really works\", \"help me design test cases\", or when a half-built feature has gates and no proof."
disable-model-invocation: true
argument-hint: "A feature, ticket, or nothing to be asked what to design cases for"
---

# Cattytest

The feature was "pick the apple off the tree". The code is clean, the typecheck passes, the unit tests are green, and the apple is still on the tree. This happens constantly, and no gate the agent writes for itself can catch it, because the gates check what the agent *understood*, and the misunderstanding is the bug.

This skill designs the other kind of test: **test cases**, written from the user's side of the screen. Each one says what a person does, with what real data, and what has to be true in the world afterwards: the apple in the basket, not a `200`, not a log line, not a green test. `tdd` keeps its gates; that is the agent's inner loop and this skill doesn't touch it. This is the outer loop: the user's proof.

It is `grilling` pointed at one question: *how would you know, without reading any code, that this did what you wanted?* Invoke the "grilling" skill for the discipline (rounds, a frontier, a recommended answer on every question, facts are yours to find and decisions are theirs). This file is what to read first, what to ask, and what to write down.

You design cases; you don't run them here and you don't write code. `verify` runs the cases against the built thing; the user runs the ones only a human can judge.

## 0. Scope, one question

Before anything else, one question, two options, wait:

> **Q1 - Scope**: design cases for (a) the current feature or ticket, or (b) the whole product as it stands?
> ➡️ Recommend (a) when there is an in-flight ticket or spec; the cases attach to it and `verify` walks them at the end of `implement`. Recommend (b) when there is no ticket, the user said "the whole thing", or a green build has already shipped something that didn't work. (b) takes more rounds and ends with a ranked sheet, not a flat one.

If the argument already says (a ticket id, "everything", a feature name), take it and say so.

## 1. Read first, silently

Facts are your job. Look before the first real round; mention only what changes a question:

- The **ticket or spec** in scope: its acceptance criteria and user stories are the first draft of the cases, and also the first place the apple goes missing (a criterion written as "the endpoint returns the rows" instead of "the user sees their notes").
- `CONTEXT.md`: cases are written in its words. Absent is fine; use the user's.
- `docs/agents/feedback-loops.md`: how the thing boots, whether a browser is wired, where logs land. This decides which cases `verify` can run and which only a human can.
- **The gates that exist**: the test files, CI checks, lint and typecheck in scope. Don't judge their quality (`test-audit` does that); list *what each one would prove if green*, in one line each, so the user can see the gap between the gates and the apple.
- **The entry points a user touches**: screens, commands, routes, jobs, and what each writes to the world (a row, a file, an email, a payment, a message to another system). The apples live at the end of those.
- A `test-cases.md` already in scope: this is a revisit. Load it; rounds start from its **Open** section.

## 2. The interview

Rounds, each question numbered with a recommended answer drawn from what you read. The branches in dependency order, with the question bank in [QUESTIONS.md](QUESTIONS.md):

1. **The apple**: for the scope, what did the user want to be true in the world afterwards? Not the feature name; the outcome. "The customer gets the invoice email with the right total." "The file on disk opens in Excel with the accents intact." One sentence per outcome, observable without reading code. Draft them from the stories and the entry points; the user corrects the sentences.
2. **Proxies**: put the existing gates next to the apples. "If every one of these is green, can the apple still be on the tree?" Almost always yes; name how (the mail is sent to the wrong address, the file is written with the wrong encoding, the total is right and the currency is wrong). Every way it can still fail is a case.
3. **The walk**: for each apple, what exactly does a person do, from where they start, step by step. Real steps ("log in as the second user, open the March invoice, press export") not abstractions ("trigger the export flow").
4. **Real data**: which account, which record, which numbers. "Some user" isn't a case; "the user with two workspaces and an unpaid invoice" is. Recommend from seeds, fixtures and the spec's examples; where none exist, the case says which data to create first.
5. **Evidence**: the artefact that shows the apple is in the basket. A screenshot of the thing the user would look at, the file opened by the program the user would open it with, the row seen through the UI (not through a query), the email in the inbox. If the only evidence is "the test passed" or "the log says sent", the case has no apple yet: ask again.
6. **The ways a real person breaks it**: per apple, in user terms: I did it twice. I came back tomorrow. I typed the amount with a comma. My connection dropped halfway. It's someone else's invoice. It's the last day of the month. Recommend the two or three that match the Stakes; the rest go in Out of scope by name.
7. **Who runs it**: `verify` (the agent boots the thing and walks the case with evidence), the user by hand (anything a human has to judge: looks right, reads right, arrived in the real inbox), or an automated end-to-end test (only when the apple is machine-observable and the case will be run every merge). Recommend `verify` by default; by hand for the judgement calls; automation for the two or three cases the user would run every single time.
8. **Order and budget**: which cases must pass before this merges, and which can wait. Rank by what the user would hear about first.

Rules of the interview, beyond `grilling`'s:

- **Never accept a proxy as an apple.** Status codes, log lines, "the function returns", green gates: none of these is what the user wanted. Keep asking "and then what would you see?" until the answer is something a person can point at.
- **Never ask what the code answers.** Which routes exist, what the tests check, how the app boots: look. Ask what the code can't say: what was wanted, what counts as done, what matters most.
- **Cases in the user's language.** If a case needs a function name to make sense, rewrite it. The user is the one who will read it back and say "yes, that's what I meant".
- **Don't design gates.** If a case turns out to be "this function returns X for input Y", it belongs to `tdd`; say so and drop it from the sheet. The sheet holds outcomes.

## 3. Write the sheet

Beside the spec: `.scratch/<feature>/test-cases.md` (whole product: `.scratch/test-cases/test-cases.md`). On a real tracker the file lives in the same place and the ticket gets a one-line comment pointing at it; no separate issue.

```
# Test cases: <scope>

Boot: <from feedback-loops.md, or "not wired: run /setup-feedback-loops before verify can walk these">
Apples: <the outcomes from round 1, one line each, ranked>

## Cases
| # | Case | You do | With | The apple | Evidence | Run by |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Export the March invoice | Log in as Ana, open March, press Export | Ana: two workspaces, one unpaid invoice | A PDF Ana can open, total 1 240,00 EUR, her company name on it | The PDF opened, screenshot of page 1 | verify |
| 2 | Export twice in a row | Case 1, then Export again | same | One PDF, not two; the second is identical | Directory listing + diff | verify |
| 3 | Invoice arrives by email | Case 1, then wait | Ana's real test inbox | The email in the inbox, PDF attached, subject has the month | Screenshot of the inbox | by hand |
| 4 | Someone else's invoice | Log in as Ben, open Ana's March invoice by URL | Ben: no access to Ana's workspace | Ben sees "not found", nothing exported, nothing emailed | Screenshot + Ana's inbox unchanged | verify |

## Gates that don't count as proof
<each existing gate in scope, one line: what it proves, and which apple it can't see>

## Out of scope
<the wrong paths and apples named and left out, with the sentence that put them out>

## Open
<outcomes the user couldn't pin down, spec questions surfaced by writing a case, data that has to exist before a case can run>
```

Hand it back in one screen: the Apples lines, the case count, the ones marked *before merge*, the Open list. End with: **"Walk these in your head. Is there a way all of them pass and you still don't have what you wanted?"** and wait. If the answer is yes, that's the next case.

## 4. After confirmation

Stop, and say what's next:

- **Inside a feature**: append a one-line comment to the ticket pointing at the sheet. `verify` at the end of `implement` walks the sheet's `verify` cases in place of, or on top of, the bare criteria; each FAIL comes back as a red test for `tdd`, same as today.
- **The user says go**: invoke the "verify" skill on the sheet now, against whatever is built. Expect failures; the point of the sheet is to find the apple still on the tree before the user does.
- **By-hand cases**: list them with their evidence line so the user can run them in five minutes and paste the result under the case.
- **Automated cases**: only the ones marked so, and only once the case has passed by hand or by `verify` at least once. Then they're a `tdd` job with the case as the spec; the case sheet stays the source, the test is its automation.
- **Anything in Open**: a spec question first. `refocus` if the answer should be on disk, the ticket's comments if the user has to decide.

## Rules

- **Apples, not proxies.** Every case ends in something a person can point at in the world. No case ends in a status code, a log line, or a passing test.
- **Design, don't run, don't code.** Running is `verify`'s job; gates are `tdd`'s. A case that needs a function name is a gate in disguise; hand it over.
- **Scope first, read second, ask third.** One question, then look, then rounds. Never open with a wall of questions about a product you haven't looked at.
- **Facts from the repo, outcomes from the user.** Propose walks, data and evidence from what you read; the user says what they wanted.
- **The sheet is finishable.** Ranked, with a *before merge* line drawn. Sixty cases is a description; the ones above the line are the plan.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
