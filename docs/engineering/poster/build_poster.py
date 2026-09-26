from PIL import Image, ImageDraw, ImageFont
import re, math, os
from pathlib import Path
from functools import lru_cache

W, H = 2000, 3920
BG = (255, 248, 236)
INK = (47, 42, 38)
GRAY = (120, 112, 104)

HERE = Path(__file__).resolve().parent
FONTS = Path(os.environ.get("POSTER_FONTS", HERE / "fonts"))
MONO_PATH = os.environ.get("POSTER_MONO", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")
@lru_cache(maxsize=None)
def F(size, bold=True):
    return ImageFont.truetype(str(FONTS / ("NotoSansSC-700-full.ttf" if bold else "NotoSansSC-400-full.ttf")), size)
@lru_cache(maxsize=None)
def MONO(size):
    return ImageFont.truetype(MONO_PATH, size)

LANES = {
    "story":  dict(fill=(255, 237, 231), edge=(198, 96, 113), dark=(144, 54, 76)),
    "setup":  dict(fill=(238, 236, 231), edge=(120, 112, 104), dark=(90, 84, 78)),
    "build":  dict(fill=(222, 235, 255), edge=(59, 111, 214), dark=(35, 75, 160)),
    "fix":    dict(fill=(255, 226, 220), edge=(217, 83, 79),  dark=(160, 50, 46)),
    "review": dict(fill=(221, 243, 228), edge=(58, 157, 93),  dark=(30, 110, 60)),
    "tidy":   dict(fill=(235, 226, 255), edge=(123, 92, 214), dark=(85, 60, 160)),
    "focus":  dict(fill=(255, 241, 194), edge=(217, 164, 0),  dark=(150, 110, 0)),
}

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- text helpers ----------
def tokens(s):
    # Keep commands intact and closing punctuation with the preceding word/glyph.
    raw = re.findall(r"[A-Za-z0-9_/.:,'()+→←=<>#*-]+|\n|[ \t]+|.", s)
    closing = "\u3001\u3002\uff0c\uff01\uff1f\uff1b\uff1a\uff09\u3011\u300b\u3009\u201d\u2019?!;:.)]}"
    grouped = []
    for token in raw:
        if token in closing and grouped and not grouped[-1].isspace():
            grouped[-1] += token
        else:
            grouped.append(token)
    return grouped

def wrap(s, font, maxw):
    lines, cur = [], ""
    for t in tokens(s):
        if t == "\n":
            lines.append(cur); cur = ""; continue
        if font.getlength(cur + t) <= maxw or cur == "":
            cur += t
        else:
            lines.append(cur.rstrip()); cur = t.lstrip()
    lines.append(cur)
    return [l for l in lines]

def text(x, y, s, font, fill=INK, maxw=None, align="left", spacing=1.35, anchor_center=False):
    lines = wrap(s, font, maxw) if maxw else s.split("\n")
    lh = int(font.size * spacing)
    for i, l in enumerate(lines):
        lw = font.getlength(l)
        if align == "center":
            xx = x - lw / 2
        elif align == "right":
            xx = x - lw
        else:
            xx = x
        d.text((xx, y + i * lh), l, font=font, fill=fill)
    return y + len(lines) * lh

def text_h(s, font, maxw, spacing=1.35):
    return len(wrap(s, font, maxw)) * int(font.size * spacing)

# ---------- shapes ----------
def rbox(x0, y0, x1, y1, fill, edge, r=26, width=5):
    d.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=fill, outline=edge, width=width)

def panel(x0, y0, x1, y1, lane, title, subtitle=None):
    c = LANES[lane]
    rbox(x0, y0, x1, y1, (255, 255, 255), c["edge"], r=34, width=6)
    # title tab
    tf = F(40)
    tw = tf.getlength(title) + 60
    d.rounded_rectangle((x0 + 30, y0 - 34, x0 + 30 + tw, y0 + 34), radius=20, fill=c["edge"])
    d.text((x0 + 60, y0 - 27), title, font=tf, fill=(255, 255, 255))
    if subtitle:
        # inside the panel, clear of the border
        d.text((x0 + 30, y0 + 34), subtitle, font=F(28, False), fill=c["dark"])

