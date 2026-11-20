#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261119 (v3).

Dense one-page newspaper front page, 1024x1024, drawn procedurally with PIL.
31 stories, all from Thursday 19 November 2026. Deterministic: same input
gives byte-identical output (no timestamps, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 227)
CARD = (255, 253, 246)
INK = (26, 26, 26)
GREY = (90, 86, 76)
RED = (179, 35, 27)
NAVY = (31, 58, 95)
TEAL = (14, 107, 107)
SKY = (198, 222, 240)
SAND = (232, 214, 170)
SEA = (205, 226, 238)
GOLD = (197, 146, 44)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def serif(size, bold=False):
    name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_serif_bold(text, max_w, start=64):
    size = start
    while size > 20:
        f = serif(size, bold=True)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return serif(20, bold=True)


def wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, font, max_w, fill, lh=None, max_lines=None):
    lines = wrap(d, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = lh or int(font.size * 1.25)
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


# ---------------------------------------------------------------- flags ----
def flag_us(d, x, y, w, h):
    for i in range(7):
        d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 2 + c * w * 0.09, y + 2 + r * h * 0.11,
                       x + 4 + c * w * 0.09, y + 4 + r * h * 0.11],
                      fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.ellipse([x + w * 0.12, y + h * 0.12, x + w * 0.32, y + h * 0.42],
              fill=(255, 222, 0))
    for dx, dy in [(0.55, 0.12), (0.68, 0.28), (0.55, 0.48)]:
        d.ellipse([x + w * dx, y + h * dy, x + w * dx + 3, y + h * dy + 3],
                  fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_ru(d, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_dk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(198, 12, 48))
    d.rectangle([x + w * 0.3, y, x + w * 0.42, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.4, x + w, y + h * 0.6], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_kr(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.ellipse([x + w * 0.38, y + h * 0.22, x + w * 0.62, y + h * 0.78],
              fill=(205, 49, 50))
    d.pieslice([x + w * 0.38, y + h * 0.22, x + w * 0.62, y + h * 0.78],
               180, 360, fill=(0, 71, 160))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_in(d, x, y, w, h):
    for i, c in enumerate([(255, 153, 51), (255, 255, 255), (19, 136, 8)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    d.ellipse([x + w * 0.44, y + h * 0.38, x + w * 0.56, y + h * 0.62],
              outline=(0, 0, 136), width=1)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_au(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 47, 108))
    d.rectangle([x, y, x + w * 0.45, y + h * 0.5], fill=(200, 16, 46))
    d.ellipse([x + w * 0.62, y + h * 0.25, x + w * 0.72, y + h * 0.4],
              fill=(255, 255, 255))
    d.ellipse([x + w * 0.78, y + h * 0.55, x + w * 0.86, y + h * 0.68],
              fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_co(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.5], fill=(252, 209, 22))
    d.rectangle([x, y + h * 0.5, x + w, y + h * 0.75], fill=(0, 56, 147))
    d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(206, 17, 38))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


FLAGS = {"us": flag_us, "cn": flag_cn, "ru": flag_ru, "dk": flag_dk,
         "kr": flag_kr, "in": flag_in, "au": flag_au, "co": flag_co}


# ------------------------------------------------------------- figures ----
def person(d, cx, base_y, h, suit, skin=(232, 190, 150), hair=(60, 45, 30),
           tie=(179, 35, 27)):
    """Flat suited figure: head + shoulders, standing on base_y."""
    hw = h * 0.30
    d.ellipse([cx - hw / 2, base_y - h, cx + hw / 2, base_y - h + hw],
              fill=skin, outline=INK, width=1)
    d.pieslice([cx - hw / 2, base_y - h, cx + hw / 2, base_y - h + hw],
               180, 360, fill=hair)
    d.polygon([(cx - hw * 0.85, base_y), (cx - hw * 0.55, base_y - h * 0.52),
               (cx + hw * 0.55, base_y - h * 0.52), (cx + hw * 0.85, base_y)],
              fill=suit, outline=INK)
    d.polygon([(cx - 2, base_y - h * 0.50), (cx + 2, base_y - h * 0.50),
               (cx + 3, base_y - h * 0.22), (cx, base_y - h * 0.14),
               (cx - 3, base_y - h * 0.22)], fill=tie)


def burst(d, cx, cy, r, fill=(255, 200, 0), outline=RED):
    pts = []
    for i in range(16):
        ang = i * 3.14159 / 8
        rr = r if i % 2 == 0 else r * 0.45
        import math
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=outline)


def scales(d, x, y, w, h, color=GOLD):
    d.line([x + w / 2, y, x + w / 2, y + h], fill=color, width=3)
    d.line([x + 4, y + h * 0.18, x + w - 4, y + h * 0.18], fill=color, width=3)
    for px in (x + 6, x + w - 6):
        d.line([px, y + h * 0.18, px, y + h * 0.55], fill=color, width=2)
        d.polygon([(px - w * 0.22, y + h * 0.55), (px + w * 0.22, y + h * 0.55),
                   (px, y + h * 0.78)], fill=color, outline=INK)
    d.line([x + w * 0.3, y + h, x + w * 0.7, y + h], fill=color, width=3)
    d.ellipse([x + w / 2 - 3, y - 3, x + w / 2 + 3, y + 3], fill=color)


def courthouse(d, x, y, w, h, wall=(240, 230, 210), roof=(150, 60, 50)):
    d.polygon([(x, y + h * 0.28), (x + w / 2, y), (x + w, y + h * 0.28)],
              fill=roof, outline=INK)
    d.rectangle([x + w * 0.04, y + h * 0.28, x + w * 0.96, y + h],
                fill=wall, outline=INK, width=1)
    n = 5
    for i in range(n):
        cx = x + w * (0.12 + 0.76 * i / (n - 1))
        d.rectangle([cx - w * 0.035, y + h * 0.36, cx + w * 0.035, y + h * 0.9],
                    fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x, y + h * 0.9, x + w, y + h], fill=(200, 190, 170))


def globe(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200),
              outline=INK, width=1)
    for dx, dy, wr, hr in [(-0.45, -0.35, 0.5, 0.35), (0.15, 0.25, 0.55, 0.4),
                           (0.3, -0.5, 0.4, 0.3)]:
        d.ellipse([cx + dx * r, cy + dy * r, cx + (dx + wr) * r,
                   cy + (dy + hr) * r], fill=(90, 180, 110))


