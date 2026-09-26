# Conversation and routing evaluation scenarios

These are behavioral acceptance scenarios, not a claim that a model has passed them. The automated tests cover packaged rules, route coverage, and Askcat's actual renderer; a human or a multi-turn agent harness must still evaluate the conversational behavior below.

## Portable voice

| Situation | Expected behavior |
| --- | --- |
| Invoke a single copied `SKILL.md` in a project without setup | The local conversation block supplies the gentle voice and paragraph marker without needing this repository's root instructions |
| Invoke a model-reachable skill such as `tdd` or `research` directly | Human-facing explanations use the same voice; internal machine-facing results keep their schema |
| Start a new interview, then answer "I don't know" | Patient explanation and a helpful recommendation; no ridicule, pressure, or invented user decision |
| A test fails or a security check blocks shipping | Calm and explicit about the failure; no softened verdict or unsupported reassurance |
| A reply has one paragraph, several paragraphs, or a prose list | Exactly one `喵！` at each conversational paragraph boundary, including the final paragraph; no standalone marker-only paragraph |
| The user speaks a different language | Surrounding prose follows that language; the literal marker stays unchanged |
| Return an exact JSON object, a command, a quotation, a table, or a SPEC file | The technical output remains exact. No decorative suffix in values, paths, status cells, quoted evidence, or saved artifact prose |
| A wrapper invokes another skill and reports its result | One coherent voice in the parent reply, with no doubled suffixes from nested output |
| Run setup a second time | One updated `Agent skills` section and one conversation sub-block; unrelated project instructions remain intact |

## Vibe boundaries

| Request | Expected route |
| --- | --- |
| Product experience unclear in an empty repo | `tell-a-story` before setup or sizing |
| Explain the installed kit in an empty repo | `askcat`, not a forced first-run setup card |
| Continue from an old export without tracker config | `takeover` with the record; no fresh feature interview |
| The experience is agreed but proof cases are missing | `cattytest` |
| Existing acceptance cases need to be run | `verify` |
| What do these existing tests actually protect? | `test-audit` |
| Which library or how does this API work? | `research`; it is not mistakenly excluded from the kit |
| A greenfield effort has many unresolved decisions across sessions | `wayfinder`; story alignment first only when the destination is unclear |
| User names a specific available command | Read its actual instructions and honor the target rather than matching a broad keyword |
| A user-invoked command is absent from the model's implicit list | Check accessible installation files or a manifest before calling it missing |
| A beta command is mentioned | Verify installation and label it beta; do not silently treat it as shipped |
| A route is chosen | One short, considerate explanation and a clean command card; no unauthorized invocation |

## Askcat inventory and presentation

- Link one skill into multiple harness directories: one card, one count, one progress identity.
- Provide different versions under project and user paths: select the effective source with evidence, or ask when precedence is unknown.
- Show only a repository checkout: visibly label a catalog, not a verified installation.
- Install a new promoted skill: its inventory entry and card appear together; the old hard-coded count is never reused.
- Install a partial kit: no unavailable picker target or first-run command is invented.
- Include `tell-a-story`: show the calico storyteller, both narrator choices, revisions and confirmation, and the draft-only boundary.
- Open the HTML from disk: it loads without outside assets, and examples remain copyable while narration uses the paragraph marker.
- Deny browser storage: progress works while the page remains open, without claiming persistence after reload.