def measure_node(w, cmd=None, label=None, note=None, cmd_size=32, pad=40, hmin=0):
    total = 0
    if cmd: total += int(MONO(cmd_size).size * 1.3)
    if label: total += text_h(label, F(30), w - pad)
    if note: total += text_h(note, F(26, False), w - pad, 1.3)
    return max(hmin, total + 52)

def node(cx, cy, w, h, lane, cmd=None, label=None, note=None, cmd_size=32, pad=40):
    c = LANES[lane]
    parts = []
    if cmd: parts.append(("cmd", cmd))
    if label: parts.append(("lab", label))
    if note: parts.append(("note", note))
    # measure, then grow the box to fit the text
    total = 0; measured = []
    for kind, s in parts:
        if kind == "cmd":
            f = MONO(cmd_size); hh = int(f.size * 1.3)
        elif kind == "lab":
            f = F(30); hh = text_h(s, f, w - pad)
        else:
            f = F(26, False); hh = text_h(s, f, w - pad, 1.3)
        measured.append((kind, s, f, hh)); total += hh
    h = max(h, total + 52)
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    rbox(x0, y0, x1, y1, c["fill"], c["edge"], r=22, width=5)
    y = cy - total / 2
    for kind, s, f, hh in measured:
        col = c["dark"] if kind == "cmd" else (INK if kind == "lab" else GRAY)
        text(cx, y, s, f, fill=col, maxw=w - pad, align="center", spacing=1.3)
        y += hh
    return (x0, y0, x1, y1)

def place_below(prev_box, w, hmin=0, gap=28, **kw):
    # Center-y for a node stacked under prev_box with a fixed gap.
    h = measure_node(w, hmin=hmin, **kw)
    return prev_box[3] + gap + h / 2

def diamond(cx, cy, w, h, lane, label):
    c = LANES[lane]
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    d.polygon(pts, fill=c["fill"], outline=c["edge"], width=5)
    f = F(32)
    lines = label.split("\n")
    lh = int(f.size * 1.25)
    y = cy - (len(lines) - 1) * lh / 2
    for l in lines:
        d.text((cx, y), l, font=f, fill=c["dark"], anchor="mm"); y += lh

def arrow(pts, color=INK, width=6, head=22):
    d.line(pts, fill=color, width=width, joint="curve")
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    a1 = (x1 - head * math.cos(ang - 0.5), y1 - head * math.sin(ang - 0.5))
    a2 = (x1 - head * math.cos(ang + 0.5), y1 - head * math.sin(ang + 0.5))
    d.polygon([(x1, y1), a1, a2], fill=color)

def edge_label(x, y, s, color=GRAY, size=26):
    f = F(size)
    w = f.getlength(s) + 24
    d.rounded_rectangle((x - w / 2, y - 20, x + w / 2, y + 20), radius=14, fill=(255, 255, 255), outline=color, width=3)
    d.text((x - (w - 24) / 2, y - 17), s, font=f, fill=color)

# ---------- cats ----------
def load_cat(path, height):
    # Assets are transparent cutouts; preserve white fur and fine coat markings.
    with Image.open(path) as source:
        im = source.convert("RGBA")
    bbox = im.getbbox()
    if bbox is None:
        raise ValueError(f"Empty mascot: {path}")
    im = im.crop(bbox)
    scale = height / im.height
    return im.resize((round(im.width * scale), height), Image.Resampling.LANCZOS)

def paste_cat(cat, x, y):
    img.paste(cat, (int(x), int(y)), cat)

def bubble(x0, y0, x1, y1, s, tail, size=28, fill=(255, 255, 255), edge=INK):
    # tail: (tx, ty) point outside box
    d.rounded_rectangle((x0, y0, x1, y1), radius=26, fill=fill, outline=edge, width=4)
    tx, ty = tail
    # pick base on nearest side
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if tx > x1:   base = [(x1 - 2, cy - 22), (x1 - 2, cy + 22)]
    elif tx < x0: base = [(x0 + 2, cy - 22), (x0 + 2, cy + 22)]
    elif ty > y1: base = [(cx - 22, y1 - 2), (cx + 22, y1 - 2)]
    else:         base = [(cx - 22, y0 + 2), (cx + 22, y0 + 2)]
    d.polygon([base[0], base[1], (tx, ty)], fill=fill, outline=edge, width=4)
    d.polygon([base[0], base[1], (tx, ty)], fill=fill)
    # redraw inner edge fix
    d.line([base[0], (tx, ty)], fill=edge, width=4); d.line([base[1], (tx, ty)], fill=edge, width=4)
    f = F(size, False)
    lines = wrap(s, f, (x1 - x0) - 50)
    lh = int(size * 1.45)
    y = cy - len(lines) * lh / 2 + 4
    for l in lines:
        d.text((x0 + 25, y), l, font=f, fill=INK); y += lh