def thermometer(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h * 0.8], radius=w / 2,
                        fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x + w * 0.3, y + h * 0.15, x + w * 0.7, y + h * 0.8],
                fill=RED)
    d.ellipse([x - w * 0.35, y + h * 0.68, x + w * 1.35, y + h * 1.12],
              fill=RED, outline=INK, width=1)


# --------------------------------------------------- lead illustrations ---
def illo_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 64, 110))
    # skyline
    for bx, bw, bh in [(6, 34, 30), (46, 26, 44), (78, 40, 26), (200, 30, 38),
                       (236, 36, 28), (278, 30, 46)]:
        d.rectangle([x + bx, y + h - 40 - bh, x + bx + bw, y + h - 40],
                    fill=(28, 48, 84))
    # flags on poles (kept above the figures' heads)
    for i, fk in enumerate(("us", "cn", "ru")):
        fx = x + 34 + i * 108
        d.line([fx, y + 2, fx, y + 24], fill=(220, 220, 220), width=2)
        FLAGS[fk](d, fx + 2, y + 4, 44, 18)
    # table + figures
    ty = y + h - 40
    for i, (suit, tie, hair) in enumerate(
            [((30, 30, 60), (179, 35, 27), (220, 200, 160)),
             ((20, 40, 30), (30, 60, 140), (30, 30, 30)),
             ((50, 30, 30), (40, 80, 160), (200, 200, 200))]):
        person(d, x + 56 + i * 108, ty, 40, suit, tie=tie, hair=hair)
    d.rectangle([x + 8, ty, x + w - 8, ty + 26], fill=(235, 225, 200),
                outline=INK, width=1)
    f = sans(9, bold=True)
    for i, name in enumerate(("TRUMP", "XI", "PUTIN")):
        nx = x + 30 + i * 108
        d.rectangle([nx, ty + 5, nx + 52, ty + 20], fill=(255, 255, 255),
                    outline=INK, width=1)
        d.text((nx + 26 - f.getlength(name) / 2, ty + 6), name, font=f,
               fill=INK)
    d.rectangle([x + 8, y + h - 18, x + 118, y + h - 4], fill=RED)
    d.text((x + 13, y + h - 17), "APEC 2026 · SHENZHEN",
           font=sans(8, bold=True), fill=(255, 255, 255))


