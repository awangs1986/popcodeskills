## What it does

`askcat` builds **one offline HTML guide** to the skills available from this kit. A gentle cat guide explains each one in ordinary words, with a useful example, a tip, and signs of a good or bad run. Search, a "which skill do I need?" picker, and saved progress ticks make it a guide you can keep open while learning the workflow.

The page must match an inventory gathered from actual files, not a remembered list or count. Duplicate installations get one card. A checkout catalog is explicitly labelled as a catalog, not a claim that every command is installed. No skills are run just because the page recommends them.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

You invoke this by typing `/askcat`; the agent won't reach for it on its own. Pass a language, an output path, or a skill name to open on. It works before project setup.

| Situation | Reach for |
| --- | --- |
| First week with the kit, and the README feels like too much | `/askcat` |
| Showing the skills to someone you're onboarding | `/askcat`, in their language |
| You installed a new skill and the old guide is missing it | Regenerate with `/askcat` |
| You want just the next command, not the tour | [vibe](../engineering/vibe.md) |
| A message from the agent did not land | [wait-what](./wait-what.md) |
| You need to describe the product experience itself | [tell-a-story](../engineering/tell-a-story.md) |

## Prerequisites

The skill needs readable skill files and a place to save the HTML. It does not need an issue tracker or engineering setup. A bundled, dependency-free Node.js helper validates the inventory and builds the page when Node.js is available; otherwise the agent performs the same checks manually and says so. Existing output files are replaced only with your approval.

## A current guide, not a frozen list

Chapters follow the workflow: start here, picture the product when that route is available, build, fix, review, tidy, session care, and the rest. The calico storyteller explains `tell-a-story`, including the choice of narrator and the confirmation before a SPEC or BACKLOG draft. Other inline cats have distinct coats and props, without needing external image files. A tiny embedded font covers the fixed conversation marker even on a machine without Chinese fonts.

The picker separates five easy-to-confuse requests: align the product experience, design acceptance cases, run those cases, audit the existing tests, and research an external fact. It never recommends an unavailable command. A partial installation produces a smaller guide rather than invented cards.

The guide's paragraphs use the same warm conversational voice as the chat. The renderer adds `喵！` at paragraph boundaries; headings, buttons, file paths, and copyable example prompts remain undecorated. Progress ticks live in that browser, not in the project or on a server. If browser storage is blocked, they still work for the open page but do not survive a reload.

## Common questions

**Will a newly added skill be left out?**

The inventory is rebuilt on each run. The page builder compares card names, invocation modes, and beta flags against that separate inventory, so an omitted or duplicated card fails validation. It still depends on the agent finding the right installation roots and reading the right versions; the visible source and scope let you check that.

**Why does it say "repository catalog" instead of "installed skills"?**

A checked-out `SKILL.md` is not proof that your current agent has installed it. The guide can explain the repository before installation, but it keeps that distinction visible. Conversely, a user-invoked skill missing from the model's implicit list is not automatically uninstalled.

**Can it open on one skill?**

Yes. `/askcat tell-a-story` builds the guide and links directly to that card when it is in the inventory. If it is not found, the agent explains that instead of making up a card or returning a broken anchor.

**Can source text accidentally turn into executable HTML?**

The builder escapes script delimiters during JSON insertion, and the renderer escapes content and rejects unsafe link schemes. These are safeguards against accidental markup and untrusted text, not permission to skip reviewing the generated file.

**Do I need to regenerate after updates?**

Yes. The guide is a snapshot of the files read for that run. Rebuilding refreshes the cards and picker; progress ticks survive while the source identity, skill names, and browser storage remain the same.

## It's working if

- You can recognize the right skill without learning software jargon first.
- The visible count matches unique skills in the chosen installation or catalog, including newly added ones.
- The story picker reaches the calico storyteller, and proof cases are not confused with test audits.
- Examples remain clean to copy while the explanations sound warm rather than like a system log.
- Search, picker, deep links, and progress ticks work offline, without loading outside assets.

## Where it fits

A **standalone onboarding guide** over the available kit. [vibe](../engineering/vibe.md) gives the next command, [ask-matt](../engineering/ask-matt.md) maps the broader flows, and [tell-a-story](../engineering/tell-a-story.md) aligns the product itself. Regenerate this guide when the installed files change; it explains those skills without invoking them.