cat_teacher = load_cat((HERE / "cats" / "cat_teacher.png"), 250)
cat_det = load_cat((HERE / "cats" / "cat_detective.png"), 165)
cat_clip = load_cat((HERE / "cats" / "cat_clipboard.png"), 240)
cat_broom = load_cat((HERE / "cats" / "cat_broom.png"), 170)
cat_dizzy = load_cat((HERE / "cats" / "cat_dizzy.png"), 190)
cat_shield = load_cat((HERE / "cats" / "cat_shield.png"), 175)
cat_storyteller = load_cat((HERE / "cats" / "cat_storyteller.png"), 285)

# =================== HEADER ===================
d.text((80, 60), "The Vibe Coding Workflow", font=F(66), fill=INK)
d.text((84, 160), "One person + one agent. A closed loop, guided by cats.", font=F(30, False), fill=GRAY)
paste_cat(cat_teacher, 1640, 10)
bubble(1100, 40, 1600, 215, "Not sure what to type?\nStart with /vibe.\nLet's find your next step.", (1650, 150), size=27)

# =================== SETUP BAND ===================
panel(80, 330, 1920, 650, "setup", "Step 0 · Foundations", "once per repo, before publishing issues or building")
node(430, 510, 560, 150, "setup", cmd="/setup-matt-pocock-skills", cmd_size=30, label="where issues live, where the glossary goes", note="solo project: pick Local markdown")
arrow([(715, 510), (785, 510)])
node(1105, 510, 620, 150, "setup", cmd="/setup-feedback-loops", cmd_size=30, label="typecheck · lint · test · smoke\nlogs · browser · one command for all", note="watch every check go red once")
text(1450, 400, "Why feedback loops first?", F(28), fill=LANES["setup"]["dark"])
text(1450, 448, "tdd runs tests, verify boots the app, diagnosing-bugs reads logs. Without loops, every skill is guessing.", F(25, False), fill=GRAY, maxw=440, spacing=1.4)

# =================== BUILD LANE (left) ===================
BX0, BY0, BX1, BY1 = 80, 730, 1240, 2560
panel(BX0, BY0, BX1, BY1, "build", "① BUILD lane · I have an idea", "90% of your time is here")

node(660, 870, 240, 76, "build", label="★ an idea")
arrow([(660, 912), (660, 940)])
diamond(660, 1010, 360, 130, "build", "How big is it?")

# three branches
arrow([(480, 1010), (250, 1010), (250, 1080)])
arrow([(840, 1010), (1050, 1010), (1050, 1080)])
arrow([(660, 1075), (660, 1080)])
edge_label(250, 1112, "S · one clear sentence", LANES["build"]["dark"])
edge_label(660, 1112, "M · one sitting, open questions", LANES["build"]["dark"])
edge_label(1050, 1112, "L · several evenings", LANES["build"]["dark"])

