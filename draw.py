#!/usr/bin/env python3
"""Draw the news-image-20261124 front page (1024x1024 PNG).

Fresh build for Tuesday 24 November 2026. Run locally only:
    python3 draw.py            # writes entry.png next to this file
The grader never runs this file; main.ts only copies entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

INK = (17, 17, 17)
PAPER = (255, 255, 255)
RED = (196, 18, 28)
DARKRED = (140, 10, 18)
GREY = (110, 110, 110)
LIGHT = (242, 242, 240)
MIDGREY = (226, 226, 222)
NAVY = (16, 32, 64)
TEAL = (18, 96, 110)
GOLD = (212, 160, 23)

FD = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def tw(text, f):
    return d.textlength(text, font=f)

def wrap(text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def block(x, y, max_w, lines, f, fill=INK, leading=None, align="left"):
    """Draw wrapped lines; return bottom y. Raises if a line is too wide."""
    lh = leading or int(f.size * 1.18)
    yy = y
    for ln in lines:
        assert tw(ln, f) <= max_w + 1, f"OVERFLOW: {ln!r} width {tw(ln, f)} > {max_w}"
        if align == "center":
            d.text((x + (max_w - tw(ln, f)) / 2, yy), ln, font=f, fill=fill)
        else:
            d.text((x, yy), ln, font=f, fill=fill)
        yy += lh
    return yy

def centre(x, y, w, text, f, fill=INK):
    d.text((x + (w - tw(text, f)) / 2, y), text, font=f, fill=fill)

# ---------------------------------------------------------------- top strip
d.rectangle([0, 0, W, 26], fill=INK)
d.text((10, 5), "TUESDAY 24 NOVEMBER 2026", font=SANS_B(13), fill=(255, 255, 255))
r = "THE WORLD IN ONE PAGE  •  35 STORIES  •  9 REGIONS"
d.text((W - 10 - tw(r, SANS_B(13)), 5), r, font=SANS_B(13), fill=(255, 255, 255))

# ---------------------------------------------------------------- masthead
centre(0, 32, W, "THE WORLD TODAY", SERIF_B(56), INK)
d.rectangle([24, 96, W - 24, 99], fill=RED)
centre(0, 104, W, "Tuesday 24 November 2026 — every story checked against the day's wires",
       SANS(14), (60, 60, 60))

# ---------------------------------------------------------------- UTC timeline
TY, TH = 124, 42
d.rectangle([10, TY, W - 10, TY + TH], outline=(180, 180, 180), width=1)
d.rectangle([10, TY, 118, TY + TH], fill=INK)
d.text((18, TY + 7), "THE DAY", font=SANS_B(13), fill=(255, 255, 255))
d.text((18, TY + 24), "IN UTC", font=SANS_B(13), fill=(255, 255, 255))
timeline = [
    ("08:57", "EU budget talks fail"),
    ("10:16", "Dymer toll hits 12"),
    ("12:03", "UK sanctions Houthis"),
    ("13:49", "Iran shuts Hormuz tighter"),
    ("15:03", "Wall St reverses; Nvidia -6%"),
    ("20:40", "Kyiv-region toll confirmed"),
    ("EVE", "Riyadh tower hit; 11 hurt"),
]
col_w = (W - 10 - 118 - 8) / 7
for i, (t, ev) in enumerate(timeline):
    x = 118 + 8 + i * col_w
    d.text((x, TY + 5), t, font=SANS_B(12), fill=RED)
    for j, ln in enumerate(wrap(ev, SANS(10), col_w - 6)):
        d.text((x, TY + 21 + j * 12), ln, font=SANS(10), fill=INK)
    if i:
        d.line([x - 4, TY + 4, x - 4, TY + TH - 4], fill=MIDGREY)

# ---------------------------------------------------------------- 6 big numbers
NY, NH = 174, 60
numbers = [
    ("11", "HURT IN RIYADH TOWER ATTACK"),
    ("4", "TANKERS HIT MINES IN HORMUZ"),
    ("50,018", "DOW'S FIRST CLOSE ABOVE 50K"),
    ("460,000+", "RUSSIAN DEATHS COUNTED"),
    ("5,258", "UK HEAT DEATHS IN 2026"),
    ("96", "DRONES FIRED AT UKRAINE"),
]
bw = (W - 20 - 5 * 6) / 6
for i, (num, lab) in enumerate(numbers):
    x = 10 + i * (bw + 6)
    d.rectangle([x, NY, x + bw, NY + NH], outline=(200, 200, 200), width=1)
    d.rectangle([x, NY, x + bw, NY + 4], fill=RED)
    centre(x, NY + 9, bw, num, SANS_B(27), RED if i % 2 == 0 else INK)
    for j, ln in enumerate(wrap(lab, SANS_B(9), bw - 8)):
        centre(x, NY + 40 + j * 11, bw, ln, SANS_B(9), (70, 70, 70))

# ---------------------------------------------------------------- region bar
RY, RH = 242, 20
regions = [
    ("AMERICAS 6", 6, (31, 119, 180)),
    ("EUROPE 10", 10, (44, 130, 80)),
    ("MIDDLE EAST 9", 9, (196, 18, 28)),
    ("AFRICA 1", 1, (212, 160, 23)),
    ("EAST ASIA 4", 4, (120, 60, 150)),
    ("SE ASIA 2", 2, (18, 130, 120)),
    ("S. ASIA 1", 1, (230, 120, 20)),
    ("OCEANIA 1", 1, (90, 90, 90)),
    ("GLOBAL 1", 1, (150, 150, 150)),
]
x = 10
tot = sum(c for _, c, _ in regions)
for name, c, col in regions:
    wseg = (W - 20) * c / tot
    d.rectangle([x, RY, x + wseg, RY + RH], fill=col)
    if wseg > 52:
        centre(x, RY + 4, wseg, name, SANS_B(10), (255, 255, 255))
    x += wseg

# ---------------------------------------------------------------- hero scenes
def scene_riyadh(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(13, 22, 48))
    for sx, sy in [(30, 8), (90, 18), (160, 7), (240, 20), (700, 8), (790, 18),
                   (860, 7), (930, 16)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    # skyline silhouettes (kept inside the scene box)
    for bx, bw_, bh in [(0, 70, 22), (80, 54, 30), (150, 90, 20), (700, 80, 26),
                        (790, 60, 34), (860, 110, 20), (950, 54, 28)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw_, y + h], fill=(28, 44, 84))
    # KAFD tower: tall, tapering, lit windows
    tx, tw_, th = x + 300, 150, h - 4
    d.polygon([(tx, y + h), (tx + 22, y + h - th), (tx + tw_ - 22, y + h - th),
               (tx + tw_, y + h)], fill=(52, 84, 138))
    d.polygon([(tx + 22, y + h - th), (tx + tw_ - 22, y + h - th),
               (tx + tw_ - 8, y + h - th + 8), (tx + 8, y + h - th + 8)],
              fill=(120, 170, 220))
    for wy in range(y + h - th + 14, y + h - 6, 10):
        for wx in range(tx + 28, tx + tw_ - 28, 15):
            if (wx + wy) % 3:
                d.rectangle([wx, wy, wx + 8, wy + 5], fill=(255, 214, 90))
    # explosion + smoke at tower base, right side, inside the box
    d.ellipse([x + 470, y + h - 34, x + 540, y + h - 2], fill=(255, 122, 26))
    d.ellipse([x + 488, y + h - 46, x + 528, y + h - 16], fill=(255, 190, 60))
    d.ellipse([x + 500, y + h - 56, x + 548, y + h - 30], fill=(150, 150, 150))
    d.ellipse([x + 532, y + h - 58, x + 574, y + h - 34], fill=(120, 120, 120))
    d.polygon([(x + 478, y + h), (x + 496, y + h - 28), (x + 514, y + h - 6),
               (x + 532, y + h - 24), (x + 550, y + h)], fill=(255, 90, 20))

def scene_hormuz(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 205, 225))
    d.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(255, 214, 140))
    d.ellipse([x + w - 70, y + 8, x + w - 30, y + 48], fill=(255, 190, 60))
    # cliffs left and right
    d.polygon([(x, y + h), (x, y + 30), (x + 46, y + 44), (x + 40, y + h)], fill=(120, 90, 60))
    d.polygon([(x + w, y + h), (x + w, y + 26), (x + w - 44, y + 40), (x + w - 38, y + h)],
              fill=(120, 90, 60))
    # sea
    d.rectangle([x, y + int(h * 0.42), x + w, y + h], fill=(18, 96, 130))
    for wy in (int(h * 0.55), int(h * 0.72), int(h * 0.88)):
        for wx in range(0, int(w), 34):
            d.arc([x + wx, y + wy, x + wx + 22, y + wy + 8], 0, 180, fill=(140, 205, 225))
    # tanker
    hx, hy = x + int(w * 0.22), y + int(h * 0.55)
    d.rectangle([hx, hy, hx + 190, hy + 20], fill=(30, 30, 34))
    d.rectangle([hx + 164, hy - 13, hx + 190, hy], fill=(30, 30, 34))
    for i, col in enumerate([(196, 18, 28), (31, 119, 180), (212, 160, 23), (44, 130, 80)]):
        d.rectangle([hx + 10 + i * 38, hy - 15, hx + 42 + i * 38, hy], fill=col)
    # mine + blast (kept inside the scene box, clear of the CONFIRMED tag)
    mx, my = x + int(w * 0.62), y + int(h * 0.68)
    d.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(20, 20, 20))
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([mx + dx * 11, my + dy * 11, mx + dx * 13, my + dy * 13],
               fill=(20, 20, 20), width=3)
    d.ellipse([mx - 22, my - 24, mx + 22, my + 2], fill=(255, 122, 26))
    d.ellipse([mx - 12, my - 16, mx + 12, my - 2], fill=(255, 190, 60))

def scene_dow(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 245, 233))
    for gy in range(0, int(h), 14):
        d.line([x, y + gy, x + w, y + gy], fill=(200, 220, 202))
    # candlesticks rising
    import random
    random.seed(7)
    cx = x + 14
    base = y + h - 12
    while cx < x + w - 110:
        ch = random.randint(8, 22)
        d.rectangle([cx, base - ch, cx + 12, base], fill=(34, 139, 34))
        d.line([cx + 6, base - ch - 6, cx + 6, base + 2], fill=(34, 139, 34), width=2)
        cx += 22
        base -= random.randint(2, 7)
    # green arrow line to 50,018
    pts = [(x + 10, y + h - 14), (x + int(w * 0.3), y + h - 30),
           (x + int(w * 0.55), y + h - 44), (x + int(w * 0.8), y + h - 58),
           (x + w - 12, y + 12)]
    d.line(pts, fill=(20, 110, 30), width=5, joint="curve")
    d.polygon([(x + w - 12, y + 12), (x + w - 34, y + 16), (x + w - 16, y + 32)],
              fill=(20, 110, 30))

# hero 1 — full width, red banner headline
HY = 268
d.rectangle([10, HY, W - 10, HY + 120], outline=(200, 200, 200), width=1)
scene_riyadh(11, HY + 1, W - 22, 58)
d.rectangle([10, HY + 59, W - 10, HY + 120], fill=RED)
d.text((20, HY + 63), "HOUTHIS HIT RIYADH TOWER", font=SANS_B(24), fill=(255, 255, 255))
d.text((20, HY + 93), "11 hurt as a skyscraper in the capital's financial district is struck — the war",
       font=SANS(12), fill=(255, 255, 255))
d.text((20, HY + 108), "reaches Saudi Arabia's gleaming KAFD quarter.",
       font=SANS(12), fill=(255, 255, 255))
d.rectangle([W - 130, HY + 63, W - 18, HY + 88], outline=(255, 255, 255), width=2)
centre(W - 130, HY + 67, 112, "CONFIRMED", SANS_B(12), (255, 255, 255))

# heroes 2 & 3 — side by side
HY2 = HY + 124
HW = (W - 20 - 8) / 2
for idx, (scene, head, sub, tag) in enumerate([
        (scene_hormuz, "IRAN SHUTS HORMUZ TIGHTER",
         "Four tankers hit mines as Tehran orders the strait closed until the US meets its demands.",
         "CONFIRMED"),
        (scene_dow, "DOW TOPS 50,000",
         "First close above 50k — even as Nvidia's relief rally fades, down 6% in a day.",
         "CONFIRMED"),
]):
    x = 10 + idx * (HW + 8)
    d.rectangle([x, HY2, x + HW, HY2 + 92], outline=(200, 200, 200), width=1)
    scene(x + 1, HY2 + 1, HW - 2, 44)
    lines = wrap(head, SANS_B(15), HW - 16)
    yy = block(x + 8, HY2 + 48, HW - 16, lines, SANS_B(15), INK, leading=17)
    block(x + 8, yy + 1, HW - 16, wrap(sub, SANS(10), HW - 16), SANS(10),
          (70, 70, 70), leading=12)
    d.rectangle([x + HW - 84, HY2 + 6, x + HW - 8, HY2 + 24], fill=RED)
    centre(x + HW - 84, HY2 + 8, 76, tag, SANS_B(9), (255, 255, 255))

# ---------------------------------------------------------------- secondary (10)
SY = HY2 + 96
secondaries = [
    ("HUAWEI CONVICTED IN US", "Guilty over Iran business and stolen trade secrets.", "gavel"),
    ("NVIDIA BOUNCE FADES", "Shares -6%; Anthropic falls below its IPO price.", "chart"),
    ("CHINA PROBES TOP OFFICIAL", "Politburo member Chen Jining under investigation.", "lens"),
    ("FLY WITH ME TO MOSCOW", "Lukashenko's offer to Zelenskyy: a joint trip for talks.", "plane"),
    ("ISRAEL'S FIRST COALITION DEAL", "Eisenkot signs a pact with Lieberman.", "flags"),
    ("BAGHDAD SEIZES KURD BORDERS", "PM takes over crossings after an oil-smuggling probe.", "gate"),
    ("UK SANCTIONS HOUTHIS", "Group designated; four senior figures targeted.", "stamp"),
    ("PUIGDEMONT AMNESTIED", "Spain's court closes the 2017 independence cases.", "scales"),
    ("SENEGAL ARE CHAMPIONS AGAIN", "CAS overturns CAF; the AFCON crown is restored.", "trophy"),
    ("UK HEAT DEATHS HIT RECORD", "5,258 died in 2026 — the worst year on record.", "sun"),
]

def mini_scene(kind, x, y, w, h):
    if kind == "gavel":
        d.rectangle([x, y, x + w, y + h], fill=(30, 42, 84))
        d.rectangle([x + 14, y + 12, x + 48, y + 22], fill=(180, 140, 80))
        d.rectangle([x + 40, y + 20, x + 48, y + 34], fill=(150, 110, 60))
        d.rectangle([x + 10, y + 34, x + 54, y + 38], fill=(120, 90, 50))
    elif kind == "chart":
        d.rectangle([x, y, x + w, y + h], fill=(255, 235, 235))
        d.line([(x + 6, y + 10), (x + 22, y + 16), (x + 36, y + 14), (x + 52, y + 32)],
               fill=(196, 18, 28), width=4)
        d.polygon([(x + 52, y + 32), (x + 42, y + 30), (x + 52, y + 40)], fill=(196, 18, 28))
    elif kind == "lens":
        d.rectangle([x, y, x + w, y + h], fill=(255, 240, 200))
        d.ellipse([x + 14, y + 6, x + 44, y + 36], outline=(196, 18, 28), width=4)
        d.line([x + 40, y + 32, x + 54, y + 40], fill=(196, 18, 28), width=4)
        d.text((x + 24, y + 15), "?", font=SANS_B(16), fill=(196, 18, 28))
    elif kind == "plane":
        d.rectangle([x, y, x + w, y + h], fill=(140, 205, 225))
        d.polygon([(x + 8, y + 22), (x + 50, y + 14), (x + 56, y + 20), (x + 30, y + 28),
                   (x + 14, y + 28)], fill=(255, 255, 255))
        d.polygon([(x + 24, y + 14), (x + 34, y + 8), (x + 38, y + 14)], fill=(230, 230, 230))
    elif kind == "flags":
        d.rectangle([x, y, x + w, y + h], fill=(240, 240, 240))
        d.rectangle([x + 6, y + 8, x + 28, y + 34], fill=(255, 255, 255),
                    outline=(0, 56, 184), width=2)
        d.line([x + 6, y + 14, x + 28, y + 14], fill=(0, 56, 184), width=3)
        d.line([x + 6, y + 28, x + 28, y + 28], fill=(0, 56, 184), width=3)
        d.rectangle([x + 34, y + 8, x + 56, y + 34], fill=(0, 120, 200))
        d.ellipse([x + 40, y + 14, x + 50, y + 24], fill=(255, 255, 255))
    elif kind == "gate":
        d.rectangle([x, y, x + w, y + h], fill=(255, 244, 200))
        d.rectangle([x + 6, y + 12, x + 58, y + 20], fill=(255, 200, 40))
        for i in range(5):
            d.rectangle([x + 8 + i * 11, y + 12, x + 14 + i * 11, y + 20], fill=(17, 17, 17))
        d.rectangle([x + 8, y + 20, x + 12, y + 38], fill=(90, 90, 90))
        d.rectangle([x + 52, y + 20, x + 56, y + 38], fill=(90, 90, 90))
    elif kind == "stamp":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.ellipse([x + 10, y + 5, x + 54, y + 37], outline=(196, 18, 28), width=3)
        d.line([x + 14, y + 33, x + 50, y + 9], fill=(196, 18, 28), width=3)
        d.text((x + 18, y + 14), "NO", font=SANS_B(13), fill=(196, 18, 28))
    elif kind == "scales":
        d.rectangle([x, y, x + w, y + h], fill=(255, 240, 180))
        d.line([x + 32, y + 6, x + 32, y + 34], fill=(120, 90, 20), width=3)
        d.line([x + 12, y + 10, x + 52, y + 10], fill=(120, 90, 20), width=3)
        d.polygon([(x + 12, y + 10), (x + 18, y + 24), (x + 6, y + 24)], fill=(212, 160, 23))
        d.polygon([(x + 52, y + 10), (x + 58, y + 24), (x + 46, y + 24)], fill=(212, 160, 23))
        d.rectangle([x + 24, y + 34, x + 40, y + 38], fill=(120, 90, 20))
    elif kind == "trophy":
        d.rectangle([x, y, x + w, y + h], fill=(255, 244, 200))
        d.polygon([(x + 20, y + 6), (x + 44, y + 6), (x + 40, y + 26), (x + 24, y + 26)],
                  fill=(212, 160, 23))
        d.arc([x + 12, y + 8, x + 24, y + 22], 90, 270, fill=(212, 160, 23), width=3)
        d.arc([x + 40, y + 8, x + 52, y + 22], -90, 90, fill=(212, 160, 23), width=3)
        d.rectangle([x + 28, y + 26, x + 36, y + 32], fill=(212, 160, 23))
        d.rectangle([x + 20, y + 32, x + 44, y + 36], fill=(212, 160, 23))
    elif kind == "sun":
        d.rectangle([x, y, x + w, y + h], fill=(255, 230, 200))
        d.ellipse([x + 14, y + 6, x + 40, y + 32], fill=(255, 140, 0))
        for ang in range(0, 360, 45):
            import math
            dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            d.line([x + 27 + dx * 16, y + 19 + dy * 16, x + 27 + dx * 21, y + 19 + dy * 21],
                   fill=(255, 140, 0), width=3)
        d.rectangle([x + 48, y + 22, x + 52, y + 38], fill=(196, 18, 28))

CW = (W - 20 - 8) / 2
for i, (head, sub, kind) in enumerate(secondaries):
    row, col = divmod(i, 2)
    x = 10 + col * (CW + 8)
    y = SY + row * 40
    d.rectangle([x, y, x + CW, y + 38], outline=(205, 205, 205), width=1)
    mini_scene(kind, x + 1, y + 1, 64, 36)
    lines = wrap(head, SANS_B(12), CW - 72 - 8)
    yy = block(x + 72, y + 3, CW - 72 - 8, lines[:2], SANS_B(12), INK, leading=14)
    block(x + 72, yy, CW - 72 - 8, wrap(sub, SANS(10), CW - 72 - 8)[:1],
          SANS(10), (70, 70, 70), leading=12)

# ---------------------------------------------------------------- ALSO list
AY = SY + 5 * 40 + 6
d.text((10, AY), "ALSO ON TUESDAY", font=SANS_B(14), fill=INK)
d.rectangle([168, AY + 7, W - 10, AY + 8], fill=RED)
also = [
    "Trump to unveil new tariffs after probe of 16 partners",
    "China extends gallium export-ban pause to 27 Jan",
    "Houthis 60 km from Aden — army: they won't take it",
    "Saudi 2027 budget: SR1.39 trillion approved",
    "Gaza strike kills Hamas security chief; 7 dead",
    "Abrego Garcia to leave the US voluntarily",
    "UK opens inquiry into nuclear-test veterans",
    "EU budget fight: Germany pays €14.9bn; Merz veto threat",
    "Zelenskyy meets Hungary's Magyar; warns of new strikes",
    "Dymer toll 12; Zaporizhzhia strike: 2 dead, 40 hurt",
    "Guardian counts 460,000+ Russian war deaths",
    "China names Shenzhou-24 crew, first foreign astronaut",
    "UN chief: AI is transforming modern warfare",
    "PKK quits 14 more bases in northern Iraq",
    "Awami League clashes in Bangladesh: 30 hurt",
    "Bomb threats hit hundreds of schools in Denmark, Germany",
    "UAE bus crash kills 13 in Ras Al Khaimah",
    "PNG votes on Bougainville independence",
    "Philippines opens 2027 budget debate; growth 2.1%",
    "UK sanctions 5 Myanmar generals; recognises Rohingya genocide",
    "Peru dengue deaths reach 45 in Lambayeque",
    "Chile mourns actress Delfina Guzmán, 98",
]
f_num = SANS_B(11)
f_txt = SANS(11)
colw = (W - 20 - 16) / 2
for i, item in enumerate(also):
    col, row = divmod(i, 11)
    x = 10 + col * (colw + 16)
    y = AY + 20 + row * 13
    n = f"{14 + i}."
    d.text((x, y), n, font=f_num, fill=RED)
    nx = x + tw(n, f_num) + 5
    txt = item
    while tw(txt, f_txt) > colw - (nx - x) and len(txt) > 10:
        txt = txt[:-1]
    assert tw(txt, f_txt) <= colw - (nx - x) + 1, f"ALSO overflow: {item!r}"
    d.text((nx, y), txt, font=f_txt, fill=INK)

# ---------------------------------------------------------------- map
MY = AY + 20 + 11 * 13 + 5
MH = 84
d.rectangle([10, MY, W - 10, MY + MH], fill=(235, 240, 245), outline=(180, 180, 180))
d.text((16, MY + 3), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
def project(lon, lat):
    return (10 + (lon + 180) / 360 * (W - 20),
            MY + 14 + (75 - lat) / 130 * (MH - 18))
continents = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 30),
     (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28), (-58, -35),
     (-65, -40), (-70, -52), (-73, -40), (-80, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (0, 48), (-2, 50), (5, 53), (8, 57), (10, 59), (18, 56),
     (21, 55), (28, 59), (30, 60), (25, 65), (20, 70), (15, 70), (5, 70), (-5, 60), (-10, 50)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28), (43, 12),
     (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -25),
     (12, -5), (9, 4), (-8, 5)],
    [(30, 36), (36, 36), (43, 38), (48, 30), (54, 26), (58, 25), (62, 25), (66, 25),
     (70, 20), (72, 20), (77, 8), (80, 7), (85, 20), (89, 22), (92, 21), (95, 16),
     (98, 10), (100, 8), (103, 2), (104, 1), (100, 8), (105, 10), (108, 12), (109, 15),
     (108, 18), (106, 20), (110, 20), (114, 22), (118, 25), (120, 28), (122, 32),
     (124, 38), (127, 40), (130, 42), (135, 44), (140, 45), (142, 50), (140, 55),
     (135, 60), (130, 65), (125, 70), (120, 73), (110, 74), (100, 76), (90, 75),
     (80, 73), (70, 72), (60, 69), (50, 68), (40, 68), (30, 70), (30, 66)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (129, -32), (132, -32), (136, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]
for poly in continents:
    d.polygon([project(lo, la) for lo, la in poly], fill=(190, 205, 185),
              outline=(120, 140, 120))
pins = [
    (1, 46.7, 24.7, 0, -12), (2, 56.5, 26.5, 16, 10), (3, -74.0, 40.7, 0, 0),
    (4, 30.5, 50.5, 6, -10), (5, 116.4, 39.9, 0, -8), (6, -0.1, 51.5, -12, -8),
    (7, 34.5, 31.5, -16, 12), (8, 45.0, 12.8, 12, 14), (9, -17.4, 14.7, 0, 0),
    (10, -3.7, 40.4, -10, 12), (11, 147.2, -9.5, 0, 0), (12, 121.0, 14.6, 0, -12),
]
for n, lon, lat, dx, dy in pins:
    px, py = project(lon, lat)
    qx, qy = px + dx, py + dy
    if dx or dy:
        d.line([px, py, qx, qy], fill=RED, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.ellipse([qx - 9, qy - 9, qx + 9, qy + 9], fill=RED, outline=(255, 255, 255), width=2)
    t = str(n)
    d.text((qx - tw(t, SANS_B(10)) / 2, qy - 7), t, font=SANS_B(10), fill=(255, 255, 255))

# ---------------------------------------------------------------- footer
FY = MY + MH + 6
d.rectangle([10, FY, 640, H - 8], outline=RED, width=2)
d.text((18, FY + 5), "DATE CHECK — NOT 24 NOVEMBER", font=SANS_B(11), fill=RED)
dc = ("Nvidia's Huang returns (+33%) — 23 Nov  •  Iran's $290bn claim — 23 Nov  •  "
      "Indonesia ship seizure — 7 / 20 Nov  •  Tajikistan quits ICC — 23 Nov  •  "
      "COP31 collapse — 22 Nov  •  Kyiv bridge barrage — 20 Nov")
block(18, FY + 21, 640 - 36, wrap(dc, SANS(10), 640 - 36), SANS(10), INK, leading=13)
d.rectangle([648, FY, W - 10, H - 8], outline=(180, 180, 180), width=1)
d.text((656, FY + 5), "HOW WE CHECKED", font=SANS_B(11), fill=INK)
hc = ("Every story dated 24 Nov 2026 via Reuters, WSJ, AP, Al Jazeera, "
      "Xinhua, BBC and official statements. Claims labelled; full list in "
      "VERIFICATION.md.")
block(656, FY + 21, W - 10 - 656 - 8, wrap(hc, SANS(10), W - 10 - 656 - 8),
      SANS(10), INK, leading=13)

img.save(OUT, optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
