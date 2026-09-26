# Askcat data format

`template.html` renders the object assigned to `window.ASKCAT`. All content strings are plain text and HTML-escaped. Write narration in the user's requested language; keep skill names, commands, and paths unchanged. The renderer appends `喵！` once per prose paragraph, including bubbles, explanations, and tips. Do not add it to headings, labels, examples, commands, links, or other structured fields.

## Inventory first

Gather this independently by inspecting actual skill files, before writing the cards. Keep a path ledger beside it for your own source checks. Resolve duplicate installs before producing this list.

```json
{
  "scope": "installed",
  "skills": [
    { "name": "vibe", "invoke": "you", "beta": false },
    { "name": "tell-a-story", "invoke": "you", "beta": false },
    { "name": "research", "invoke": "agent", "beta": false }
  ]
}
```

`scope` is `installed` for verified installations, or `repository` for an explicitly labelled checkout catalog. A repository catalog does not imply the commands are installed. Include installed beta skills with `beta: true`; don't include uninstalled beta, misc, or deprecated skills in the introductory tour. The inventory and cards must have exactly the same unique names and invocation/beta flags.

## Guide data

```js
window.ASKCAT = {
  "scope": "installed",                   // exactly the inventory scope
  "lang": "en",                           // BCP-47 tag; sets <html lang>
  "title": "…",                           // page title, not narration
  "subtitle": "…",                        // short narrative introduction
  "generated": "2026-09-27",              // use the actual generation date
  "source": "awangs1986/popcodeskills",   // actual kit/source identity, stable for progress storage
  "cat": { "name": "…", "moods": { "storyteller": "…" } }, // optional localized mood descriptions

  "labels": {
    "search": "…", "youType": "…", "agentUses": "…", "beta": "…",
    "when": "…", "see": "…", "example": "…", "tip": "…", "tried": "…",
    "progress": "…", "picker": "…", "pickerIntro": "…", "restart": "…",
    "result": "…", "firstRun": "…", "glossary": "…", "openFile": "…",
    "chapters": "…", "noMatch": "…", "installedScope": "…", "repositoryScope": "…"
  },

  "intro": {
    "heading": "…",
    "paragraphs": ["…", "…"],              // what skills are and how to use this guide
    "bubble": "…"                           // a warm, useful opening line
  },

  "chapters": [
    {
      "id": "story",                        // unique slug; omit empty chapters
      "title": "…", "blurb": "…",
      "mood": "storyteller", "bubble": "…",
      "skills": [
        {
          "name": "tell-a-story",
          "invoke": "you",                  // you: human only; agent: model or human
          "beta": false,
          "mood": "storyteller",             // optional per-card override
          "oneLiner": "…",                   // purpose, not a feature wishlist
          "when": "…", "see": "…",
          "example": "/tell-a-story",        // copyable prompt, never narration
          "tip": "…", "working": "…", "broken": "…",
          "file": "skills/engineering/tell-a-story/SKILL.md" // relative to the output file, or a real URL
        }
      ]
    }
  ],

  "picker": {
    "start": "q1",
    "questions": [
      {
        "id": "q1", "text": "…",
        "options": [
          { "label": "…", "next": "q2" },
          { "label": "…", "skill": "tell-a-story", "prompt": "/tell-a-story" }
        ]
      }
    ]
  },

  "firstRun": [
    { "step": 1, "type": "/tell-a-story", "watch": "…" }
  ],
  "glossary": [ { "term": "spec", "plain": "…" } ],
  "footer": "…"
};
```

This is a shape example, not a complete guide: supply all inventoried cards and define any referenced question such as `q2`. The usual first-run sequence comes from the current handbook, not from this one illustrative step. The catalog size is always calculated, never hard-coded.

## Cat moods and coats

The template contains its own SVG illustrations. No external images, fonts, network requests, or repository asset paths are needed to display them.

| Mood | Coat and prop | Use for |
| --- | --- | --- |
| `teacher` | ginger-and-white, glasses and pointer | introduction, setup, glossary |
| `storyteller` | calico, open lavender book and sparkles | product alignment, `tell-a-story` |
| `builder` | ginger tabby, hard hat and pencil | build lane |
| `detective` | silver tabby, detective cap and magnifier | diagnosis |
| `guard` | brown tabby, helmet and shield | review and security |
| `sweeper` | chocolate-point palette, headscarf and broom | architecture upkeep |
| `dizzy` | blue-grey and apricot patches, swirl eyes and stars | session recovery |
| `reader` | black-and-white tuxedo, clipboard | verification, test audit, acceptance cases |

Chapters may use `start`, `story`, `build`, `fix`, `review`, `tidy`, `session`, or `other` for the built-in palette. Other unique slugs can choose a `color` from that set. A card-level `mood` overrides its chapter; `tell-a-story` defaults to `storyteller` even in another chapter.

## Marker font maintenance

The template embeds a tiny, two-glyph Noto Sans SC subset for the fixed conversation marker, so it renders offline even on a machine without CJK fonts. It is renamed Askcat Marker; the original SIL OFL 1.1 license is included in the template and in [assets/OFL.txt](assets/OFL.txt). The rest of the guide uses system fonts.

To regenerate the embedded subset, install `fonttools` and `brotli` in a temporary Python environment, extract `@fontsource/noto-sans-sc@5.3.0` in a temporary directory, and run `scripts/embed-marker-font.py --fontsource <extracted-package>`. This is a maintainer step, not a guide runtime dependency. Keep the font block and license together.

## Validation and safety

- `chapters[].id`, all `skills[].name`, and `picker.questions[].id` are unique slugs.
- Each inventory entry appears once, with matching invocation and beta flags. Hidden user-invoked commands are not automatically missing.
- Every picker option has exactly one target: `next` or `skill`. Targets exist, all questions are reachable, there are no cycles, and no path exceeds four questions.
- If present in the inventory, `tell-a-story`, `cattytest`, `verify`, `test-audit`, and `research` must have reachable picker results. These are different intentions, not interchangeable answers to "it is wrong".
- User-invoked example and picker prompts begin with that skill's command. Examples and first-run commands are never decorated with the conversation marker.
- All label keys shown above are required. Source links are safe relative paths, or HTTP(S)/file URLs; URL-encode spaces and check local targets against the output directory.
- Keep the data under 150 KB. The final HTML contains the data, styles, illustrations, and renderer, not links to scratch JSON files.
- Prefer the bundled `scripts/build-page.mjs` to validate and serialize. Its single anchored insertion escapes `<`, including a literal closing script tag in untrusted source text. Plain HTML escaping of a JSON string alone is not enough.
