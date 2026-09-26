# Chinese edition of the vibe workflow poster.
#
# Renders ../vibe-workflow-poster.zh-CN.png from the same handbook, with the
# same sections and commands as build_poster.py. Layout differences are fixes:
# subtitles sit inside their panel instead of on its border, nodes grow to fit
# their text, and the implement chain is computed from the box width.
#
# Fonts: same directory as the English poster (see README.md in this folder).
# The Chinese strings below are readable on purpose; scripts/check-skills.mjs
# and CLAUDE.md carry a narrow exception for this one file.
#
#   POSTER_FONTS=docs/engineering/poster/fonts python3 docs/engineering/poster/build_poster_zh.py

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
d.text((80, 60), "Vibe Coding 工作流", font=F(66), fill=INK)
d.text((84, 160), "一个人 + 一个 agent，一条闭环，一群猫咪带路", font=F(30, False), fill=GRAY)
paste_cat(cat_teacher, 1640, 10)
bubble(1100, 40, 1600, 215, "不知道下一步敲什么？\n先来 /vibe。\n我带你找到下一步。", (1650, 150), size=27)

# =================== SETUP BAND ===================
panel(80, 330, 1920, 650, "setup", "第 0 步 · 地基", "每个仓库做一次，发布 issue 或动手开发之前先配好")
node(430, 510, 560, 150, "setup", cmd="/setup-matt-pocock-skills", cmd_size=30, label="issue 存哪，词汇表放哪", note="个人项目：选本地 Markdown")
arrow([(715, 510), (785, 510)])
node(1105, 510, 620, 150, "setup", cmd="/setup-feedback-loops", cmd_size=30, label="typecheck · lint · 测试 · 冒烟\n日志 · 浏览器 · 一条命令全跑", note="每条检查都亲眼看它红一次")
text(1450, 400, "为啥先接反馈回路？", F(28), fill=LANES["setup"]["dark"])
text(1450, 448, "tdd 要跑测试，verify 要起应用，diagnosing-bugs 要读日志。没有回路，每个 skill 都是在蒙。", F(25, False), fill=GRAY, maxw=440, spacing=1.4)

# =================== BUILD LANE (left) ===================
BX0, BY0, BX1, BY1 = 80, 730, 1240, 2560
panel(BX0, BY0, BX1, BY1, "build", "① Build 车道 · 我有个想法", "九成时间都在这里")

node(660, 870, 240, 76, "build", label="★ 一个想法")
arrow([(660, 912), (660, 940)])
diamond(660, 1010, 360, 130, "build", "有多大？")

# three branches
arrow([(480, 1010), (250, 1010), (250, 1080)])
arrow([(840, 1010), (1050, 1010), (1050, 1080)])
arrow([(660, 1075), (660, 1080)])
edge_label(250, 1112, "S · 一句话能说清", LANES["build"]["dark"])
edge_label(660, 1112, "M · 一次做完，还有问题没想明白", LANES["build"]["dark"])
edge_label(1050, 1112, "L · 得花好几个晚上", LANES["build"]["dark"])

# S column
s_box = node(250, 1260, 330, 150, "build", label="直接说", note="“加 --json，先写测试”\nagent 自己会用 tdd")
arrow([(250, s_box[3]), (250, 1920)])
# M column
m1_box = node(660, 1240, 360, 150, "build", cmd="/grill-with-docs", cmd_size=32, note="分轮提问\n写 CONTEXT.md 和 ADR")
arrow([(660, m1_box[3]), (660, m1_box[3] + 30)])
m2_box = node(660, 1430, 350, 130, "build", cmd="/implement", note="同一个窗口\n中间别 clear")
arrow([(660, m2_box[3]), (660, 1920)])
# L column
l1_box = node(1050, 1210, 360, 110, "build", cmd="/grill-with-docs", cmd_size=32, note="卡住了？先做个原型")
arrow([(1050, l1_box[3]), (1050, l1_box[3] + 28)])
l2_box = node(1050, 1375, 360, 100, "build", cmd="/to-spec", note="只整理，不提问")
arrow([(1050, l2_box[3]), (1050, l2_box[3] + 28)])
l3_box = node(1050, 1580, 360, 130, "build", cmd="/to-tickets", note="切片 + 阻塞关系\n（第1-3步：同一窗口）")
arrow([(1050, l3_box[3]), (1050, l3_box[3] + 28)])
l4_box = node(1050, 1780, 360, 100, "build", cmd="/clear → /implement", cmd_size=26, note="一张 ticket 一个窗口")
arrow([(1050, l4_box[3]), (1050, 1920)])

