---
name: ask-matt
description: Ask which skill or flow fits your situation. A router over the skills in this repo.
disable-model-invocation: true
---

# Ask Matt

You don't remember every skill, so ask.

A **flow** is a path through the skills. Most paths run along one **main flow**, and situational **on-ramps** merge onto it. Everything else is standalone, or a vocabulary layer that runs underneath.

**Working alone?** **`/vibe`** is a pre-decided subset of this map for one developer with no team process: four lanes (build, fix, review, tidy), a sizing question, and a route card naming the next command. It covers the main flow, the bug on-ramp, and codebase health, and deliberately leaves out `triage`, `to-questionnaire` and `wizard` (with `wayfinder` brought back for multi-session decisions). Send solo users there first; send them back here the moment other people enter the picture.

## The main flow: idea → ship

The route most work travels. You have an idea and want it built.

1. **`/grill-with-docs`** sharpens a shared product idea by interview. For unresolved design questions when you are **working in a working directory**, start here: it's stateful, retaining what it learns in `CONTEXT.md` and ADRs. (No working directory? Use `/grill-me` instead, covered under Standalone. Both run the same `/grilling` primitive; `grill-with-docs` is the one that leaves a paper trail, which makes it the better of the two whenever a repo is there to leave it in.)
2. **Branch: can you settle every question in conversation?** If a question needs a runnable answer (state, business logic, a UI you have to see), detour through a prototype, bridged by **`/handoff`** in both directions (a prototype lives in its own directory, which is exactly what `/handoff` is for; see Phase boundaries):
   - **`/handoff`** out, then open a fresh session against that file,
   - **`/prototype`** to answer the question with throwaway code,
   - **`/handoff`** back what you learned, and reference it from the original idea thread.
3. **Branch: is this a multi-session build?**
   - **Yes** → **`/to-spec`** (turn the thread into a spec), then **`/to-tickets`** to split it into tracer-bullet tickets, each declaring its **blocking edges**. On a local tracker that's one file per ticket under `.scratch/<feature>/issues/`, worked blockers-first by hand; on a real tracker the edges become native blocking links, so any ticket whose blockers are done can be grabbed: kick off **`/implement`** per ticket, **`/clear`ing context between each one**. Each ticket is self-contained, so the last one's context is disposable.
   - **No** → **`/implement`** right here, in the same context window.

   Either way, **`/implement`** builds each issue by driving **`/tdd`** internally (one red-green slice at a time), runs **`/verify`** once the suite is green (boots the thing and walks the acceptance criteria as a user would, with evidence per row; a FAIL goes back into `/tdd`), then **`/test-audit`** (renders every test as a plain-language claim for you to judge, maps claims to criteria, and probes with a dozen mutants to see which rules no test protects; survivors go back into `/tdd`), then closes out by running **`/code-review`**, a review of the diff along Standards and Spec, plus **`/security-review`** as a third sub-agent whenever the diff touches a route, auth, a query, env, or a dependency, before committing. Reach for **`/tdd`** on its own when you just want to build a concrete behaviour test-first without a full spec, **`/verify`** on its own when you want to see something work rather than be told it does, **`/test-audit`** on its own when a green suite is hiding logic errors and you want to know what the tests actually claim, **`/code-review`** on its own whenever you want to review a branch or PR against a fixed point, and **`/security-review`** on its own before anything first faces the internet.

### Context hygiene

