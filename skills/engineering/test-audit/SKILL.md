---
name: test-audit
description: "Audit the tests behind a change for whether they protect the business logic or only pass: translate each test into a plain-language claim the domain expert can judge, map claims to the acceptance criteria and user stories, and run a targeted mutation probe (break the logic on purpose, see whether any test dies). Use after tdd, before code review, when the user asks \"are these tests real\", \"what do the tests actually check\", or when green tests keep hiding logic errors."
---

# Test Audit

Green proves nothing on its own. A test can pass because the logic is right, because the test cannot fail, or because the test and the code share the same misunderstanding of the rule. `tdd` says how to write tests that avoid this; this skill checks whether the ones that got written actually did, and it makes the result legible to the one person who can judge the business rule: the user.

Three questions, three sections, one report. You **audit**; you don't fix. Every gap you find is a red test for `tdd` to write next.

## Read first

- `docs/agents/feedback-loops.md` for the single-file test command and its duration. The mutation probe runs it many times; without a fast single-file loop, cap the probe hard.
- The acceptance criteria of the ticket and the user stories of the spec this change implements (in context when `implement` calls you; otherwise from the argument, or ask).
- `CONTEXT.md`, so the claims are written in the project's words.

## Scope

The test files added or changed since the fixed point (the ticket's base commit, or `main`), and the production code they exercise. For a whole-feature audit before merge, every test file the feature's tickets touched.

## 1. What the tests claim

Read every test in scope. Translate each into **one sentence a domain expert would say**, in `CONTEXT.md` vocabulary, stating the rule the test enforces. Not what the code does; what is true of the product if this test is green.

```
1. [tags.test.ts:12]  Adding a tag a note already has leaves the note with one copy of it.
2. [tags.test.ts:25]  "Work" and "work" are the same tag.
3. [due.test.ts:8]    A highlight reviewed today is not due again tomorrow.
```

While translating, flag three things inline:

- **Name and assertion disagree**: the name says "rejects an invalid email", the body only checks nothing threw. Report the claim the *assertion* makes, and mark the name as misleading.
- **Claims nothing**: no assertion, an `expect(x).toBeDefined()` on something that is always defined, `expect.anything()`, a snapshot of an entire object with no stated rule. Mark it **claims nothing**.
- **Assertion derived from the code**: the expected value is computed by the same helper, formula, or fixture path the code uses, so the test agrees with the code by construction (`tdd`'s tautological anti-pattern). Mark it **tautological**.

This list is the human checkpoint. End it with: **"Read these as business rules. Is any of them wrong?"** A wrong claim here is the logic error that would otherwise surface in production six weeks from now, with a green suite the whole way.

## 2. Are the rules covered?

Map criteria to claims, both directions:

```
| Criterion or user story           | Claims  | Gap                          |
| --- | --- | --- |
| AC1 duplicate tags collapse        | 1, 2    |                              |
| AC3 a tag can be removed           | none    | UNCOVERED                    |
| US14 two books with the same title | none    | UNCOVERED                    |
| (no criterion)                     | 7       | tests something nobody asked for: keep, or is the spec missing a story? |
```

Also list the **wrong paths** the criteria imply that no claim covers: empty input, the boundary value, the second call, the record that belongs to someone else. Happy-path-only suites are the usual shape of "all green, still broken".

## 3. Can they fail?

The mutation probe. For each **business-rule site** in the production code in scope, break it on purpose, run the relevant test files, and record whether any test died.

Business-rule sites, in priority order: comparisons and boundaries (`<=` vs `<`, off-by-one), conditionals and early returns, arithmetic and defaults, sort and dedupe keys, anything that reads a `CONTEXT.md` term. Skip logging, formatting, and glue.

Discipline:

- **One mutant at a time.** Apply, run the test files that exercise that code (the single-file command), record `killed by <claim #>` or **SURVIVED**, revert. Confirm the revert with `git diff` before the next mutant. Never leave a mutant in the tree: if anything interrupts you, `git checkout` the file first and explain second.
- **Cap it.** Ten to fifteen mutants for a ticket, chosen for business weight, not exhaustive coverage. This is a probe, not a mutation-testing run; if the repo wants the full thing, that is a tool (`stryker`, `mutmut`, `cargo-mutants`) and a `setup-feedback-loops` conversation.
- **Time-box** by the suite's single-file duration from `feedback-loops.md`. A 20-second loop means eight mutants, not fifteen.

```
| Mutant                         | Site         | Result             |
| --- | --- | --- |
| `<=` → `<`                     | due.ts:41    | SURVIVED           |
| removed normalizeTag()         | tags.ts:18   | killed by 2        |
| early return on empty list removed | review.ts:12 | SURVIVED       |
```

Every **SURVIVED** row is a rule no test protects. Say which claim *should* have died and didn't, or that no claim addresses the site at all.

## 4. Smells

Only ones that change the verdict; `code-review` owns style. From `tdd`'s anti-patterns plus the ones that specifically produce false green:

- **Mocked the thing under test**: the seam is stubbed, so the test passes whatever the real code does.
- **Implementation-coupled**: asserts on calls, order, or internals; will break on a refactor and stay green on a wrong result.
- **Order-dependent or shared state**: passes alone, or passes only after another test ran.
- **Broad matcher on the load-bearing assertion**: `toBeTruthy()`, `toContain` on a big string, `any` in the expected shape.
- **Fixture hides the rule**: the interesting value lives in a fixture file nobody reads, so the test asserts "same as the fixture" and the fixture is wrong.

## 5. Report

```
## Test audit: <ticket or feature>

### Claims
<numbered list from section 1, with inline flags>
Read these as business rules. Is any of them wrong?

### Coverage
<table from section 2>
Wrong paths nobody tests: <list>

### Mutation probe (<n> mutants, <m> survived)
<table from section 3>

### Smells
<list, or none>

### Verdict
Protected: <the rules with a killing claim and a criterion>
Unprotected: <survivors + uncovered criteria + claims-nothing tests>
Next red tests, in order: <one line each, ready for tdd>
```

Then stop. Whoever called you decides:

- `implement` takes **Next red tests** back into its `tdd` loop before `code-review`. A wrong claim the user flags is a spec question first (`refocus` or the ticket's comments), then a red test.
- Standalone, the user reads the claims; anything they mark wrong is the finding that matters most.

## Rules

- **Claims in the user's language.** If a claim needs a variable name to make sense, rewrite it. The user is the reader.
- **Never leave a mutant behind.** `git diff` clean between every probe and at the end.
- **Audit, don't fix.** Writing the missing test here skips the red step; hand it to `tdd`.
- **A probe, not a proof.** Say how many mutants you ran and why those; never imply exhaustive coverage.
- **"All killed, all covered" is a valid verdict.** Don't invent survivors to look thorough.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
