"""Maintainer-only: embed two OFL-licensed glyphs for the fixed conversation marker.

Runtime guides need neither Python nor external font files. Regenerate from the
@fontsource/noto-sans-sc@5.3.0 package with fonttools and brotli installed.
"""
import argparse
import base64
from io import BytesIO
from pathlib import Path

from fontTools import subset
from fontTools.merge import Merger
from fontTools.ttLib import TTFont

START = "/* ASKCAT_MARKER_FONT_START */"
END = "/* ASKCAT_MARKER_FONT_END */"
GLYPHS = {0x55B5, 0xFF01}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fontsource", type=Path, required=True, help="Extracted fontsource package directory")
    parser.add_argument("--template", type=Path, default=Path(__file__).resolve().parent.parent / "template.html")
    args = parser.parse_args()
    remaining, sources = GLYPHS.copy(), []
    for path in sorted((args.fontsource / "files").glob("noto-sans-sc-*-400-normal.woff2")):
        with TTFont(path) as candidate:
            found = remaining.intersection(candidate.getBestCmap())
        if found:
            sources.append(str(path))
            remaining -= found
        if not remaining:
            break
    if remaining:
        raise SystemExit(f"Missing marker glyphs: {remaining}")
    font = Merger().merge(sources) if len(sources) > 1 else TTFont(sources[0])
    options = subset.Options()
    options.name_IDs = ["*"]
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=GLYPHS)
    subsetter.subset(font)
    names = {1: "Askcat Marker", 2: "Regular", 3: "AskcatMarker-1.0", 4: "Askcat Marker", 6: "AskcatMarker"}
    for record in font["name"].names:
        if record.nameID in names:
            record.string = names[record.nameID].encode(record.getEncoding())
    font.flavor = "woff2"
    font.recalcTimestamp = False
    output = BytesIO()
    font.save(output)
    encoded = base64.b64encode(output.getvalue()).decode("ascii")
    license_text = (args.fontsource / "LICENSE").read_text().strip()
    css = f'''{START}
  /* Noto Sans SC subset, renamed Askcat Marker. Original license follows.
{license_text}
  */
  @font-face {{
    font-family: "AskcatMarker";
    src: url("data:font/woff2;base64,{encoded}") format("woff2");
    font-weight: 400;
    font-style: normal;
    font-display: swap;
    unicode-range: U+55B5, U+FF01;
  }}
  .miao {{ font-family: "AskcatMarker", sans-serif; font-weight: 400; white-space: nowrap; }}
  {END}'''
    text = args.template.read_text()
    if text.count(START) != 1 or text.count(END) != 1:
        raise SystemExit("Template must have one marker-font slot")
    begin, end = text.index(START), text.index(END) + len(END)
    args.template.write_text(text[:begin] + css + text[end:])
    print(f"Embedded {len(output.getvalue())} bytes of marker font")


if __name__ == "__main__":
    main()
