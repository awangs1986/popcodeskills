---
name: askcat
description: "Build one offline HTML guide to the skills actually available: gentle cat explanations, a current skill picker, examples, and a first-run checklist, all in the user's language."
disable-model-invocation: true
argument-hint: "Nothing, a language, an output path, or one skill name to start the tour on"
---

# Askcat

Help the user get comfortable with the kit. Produce **one self-contained HTML file** with a warm cat guide, one card per discovered skill, a "which one do I need?" picker, and a first-run checklist. Explain the work patiently in ordinary words. The layout is bundled; understanding the installed skills and writing trustworthy guidance are the job.

This is a guide, not an execution flow. You may inspect files and run this skill's page builder, but do not invoke the skills being explained, install anything, or start project setup. The tour works before setup.

## 1. Gather an inventory, then read

1. **Discover actual files.** Inspect the current harness's project and user skill locations (`.claude/skills`, `.agents/skills`, `.pi/skills` or `.pi/agent/skills`, and their user-level equivalents), accessible plugin manifests and skill paths, and, when appropriate, this checkout's `skills/<bucket>/<name>/SKILL.md`. Absence from the model's implicit skill list is not evidence that a user-invoked command is missing.
2. **Identify the scope.** Installed skills from this kit are the default. In a checkout with no verifiable installation, offer a **repository catalog**, labelled as such, not a claim that its commands are installed. Use `scope: installed` or `scope: repository` in both inventory and guide data. If neither source is readable, say what access or path is needed instead of fabricating the kit.
3. **Deduplicate.** Resolve symlinks; the same skill linked into several harnesses gets one card. When copies with the same name differ, use the current harness's effective project/plugin/user precedence when known, record the chosen path, and mention a meaningful version conflict. If precedence cannot be established, ask which copy to describe. Do not silently merge different versions.
4. **Respect the buckets.** Include the promoted set available in the chosen scope. Include `in-progress` only when actually installed, clearly marked beta. Skip `misc` and `deprecated` in this introductory guide; say they are outside the tour rather than silently promising "every file in the checkout". A plugin manifest describes that plugin, not every other separately installed skill.
5. **Read each chosen `SKILL.md`.** Read the frontmatter and the behavior, output, prerequisites, and boundaries. Determine `invoke: you` from `disable-model-invocation: true` and the matching Codex policy; otherwise `invoke: agent`. Read its docs page when available. A claim not established by the source remains a stated uncertainty.
6. **Record the inventory independently of the cards.** Follow [DATA-FORMAT.md](DATA-FORMAT.md): one entry per unique name, with invocation mode and beta flag, plus a private path ledger showing which files you read. Compute counts from that inventory; never reuse a remembered skill count.
7. **Read the current map.** Read the installed `vibe` handbook and route coverage file when available, and `ask-matt` for the broader map. These are supporting material to inspect, not skills to invoke. The target `SKILL.md` wins if a summary is stale.

## 2. Write the guide

Use [DATA-FORMAT.md](DATA-FORMAT.md). Write the guide in the user's language, unless they explicitly request another. Keep names, commands, identifiers, and paths unchanged.

Each card has a simple explanation, a useful trigger, what the user will see, one realistic example prompt, one helpful cat tip, and observable working/broken tells. A person who has never written software should be able to choose their next step. Explain an unavoidable term once and add it to the glossary. Where the source says too little, say so rather than filling the gap with marketing.

The tone is gentle and practical, like a considerate secretary helping someone find their way. Invite and recommend rather than command, flatter, or scold. The template adds the conversation marker at each guide paragraph boundary; write clean prose fields, and keep example prompts, UI labels, and source links free of decorative suffixes.

Order chapters by use: **Start here**, optional **Picture the product**, **Build**, **Fix**, **Review**, **Tidy**, **When the session goes wrong**, **Everything else**. Omit empty chapters. `story` is an optional on-ramp, not a fifth engineering lane; use its calico `storyteller` mood. Card-level moods let `reader` guide verification and test audits within other chapters. All artwork is inline SVG with distinct coats; don't add external images or dependencies.

### Keep the new routes visible

When present in the inventory, explain these boundaries in the picker instead of treating every "green but wrong" request the same:

| User's need | Route |
| --- | --- |
| Describe an intended product experience, or hear one from the source | `tell-a-story`: 1 user tells, 2 agent tells; revise, confirm, then optional product SPEC / BACKLOG drafts |
| Design cases that prove the agreed outcome | `cattytest` |
| Run already-agreed cases and collect evidence | `verify` |
| Understand what existing tests claim and whether they can detect faults | `test-audit` |
| Research a library, API, or external fact | `research` |
| Recover a dead session rather than refocus a live one | `takeover`, distinct from `refocus` and `handoff` |

The picker is a shallow decision tree, at most four questions to a result. Every leaf must name a card in this inventory, respect its invocation mode, and supply a usable prompt. Never invent an uninstalled fallback. A partial install gets a smaller honest picker. The first-run sequence follows the current handbook, filtered to the available commands; describe missing prerequisites as missing, not as installed steps.

## 3. Validate and build

1. Read [template.html](template.html). Keep its layout and renderer; supply content, not a replacement interface.
2. Keep `inventory.json` and `guide.json` in a scratch location, not as extra runtime dependencies. With Node.js available, use the bundled builder from this skill's own installed directory:

   ```bash
   node <skill-dir>/scripts/build-page.mjs --data <scratch>/guide.json --inventory <scratch>/inventory.json --out <output>/askcat.html
   ```

   It checks inventory/card equality, invocation and beta flags, unique anchors, labels, source-link safety, important picker routes, unreachable questions and cycles, and the depth limit. It inserts JSON safely, including escaping `<` so a source string cannot terminate the script element. It refuses to overwrite an existing output; use `--force` only after the user approves that replacement.
3. If Node.js is unavailable, perform the same checks yourself and replace only the **standalone** `/*ASKCAT_DATA*/` line with `window.ASKCAT = <serialized JSON>;`. Escape `<` as `\u003c` and the Unicode line/paragraph separators as `\u2028` / `\u2029`. Do not use raw interpolation or a blanket replacement of every marker mention. State which validation was manual rather than claiming the helper ran.
4. Resolve each source link from the output file's location, not from the current working directory; URL-encode spaces. Use a real repository URL only when known. Confirm local targets exist. Ask before changing an existing output file, regardless of which build path you use.
5. Open the result and check a search, a picker path, and a progress tick when a browser is available. Check `tell-a-story`'s card and picker result specifically when installed. The guide must open from disk with no runtime network requests. If browser checking is unavailable, say so.
6. If an initial skill name was supplied, link to `#skill-<name>` only if it is in the inventory. Otherwise explain that it was not found and offer the full tour. Use the host's file viewer when available, otherwise give the path.

## 4. Hand it back

Briefly explain where the guide is, whether it covers installed skills or a repository catalog, and its deduplicated count. Mention that progress ticks stay in that browser when storage is available, and regenerating the guide refreshes its inventory. With storage blocked, ticks last only for the open page. Give a calm, concrete next step if the user asks for one; do not execute it on their behalf.

A guide is complete only when its cards match the independently gathered inventory, its prompts remain copyable, its narration is warm, and every recommendation is grounded in a file you read. Report unverified behavior honestly.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
