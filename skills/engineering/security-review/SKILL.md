---
name: security-review
description: "Check a diff for the five security failures that actually ship in apps built by one person with an agent: secrets in code or client bundles, routes without authentication or per-record authorisation, unvalidated input at a boundary, data access that bypasses row-level or tenant isolation, and vulnerable or suspicious dependencies. Use before anything is exposed to the internet, when a diff touches auth, routes, data access, env, or dependencies, or when the user asks for a security check."
---

# Security Review

Not an audit. A short, targeted pass over a diff for the **five failures** that account for nearly every incident in solo-built apps. It runs as its own sub-agent (`code-review` spawns it beside Standards and Spec when the diff touches a trigger), reports under its own heading, and is never merged into another axis's score.

## Scope

The diff since a fixed point, supplied by whoever called you (a SHA, `main`, a branch); ask if it wasn't. Plus **one hop**: the functions the diff's routes and handlers call into, because the check is on the *path* from request to data, not on the hunk. A route that looks fine calling a query that ignores the user id is the finding.

Read `docs/agents/feedback-loops.md` if present, and skip anything tooling there already enforces (a lint rule against raw SQL, an audit step in CI).

## The five

1. **Secrets where they don't belong.** Keys, tokens, connection strings, or passwords in source, in a committed `.env`, in a log line, or in a client bundle. Check env names: a server secret behind a `NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_` or similar prefix is shipped to every browser. A newly committed `.env`-like file: check git history, because deleting it later does not un-leak it.

2. **Routes anyone can call, or call for someone else's data.** For every new or changed route, server action, RPC, or webhook: who can call it (**authentication**), and is the caller allowed to touch *this specific record* (**authorisation**: an ownership or tenant check on the row, not merely "is logged in"). The insecure direct object reference, `/orders/123` served to whoever asks, is the single most common finding in this category. Admin-only behaviour gated by a client-side flag counts as ungated.

3. **Input trusted at a boundary.** Request bodies, query params, path params, headers, file uploads, and webhook payloads parsed and validated against a schema *before* use. Nothing from outside interpolated into SQL, a shell command, HTML, a filesystem path, or a redirect URL. Webhooks verify their signature. File uploads check type and size server-side.

4. **Data access that bypasses the guard.** Raw queries that skip the ORM's parameterisation. A backend-as-a-service (Supabase, Firebase, and their kin) table created without row-level security or rules, or a new table when RLS is on by default elsewhere. A service-role or admin key reachable from client code or from a route the client can call. Mass assignment: a request body spread straight into an update.

5. **Dependencies you didn't look at.** New packages: run the stack's audit (`npm audit`, `pip-audit`, `cargo audit`), check for a typosquat of a popular name, check for install scripts. Pinned versions with known advisories.

Where you cannot tell whether a route is *meant* to be public, that is a question for the user, listed as such, not a finding to bury or a pass to assume.

## Report

```
## Security

| # | Finding | Where | Severity | Fix |
| --- | --- | --- | --- | --- |
| 1 | <what an attacker can do> | <file:line, the hunk quoted> | block | <one line> |

Questions for the user: <routes whose intended audience is unclear, or none>
Checked and clean: <which of the five had nothing to report>
```

Severity has three levels and nothing in between:

- **block**: exploitable now by an anonymous caller, or a leaked secret. Nothing ships until it's fixed.
- **fix-before-ship**: exploitable by a logged-in user, or exposes another user's data.
- **note**: hardening. Worth a ticket, not a stop.

Under 400 words. Quote the hunk. "Checked and clean" is a real line with real value; write it rather than padding the table.

## Rules

- **Path, not hunk.** Follow the route to the query before you call it clean.
- **Report, don't fix.** Fixes go through `tdd`: a test asserting that an unauthorised call gets a 403 is the regression test the fix needs anyway.
- **Five things, not fifty.** If you find yourself writing about CSP headers on a prototype, stop; the five are the ones that get solo developers breached.
- **Redact.** If you quote a leaked secret to prove it leaked, quote its name and location, never its value.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