# converge into implement internals box
d.line([(250, 1920), (1050, 1920)], fill=INK, width=6)
arrow([(660, 1920), (660, 1955)])

IX0, IY0, IX1, IY1 = 130, 1960, 1190, 2300
rbox(IX0, IY0, IX1, IY1, (245, 249, 255), LANES["build"]["edge"], r=28, width=4)
d.text((IX0 + 24, IY0 + 18), "/implement 里面自动发生（你只看结果）", font=F(30), fill=LANES["build"]["dark"])
chain = [("tdd", "先红后绿\n一次一小片"), ("verify", "真跑起来\n截图为证"), ("test-audit", "测试有用？\n看 Claims"), ("code-review", "规范 + spec\n（含安全）"), ("commit", "提交并附上\nChecks 台账")]
step = ((IX1 - IX0) - 80) / 5
chain_cy = IY0 + 160
for i, (c, n) in enumerate(chain):
    cx = IX0 + 40 + step / 2 + i * step
    node(cx, chain_cy, step - 26, 120, "build", cmd=c, cmd_size=22, note=n, pad=24)
    if i < len(chain) - 1:
        arrow([(cx + (step - 26) / 2 + 2, chain_cy), (cx + step - (step - 26) / 2 - 2, chain_cy)], width=5, head=15)
text(IX0 + 24, IY0 + 255, "每个 FAIL 和活下来的变异体都会打回 tdd，变成新的红测试。有 FAIL 没清，就不 review。", F(24, False), fill=GRAY, maxw=1010, spacing=1.4)

# clipboard cat + bubble (bottom of build panel)
paste_cat(cat_clip, 120, 2300)
bubble(400, 2315, 1200, 2485, "重点看 test-audit 的 Claims 清单！每行都是一条业务规则。测试和代码可能错在同一个地方，还一起变绿，工具抓不住，你扫一眼就行。", (395, 2400), size=26)

# =================== RIGHT COLUMN ===================
RX0, RX1 = 1300, 1920

# FIX
panel(RX0, 730, RX1, 1330, "fix", "② Fix 车道 · 坏了")
diamond(1610, 880, 340, 120, "fix", "知道原因吗？")
arrow([(1440, 880), (1450, 880), (1450, 955)])
edge_label(1450, 918, "知道", LANES["fix"]["dark"], 22)
node(1450, 1050, 240, 140, "fix", label="直接说", note="先写测试\n变红 → 修 → 变绿")
arrow([(1780, 880), (1780, 955)])
edge_label(1780, 918, "不知道 / 时好时坏 / 变慢", LANES["fix"]["dark"], 20)
node(1780, 1050, 240, 140, "fix", cmd="/diagnosing-bugs", cmd_size=20, note="六个阶段\n先不许猜")
paste_cat(cat_det, 1320, 1150)
bubble(1560, 1150, 1900, 1300, "拿出让 bug 变红的命令之前，不许猜原因。这条规矩就是这个 skill 的全部。", (1555, 1225), size=25)

# REVIEW
panel(RX0, 1390, RX1, 1950, "review", "③ Review · 合并之前")
r1_box = node(1690, 1540, 430, 140, "review", cmd="/code-review main", cmd_size=30, note="两个检查并排跑：\n规范 + spec")
arrow([(1690, r1_box[3]), (1690, r1_box[3] + 30)])
r2_box = node(1690, 1740, 430, 140, "review", cmd="security-review", cmd_size=30, note="碰到鉴权 / 路由 / 查询就跟上；\n发到网上之前再跑一次")
paste_cat(cat_shield, 1310, 1785)
bubble(1480, 1830, 1900, 1940, "五项检查，个人项目就栽在这上面。", (1452, 1885), size=22)

