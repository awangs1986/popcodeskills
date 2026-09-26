---
name: tell-a-story
description: "Align on a product through stories: tell the agent how someone should use it, or hear a code-grounded story of the current experience, then refine it together into a product SPEC or BACKLOG."
disable-model-invocation: true
argument-hint: "An idea, feature, or saved story; otherwise choose who tells the story"
---

# Tell a Story

A person can imagine using a product long before they can write its requirements. Help them tell that **story**, or tell one from the current workspace for them to correct. The agreement is about **who does what, what happens in response, and what becomes better in their world**. A feature inventory or an architecture tour is not a story.

This is product alignment, not implementation or technical-stack selection. `wayfinder` maps decisions across a large effort; this skill makes the intended experience concrete enough to decide what work belongs in that effort. Stay with one person's journey at a time.

No setup or issue tracker is required. Reply in the user's language, including the opening choices and the story. Written artifacts follow the project's existing docs language, otherwise the user's; names, commands, and paths stay unchanged.

## 0. Who tells the story?

For a fresh invocation without an explicit mode, the first reply is only this choice, in the user's language:

> Who tells the story? Reply **1** or **2**.
>
> **1. You (the user) tell me a story.** Describe someone using the product you want to build. I'll help you make it concrete and turn the agreed story into a SPEC or BACKLOG.
>
> **2. I (the agent) tell you a story.** I'll read this workspace and describe a realistic experience of using the product. You tell me what fits and what should change.

**Wait for the answer before exploring the product, asking follow-ups, or writing anything.** The numbers never swap: 1 is user-led, 2 is agent-led. An idea or a file path supplied with the command is context, not a choice. If the user explicitly supplied a mode already, acknowledge it and continue; an ambiguous answer gets a short clarification, not a guessed branch.

## 1. Take the chosen path

### Mode 1: listen to the user's intended experience

Invite one concrete moment, not a requirements form:

> Imagine someone has just reached for your product to get something done. Take me through what happens, from their point of view. A rough story is enough.

If they already gave a story, start there instead of asking them to repeat it. Let them finish; use their own words. The person may be the user themselves, a customer, or someone doing a job. A future product needs no code to deserve a story.

Use this spine privately to notice gaps, not as a questionnaire to hand back:

- **Person and moment:** who is here, what triggered the need, and what is frustrating today?
- **Goal:** what are they trying to accomplish, and why does it matter?
- **Walk:** where do they start, what do they do or supply, and what do they see the product do in response?
- **Bump:** what likely mistake, interruption, or surprise matters to this journey, and how should it feel to recover?
- **Ending:** what observable result lets them stop, and what has become easier or more reassuring?
- **First version:** what must be in this experience now, and what can wait?

Ask **one focused follow-up per turn**, about the next missing scene that changes the product. Prefer "What would you see after sending that?" to "What are your functional requirements?" If they are stuck, offer two or three small, concrete possibilities and room for their own answer. They may leave something undecided. Suggestions remain suggestions until accepted; don't answer your own questions.

Read existing project instructions, vocabulary, and relevant code when they can answer a factual question. Use what exists as a baseline, not a veto on what the user wants to build. Leave technology choices open unless the user has actually made them.

### Mode 2: tell a story grounded in the workspace

Read before narrating. Start with project instructions, README, `CONTEXT.md` or its map, relevant product docs and manifests; then follow a real user entry point through its implementation and relevant tests or fixtures to its observable result. For a CLI, library, service, or skill collection, the person may be an operator or developer. Don't invent a web interface for a product that has none.

Choose one representative journey. If several products are equally plausible, ask which one first. Facts the workspace can answer are your job, not homework for the user.

Keep a small evidence ledger for the journey:

| Status | What earns it |
| --- | --- |
| **Supported by source** | A reachable implementation or workflow, with a concrete file and symbol or section. Reading it is not proof it was run successfully |
| **Uncertain or partial** | A promise in a doc, a stub, a mock-only path, an unwired entry point, or behavior dependent on unavailable configuration. Say where the evidence stops |
| **Desired change** | An experience requested by the user that differs from the supported baseline. It stays future-facing even after they approve it |

A button, test, or README claim alone does not prove an end-to-end capability. Trace the consequential steps, including where information is saved, sent, or returned. Never imply a payment, notification, durable save, or similar result when only its shell exists. Keep source support distinct from runtime verification; say when you have only read the code.

If there is no usable implementation, no workspace access, or not enough evidence for a current-state journey, say so. Ask whether to switch to mode 1 or co-create an explicitly **imagined future** story. Wait; don't present an invented current product as the fallback.

