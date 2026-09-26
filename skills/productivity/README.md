# Productivity

General workflow tools, not code-specific.

## User-invoked

Reachable only when you type them (Claude Code: `disable-model-invocation: true`; Codex: `policy.allow_implicit_invocation: false` in `agents/openai.yaml`).

- **[askcat](./askcat/SKILL.md)**: Build one HTML page where a cartoon cat explains every installed skill in plain words: what it does, when to type it, what a good run looks like, plus a "which one do I need?" picker and a first-run checklist. In your language.
- **[grill-me](./grill-me/SKILL.md)**: Talk through a plan or design in patient, thorough rounds until every branch of the design tree is resolved.
- **[handoff](./handoff/SKILL.md)**: Compact the current conversation into a handoff document so another agent can continue the work.
- **[takeover](./takeover/SKILL.md)**: Resume a long or stalled conversation in a fresh session from an ID, export, URL, or handoff file: the new session indexes the records, rebuilds concise context, describes the project in up to ten sentences, and confirms before continuing. Needs nothing from the old session.
- **[teach](./teach/SKILL.md)**: Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./to-questionnaire/SKILL.md)**: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can (filled in async, or together over a meeting).
- **[wait-what](./wait-what/SKILL.md)**: Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain words, in your language, using your `CONTEXT.md` vocabulary.

## Model-invoked

Model- or user-reachable (rich trigger phrasing so the model can reach for them).

- **[grilling](./grilling/SKILL.md)**: Interview the user patiently and thoroughly about a plan, decision, or idea until every branch of the design tree is resolved.
- **[writing-for-agents](./writing-for-agents/SKILL.md)**: Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