# TIDY
panel(RX0, 2010, RX1, 2560, "tidy", "④ Tidy · 每隔几天")
t1_box = node(1670, 2160, 440, 130, "tidy", cmd="/improve-codebase-architecture", cmd_size=21, note="浅模块报告；\n挑一个，它来问你")
arrow([(1670, t1_box[3]), (1670, t1_box[3] + 30)])
t2_box = node(1670, 2350, 440, 130, "tidy", label="想法 → 回到 ① Build", note="“没有接缝”的诊断结论\n也落到这里")
paste_cat(cat_broom, 1305, 2335)
bubble(1480, 2440, 1900, 2540, "扫一扫：改一处不再跳七个文件。", (1452, 2490), size=22)

# =================== SESSION BAND: refocus / handoff / takeover ===================
panel(80, 2640, 1920, 3120, "focus", "会话出状况？三招", "这个窗口跑偏了 · 要主动离开 · 旧会话没了")
paste_cat(cat_dizzy, 130, 2730)
SX = [520, 1000, 1480]
node(SX[0], 2800, 420, 120, "focus", cmd="/refocus", label="还开着，跑偏了，不换地方")
node(SX[1], 2800, 420, 120, "focus", cmd="/handoff", label="还开着，工作要搬走")
node(SX[2], 2800, 420, 120, "focus", cmd="/takeover", label="会话没了 / 太长了不敢信")
text(SX[0], 2895, "对照磁盘上的 spec、ticket、CONTEXT.md 和你说过的决定，检查做出来的东西（丢了 / 偏了 / 矛盾了），问一轮，答案写回 ticket。然后再 compact。", F(23, False), fill=INK, maxw=440, align="center", spacing=1.4)
text(SX[1], 2895, "离开的会话写个小文件放临时目录：换目录、换工具、分叉支线任务、绕道做原型。没有东西要带走？那就不需要它。", F(23, False), fill=INK, maxw=440, align="center", spacing=1.4)
text(SX[2], 2895, "额度用完、崩溃、关掉，或者换了工具。新会话自己读记录（ID / 导出 / URL / handoff），十句话以内复述项目，问一次。你确认之前它是只读的。", F(23, False), fill=INK, maxw=440, align="center", spacing=1.4)

# =================== BOTTOM: context rules + stuck ===================
panel(80, 3200, 1010, 3660, "setup", "上下文规则（记住这七条就够了）")
rules = [("故事 / 访谈 → spec → tickets", "", "同一个窗口，别 clear"),
         ("ticket 之间", "/clear", "，开新窗口"),
         ("agent 跑偏了", "/refocus", "，compact 之前先跑它"),
         ("换目录 / 换工具 / 分叉", "/handoff", ""),
         ("旧会话没了", "/takeover", "，拿它的记录接上"),
         ("要跑代码才答得上来", "/handoff", " → 原型 → 答案带回"),
         ("没听懂它在说啥", "/wait-what", "")]
y = 3280
for a, cmd, rest in rules:
    d.text((120, y), a, font=F(25), fill=INK)
    x = 560
    if cmd:
        d.text((x, y + 2), cmd, font=MONO(25), fill=LANES["build"]["dark"]); x += MONO(25).getlength(cmd)
    if rest:
        d.text((x, y), rest, font=F(25, False), fill=LANES["build"]["dark"])
    y += 52

panel(1050, 3200, 1920, 3660, "fix", "错了三次？停！")
text(1090, 3260, "别试第四第五次。扔掉它，/clear，然后写一句话：", F(26, False), fill=INK, maxw=790)
rbox(1090, 3310, 1880, 3380, (255, 255, 255), LANES["fix"]["edge"], r=18, width=3)
text(1485, 3328, "当我输入 ___，我期望 ___，但得到 ___", F(28), fill=LANES["fix"]["dark"], align="center")
text(1090, 3405, "写不出来 → 不是 bug，是需求没对上 → /refocus 或 /grill-with-docs\n写得出来 → 先把它变成一个失败的测试：\n    一次修好就绿了 → 当时缺反馈回路（tdd）\n    一直红 / 修好这个坏了那个 → 真 bug（/diagnosing-bugs）\n    每次改动都碰五个文件 → 没接缝（④ Tidy）", F(24, False), fill=INK, spacing=1.5)