def illo_icj(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 66, y + 6, x + w - 40, y + 32], fill=(255, 240, 150),
              outline=GOLD, width=1)
    courthouse(d, x + 14, y + 28, w * 0.58, h - 40)
    scales(d, x + w * 0.68, y + 28, w * 0.26, h - 48)
    d.rectangle([x + w - 62, y + h - 30, x + w - 8, y + h - 6], fill=RED)
    d.text((x + w - 54, y + h - 29), "9 – 6", font=sans(13, bold=True),
           fill=(255, 255, 255))
    d.rectangle([x + 8, y + 6, x + 176, y + 22], fill=NAVY)
    d.text((x + 13, y + 7), "WORLD COURT · THE HAGUE",
           font=sans(9, bold=True), fill=(255, 255, 255))


def illo_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 94, 94))
    globe(d, x + 52, y + h / 2 + 2, 34)
    thermometer(d, x + 108, y + 16, 14, 62)
    # draft paper
    px, py, pw, ph = x + 150, y + 12, w - 168, h - 24
    d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([px, py, px + pw, py + 16], fill=NAVY)
    d.text((px + 6, py + 2), "DRAFT TEXT · 19 NOV", font=sans(9, bold=True),
           fill=(255, 255, 255))
    f = sans(12, bold=True)
    d.text((px + 10, py + 26), "FOSSIL FUELS", font=f, fill=INK)
    d.line([px + 8, py + 35, px + 112, py + 35], fill=RED, width=3)
    for i in range(3):
        d.line([px + 10, py + 52 + i * 10, px + pw - 24 - i * 14, py + 52 + i * 10],
               fill=(180, 180, 180), width=3)
    d.rectangle([px + pw - 52, py + ph - 22, px + pw - 8, py + ph - 6],
                outline=RED, width=2)
    d.text((px + pw - 44, py + ph - 21), "CUT", font=sans(10, bold=True),
           fill=RED)
    d.text((x + 10, y + h - 18), "COP31 · ANTALYA", font=sans(10, bold=True),
           fill=(255, 255, 255))


# -------------------------------------------------- small illustrations ---
def illo_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 228, 244))
    cx, cy = x + w * 0.32, y + h * 0.55
    for i, r in enumerate((26, 20, 14, 8)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + i * 40, 300 + i * 30,
              fill=(43, 108, 176), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for i in range(5):
        lx = x + w * 0.62 + i * 12
        d.line([lx, y + 8, lx - 4, y + 22], fill=(43, 108, 176), width=2)
    d.rectangle([x + w - 58, y + 4, x + w - 4, y + 18], fill=RED)
    d.text((x + w - 52, y + 5), "ODISHA", font=sans(8, bold=True),
           fill=(255, 255, 255))
    d.text((x + w * 0.58, y + h - 16), "100,000+ moved", font=sans(9, bold=True),
           fill=NAVY)


def illo_ipo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 58, 40))
    vals = [10, 14, 12, 18, 22, 20, 28, 34]
    bw = w / 10
    for i, v in enumerate(vals):
        bx = x + 8 + i * bw
        d.rectangle([bx, y + h - 8 - v, bx + bw - 3, y + h - 8],
                    fill=(72, 187, 120))
    d.line([x + 8, y + h - 20, x + w - 14, y + 12], fill=(255, 220, 80),
           width=2)
    d.text((x + 8, y + 4), "ANT · NASDAQ", font=sans(9, bold=True),
           fill=(255, 255, 255))
    d.text((x + w - 46, y + h - 20), "$83", font=sans(13, bold=True),
           fill=(255, 220, 80))