# S column
s_box = node(250, 1260, 330, 150, "build", label="Just say it", note="“add --json to export,\ntest first”\nthe agent uses tdd itself")
arrow([(250, s_box[3]), (250, 1920)])
# M column
m1_box = node(660, 1240, 360, 150, "build", cmd="/grill-with-docs", cmd_size=32, note="asks in rounds; writes\nCONTEXT.md and ADRs")
m2_cy = place_below(m1_box, 350, 130, cmd="/implement", note="same window,\ndon't clear in between")
m2_box = node(660, m2_cy, 350, 130, "build", cmd="/implement", note="same window,\ndon't clear in between")
arrow([(660, m1_box[3]), (660, m2_box[1])])
arrow([(660, m2_box[3]), (660, 1920)])
# L column
l1_box = node(1050, 1220, 360, 110, "build", cmd="/grill-with-docs", cmd_size=32, note="stuck? try a prototype")
l2_cy = place_below(l1_box, 360, 100, cmd="/to-spec", note="synthesis, no questions")
l2_box = node(1050, l2_cy, 360, 100, "build", cmd="/to-spec", note="synthesis, no questions")
arrow([(1050, l1_box[3]), (1050, l2_box[1])])
l3_cy = place_below(l2_box, 360, 130, cmd="/to-tickets", note="slices + blocking edges\n(steps 1 to 3: one window)")
l3_box = node(1050, l3_cy, 360, 130, "build", cmd="/to-tickets", note="slices + blocking edges\n(steps 1 to 3: one window)")
arrow([(1050, l2_box[3]), (1050, l3_box[1])])
l4_cy = place_below(l3_box, 360, 100, cmd="/clear → /implement", cmd_size=26, note="a fresh window per ticket")
l4_box = node(1050, l4_cy, 360, 100, "build", cmd="/clear → /implement", cmd_size=26, note="a fresh window per ticket")
arrow([(1050, l3_box[3]), (1050, l4_box[1])])
arrow([(1050, l4_box[3]), (1050, 1920)])

# converge into implement internals box
d.line([(250, 1920), (1050, 1920)], fill=INK, width=6)
arrow([(660, 1920), (660, 1955)])

IX0, IY0, IX1, IY1 = 100, 1960, 1225, 2300
rbox(IX0, IY0, IX1, IY1, (245, 249, 255), LANES["build"]["edge"], r=28, width=4)
d.text((IX0 + 24, IY0 + 18), "What happens inside /implement (automatic; you only read the results)", font=F(30), fill=LANES["build"]["dark"])
chain = [("tdd", "red, then green\none slice at a time"), ("verify", "really runs it\nscreenshot as proof"), ("test-audit", "do tests guard logic?\nyou get a Claims list"), ("code-review", "standards + spec\n(+ security)"), ("commit", "ends with a\nChecks run ledger")]
step = ((IX1 - IX0) - 60) / 5
chain_cy = IY0 + 120
for i, (c, n) in enumerate(chain):
    cx = IX0 + 30 + step / 2 + i * step
    node(cx, chain_cy, 180, 66, "build", cmd=c, cmd_size=22, pad=30)
    text(cx, IY0 + 170, n, F(21, False), fill=GRAY, align="center", spacing=1.3)
    if i < len(chain) - 1:
        arrow([(cx + 92, chain_cy), (cx + 121, chain_cy)], width=5, head=15)
text(IX0 + 24, IY0 + 255, "Every FAIL and surviving mutant goes back to tdd as a new red test. No review while a FAIL is open.", F(24, False), fill=GRAY, maxw=1090, spacing=1.4)

# clipboard cat + bubble (bottom of build panel)
paste_cat(cat_clip, 120, 2300)
bubble(400, 2315, 1200, 2485, "Read test-audit's Claims list! Each line is one business rule. The test and the code can share the same misunderstanding and be green together; no tool catches that. You can, at a glance.", (395, 2400), size=26)

# =================== RIGHT COLUMN ===================
RX0, RX1 = 1300, 1920

# FIX
panel(RX0, 730, RX1, 1330, "fix", "② FIX lane · it broke")
diamond(1610, 880, 340, 120, "fix", "Know the cause?")
arrow([(1440, 880), (1450, 880), (1450, 955)])
edge_label(1450, 918, "yes", LANES["fix"]["dark"], 22)
node(1450, 1050, 260, 140, "fix", label="Say it, test first", note="red → fix → green")
arrow([(1780, 880), (1780, 955)])
edge_label(1780, 918, "no / flaky / slow", LANES["fix"]["dark"], 22)
node(1780, 1050, 260, 140, "fix", cmd="/diagnosing-bugs", cmd_size=20, note="six phases, no\nguessing first")
paste_cat(cat_det, 1320, 1150)
bubble(1560, 1150, 1900, 1300, "No command that goes red on the bug, no theorising. That rule is the whole skill.", (1555, 1225), size=24)

