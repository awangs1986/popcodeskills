---
"cat-skills": minor
---

Add `tell-a-story`, a user-invoked product-alignment skill with two explicit modes: the user describes an intended experience, or the agent reads the workspace and tells a source-grounded story of the current experience. Both modes use a gentle, one-question-at-a-time revision loop and require confirmation of the latest story before converting it to a product SPEC, a proposed BACKLOG, or both.

Keep supported behavior, uncertainty, and desired changes separate. Trace requirements and draft work items to accepted scenes, leave technical decisions open, and keep local drafts separate from published issues. Storytelling works before setup and does not start implementation or invoke another user-invoked skill. Register the skill in the plugin, synchronize the English and Chinese indexes, and add product-alignment routes to `ask-matt` and `vibe` with matching docs and regression scenarios.