def illo_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 40, 110))
    d.ellipse([x + w * 0.62, y + 4, x + w * 0.62 + 26, y + 30],
              fill=(255, 190, 90))
    for bx, bw, bh in [(4, 22, 22), (30, 18, 30), (52, 26, 18), (120, 20, 26),
                       (146, 24, 20), (174, 16, 30)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(40, 20, 60))
    # gamepad
    gx, gy = x + w * 0.38, y + h * 0.42
    d.rounded_rectangle([gx, gy, gx + 52, gy + 26], radius=8,
                        fill=(30, 30, 40), outline=(255, 255, 255), width=1)
    d.rectangle([gx + 8, gy + 9, gx + 18, gy + 13], fill=(255, 255, 255))
    d.rectangle([gx + 11, gy + 6, gx + 15, gy + 16], fill=(255, 255, 255))
    for dx, dy, c in [(36, 8, (255, 80, 80)), (42, 13, (255, 220, 80)),
                      (36, 16, (80, 200, 120))]:
        d.ellipse([gx + dx, gy + dy, gx + dx + 5, gy + dy + 5], fill=c)
    d.text((x + 6, y + 4), "VI · OUT TODAY", font=sans(9, bold=True),
           fill=(255, 255, 255))


def illo_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(90, 140, 190))
    d.line([x + 8, y + h * 0.55, x + w - 8, y + h * 0.55], fill=INK, width=4)
    for tx in (0.25, 0.7):
        d.line([x + w * tx, y + 12, x + w * tx, y + h * 0.55], fill=INK,
               width=3)
    d.line([x + w * 0.25, y + 12, x + w * 0.48, y + h * 0.55], fill=INK,
           width=1)
    d.line([x + w * 0.7, y + 12, x + w * 0.48, y + h * 0.55], fill=INK,
           width=1)
    burst(d, x + w * 0.48, y + h * 0.42, 12)
    d.rectangle([x + 6, y + 4, x + 96, y + 18], fill=INK)
    d.text((x + 10, y + 5), "3RD HIT IN A WEEK", font=sans(8, bold=True),
           fill=(255, 255, 255))


def illo_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))
    for bx, bw, bh in [(6, 20, 26), (30, 16, 36), (50, 22, 22), (130, 18, 30),
                       (152, 24, 20), (180, 12, 26)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(50, 70, 110))
        for wy in range(2):
            d.rectangle([x + bx + 4, y + h - bh + 4 + wy * 9, x + bx + 8,
                         y + h - bh + 8 + wy * 9], fill=(255, 220, 120))
    d.line([x + 78, y + 34, x + 108, y + 10], fill=(255, 255, 255), width=2)
    burst(d, x + 110, y + 9, 9)
    d.line([x + 96, y + 40, x + 118, y + 18], fill=(255, 200, 80), width=2)
    d.text((x + 6, y + 4), "OVER RIYADH", font=sans(9, bold=True),
           fill=(255, 255, 255))


def illo_exam(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 210))
    d.rectangle([x + 14, y + 8, x + w - 60, y + h - 10], fill=(255, 255, 255),
                outline=INK, width=1)
    for i in range(4):
        d.line([x + 22, y + 16 + i * 8, x + w - 74 - i * 8, y + 16 + i * 8],
               fill=(170, 170, 170), width=2)
    d.ellipse([x + w - 50, y + 10, x + w - 14, y + 42], fill=RED)
    d.text((x + w - 41, y + 18), "551k", font=sans(9, bold=True),
           fill=(255, 255, 255))
    flag_kr(d, x + w - 52, y + h - 24, 26, 16)