# REVIEW
panel(RX0, 1390, RX1, 1950, "review", "③ REVIEW · before merge")
r1_box = node(1690, 1540, 430, 140, "review", cmd="/code-review main", cmd_size=30, note="two sub-agents in parallel:\nStandards axis + Spec axis")
r2_cy = place_below(r1_box, 430, 140, cmd="security-review", cmd_size=30, note="auto on auth / routes / queries;\nonce more before shipping")
r2_box = node(1690, r2_cy, 430, 140, "review", cmd="security-review", cmd_size=30, note="auto on auth / routes / queries;\nonce more before shipping")
arrow([(1690, r1_box[3]), (1690, r2_box[1])])
paste_cat(cat_shield, 1310, 1785)
bubble(1480, 1830, 1900, 1940, "Five checks. That is how solo apps get hacked.", (1452, 1885), size=22)

# TIDY
panel(RX0, 2010, RX1, 2560, "tidy", "④ TIDY · every few days")
t1_box = node(1670, 2160, 440, 130, "tidy", cmd="/improve-codebase-architecture", cmd_size=21, note="report of shallow modules;\npick one, it grills you")
t2_cy = place_below(t1_box, 440, 130, label="idea → back to ① BUILD", note="“no seam” from a diagnosis\nlands here too")
t2_box = node(1670, t2_cy, 440, 130, "tidy", label="idea → back to ① BUILD", note="“no seam” from a diagnosis\nlands here too")
arrow([(1670, t1_box[3]), (1670, t2_box[1])])
paste_cat(cat_broom, 1305, 2335)
bubble(1480, 2440, 1900, 2540, "Sweep: no more seven-file\nhops per change.", (1452, 2490), size=22)

# =================== SESSION BAND: refocus / handoff / takeover ===================
panel(80, 2640, 1920, 3120, "focus", "Session trouble? Three moves", "drifting in this window · leaving on purpose · the old session is gone")
paste_cat(cat_dizzy, 130, 2730)
SX = [520, 1000, 1480]
node(SX[0], 2800, 420, 120, "focus", cmd="/refocus", label="still open, drifting, staying here")
node(SX[1], 2800, 420, 120, "focus", cmd="/handoff", label="still open, the work is moving")
node(SX[2], 2800, 420, 120, "focus", cmd="/takeover", label="session gone / too long to trust")
text(SX[0], 2895, "Re-reads spec, ticket, CONTEXT.md and your spoken decisions from disk, diffs them against the work (dropped / drifted / contradicted), asks one round, saves the answers to the ticket. Then compact.", F(23, False), fill=INK, maxw=440, align="center", spacing=1.4)
text(SX[1], 2895, "The outgoing session writes a small portable file to the temp dir: new directory, new tool, a forked side task, a prototype detour. Nothing travelling? You don't need it.", F(23, False), fill=INK, maxw=440, align="center", spacing=1.4)
text(SX[2], 2895, "Quota gone, crashed, closed, or another tool. The new session reads the record itself (ID / export / URL / handoff), retells the project in 10 sentences at most, asks once. Read-only until you confirm.", F(23, False), fill=INK, maxw=440, align="center", spacing=1.4)

# =================== BOTTOM: context rules + stuck ===================
panel(80, 3200, 1010, 3660, "setup", "Context rules (these seven are enough)")
rules = [("story / grill → spec → tickets", "", "one window, don't clear"),
         ("between tickets", "/clear", ", fresh window"),
         ("agent drifted", "/refocus", ", before compact"),
         ("new dir / tool / fork", "/handoff", ""),
         ("old session gone", "/takeover", " its record"),
         ("needs running code", "/handoff", " → prototype → answer back"),
         ("didn't follow it", "/wait-what", "")]
y = 3280
for a, cmd, rest in rules:
    d.text((120, y), a, font=F(25), fill=INK)
    x = 520
    if cmd:
        d.text((x, y + 2), cmd, font=MONO(25), fill=LANES["build"]["dark"]); x += MONO(25).getlength(cmd)
    if rest:
        d.text((x, y), rest, font=F(25, False), fill=LANES["build"]["dark"])
    y += 52