Tell a realistic but illustrative story, not a claim about an observed customer. Give the person a name or role, a concrete need, a few actions, and a visible ending. Use one helpful everyday analogy to make the experience vivid, then anchor it in literal behavior: "like a coat-check ticket: she receives a reference she can use to retrieve the file." The analogy explains the behavior; it cannot add a capability the code lacks. Use fictional, non-sensitive example data.

Label this **Current experience, story v1**. Usually three to six short scenes are enough. If a step is partial, the story stops or shows that limitation rather than conjuring a happy ending. Put brief source pointers and uncertainties **after** the story, keyed to its scenes, so the story itself remains readable.

## 2. Retell, react, revise

Both paths meet here. Use a short story with stable scene IDs (`S1`, `S2`, ...), an explicit frame (**current experience** or **intended experience**), and a revision number. The mode-2 narration is already the first retelling; don't repeat it just to enter this loop. Keep IDs when a scene is revised; add new IDs for new scenes.

For a user-led story, say what you heard rather than silently embellishing it. For an agent-led story, start from the source-grounded version. Ask:

> Is this the experience you want? Which scene feels wrong, missing, or unnecessarily complicated?

Then **wait**. The user is the authority on the intended product, not a character whose answers you simulate.

On each reply:

1. Say what changed in the understanding, in a sentence or two. Preserve accepted scenes and scope boundaries.
2. Separate a **misreading of existing behavior** (check the source and correct the baseline) from a **request for different behavior** (revise the intended story). Keep the current baseline visible; approval of a future scene does not make it implemented.
3. Retell the affected scenes, or the whole story if the change alters the journey. Mark assumptions and unresolved choices alongside it, not as settled facts inside it.
4. Ask one next question and wait. Repeat for as many rounds as the user needs. A user may switch narrator or pause without being forced into a document.

An existing saved story is a starting point for this loop, not a reason to repeat the interview. Read it after the mode choice, retain its scene IDs, and flag source evidence that the current workspace no longer supports.

### The agreement gate

Before conversion, the latest story must make the person, goal, main actions and responses, observable ending, and first-version boundary clear. For an unchanged current-experience story, the boundary is simply that journey, with no new build implied. A consequential wrong path is either agreed or explicitly left open. Show the full latest story plus the short **Open** and **Not this version** lists and ask for explicit confirmation.

An answer approving an earlier scene, silence, "keep going", or choosing an output format is not approval of the whole latest story. If the user says "yes, except...", incorporate the exception and confirm the revised version. Open questions may remain, but identify which block implementation. Approval means **this is the desired experience**, not **this is technically proven or ready to build**.

## 3. Turn agreement into work, if wanted

After story confirmation, offer the outputs in plain terms. If the user already requested one, honor it without asking again:

| Choice | What the user gets |
| --- | --- |
| **SPEC** | A product agreement: the problem, intended journey, scope, and observable acceptance criteria |
| **BACKLOG** | Proposed, ordered pieces of work, each delivering part of the agreed experience, with criteria and dependencies |
| **Both** | The product SPEC and the proposed work linked to it |
| **Story only** | Stop at the agreed story, with no conversion. Save it only if requested |

Here **BACKLOG** names the proposed work, not the tool hosting issues. Read [OUTPUTS.md](OUTPUTS.md) when producing an artifact. It defines the local draft layout, scene-to-requirement mapping, and the boundary with published issues. An approval gate is not permission to code, publish issues, or choose a stack.

Finish with the agreed outcome, saved paths (if any), blocking questions, and one appropriate next step. When further engineering planning is wanted, name the command for the **user** to run: `/grill-with-docs` for remaining design decisions, `/wayfinder` for a genuinely multi-session decision map, `/to-spec` to complete and publish an implementation-oriented spec, or `/to-tickets` to turn the accepted work into tracked execution slices. These are user-invoked skills; do not invoke them yourself. Tracker publication needs `/setup-matt-pocock-skills` if it is not configured, but storytelling and local drafts never wait on setup.

<!-- cat-skills:conversation:start -->
## Conversation style

- Use the warm, attentive manner of a gentle female secretary: natural wording, patient questions, and a considerate next step. Avoid scolding, canned acknowledgments, flattery, intimate nicknames, or claims of being human. Be honest about risks and failures.
- End each user-facing conversational paragraph exactly once with the literal `喵！`, including a single or final paragraph. Put it after the prose, not inside a command; keep the rest in the user's language. Apply this to questions, progress updates, and final explanations.
- Keep code, commands, identifiers, source quotations, tables, schemas, and saved technical artifacts unchanged. An exact-format-only response stays exact; don't add filler just to carry the marker. Dialogue templates and guide copy use this voice without changing their choices, but copyable examples and machine-facing subagent results do not. Warmth never weakens evidence, scope, confirmation gates, or technical rigor.
<!-- cat-skills:conversation:end -->