def illo_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 235, 200))
    d.rectangle([x + 30, y + 6, x + w - 30, y + 20], fill=(252, 209, 22),
                outline=INK, width=1)
    d.text((x + w / 2 - 26, y + 7), "PARO NACIONAL", font=sans(8, bold=True),
           fill=INK)
    for i in range(6):
        cx = x + 22 + i * 30
        d.ellipse([cx - 6, y + 26, cx + 6, y + 38], fill=(232, 190, 150),
                  outline=INK, width=1)
        d.rectangle([cx - 9, y + 38, cx + 9, y + h - 2],
                    fill=((179, 35, 27), (31, 58, 95), (14, 107, 107),
                          (197, 146, 44), (107, 70, 193), (39, 103, 73))[i])
    flag_co(d, x + 6, y + h - 20, 26, 15)


def illo_jobs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 245))
    vals = [12, 15, 14, 18, 24]
    for i, v in enumerate(vals):
        bx = x + 14 + i * 22
        c = RED if i == 4 else NAVY
        d.rectangle([bx, y + h - 10 - v, bx + 16, y + h - 10], fill=c)
    d.text((x + w - 62, y + 4), "4.9%", font=sans(16, bold=True), fill=RED)
    d.text((x + w - 62, y + 24), "5-YEAR HIGH", font=sans(8, bold=True),
           fill=INK)
    flag_au(d, x + 6, y + 4, 30, 18)


def illo_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 232, 240))
    # gavel
    d.rectangle([x + 20, y + 12, x + 78, y + 24], fill=(139, 90, 43),
                outline=INK, width=1)
    d.line([x + 49, y + 24, x + 49, y + 44], fill=(139, 90, 43), width=6)
    d.rectangle([x + 30, y + 42, x + 68, y + 48], fill=(90, 60, 30))
    d.rectangle([x + 92, y + 12, x + w - 8, y + 30], outline=RED, width=2)
    d.text((x + 98, y + 15), "OVERTURNED", font=sans(9, bold=True), fill=RED)
    flag_kr(d, x + 100, y + 34, 30, 18)


def illo_arctic(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 240))
    d.polygon([(x + 10, y + h), (x + 60, y + 14), (x + 110, y + h)],
              fill=(255, 255, 255), outline=INK)
    d.polygon([(x + 90, y + h), (x + 140, y + 26), (x + 180, y + h)],
              fill=(230, 240, 250), outline=INK)
    flag_dk(d, x + 8, y + 6, 30, 18)
    flag_us(d, x + 42, y + 6, 30, 18)
    d.rectangle([x + w - 56, y + 4, x + w - 4, y + 20], fill=RED)
    d.text((x + w - 50, y + 5), "109 – 0", font=sans(10, bold=True),
           fill=(255, 255, 255))


# ------------------------------------------------------------------ map ---
def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=1)
    # graticule
    for gx in range(1, 8):
        d.line([x + gx * w / 8, y, x + gx * w / 8, y + h],
               fill=(185, 210, 225), width=1)
    for gy in range(1, 4):
        d.line([x, y + gy * h / 4, x + w, y + gy * h / 4],
               fill=(185, 210, 225), width=1)
    sx, sy = w / 294.0, h / 114.0

    def P(pts):
        return [(x + px * sx, y + py * sy) for px, py in pts]

    continents = [
        [(8, 18), (30, 10), (55, 8), (78, 16), (88, 28), (82, 42), (70, 48),
         (60, 44), (52, 58), (40, 62), (28, 55), (14, 48), (6, 34)],
        [(78, 6), (95, 4), (100, 12), (88, 16)],
        [(72, 66), (92, 62), (104, 72), (100, 88), (88, 106), (78, 100),
         (70, 82)],
        [(138, 48), (162, 44), (180, 52), (178, 72), (166, 96), (150, 100),
         (140, 80), (134, 62)],
        [(138, 14), (158, 8), (172, 14), (170, 26), (156, 32), (142, 28)],
        [(132, 16), (140, 14), (142, 22), (134, 24)],
        [(172, 10), (230, 6), (278, 14), (286, 30), (270, 48), (250, 58),
         (232, 66), (214, 60), (196, 50), (182, 44), (176, 28)],
        [(238, 70), (252, 74), (248, 82), (236, 80)],
        [(248, 88), (282, 86), (288, 100), (272, 110), (252, 106)],
    ]
    for c in continents:
        d.polygon(P(c), fill=SAND, outline=(160, 140, 100))
    dots = {1: (255, 52), 2: (138, 30), 3: (180, 42), 4: (228, 60),
            5: (68, 36), 7: (182, 26), 8: (194, 54), 9: (266, 42),
            10: (80, 78), 11: (272, 100), 12: (280, 28), 13: (158, 14)}
    f = sans(8, bold=True)
    for n, (px, py) in dots.items():
        cx, cy = x + px * sx, y + py * sy
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(n)
        d.text((cx - f.getlength(t) / 2, cy - 6), t, font=f,
               fill=(255, 255, 255))


