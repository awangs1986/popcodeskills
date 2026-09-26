# Vibe workflow poster

Two one-page pictures of [the vibe handbook](../../../skills/engineering/vibe/WORKFLOW.md): the optional `tell-a-story` product-alignment on-ramp, setup, the four lanes, the `implement` chain, the three session-seam moves (`refocus`, `handoff`, `takeover`), the context rules and the "three times wrong" stop rule.

- `../vibe-workflow-poster.png`, drawn by `build_poster.py` (English, linked from the top-level `README.md`).
- `../vibe-workflow-poster.zh-CN.png`, drawn by `build_poster_zh.py` (Chinese, linked from `README.zh-CN.md`). Its Chinese strings are readable source on purpose; `scripts/check-skills.mjs` allows CJK in exactly that path (see `CLAUDE.md`).

Both posters are 2000 × 4440 pixels. The story band sits before setup because storytelling needs no issue tracker: 1 is user-led, 2 is agent-led, both allow revisions, and only a confirmed story becomes optional SPEC / BACKLOG drafts. It does not add a fifth lane or authorize coding and issue publication. The footer counts the curated kit (26 skills), not the entire promoted collection.

## The cat crew

The layout and all text are drawn with Pillow, so commands stay exact; the seven mascot illustrations are AI-generated. Their transparent PNG cutouts are shared by both posters and both READMEs.

| Asset | Role | Coat and identifying prop |
| --- | --- | --- |
| `cats/cat_teacher.png` | Dispatcher | Ginger-and-white tabby, round glasses and pointer |
| `cats/cat_storyteller.png` | Product alignment | Calico, lavender storybook and teal scarf |
| `cats/cat_clipboard.png` | Verification and test audit | Black-and-white tuxedo, mint clipboard |
| `cats/cat_detective.png` | Bug diagnosis | Silver tabby, detective cap and magnifying glass |
| `cats/cat_shield.png` | Code and security review | Brown tabby, silver-blue helmet and teal shield |
| `cats/cat_broom.png` | Architecture upkeep | Chocolate-point Siamese, lavender headscarf and broom |
| `cats/cat_dizzy.png` | Session recovery | Dilute blue-grey and apricot tortoiseshell, orbiting stars |

Keep replacements as 640 × 640 RGBA PNGs with transparent backgrounds, complete silhouettes, and a little padding. Remove only the exterior background, not white fur. The renderers crop to the alpha bounds before scaling; they do not color-key white, which would damage the new coats. Keep role props and the warm outlined illustration style consistent across the crew.

## Re-render

After changing the handbook or illustrations, update both generators and render both PNGs from the repository root:

```bash
pip install pillow
python3 docs/engineering/poster/build_poster.py
python3 docs/engineering/poster/build_poster_zh.py
npm run check-skills
```

The default font directory is `docs/engineering/poster/fonts/`; it must contain `NotoSansSC-400-full.ttf` and `NotoSansSC-700-full.ttf`. Set `POSTER_FONTS=/path/to/fonts` to use another location. `POSTER_MONO` overrides the monospace font (default: DejaVu Sans Mono Bold). Fonts are not committed; the default font directory is gitignored.

To build the full TTFs from the fontsource subsets, run these in a temporary directory rather than adding the font package to the repository:

```bash
npm pack @fontsource/noto-sans-sc@5.3.0
tar -xzf fontsource-noto-sans-sc-5.3.0.tgz
pip install fonttools brotli
python3 - <<'PY'
from fontTools.merge import Merger
import glob
for weight, out in [('400', 'NotoSansSC-400-full.ttf'), ('700', 'NotoSansSC-700-full.ttf')]:
    files = sorted(glob.glob(f'package/files/noto-sans-sc-*-{weight}-normal.woff2'))
    font = Merger().merge(files)
    font.flavor = None
    font.save(out)
PY
```

Copy the two TTFs into the font directory, or point `POSTER_FONTS` at the temporary directory. Inspect both finished posters at full size and at the README's display width after rendering: confirm mode numbering, readable commands, no clipped text or overlapping cards, all seven cats, and matching English and Chinese content. Keep the PNGs, generators, README captions, and mascot table in sync.
