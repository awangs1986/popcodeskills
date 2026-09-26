# Vibe route coverage

Every promoted skill has a place here. Read this alongside `WORKFLOW.md` when choosing a route; open the target's `SKILL.md` before making a load-bearing claim about its behavior or prerequisites. Invocation mode comes from that file, not from this table. User-invoked skills remain commands for the human to type.

`kit` is the curated daily workflow. `bring-back` is a situational detour, not an extra lane. `full-map` stays outside the kit, with an explicit route to the broader map or the named standalone. `npm run check-skills` compares this inventory with the promoted directories, so a new skill cannot silently disappear from the guidance.

| Skill | Place | Route when |
| --- | --- | --- |
| `ask-matt` | full-map | Team work, unfamiliar combinations, or a task outside the solo kit needs the full map |
| `askcat` | kit | The user wants the installed skills explained as a friendly guide, even before setup |
| `cattytest` | kit | The intended outcome is known, but the user needs cases that prove it, not another look at green tests |
| `code-review` | kit | Review the diff against standards and requirements before merge |
| `codebase-design` | kit | A module's interface, depth, or testing seam needs design work |
| `diagnosing-bugs` | kit | A real bug is hard to reproduce, flaky, slow, or has an unknown cause |
| `domain-modeling` | kit | Domain terms or relationships need clarification and documentation |
| `grill-me` | full-map | A patient, thorough design interview with no repository or persistent docs |
| `grill-with-docs` | kit | The product picture is shared and design decisions remain in a workspace |
| `grilling` | kit | The interview primitive; normally used within an interview wrapper |
| `handoff` | kit | The live session is handing work to another place or person |
| `implement` | kit | An agreed spec or tracked issue is ready for implementation |
| `improve-codebase-architecture` | kit | Survey codebase health or find a better seam after diagnosis |
| `prototype` | kit | A design question needs something runnable or visible to settle it |
| `refocus` | kit | The current session has drifted from its requirements |
| `research` | kit | A library, API, or external fact needs primary-source investigation |
| `resolving-merge-conflicts` | bring-back | A merge or rebase conflict is actually in progress |
| `security-review` | kit | Check exposure before deployment or a security-sensitive change |
| `setup-feedback-loops` | kit | Typecheck, tests, smoke checks, logs, or browser feedback need wiring |
| `setup-matt-pocock-skills` | kit | A tracker-dependent flow needs repo-specific issue and doc conventions |
| `takeover` | kit | A fresh session must recover an old record, export, or handoff |
| `tdd` | kit | Build one concrete behavior or known fix test-first |
| `teach` | full-map | Learning a topic over time, rather than touring this skill kit |
| `tell-a-story` | kit | Align the product experience: 1 user tells, 2 agent tells from source, then revise and confirm |
| `test-audit` | kit | Inspect what the existing tests claim and whether they detect broken logic |
| `to-questionnaire` | full-map | A decision needs answers from somebody outside the current conversation |
| `to-spec` | kit | Agreed discussion or product drafts need an implementation-oriented spec published to the tracker |
| `to-tickets` | kit | Accepted planning material needs approved execution slices and real blocking relationships |
| `triage` | full-map | Process raw issues filed by other people |
| `verify` | kit | Walk already-agreed criteria against the running product and collect evidence |
| `vibe` | kit | Find the next command, resume in-flight work, or learn the first-run sequence |
| `wait-what` | kit | Rephrase a message with the missing context, without requiring project setup |
| `wayfinder` | bring-back | Unresolved decisions span sessions, for a new product or a project split |
| `wizard` | full-map | A human-only provisioning or dashboard step needs a guided procedure |
| `writing-for-agents` | full-map | Write or improve skills, project instructions, and agent-facing documentation |

## Optional work is not missing work

`in-progress`, `misc`, and `deprecated` are not part of the promoted kit. The handbook names beta `retro`, `pr`, and `setup-ts-deep-modules` for specific situations. Confirm a beta's files are actually installed before recommending it, say it is beta, and keep its original invocation policy. A file in this checkout is not proof it is installed in the user's harness. Do not silently promote the other experimental or misc skills into the everyday flow.

When a user names another available skill directly, explain that it sits outside the curated kit and read its own instructions before advising them. When it is unavailable, say what you could and could not verify; absence from the model's implicit skill list is not evidence that a user-invoked command is missing.