# --------------------------------------------------------------- cards ----
def num_badge(d, x, y, n, color=RED, r=9):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=color)
    f = sans(10, bold=True)
    t = str(n)
    d.text((x + r - f.getlength(t) / 2, y + 2), t, font=f,
           fill=(255, 255, 255))
    return 2 * r + 4


def lead_card(d, x, y, w, h, n, tag, tag_color, illo, headline, body):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=1)
    illo(d, x + 1, y + 1, w - 2, 104)
    cy = y + 112
    num_badge(d, x + 8, cy, n)
    d.text((x + 30, cy + 1), tag, font=sans(10, bold=True), fill=tag_color)
    cy += 22
    cy = draw_wrapped(d, x + 8, cy, headline, serif(20, bold=True), w - 16,
                      INK, lh=23, max_lines=2)
    cy += 3
    draw_wrapped(d, x + 8, cy, body, sans(12), w - 16, INK, lh=15,
                 max_lines=4)


def small_card(d, x, y, w, h, n, tag, tag_color, illo, headline, body):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=1)
    illo(d, x + 1, y + 1, w - 2, 52)
    cy = y + 58
    num_badge(d, x + 6, cy, n, r=8)
    d.text((x + 26, cy), tag, font=sans(9, bold=True), fill=tag_color)
    cy += 19
    cy = draw_wrapped(d, x + 6, cy, headline, serif(14, bold=True), w - 12,
                      INK, lh=17, max_lines=2)
    cy += 2
    draw_wrapped(d, x + 6, cy, body, sans(11), w - 12, INK, lh=13.5,
                 max_lines=3)