# =================== FOOTER ===================
d.line([(80, 3720), (1920, 3720)], fill=(210, 200, 185), width=3)
text(80, 3745, "第一次来？空仓库里敲 /vibe：一张 First run 卡片带你九步走完整个闭环，每步都跟你确认。", F(27), fill=INK, maxw=1840)
text(80, 3788, "完整手册：skills/engineering/vibe/WORKFLOW.md   ·   26 个精选 skill，15 个你来敲，11 个 agent 自己用   ·   github.com/awangs1986/popcodeskills", F(24, False), fill=GRAY, maxw=1840)
text(80, 3828, "口诀：先对齐，再写 spec；先变红，再变绿；跑起来；看 Claims；合并前先 review；每周扫一次；跑偏了 refocus，没了 takeover。", F(26), fill=LANES["build"]["dark"], maxw=1840)

# =================== PRODUCT STORY ON-RAMP ===================
# Insert a band after the header, keeping the four-lane map's coordinates intact.
# Header artwork ends above this cut; the setup title starts below it.
FLOW_TOP, STORY_HEIGHT = 280, 520
flow = img
img = Image.new("RGB", (W, H + STORY_HEIGHT), BG)
img.paste(flow.crop((0, 0, W, FLOW_TOP)), (0, 0))
img.paste(flow.crop((0, FLOW_TOP, W, H)), (0, FLOW_TOP + STORY_HEIGHT))
d = ImageDraw.Draw(img)

panel(80, 330, 1920, 790, "story", "动手之前 · 先讲个故事", "先对齐产品体验。按需使用，不用先做初始化。")
d.ellipse((100, 410, 405, 715), fill=LANES["story"]["fill"])
paste_cat(cat_storyteller, 105, 425)
text(252, 725, "讲故事的三花猫", F(23), fill=LANES["story"]["dark"], align="center")
text(440, 418, "/tell-a-story", MONO(38), fill=LANES["story"]["dark"])
text(820, 430, "选 1 或 2，一起把故事改到对上。", F(25, False), fill=GRAY)

rbox(430, 495, 850, 655, LANES["story"]["fill"], LANES["story"]["edge"], r=22, width=3)
d.ellipse((453, 516, 497, 560), fill=LANES["story"]["edge"])
d.text((475, 538), "1", font=F(28), fill="white", anchor="mm")
text(515, 514, "你来讲", F(30), fill=LANES["story"]["dark"])
text(455, 568, "谁在用，要做成什么事，\n用起来该是什么体验。", F(24, False), maxw=370, spacing=1.3)

rbox(885, 495, 1305, 655, LANES["story"]["fill"], LANES["story"]["edge"], r=22, width=3)
d.ellipse((908, 516, 952, 560), fill=LANES["story"]["edge"])
d.text((930, 538), "2", font=F(28), fill="white", anchor="mm")
text(970, 514, "Agent 来讲", F(30), fill=LANES["story"]["dark"])
text(910, 568, "照着当前代码讲个故事，\n你来听、纠正、补充。", F(24, False), maxw=370, spacing=1.3)

arrow([(1325, 575), (1410, 575)], color=LANES["story"]["edge"], width=5, head=18)
node(1650, 575, 440, 170, "story", cmd="SPEC / BACKLOG", label="两者都要 / 只保留故事", note="你确认后，才整理", cmd_size=29)
text(440, 678, "先讲 → 再聊 → 多轮修改 → 确认故事", F(28), fill=LANES["story"]["dark"])
text(440, 730, "分清已有、待确认、希望新增。只做产品草稿，不自动写代码或发布 issue。", F(24, False), fill=GRAY, maxw=1440, spacing=1.25)

img.save(str(HERE.parent / "vibe-workflow-poster.zh-CN.png"), optimize=True)
print("saved")
