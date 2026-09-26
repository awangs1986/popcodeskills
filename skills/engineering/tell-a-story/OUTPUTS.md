# From a story to a product agreement

Read this only when saving an agreed story or converting it to SPEC, BACKLOG, or both. The story stays the source; the documents make it usable for planning without requiring the user to learn requirements-writing first.

## Where the drafts live

Use the project's established product-draft location if it has one. Otherwise use:

```text
.scratch/<feature>/story.md                    the agreed narrative and evidence
.scratch/<feature>/spec.md                     only when SPEC was requested
.scratch/<feature>/backlog.md                  only when BACKLOG was requested, an index
.scratch/<feature>/backlog/<NN>-<slug>.md       one proposed work item per file
```

Show the intended paths before writing. Read existing files first; never replace a spec, story, or work item from another effort. If a destination is occupied, propose a separate draft name and ask before changing existing content. On a revisit, show the proposed revisions and get permission before applying them. With no writable workspace, return the same Markdown in the conversation instead; don't block on setup.

These are **product drafts**, not published issues. Keep backlog drafts out of the local tracker's `issues/` directory, don't apply triage labels such as `ready-for-agent`, and don't post or modify anything on an external issue tracker. Document status is `draft`, with blocking questions called out explicitly. Story approval is recorded separately from implementation readiness.

## The story record

`story.md` contains:

- **Scope and frame:** which product or feature, current or intended experience, revision, and the user's explicit confirmation of that revision. Record the actual confirmation, not an invented quotation.
- **Story:** the latest approved scenes with stable IDs. Keep the vivid narrative here rather than copying it into every work item.
- **Reality check:** each consequential scene's supported baseline, source pointer where available, uncertainties, and agreed desired changes. No code yet means no implementation claim. Source inspection and runtime observation are distinct evidence.
- **First version**, **Not this version**, and **Open:** scope boundaries and unanswered questions, with the ones blocking implementation marked.

When the session changes a current-state story into a future one, retain the baseline in the reality check. A fictional persona or decorative detail does not become a requirement; a requested behavior or outcome does.

## SPEC: what experience are we agreeing to build?

Use this product-level frame. It can feed `to-spec` later without pretending that technical decisions or test seams have already been settled.

```markdown
# Product spec: <name>

Status: draft (product alignment, not implementation-ready)
Story: <link to story.md, approved revision>

## Problem Statement
<person, situation, goal, and the pain in today's experience>

## Solution
<the intended experience and its observable outcome, from the person's side>

## User Stories
<numbered, agreed behaviors; each cites its source scene IDs>

## Acceptance Criteria
<AC1, AC2, ...; each cites a scene and user story, with a concrete condition,
action, and externally visible result, including agreed wrong paths>

## First Version
<what is needed for the smallest useful complete journey>

## Implementation Decisions
<only decisions actually made; otherwise "Not decided" and an Open Questions pointer>

## Testing Decisions
<agreed observable checks, and any actual testing decisions; unchosen seams
or tooling stay open rather than being invented>

## Out of Scope
<explicit exclusions and deferred scenes, with the user's reason>

## Open Questions
<question, why it matters, whether it blocks implementation, who can answer>

## Further Notes
<known current limitations and the reference to the story's reality check>
```

Every requirement must trace to an accepted scene or an explicit user decision. Keep the list as large as the agreed experience needs, not an exhaustive wishlist. An analogy such as "a helpful librarian" does not authorize recommendations, chat, search, or accounts unless those behaviors were agreed.

Acceptance criteria describe what a person can observe. "The list contains the saved appointment after reopening it" is a checkable outcome; "the experience is seamless" is not. Ask about a missing behavior instead of inventing response-time targets, retention periods, permissions, or other product rules. Unresolved essentials stay open and block readiness.

## BACKLOG: what work would deliver that experience?

Produce **proposed vertical slices**: each item gives a person a small, complete, demonstrable outcome, rather than "build database", "build API", "build UI". Order the first useful journey before its refinements. Separate must-have and later work according to the user's scope decisions; distinguish a proposed order from one they have approved.

Compare against the reality check first:

- **Already supported and unchanged:** baseline, not a new build item.
- **Agreed new or changed behavior:** proposed work, with its story source.
- **Uncertain existing behavior:** an explicit investigation or blocking question, not an assertion that a feature is missing.
- **No desired changes:** say there is no new implementation backlog. An empty index with the baseline explanation is a valid result.

`backlog.md` is an index: story revision, spec link if one was requested, proposed order, links to the individual draft items, real blocking edges, and unresolved questions. The detail lives once, in each item's file:

```markdown
# <NN>: <user-visible outcome>

Status: draft (not a published issue)
Story: <link and scene IDs>
Spec: <link and criterion IDs, if a SPEC exists; otherwise omit>
Scope: <first version or later, as agreed>

## What changes
<current baseline versus intended outcome; what the user gains>

## Acceptance Criteria
- [ ] <observable result linked to its scene>
- [ ] <agreed wrong path, where applicable>

## Blocked by
<other draft items by title and link, or None; never invented issue IDs>

## Open Questions
<unresolved decisions; explicitly mark blocking ones>
```

A dependency must explain why the outcome cannot be delivered first; mere preferred order is not blocking. Keep each slice small enough to demonstrate on its own. If technical uncertainty prevents a credible slice, mark it blocked by that decision rather than guessing the architecture. `to-tickets` later handles implementation sizing, issue publication, and tracker-native blocking links; these drafts are inputs to that work, not a second issue tracker.

## Check the translation before handing it back

- Every in-scope behavior in the agreed story is covered by the chosen output's criteria or explicitly marked open. Deferred scenes remain deferred.
- Every criterion and work item traces back to an accepted scene or decision. Remove invented scope.
- If both outputs exist, every proposed slice references the relevant spec criteria, and every requested change is covered by a slice or named blocker. Existing supported behavior does not need fake implementation work.
- Current behavior, desired changes, and uncertainty are distinguishable without reading code. Source pointers live in the story's reality check; implementation task bodies don't become brittle file-by-file plans.
- A revision invalidating an earlier draft is called out. Propose updates to all affected outputs and get permission, rather than leaving conflicting versions or silently overwriting approved work.

Return a short summary and ask whether the translation still matches the story. A correction returns to the story loop; update downstream drafts only from the newly confirmed version. Stop before coding or publication.