# ----------------------------------------------------------------- main ---
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- kicker
    d.text((12, 8), "THE WORLD IN ONE DAY", font=sans(12, bold=True),
           fill=RED)
    right = "31 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    d.text((1012 - sans(11, bold=True).getlength(right), 9), right,
           font=sans(11, bold=True), fill=INK)
    d.line([12, 28, 1012, 28], fill=INK, width=2)

    # ---- masthead
    mast = "Thursday 19 November 2026"
    mf = fit_serif_bold(mast, 1000, start=64)
    d.text(((1024 - mf.getlength(mast)) / 2, 30), mast, font=mf, fill=INK)
    sub = ("Three leaders share one table in Shenzhen · The World Court "
           "rules on Myanmar · COP31's draft drops fossil fuels")
    sf = serif(16)
    d.text(((1024 - sf.getlength(sub)) / 2, 96), sub, font=sf, fill=RED)
    d.line([12, 118, 1012, 118], fill=INK, width=2)

    # ---- stat strip
    stats = [
        ("3", "presidents at one table"),
        ("9–6", "World Court genocide vote"),
        ("$81.3bn", "record IPO on Nasdaq"),
        ("13 years", "since GTA V came out"),
        ("551,864", "sit Korea's Suneung exam"),
        ("4.9%", "Australian jobless rate"),
    ]
    sw = 1000 / 6
    for i, (num, label) in enumerate(stats):
        cx = 12 + i * sw
        d.text((cx + 6, 122), num, font=serif(24, bold=True), fill=RED)
        draw_wrapped(d, cx + 6, 150, label, sans(10), sw - 12, INK, lh=12)
        if i:
            d.line([cx, 122, cx, 164], fill=(200, 190, 165), width=1)
    d.line([12, 168, 1012, 168], fill=INK, width=2)

    # ---- leads
    leads = [
        (1, "SHENZHEN · SUMMIT", RED, illo_summit,
         "Three presidents, one table in Shenzhen",
         "Trump, Xi and Putin meet for the first time as a trio beside the "
         "APEC summit, talking for 90 minutes and signing a \u201cDeclaration "
         "on Peace\u201d on nuclear risk. — Reuters"),
        (2, "THE HAGUE · JUSTICE", NAVY, illo_icj,
         "World Court: Myanmar committed genocide",
         "By 9 votes to 6, the ICJ finds Myanmar guilty of genocide against "
         "the Rohingya and orders reparations. — Al Jazeera · UN News"),
        (3, "ANTALYA · CLIMATE", TEAL, illo_cop,
         "COP31 draft drops fossil fuels",
         "The new text names no fossil fuels, and the $120bn "
         "adaptation-aid goal is still open as talks run to Friday. "
         "— Reuters · AFP"),
    ]
    lw, gap, ly, lh = 328, 8, 174, 252
    for i, (n, tag, tc, illo, head, body) in enumerate(leads):
        lead_card(d, 12 + i * (lw + gap), ly, lw, lh, n, tag, tc, illo,
                  head, body)

    # ---- small stories
    small = [
        (4, "ODISHA · STORM", (43, 108, 176), illo_cyclone,
         "Cyclone Akvan bears down on Odisha",
         "Over 100,000 moved to safety before Friday's landfall. — IMD"),
        (5, "NEW YORK · MARKETS", (39, 103, 73), illo_ipo,
         "Anthropic lists after a record IPO",
         "Shares priced at $83; the $81.3bn sale is the biggest ever. — AP"),
        (6, "WORLDWIDE · GAMES", (107, 70, 193), illo_gta,
         "GTA VI unlocks around the world",
         "Midnight local launch, New Zealand first; ~17.1m pre-orders. — ABC"),
        (7, "CRIMEA · WAR", (156, 66, 33), illo_bridge,
         "Kerch bridge struck a third time",
         "Another strike in a week halts trains to Russia. — Euronews"),
        (8, "RIYADH · WAR", (156, 66, 33), illo_riyadh,
         "Riyadh intercepts Houthi missiles",
         "Debris fell on the capital; no casualties reported. — Reuters"),
        (9, "SEOUL · EDUCATION", (44, 82, 130), illo_exam,
         "Half a million sit Korea's exam",
         "551,864 take the Suneung; flights pause for listening. — Yonhap"),
        (10, "BOGOTÁ · LABOUR", (151, 90, 22), illo_strike,
         "Colombian unions strike nationwide",
         "Marches in Bogotá, Medellín and Cali. — Infobae"),
        (11, "CANBERRA · ECONOMY", (40, 94, 97), illo_jobs,
         "Australian jobless rate climbs",
         "Up to 4.9%, the highest since 2024; the dollar slides. — ABC"),
        (12, "SEOUL · JUSTICE", NAVY, illo_court,
         "Ex-PM Han cleared by Seoul court",
         "His martial-law conviction is overturned. — AP"),
        (13, "COPENHAGEN · SECURITY", (85, 60, 154), illo_arctic,
         "Danish MPs approve US Arctic pact",
         "Parliament votes 109–0 for the Greenland deal. — AP"),
    ]
    cw, cgap = 195, 6
    rh = 158
    for i, (n, tag, tc, illo, head, body) in enumerate(small):
        row, col = divmod(i, 5)
        small_card(d, 12 + col * (cw + cgap), 432 + row * (rh + 6), cw, rh,
                   n, tag, tc, illo, head, body)

    # ---- map + also-on
    my = 756
    d.text((12, my), "WHERE IT HAPPENED", font=sans(11, bold=True), fill=RED)
    d.text((180, my), "numbers match the stories", font=sans(9), fill=GREY)
    draw_map(d, 12, my + 18, 306, 150)
    d.text((12, my + 172), "Pins: stories 1–13 (6 is worldwide).",
           font=sans(9), fill=GREY)

    ax = 326
    d.text((ax, my), "ALSO ON THURSDAY 19 NOVEMBER 2026",
           font=sans(11, bold=True), fill=RED)
    d.text((ax + 330, my), "place · what happened · source", font=sans(9),
           fill=GREY)
    briefs = [
        (14, "Rome — Author Corrado Augias dies at 91.", "Euronews"),
        (15, "Mogadishu — Somalia expels UAE envoy.", "Al Jazeera"),
        (16, "Sudan — Absent RSF chief sentenced to death.", "AP"),
        (17, "Pretoria — Central bank holds rate at 7.25%.", "SABC"),
        (18, "Wellington — Pay-equity changes broke rights law.", "RNZ"),
        (19, "Tonga — Drought emergency takes effect.", "RNZ"),
        (20, "Space — Red giant seen eating a Sun-sized star.", "Nature"),
        (21, "Nairobi — Jepchirchir banned 3 years for doping.", "AP"),
        (22, "Gaza — Israel says its tank raid is over.", "BBC"),
        (23, "Florida — Floods shut Broward schools; 15.3 in rain.", "CBS"),
        (24, "Jakarta — Asset-seizure law finally passes.", "Kompas"),
        (25, "Paris — French left splits over Mélenchon pact.", "AFP"),
        (26, "Shenzhen — Xi urges a nuclear-arms ban.", "Al Jazeera"),
        (27, "Hormuz — Iran: mines set 5 tankers ablaze.", "Al Jazeera"),
        (28, "Krasnodar — Kyiv says it hit two oil refineries.", "Euronews"),
        (29, "Brussels — EU delays methane rules 2 years.", "Euronews"),
        (30, "UK — Yacht Bayesian \u2018vulnerable to wind\u2019.", "RNZ"),
        (31, "Zurich — Two rivals to challenge FIFA's Infantino.", "ABC"),
    ]
    bf, bfn = sans(11), sans(11, bold=True)
    col_w, row_h = 343, 19
    for i, (n, text, src) in enumerate(briefs):
        col, row = divmod(i, 9)
        bx, by = ax + col * col_w, my + 20 + row * row_h
        d.text((bx, by), str(n), font=bfn, fill=RED)
        nw = bfn.getlength(str(n)) + 5
        d.text((bx + nw, by), text, font=bf, fill=INK)
        tw = bf.getlength(text)
        d.text((bx + nw + tw + 4, by), src, font=bf, fill=GREY)

    # ---- date check
    dy = 944
    d.rectangle([12, dy, 1012, dy + 44], outline=RED, width=2)
    d.text((20, dy + 5), "DATE CHECK", font=sans(11, bold=True), fill=RED)
    dc = ("Every story here happened, or was first reported, on Thursday "
          "19 November 2026. LEFT OUT — 18 NOV: EU's \u20ac45bn Ukraine loan "
          "plan · Voyager 1 reaches one light-day · Iran fires on Kuwait "
          "and Bahrain. 17 NOV: US strikes on Iran's Qeshm Island. "
          "20 NOV: COP31 close · Akvan landfall.")
    draw_wrapped(d, 118, dy + 4, dc, sans(11), 886, INK, lh=14)

    # ---- footer
    d.line([12, 996, 1012, 996], fill=INK, width=1)
    foot = ("Claims are attributed, not stated as fact · Pictures and map: "
            "original, drawn in code · Sources: Reuters, AP, AFP, BBC, "
            "Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature · "
            "2026-11-19")
    ff = sans(9)
    d.text(((1024 - ff.getlength(foot)) / 2, 1002), foot, font=ff, fill=GREY)

    # Palette PNG: flat vector art compresses far better with 256 colours,
    # and keeps the file small (size is the leaderboard tie-break).
    img.quantize(colors=256, method=Image.Quantize.MEDIANCUT,
                 dither=Image.Dither.NONE).save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
