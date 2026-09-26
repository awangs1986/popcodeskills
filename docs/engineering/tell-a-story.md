## What it does

`tell-a-story` helps you and the agent agree on what a product should actually feel like to use. You can tell the story of someone using the product you want, or ask the agent to read the workspace and tell a story of the product that exists. You correct the story together before it becomes a product [spec](https://www.aihero.dev/ai-coding-dictionary/spec) or a proposed BACKLOG.

The story must be confirmed before it becomes requirements. In the agent-led direction, an appealing story is not permission to invent features: the agent separates what the source supports, what is uncertain, and what you want to change. It is aligning the product, not picking a stack or starting a build.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

You invoke this by typing `/tell-a-story`, and the agent won't reach for it on its own.

| Your situation | Start with |
| --- | --- |
| You can imagine using the product but cannot write professional requirements | **1: you tell the story**, and the agent helps you make it concrete |
| You have a workspace but cannot tell whether the product it describes is what you intended | **2: the agent tells the story**, based on a real path through that workspace |
| You already share the product picture and need to resolve detailed design questions | [grill-with-docs](./grill-with-docs.md) |
| The unresolved decisions span more than one conversation can hold | [wayfinder](./wayfinder.md) |
| You know the intended experience but need to prove the built thing delivers it | [cattytest](./cattytest.md) |

The opening always makes **1 = user tells, 2 = agent tells** explicit. You can supply an idea or a saved story, and you can change narrator later.

## Prerequisites

No issue tracker or setup is needed to tell a story or draft local documents. The agent-led current-experience mode needs readable source in the workspace. If there is none, it says so and asks whether to hear your story or help imagine a future one instead.

When you ask for saved output, it uses the project's product-draft location, or `.scratch/<feature>/` by default. It checks before changing existing files. Without a writable workspace, the drafts can stay in the conversation.

## The story is the agreement

Think in scenes, not feature lists. For example: a shopkeeper is closing for the evening, notices one unpaid order, opens it, and gets the information needed to decide what to do next. The next question is what that person should see or be able to do, not which database they want. A small everyday analogy can make a scene easier to picture, but cannot smuggle extra features into it.

The agent asks one focused question at a time, retells what changed, and keeps the accepted parts. If you say the product should send a reminder but the source only displays the unpaid order, the reminder becomes an intended change. It does not quietly become something the current product already does.

## What comes out

After you approve the latest story, choose how far to take it:

| Output | What it contains |
| --- | --- |
| **SPEC** | The agreed problem, experience, first-version scope, and observable acceptance criteria, each traceable to a scene |
| **BACKLOG** | An ordered index and separate draft work items: small user-visible outcomes, acceptance criteria, dependencies, and open questions |
| **Both** | The SPEC and the proposed work cross-referenced to each other |
| **Story only** | The agreement itself, without conversion; saved only if you ask |

Saved conversions include `story.md` alongside the requested documents. The BACKLOG is proposed work, not an issue tracker. Draft items live in `backlog/`, not the tracker's `issues/` directory, and nothing is automatically marked ready to build or published. Technical unknowns remain visible. If the existing behavior is already what you want, an empty implementation backlog is an honest result.

## Common questions

**Do I need to know how to write a SPEC before using this?**

No. Describe a person, what they are trying to do, and what happens. A rough or incomplete story is enough to start. The agent helps with the missing scenes and writes the structured output only after you agree with the experience it retells.

**How is this different from Wayfinder or a requirements interview?**

| Skill | The question it helps answer |
| --- | --- |
| `tell-a-story` | What should a real person experience, and is that what we both mean? |
| `grill-with-docs` | Which design decisions and domain terms still need to be resolved? |
| `wayfinder` | How do we organize a large set of unresolved decisions across multiple sessions? |

Wayfinder is broader than technology selection, but its unit is a decision. Here the unit is a scene in a user's journey. You can carry the approved story into either of the other skills.

**Will it write code or open a pile of issues when I approve the story?**

No. Approval confirms the product picture. You choose whether to get a local product SPEC, a proposed BACKLOG, both, or just the story. Publishing a technical plan and executable issues remains a separate step through [to-spec](./to-spec.md) and [to-tickets](./to-tickets.md), after any blocking questions are resolved.

## It's working if

- You can recognize the intended experience in a short story without knowing software terminology.
- Corrections change the relevant scenes instead of restarting the interview or disappearing into a generic feature list.
- You can tell which parts exist in the source, which are uncertain, and which are requests for the future.
- Every proposed requirement or work item points back to something you actually agreed, and nothing starts building just because you liked the story.

## Where it fits

A **product-alignment on-ramp** before engineering planning, also useful on its own to check an existing product's shape. [grill-with-docs](./grill-with-docs.md) resolves the design decisions the story exposes; [to-spec](./to-spec.md) and [to-tickets](./to-tickets.md) turn accepted planning material into published execution work. [ask-matt](./ask-matt.md) remains the router over the whole set.