Keep steps 1–3 in **one unbroken context window** (don't compact or clear until after `/to-tickets`) so the grilling, spec, and tickets all build on the same thinking. Each `/implement` then starts fresh, working from the ticket.

The limit on this is the **[smart zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**: the window (~150k tokens on state-of-the-art models) within which the model still reasons sharply. If a session approaches it before `/to-tickets`, don't push on degraded; `/compact` at the nearest phase boundary and carry on (see Phase boundaries).

## On-ramps

A starting situation that generates work, then merges onto the main flow.

- **You can imagine using the product but cannot write its requirements, or want to check what the current workspace feels like to use** → **`/tell-a-story`**. Choose **1** to tell the agent your intended experience, or **2** to hear a realistic, source-grounded user journey from the agent. Revise the scenes together until the latest story is explicitly confirmed, then optionally turn it into a local product SPEC, proposed BACKLOG, or both. No setup is needed; source-supported behavior, uncertainties, and desired changes stay separate.

  This aligns **what experience to build**, not the stack or a multi-session decision map. Carry the agreed story and drafts into **`/grill-with-docs`** when design decisions remain, or **`/to-spec`** and **`/to-tickets`** when ready to prepare and publish execution work. Product drafts are not automatically ready-for-agent issues. For proof that an already-agreed experience actually works, use **`/cattytest`** instead.

- **Bugs and requests piling up** → **`/triage`**. It moves issues through triage roles and produces agent-ready issues, which **`/implement`** later picks up.

  Triage is only for issues **you didn't create**: bug reports, incoming feature requests, anything that arrives raw. Tickets that `/to-tickets` produced are already agent-ready, so **don't triage them**.

- **Something's broken** → **`/diagnosing-bugs`**. For the hard ones: the bug that resists a first glance, the intermittent flake, the regression that crept in between two known-good states. It refuses to theorise until it has a **tight feedback loop** (one command that already goes red on *this* bug), then fixes with a regression test. Its post-mortem hands off to **`/improve-codebase-architecture`** when the real finding is that there's no good seam to lock the bug down.

- **A huge, foggy effort: a greenfield project or a huge feature build, too big for one session** → **`/wayfinder`**, the most cognitively demanding flow here. When the way from here to the destination isn't visible yet, it charts a **shared map** of **decision tickets** on the issue tracker and resolves them one at a time, producing **decisions, not deliverables**, until the fog is pushed back and the way is clear. Where **`/grill-with-docs`** sharpens an idea you can hold in one session, wayfinder is for the idea you can't, and it's slower and denser, so save it for exactly that, never a well-scoped feature.

  When the map clears, **it hands off, it doesn't build**: merge onto the main flow at **`/to-spec`**, which collapses the map's linked decisions into a buildable plan, then `/to-tickets` and `/implement` as usual. Looping the map straight into `/implement` skips that collapse and throws the linked detail away, so go straight to `/implement` only when the effort turned out genuinely small.

## Codebase health

Not feature work, just upkeep.

- **`/improve-codebase-architecture`** runs whenever you have a spare moment to keep the codebase good for agents to operate in. It surfaces **deepening opportunities**; picking one _generates an idea_ you can take into the main flow at `/grill-with-docs`. It's the survey that finds the candidates; **`/codebase-design`** (below) is the bench you design the chosen one on.

## Vocabulary underneath

Two model-invoked references that run *beneath* the other skills, each the single source of truth for its vocabulary. Reach for them directly when the **words**, not the process, are the problem; or let the skills above pull them in.

- **`/domain-modeling`**: sharpen the project's *domain* language: challenge a fuzzy term, resolve an overloaded word ("account" doing three jobs), record a hard-to-reverse decision as an ADR. It's the active discipline `/grill-with-docs` drives to keep `CONTEXT.md` a clean glossary.
- **`/codebase-design`** is the deep-module vocabulary (module, interface, depth, seam, adapter, leverage, locality) for designing a module's *shape*: a lot of behaviour behind a small interface at a clean seam. `/tdd` and `/improve-codebase-architecture` both speak it.

## Phase boundaries

A **phase** is a chunk of work inside a session: the grilling, the implementation, the QA. At the **boundary** between two of them you have five options, and picking between them is the fuzziest decision in this whole map:

- **Continue**: stay put. Costs nothing, loses nothing.
- **`/clear`**: empty the window, when nothing here matters to what's next.
- **`/handoff`** writes a portable markdown file. Narrow: only for a **new harness**, a **new directory**, a **colleague**, or forking a side task **mid-phase**. What it buys is portability.
- **Subagent**: send a tightly-scoped task to its own window and get a report back.
- **`/compact`** compresses this context and seeds a fresh session with it. The **default**, at the bottom of the tree rather than the first reach.

Read [PHASE-BOUNDARIES.md](PHASE-BOUNDARIES.md) for the ordered tree: the five questions, the reasoning behind each branch, and why the primary-source cost makes **Continue** the one to rule out first. Make the decision **at** a boundary; mid-phase, continue or split the rest into subagents. The one mid-phase move that isn't a context switch is **`/refocus`**: when a long session has lost the thread, it re-reads the spec, ticket and every conversation decision from their primary sources, checks the diff against them, and reports the drift in a one-screen brief. Run it before you `/compact`, and seed the compact with its brief. The five options all assume the session is still open. When it isn't (quota gone, a crash, a window too long to trust, a record from another tool), **`/takeover`** in the fresh session reads the record, rebuilds the context itself, and confirms its understanding with you before touching anything; a handoff file, if one exists, is one of the records it reads rather than a summary it trusts.

## Standalone

Off the main flow entirely.

- **`/grill-me`**: the same patient, thorough interview as `/grill-with-docs`, but **stateless**: it saves nothing locally and builds no `CONTEXT.md`. Reach for it when you are **not working in a working directory** (sharpening a plan, a design, a piece of writing, anything with no repo under it). If you are in a working directory, use `/grill-with-docs` instead: it runs the same interview and leaves a paper trail, so it is strictly the better one.
- **`/grilling`** is the interview primitive itself: rounds, the frontier, facts are the agent's job and decisions are yours. `/grill-me` and `/grill-with-docs` are the two named ways in, and `/triage`, `/wayfinder` and `/improve-codebase-architecture` all run it internally. Reach for it directly only when you want the interview with no wrapper around it.
- **`/resolving-merge-conflicts`** works an in-progress merge or rebase conflict hunk by hunk, resolving by **intent** traced to each side's primary source rather than by picking lines, then finishes the operation. It never runs `--abort`. Standalone and off every flow: reach for it when you are already mid-conflict.
- **`/prototype`** is a small, throwaway program that answers one design question: does this state model feel right, or what should this UI look like. Throwaway is a constraint on how the code is written, not a promise to destroy it: the answer folds into the real code, and the prototype itself is kept as a **primary source** on a `prototype/<name>` branch out of main, pointed at from the implementation issue. It's the detour in step 2 of the main flow, but reach for it any time a design question is hard to settle on paper.
- **`/research`**: delegate reading legwork to a **background agent**: it investigates a question against **primary sources**, then leaves a cited Markdown file in the repo. Keep working while it reads. The file it produces is something to take *into* the main flow at `/grill-with-docs`, since research feeds the thinking rather than replacing it.
- **`/to-questionnaire`** comes in when the thing blocking you isn't in your head or the codebase but in **someone else's**, and it writes them a questionnaire to fill in. It's the inverse of `/grill-me`: instead of interviewing you about the subject, it interviews you about the **send** (who it's going to, what you need back) and aims the questions at the gap. What comes back is material for `/grill-with-docs` or `/to-spec`.
- **`/wizard`** is for the steps only a **human** can take: provisioning infrastructure, setting up credentials or CI secrets, clicking through an unfamiliar third-party dashboard, running a one-off migration or cutover. It generates an interactive bash script that opens each URL, captures each value, and writes it into `.env` and GitHub secrets, so the procedure stops being something you re-explain to an agent every time. Model-invoked, so the agent reaches for it the moment it hits a wall only you can pass. If the agent could just do it itself, it should; this is for where a human is genuinely in the loop.
- **`/refocus`** is the corrective for a *session* that has drifted: the agent forgot a decision, widened the scope, or is working the wrong criterion. It re-reads the requirements from disk rather than from memory, diffs them against what was built, and reports **dropped**, **drifted** and **contradicted** items, then waits for you to confirm. Same window, no context switch; it is the thing to run *before* reaching for `/compact`.
- **`/takeover`** is the corrective for a *session that ended without you*: the old one ran out of quota, crashed, grew too long to trust, or lived in another tool, and nobody wrote a handoff. In the fresh session it indexes whatever record exists (an ID, an export, a URL, a handoff file), rebuilds the goal, constraints, turning points, stopping point and next step without importing the whole log, maps old paths onto the current checkout with verification, describes the project in at most ten sentences, and asks one confirmation before it is allowed to change anything. `/handoff` is written by the session you're leaving; `/takeover` is done by the session you're arriving in.
- **`/wait-what`** is the corrective for a message that didn't land. Use it mid-conversation, inside any other skill, and the agent re-pitches what it just said with the context you were missing, in plain words, in your language, using the `CONTEXT.md` vocabulary. It works after the fact; `/grill-with-docs` is the upfront cure, because a shared language agreed early is what stops the jargon arriving at all.
- **`/teach`**: learn a concept over multiple sessions, using the current directory as a stateful workspace.
- **`/askcat`** is `/teach` pointed at this kit: it builds one HTML page where a cat guide explains every installed skill in plain words, with a "which one do I need?" picker. For the first week, or for someone you're onboarding; after that this map and `/vibe` are faster.
- **`/cattytest`** is the grill for "it's all green and it still doesn't do what I asked". The gates `/tdd` writes check what the agent understood; this designs the cases that check what you wanted, from your side of the screen: what a person does, with what data, and what has to be true in the world afterwards (the apple in the basket, not a `200`). It ends in a test-cases sheet that `/verify` walks with evidence and you run by hand where only a human can judge. Not a `/tdd` replacement: gates are the agent's loop, cases are yours.
- **`/writing-for-agents`** is the reference for writing documents agents consume: skills, AGENTS.md, pointed-at docs.

## Precondition

**`/setup-matt-pocock-skills`**: run before your first tracker-dependent engineering flow to configure the issue tracker, triage labels, and doc layout the other skills assume. Custom issue trackers also work.

**`/setup-feedback-loops`**: run right after it, once per repo and again when the stack changes. It wires the typecheck, lint, test runner, formatter, smoke test, dev logs, browser and pre-commit guardrail that `/tdd`, `/implement`, `/verify` and `/diagnosing-bugs` all spend, proves each one goes red, and records the commands in `docs/agents/feedback-loops.md`. Without it every one of those skills is guessing at how to check its own work.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