panel(1050, 3200, 1920, 3660, "fix", "Wrong three times? Stop!")
text(1090, 3260, "No fifth attempt. Discard it, /clear, and write one sentence:", F(26, False), fill=INK, maxw=790)
rbox(1090, 3310, 1880, 3380, (255, 255, 255), LANES["fix"]["edge"], r=18, width=3)
text(1485, 3328, "When I input ___, I expect ___, but I get ___", F(28), fill=LANES["fix"]["dark"], align="center")
text(1090, 3405, "Can't write it → not a bug, misaligned requirements → /refocus or\n/grill-with-docs\nCan write it → turn it into one failing test first:\n    green after one fix → there was no feedback loop (tdd)\n    stays red / fixing it breaks something else → real bug (/diagnosing-bugs)\n    every attempt touches five files → no seam (④ TIDY)", F(23, False), fill=INK, maxw=790, spacing=1.5)

# =================== FOOTER ===================
d.line([(80, 3720), (1920, 3720)], fill=(210, 200, 185), width=3)
text(80, 3745, "First time? Type /vibe in an empty repo: a First run card walks 9 steps through the whole loop and checks each step with you.", F(27), fill=INK, maxw=1840)
text(80, 3788, "Handbook: skills/engineering/vibe/WORKFLOW.md   ·   26 curated skills: 15 you type, 11 automatic   ·   github.com/awangs1986/popcodeskills", F(24, False), fill=GRAY, maxw=1840)
text(80, 3828, "Mantra: align, then spec; red, then green; run it; read the Claims; review before merge; sweep weekly; drifting → refocus, dead → takeover.", F(26), fill=LANES["build"]["dark"], maxw=1840)

# =================== PRODUCT STORY ON-RAMP ===================
# Insert a band after the header, keeping the four-lane map's coordinates intact.
# Header artwork ends above this cut; the setup title starts below it.
FLOW_TOP, STORY_HEIGHT = 280, 520
flow = img
img = Image.new("RGB", (W, H + STORY_HEIGHT), BG)
img.paste(flow.crop((0, 0, W, FLOW_TOP)), (0, 0))
img.paste(flow.crop((0, FLOW_TOP, W, H)), (0, FLOW_TOP + STORY_HEIGHT))
d = ImageDraw.Draw(img)

panel(80, 330, 1920, 790, "story", "Before the build · Tell a Story", "First align the experience. Optional; no setup needed.")
d.ellipse((100, 410, 405, 715), fill=LANES["story"]["fill"])
paste_cat(cat_storyteller, 105, 425)
text(252, 725, "The calico storyteller", F(23), fill=LANES["story"]["dark"], align="center")
text(440, 418, "/tell-a-story", MONO(38), fill=LANES["story"]["dark"])
text(820, 430, "Choose 1 or 2. Change the story together.", F(25, False), fill=GRAY)

rbox(430, 495, 850, 655, LANES["story"]["fill"], LANES["story"]["edge"], r=22, width=3)
d.ellipse((453, 516, 497, 560), fill=LANES["story"]["edge"])
d.text((475, 538), "1", font=F(28), fill="white", anchor="mm")
text(515, 514, "You tell", F(30), fill=LANES["story"]["dark"])
text(455, 568, "A person, a goal,\nthe experience you want.", F(24, False), maxw=370, spacing=1.3)

rbox(885, 495, 1305, 655, LANES["story"]["fill"], LANES["story"]["edge"], r=22, width=3)
d.ellipse((908, 516, 952, 560), fill=LANES["story"]["edge"])
d.text((930, 538), "2", font=F(28), fill="white", anchor="mm")
text(970, 514, "Agent tells", F(30), fill=LANES["story"]["dark"])
text(910, 568, "A story from the code.\nYou react and correct.", F(24, False), maxw=370, spacing=1.3)

arrow([(1325, 575), (1410, 575)], color=LANES["story"]["edge"], width=5, head=18)
node(1650, 575, 440, 170, "story", cmd="SPEC / BACKLOG", label="Both, or just the story", note="Only after you confirm", cmd_size=29)
text(440, 678, "Tell → react → revise → confirm", F(28), fill=LANES["story"]["dark"])
text(440, 730, "Code-backed facts and wishes stay separate. Drafts only; no code or published issues.", F(24, False), fill=GRAY, maxw=1440, spacing=1.25)

img.save(str(HERE.parent / "vibe-workflow-poster.png"), optimize=True)
print("saved")
