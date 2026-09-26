---
name: verify
description: "Run the built thing and walk its acceptance criteria and user stories the way a user would, capturing evidence for each verdict. Use when work is claimed done, before code review, or when the user says \"does it actually work\", \"try it\", \"show me\", or \"walk through it\"."
---

# Verify

`tdd` proves the seams. `code-review` reads the diff. Neither one starts the application. This skill does: boot it, walk every criterion as the user would, and bring back **evidence**. "The tests pass" is not evidence that the feature works. A screenshot, a captured response, or a transcript of the command is.

You observe. You do not fix. A failure here is a red test waiting to be written by whoever called you.

## Read first

- `docs/agents/feedback-loops.md`: how to boot, where the logs land, whether a browser is wired. Missing? Fall back to the package scripts and say in the report that the user should run `/setup-feedback-loops`.
- The **acceptance criteria** of the ticket and the **user stories** of the spec this work implements. When `implement` calls you, they are in context; standalone, take the path or issue from the argument, or ask which.
- A `test-cases.md` in scope (written by the "cattytest" skill): its rows marked `verify` are the criteria in executable form, with the steps, data and evidence already decided. Walk those rows as written, on top of the bare criteria; report the ones marked `by hand` as *for the user* rather than skipping them silently.
- `CONTEXT.md`, so the report speaks the project's language.

## Redact

You will show captured output. **Redact every secret first**: write `<REDACTED>` in its place. Quote only the lines that carry the signal.

## Process

### 1. Boot

Start the thing the way `feedback-loops.md` says, with logs teed somewhere you can read. A web app: the dev server. A service: the service, then its health route. A CLI: build it. A job: the entry point with a fixture.

If it does not boot, that is finding number one. Stop and report; nothing else is verifiable.

### 2. Walk

One criterion at a time, **as the actor in the user story**, through the interface the actor would use. Never through the code.

| Surface | Drive it with | Capture |
| --- | --- | --- |
| Web UI | Headless browser (Playwright, or the harness's browser tool): navigate, act, assert on the DOM | A screenshot per step, console errors, failed network requests |
| HTTP API | `curl` or a small script with a realistic payload | Status, headers that matter, body |
| CLI | The command against a fixture | stdout, stderr, exit code |
| Background or scheduled | Trigger it directly | The side effect: the row, the file, the outbound call |

For each criterion also try the **one obvious wrong path**: empty input, the second click, a refresh mid-flow, the record that isn't yours. One per criterion, not a fuzz; the point is to catch the happy-path-only implementation.

Watch the logs while you walk. An error the UI swallowed is still a finding.

### 3. Verdict

Every criterion gets exactly one of:

- **PASS**, with the evidence that shows it.
- **FAIL**, with expected versus actual and the evidence that shows the gap.
- **UNVERIFIABLE**, with why (needs credentials you don't have, needs production data, needs a human's phone). Name what would make it verifiable.

Never "probably works", never "should be fine". A green you did not see is a lie.

### 4. Report

```
## Verify

Booted: <command> (<seconds>), logs at <path>

| # | Criterion | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | <criterion, quoted> | PASS | <path to screenshot / captured output> |
| 2 | <criterion> | FAIL | expected <…>, got <…>; <path> |
| 3 | <criterion> | UNVERIFIABLE | needs <…> |

Log errors during the walk: <lines, or none>
Unrequested behaviour noticed: <anything the criteria didn't ask about, or none>
```

Evidence lives in the OS temp directory under `verify-<timestamp>/` (`$TMPDIR`, falling back to `/tmp`, or `%TEMP%` on Windows), and the report carries the paths. A described screenshot is not a screenshot.

### 5. Hand back

Stop after the report. Whoever called you decides what happens next:

- `implement` takes each **FAIL** back into its `tdd` loop as a new red test and does not proceed to review with one open.
- A **FAIL** whose cause is not obvious from the evidence is a `diagnosing-bugs` case; say so, and hand it the exact repro you just ran, which is already most of its Phase 1.
- **UNVERIFIABLE** rows are for the user.

Kill every process you started.

## Rules

- **Observe, don't fix.** The moment you edit source, you are no longer verifying.
- **Through the interface, never the code.** If the only way to check a criterion is to read the implementation, the verdict is UNVERIFIABLE, and that is itself worth knowing.
- **Evidence is a file.** Screenshots, captured bodies, transcripts. Prose describing them is not evidence.
- **One wrong path per criterion.** Enough to catch happy-path-only work, not enough to turn this into QA.
- **Unverifiable is honest.** It is the verdict to give when you'd otherwise be guessing.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
