# Engineering

Skills I use daily for code work.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[ask-matt](./ask-matt/SKILL.md)**: Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[vibe](./vibe/SKILL.md)**: Solo developer's dispatcher: puts you on one of four lanes (build, fix, review, tidy), sizes the work, and names the exact next command. A curated subset of the map for one person working alone.
- **[tell-a-story](./tell-a-story/SKILL.md)**: Align the product through a user-told or source-grounded story, revise it together, then turn the confirmed experience into a product SPEC or proposed BACKLOG. No coding or issue publication.
- **[refocus](./refocus/SKILL.md)**: Re-anchor a long session on its requirements: re-read the spec, ticket, and every decision from its primary source, check what has actually been built against them, report the drift, and ask one round of questions about anything the sources leave ambiguous before continuing.
- **[grill-with-docs](./grill-with-docs/SKILL.md)**: Grilling session that also builds your project's domain model, sharpening terminology and updating `CONTEXT.md` and ADRs inline.
- **[triage](./triage/SKILL.md)**: Move issues through a state machine of triage roles.
- **[improve-codebase-architecture](./improve-codebase-architecture/SKILL.md)**: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[setup-matt-pocock-skills](./setup-matt-pocock-skills/SKILL.md)**: Configure this repo for the engineering skills (issue tracker, triage labels, domain doc layout). Run once per repo.
- **[setup-feedback-loops](./setup-feedback-loops/SKILL.md)**: Audit and wire the feedback loops the other skills spend (typecheck, lint, tests, formatter, smoke test, dev logs, browser, pre-commit guardrail), prove each one goes red, and record the commands in `docs/agents/feedback-loops.md`. Run once per repo, again when the stack changes.
- **[to-spec](./to-spec/SKILL.md)**: Turn the current conversation into a spec and publish it to the issue tracker.
- **[to-tickets](./to-tickets/SKILL.md)**: Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges, whether as text in a local file or as native blocking links on a real tracker.
- **[implement](./implement/SKILL.md)**: Build the work described by a spec or set of tickets, driving `/tdd` at pre-agreed seams, running `/verify` and `/test-audit` once green, and closing out with `/code-review` and a Checks run ledger before committing.
- **[cattytest](./cattytest/SKILL.md)**: Design the test cases that prove the software did what you wanted, from your side of the screen: what a person does, with what data, and what must be true in the world afterwards. Not the agent's gates. Ends in a test-cases sheet `verify` walks and you can run by hand.
- **[wayfinder](./wayfinder/SKILL.md)**: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on the issue tracker, resolved one at a time until the way to the destination is clear.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[prototype](./prototype/SKILL.md)**: Build a throwaway prototype to answer a design question: a single shareable HTML file for state/logic, or several toggleable UI variations.

- **[diagnosing-bugs](./diagnosing-bugs/SKILL.md)**: Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./research/SKILL.md)**: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./tdd/SKILL.md)**: Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./domain-modeling/SKILL.md)**: Actively build and sharpen a project's domain model by challenging terms, stress-testing with scenarios, and updating `CONTEXT.md` and ADRs inline.
- **[codebase-design](./codebase-design/SKILL.md)**: Shared discipline and vocabulary for designing deep modules: small interfaces, clean seams, testable through the interface.
- **[verify](./verify/SKILL.md)**: Run the built thing and walk its acceptance criteria and user stories as a user would, one wrong path each, with a screenshot or captured output per verdict. Observes, never fixes; `implement` calls it after the suite is green.
- **[security-review](./security-review/SKILL.md)**: Check a diff for the five security failures solo-built apps actually ship: secrets in the bundle, routes without per-record authorisation, unvalidated input, data access that bypasses RLS, unaudited dependencies. A conditional third sub-agent of `code-review`.
- **[test-audit](./test-audit/SKILL.md)**: Do the tests behind a change protect the business logic or only pass? Translates each test into a plain-language claim the domain expert can judge, maps claims to the acceptance criteria, and runs a targeted mutation probe. `implement` calls it after `verify`.
- **[code-review](./code-review/SKILL.md)**: Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), run as parallel sub-agents.
- **[resolving-merge-conflicts](./resolving-merge-conflicts/SKILL.md)**: Work through an in-progress git merge or rebase conflict hunk by hunk, resolving by intent traced to each side's primary source, then finish the operation, never `--abort`.
- **[wizard](./wizard/SKILL.md)**: Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.
