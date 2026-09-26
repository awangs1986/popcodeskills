---
name: setup-feedback-loops
description: "Audit and wire the feedback loops the other skills spend: typecheck, lint, test runner, formatter, a smoke test, readable dev-server logs, a browser for web apps, and a pre-commit guardrail. Proves each one can go red, then records the commands where the other skills read them. Run once per repo, again when the stack changes."
disable-model-invocation: true
argument-hint: "Optional: one loop to (re)wire, or nothing to audit them all"
---

# Setup Feedback Loops

A **feedback loop** is one command that tells the agent, in seconds, whether what it just did is right. Every skill in the kit spends them: `tdd` needs a test runner, `implement` runs the typecheck, `diagnosing-bugs` needs to reach the dev server, `verify` needs to boot the app, `code-review` skips whatever tooling already enforces. None of them installs one. This skill does, and proves each one bites.

Prompt-driven, not a script. Explore, propose, confirm, wire, prove, record.

## The loops

| Loop | Command shape | It is a loop only if |
| --- | --- | --- |
| **typecheck** | `tsc --noEmit`, `mypy`, `cargo check`, `go vet` | a deliberate type error turns it red |
| **lint** | the stack's linter, default rules | a deliberate violation turns it red |
| **test** | one file in seconds; the full suite once | a deliberately failing test turns it red |
| **format** | check mode, not write mode | a misformatted file turns it red |
| **smoke** | boots the app or runs the CLI once and asserts one thing | a broken boot turns it red |
| **dev logs** | the server's output lands somewhere the agent can read | the agent can quote a log line without asking you |
| **browser** | web apps only: a headless browser the agent can drive | the agent can load `/` and read the DOM |
| **guardrail** | pre-commit runs typecheck, lint, and tests on staged files; CI does the same on push if there is a remote | a commit with a failing test is rejected |

## Process

### 1. Explore

Detect the stack before proposing anything: language, package manager (from the lockfile), framework, existing `scripts` in `package.json` / `Makefile` / `pyproject.toml` / `justfile`, existing CI config, existing hooks, `tsconfig` strictness. Then **run every command that already exists** and record three things: its verdict, how long it took, and whether it is silent (a test script that finds zero tests, a lint with no rules, a typecheck with `strict: false` and `skipLibCheck` covering for it). Present but silent is worse than missing, because the agent trusts it.

### 2. Present the audit

One table, one row per loop:

| Loop | Status | Proposal |
| --- | --- | --- |
| typecheck | present, `strict: false` | turn strict on, fix the 4 errors it surfaces |
| test | missing | vitest, one config file, `test` and `test:file` scripts |
| … | | |

Status is one of `missing`, `present`, `present but silent`, `slow` (over 30s for a full suite, over 5s for a single file). Recommend the stack's conventional default for each gap, one line each, so the user can accept the whole table in a word. Drop rows that don't apply (no browser loop for a CLI). Flag the only two choices that genuinely branch: strict types on or off (recommend on; the cost is paid once), and whether the guardrail runs tests or only typecheck and lint (recommend tests when the suite is under 30s).

Wait for the user.

### 3. Wire

Minimal and conventional. Scripts get consistent names whatever the stack: `typecheck`, `lint`, `test`, `test:file <path>`, `format:check`, `smoke`, `dev`, and `check` (runs typecheck, lint, format:check and test in that order). Don't add a framework the repo doesn't already want; don't spend the session tuning lint rules (defaults plus strict types, move on; rules accrete through review, not here).

- **Dev logs**: a `dev:log` script that tees the server to `.logs/dev.log` (gitignored), or if the harness already captures process output, a note saying so. The agent must be able to read the last hundred lines with one command.
- **Browser**: web apps only. Playwright with one `smoke.spec` that loads `/`, asserts the title, and fails on any console error. If the harness has a browser tool, note it beside Playwright rather than instead of it; Playwright is the one that runs unattended.
- **Smoke**: for a CLI, run it against a fixture and assert on stdout; for a service, boot, hit the health route, exit.
- **Guardrail**: on Node, the `setup-pre-commit` shape (husky plus lint-staged). Elsewhere the stack's equivalent (`pre-commit` for Python, a git hook script otherwise). If there is a remote and no CI, propose the smallest workflow that runs `check`.

### 4. Prove red

For **every** loop you wired or found: introduce a deliberate fault, run the command, show the red output, revert, run again, show green. A type error for typecheck; a lint violation; `expect(1).toBe(2)`; a misindented line; a throw at boot for smoke; a commit attempt with the failing test in place for the guardrail.

A loop you have not seen go red is not a loop. Do not skip this for the ones that "obviously work".

Record the durations. A full suite over 30s gets a note and the fastest single-file invocation you can find, because that is what `tdd` will actually run.

### 5. Record

Write `docs/agents/feedback-loops.md`: one section per loop with the exact command, the single-file variant where there is one, typical duration, and for dev logs and browser, how to read them. Use the template in [feedback-loops.md](feedback-loops.md). Add a `### Feedback loops` sub-block under `## Agent skills` in whichever of `CLAUDE.md` / `AGENTS.md` exists, pointing at the file. `implement`, `tdd`, `diagnosing-bugs`, and `verify` read it.

Commit the wiring on its own, before any feature work, so the first real commit already has the guardrail in front of it.

## Rules

- **Prove red.** Never declare a loop wired on the strength of a green run.
- **Fast beats thorough.** A two-second typecheck the agent runs after every edit is worth more than a three-minute one it learns to avoid.
- **Silent is worse than missing.** A present-but-silent loop gets fixed or deleted, never left.
- **Don't install what the stack doesn't want.** One test runner, the stack's linter, the stack's formatter.
- **Not a rules project.** If you are arguing about a lint rule, stop; that belongs to review.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
