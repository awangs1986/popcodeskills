## What it does

`takeover` resumes work in a **fresh** [session](https://www.aihero.dev/ai-coding-dictionary/session) when the old one can't, or shouldn't, continue: it ran out of quota, it crashed, the window got too long to trust, or it lived in a different tool altogether. You point the new session at whatever record exists (a conversation ID, a local JSON/JSONL export, a URL, or a [handoff](handoff.md) file), and the agent rebuilds a short working [context](https://www.aihero.dev/ai-coding-dictionary/context) from it: the goal, the constraints that still apply, the turning points (what was tried and why it was dropped), where the work actually stopped, and the next step.

It looks at the repository before it reads the transcript: branch, uncommitted changes, recent commits, the spec and tickets if there are any. The record is then checked against that ground, and the summary says plainly which of the old session's claims are verified, which aren't yet, and which edits it says it made that the repo doesn't have. Anything dated after the record ended is listed separately, because someone else did it.

It does this **without importing the old conversation**. It indexes the record first (who said what, where in the file), reads closely only the passages that could change scope or acceptance criteria, keeps repetitive logs and superseded code out of the summary, and tracks what it has read against what it hasn't. Old project paths are mapped onto the current checkout and verified file by file rather than assumed. Then it describes the project back to you in as few sentences as it needs (ten at most), asks whether the understanding is right, and waits. Everything before that answer is read-only: no code edits, no state-changing commands, no publishing.

The distinction it draws with `handoff` is who does the work. A handoff is *prepared by the outgoing* session; a takeover is *reconstructed by the incoming* one. A handoff file, when it exists, is one more record for `takeover` to index and check against the project, not a summary to take on trust.

<!-- cat-skills:conversation-doc:start -->
Conversation follows the [shared style](../../.agents/conversation-style.md): warm, gentle, and natural, with `喵！` at prose paragraph boundaries. Commands and technical artifacts stay exact.
<!-- cat-skills:conversation-doc:end -->

## When to reach for it

You invoke this by typing `/takeover` (or "use takeover with ...") in the new session; the agent won't reach for it on its own. Give it the record and, optionally, a focus ("only the login feature") and an old-root to new-root mapping.

| Situation | Reach for |
| --- | --- |
| The old session is gone (quota, crash, closed tab, another tool) and nobody wrote a handoff | **`/takeover`** with the export, ID, or URL |
| A handoff file exists and you are opening the session that continues it | **`/takeover <path>`**. It reads the file, checks its claims against the repo, and confirms before starting; a handoff read cold becomes a false premise the moment one of its "X is done" lines is wrong |
| The session is still open, has drifted, and you want to stay in it | [refocus](../engineering/refocus.md) |
| The session is still open and the work is about to move somewhere | [handoff](handoff.md), written by the session you are leaving |
| One message didn't land | [wait-what](wait-what.md) |

Inside the [vibe](../engineering/vibe.md) workflow these three are the whole story of session seams: `refocus` when you stay, `handoff` when you leave on purpose, `takeover` when you come back to something that ended without you.

## Common questions

**Why does it ask so few questions? Won't it miss things?**
Ten questions is a ceiling across the entire takeover, not a target, and one overall "is this right?" is the common case. The skill treats a long list of questions as a symptom of not having read the record properly, and sends the agent back to the index before it asks you. You are there to catch a wrong picture, not to rebuild the project from memory for it.

**I corrected one point. Does it start an interview?**
No. A correction is checked against the record first (was it a misunderstanding, or did the requirement actually change?), the clear ones are adopted directly, and only a remaining material ambiguity gets a question. If anything in the SPEC changes as a result, it shows you the revised SPEC before adopting it. Confirming the summary is not confirming a SPEC you haven't seen.

**Can it read another tool's session storage?**
Only if that storage is readable from where it runs, and it will verify a candidate location rather than assume one product's home directory. An ID alone is not a record: if there is no reader and no export, it tells you exactly what file it needs instead of guessing the task from the ID.

**It says the old session "did X". Is that true?**
Claims in a record are evidence to check, not facts to inherit. Path mapping does not carry uncommitted changes across, so it looks for the edits the old session says it made, and lists the ones it can't find as gaps. Test results, likewise, are re-verified before they govern the next step.

**Will it re-run the old commands or re-send the old messages?**
No. Source content is read as history, never replayed as tool calls, and confirming its understanding does not widen its authorization to publish, deploy, or message anyone.

**Where do the notes go?**
For a short record, the working summary in the conversation is enough. For a long one it keeps a compact index (coverage, topic locations, evidence pointers) in a temp directory or whatever notes artifact the host offers, and tells you where. It does not add a handoff document to your project unless you ask.

## It's working if

- The first thing you see is a short description of the project you recognise, followed by one question, not a questionnaire.
- The summary separates what it verified in the repo from what the old session merely claimed, and the two lists are not the same length.
- After you confirm, the ticket or spec carries a one-line note saying the work was taken over, from where, and what was verified.
- Dropped approaches appear with the reason they were dropped, so the new session doesn't try them again.
- Old paths in the summary point at files that actually exist in the current checkout, and anything it couldn't map is listed as unresolved rather than guessed.
- Nothing in the repository changed before you confirmed.
- A correction from you produced a revised SPEC to look at, not a fresh round of interviewing.
- When the record was incomplete, it named the missing file or range instead of filling the gap with a plausible story.

## Where it fits

The incoming half of a session seam. [handoff](handoff.md) is the outgoing half: the session that is leaving writes a small portable file. `takeover` needs no such file; it rebuilds from whatever record survived (an export, an ID, a URL, or a handoff) and confirms before continuing. [refocus](../engineering/refocus.md) is the same re-anchoring done inside a session that is still open. After confirmation it routes to [implement](../engineering/implement.md), [diagnosing-bugs](../engineering/diagnosing-bugs.md), [tdd](../engineering/tdd.md) or [vibe](../engineering/vibe.md); [ask-matt](../engineering/ask-matt.md) is the router over the whole set.
