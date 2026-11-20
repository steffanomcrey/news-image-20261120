#!/usr/bin/env python3
"""news-image-20261120: Friday 20 November 2026 in one image.

Fresh authoring: 1024x1024 broadsheet front page, 52 stories, 16
illustrated panels, world map with numbered pins, briefs, DATE CHECK.
Build-time only (PIL). main.py copies entry.png to the output dir.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 252, 247, 255)
INK = (20, 20, 20, 255)
RED = (176, 32, 32, 255)
NAVY = (28, 56, 92, 255)
GREY = (112, 110, 104, 255)
LIGHT = (238, 236, 229, 255)
RULEC = (198, 196, 188, 255)
SKY = (214, 228, 240, 255)
SEA = (168, 196, 222, 255)
LAND = (232, 226, 205, 255)
GOLD = (198, 152, 44, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_FCACHE = {}


def font(path, size):
    key = (path, int(size))
    if key not in _FCACHE:
        _FCACHE[key] = ImageFont.truetype(path, int(size))
    return _FCACHE[key]


def serif(size):
    return font(SERIF, size)


def serifb(size):
    return font(SERIFB, size)


def sans(size):
    return font(SANS, size)


def sansb(size):
    return font(SANSB, size)


def tw(d, text, fnt):
    return int(d.textlength(text, font=fnt))


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if tw(d, trial, fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


STATS = {"overflow": []}


def block(d, x, y, lines, fnt, fill, lh, max_lines, tag):
    """Draw up to max_lines lines; record overflow (never more)."""
    if len(lines) > max_lines:
        STATS["overflow"].append((tag, len(lines), max_lines))
    use = lines[:max_lines]
    for i, ln in enumerate(use):
        d.text((x, y + i * lh), ln, font=fnt, fill=fill)
    return y + len(use) * lh


# ---------------------------------------------------------------- data
# (number, region, field, headline, deck, date label, lat, lon)
STORIES = [
    (1, "ASIA", "WEATHER", "Cyclone Akvan hits Odisha",
     "Comes ashore near Gopalpur by noon; 300,000 evacuated, gusts to 110 km/h.",
     None, 19.3, 84.9),
    (2, "AMERICAS", "DIPLOMACY", "Trump puts the Iran decision off to 2027",
     "He says there is 'no rush' and he will decide after the new year.",
     None, 38.9, -77.0),
    (3, "MIDEAST", "CONFLICT", "Houthi missile hits Riyadh's KAFD tower",
     "Windows blown out over 7-8 floors of the 80-storey PIF Tower; no one hurt.",
     "19 NOV", 24.7, 46.7),
    (4, "EUROPE", "LAW", "World court: Myanmar guilty of genocide",
     "ICJ rules 9-6 over the 2017 Rohingya crackdown and orders reparations.",
     "19 NOV", 52.1, 4.3),
    (5, "ASIA", "DIPLOMACY", "Trump, Xi, Putin meet in Shenzhen",
     "First three-way talks: nukes, the UN, oil and the ICC.",
     "19 NOV", 22.5, 114.1),
    (6, "EUROPE", "DIPLOMACY", "Europe ready to talk with Russia",
     "Leaders say they will negotiate on Ukraine, the BBC reports.",
     None, 52.5, 13.4),
    (7, "EUROPE", "WAR", "Russian strikes hit two Kyiv embassies",
     "Austrian and Dutch missions damaged; one killed, five hurt.",
     "19 NOV", 50.45, 30.52),
    (8, "EUROPE", "WAR", "Crimean Bridge hit again, rail halted",
     "Ukraine strikes the rail link for a third time this week.",
     None, 45.3, 36.5),
    (9, "ASIA", "SECURITY", "North Korea expands uranium enrichment",
     "IAEA: new Yongbyon extension built; concern is 'serious'.",
     "18 NOV", 39.8, 125.3),
    (10, "AMERICAS", "DIPLOMACY", "US and Venezuela restore military ties",
     "The two sides sign a deal to work together again.",
     None, 10.5, -66.9),
    (11, "ASIA", "JUSTICE", "South Korea court clears ex-PM Han",
     "Han's martial-law conviction is overturned on appeal.",
     None, 37.6, 127.0),
    (12, "OCEANIA", "CLIMATE", "Fiji declares a national disaster over drought",
     "El Nino leaves water short; a state of disaster is declared.",
     None, -18.1, 178.4),
    (13, "WORLD", "SPACE", "Voyager 1 crosses one light-day",
     "The 1977 probe is now a full light-day out: 16.1bn miles.",
     "18 NOV", 34.2, -118.1),
    (14, "ASIA", "SPACE", "Hayabusa2 gives up its asteroid landing",
     "Engine trouble forces JAXA to swap its 2031 target for a flyby.",
     "17 NOV", 35.55, 139.38),
    (15, "WORLD", "GAMES", "GTA VI sales pass $1.8bn",
     "Sensor Tower: day one $1.84bn, past The Odyssey's $1.805bn.",
     None, 25.8, -80.2),
    (16, "AMERICAS", "TECH", "Anthropic 'worth $1.5 trillion'",
     "IPO priced at $83 a share; $81.3bn raised; closes today.",
     None, 37.8, -122.4),
]

# (number, region, one-line text, lat, lon)
BRIEFS = [
    (17, "EUROPE", "EU-UK summit opens in Brussels; Burnham meets Costa", 50.8, 4.4),
    (18, "ASIA", "Justice Varma: resignation is not guilt, letter says", 28.6, 77.2),
    (19, "OCEANIA", "Nicholls 113 not out lifts NZ to 243 for 5, day one", -41.3, 174.8),
    (20, "ASIA", "Sensex up 1.21%, Nifty up 1.14% on Thursday", 19.1, 72.9),
    (21, "ASIA", "Modi meets the Prince and Princess of Wales", 28.6, 77.2),
    (22, "ASIA", "Modi opens FICCI's centenary convention in Delhi", 28.6, 77.2),
    (23, "ASIA", "Fire at Yunus ancestral home; arson is feared", 23.8, 90.4),
    (24, "WORLD", "COP31: India pushes climate finance in Turkiye", 39.9, 32.9),
    (25, "ASIA", "APEC leaders meet in Shenzhen; Xi urges open trade", 22.5, 114.1),
    (26, "EUROPE", "Denmark backs Trump's Greenland military pact", 55.7, 12.6),
    (27, "AMERICAS", "Jeffries set to be first Black House Speaker", 38.9, -77.0),
    (28, "AMERICAS", "Trump aide floated ceding Guyanese land: Reuters", 6.8, -58.2),
    (29, "EUROPE", "EU Commission hit by cyberattack, Politico says", 50.8, 4.4),
    (30, "AMERICAS", "South Florida floods; Broward gets 15 in of rain", 25.8, -80.2),
    (31, "WORLD", "Carlsen's shock forfeit leaves chess world fuming", 59.9, 10.7),
    (32, "AFRICA", "Bavuma ruled out of Bangladesh Test decider", 23.8, 90.4),
    (33, "ASIA", "India beat Malaysia in Hong Kong Open badminton", 22.3, 114.2),
    (34, "ASIA", "Women's Asian Hockey Champions Trophy begins", 28.6, 77.2),
    (35, "ASIA", "Pakistan minister heads to Delhi for SCO talks", 28.6, 77.2),
    (36, "OCEANIA", "Australia sanctions Israeli settlers in West Bank", 31.9, 35.2),
    (37, "ASIA", "Philippines-Chile trade deal is signed", 14.6, 121.0),
    (38, "AMERICAS", "Musk plans new projects in the Philippines", 14.6, 121.0),
    (39, "ASIA", "Harimau Shakti exercise opens in Ipoh", 4.6, 101.1),
    (40, "ASIA", "India electronics exports jump 44%", 28.6, 77.2),
    (41, "WORLD", "Crude oil futures fall more than 3%", 51.5, -0.1),
    (42, "AMERICAS", "US jobless claims come in at 203,000", 38.9, -77.0),
    (43, "WORLD", "World Children's Day is marked around the globe", 46.2, 6.1),
    (44, "EUROPE", "NATO assembly opens its 72nd session", 50.8, 4.4),
    (45, "EUROPE", "Merz hosts Qatar's emir in Berlin", 52.5, 13.4),
    (46, "EUROPE", "Bayern Munich beat Koln 3-0", 48.1, 11.6),
    (47, "AMERICAS", "Argentina 0-2 Australia in the U17 Cup", 25.3, 51.5),
    (48, "EUROPE", "EU delays methane rules by 24 months", 50.8, 4.4),
    (49, "EUROPE", "Youth anti-war protests march across Europe", 48.9, 2.3),
    (50, "AMERICAS", "US stocks slide; the Dow falls 1,084", 40.7, -74.0),
    (51, "ASIA", "Amur falcons cross the Arabian Sea", 15.0, 60.0),
    (52, "ASIA", "India's first bird-flu vaccine is ready", 28.6, 77.2),
]

NUMBERS = [
    ("300,000", "evacuated ahead of Akvan"),
    ("9-6", "ICJ vote: Myanmar guilty"),
    ("$1.8bn", "GTA VI day-one sales, est."),
    ("16.1bn mi", "Voyager 1 from Earth"),
    ("$1.5tn", "Anthropic, fully diluted"),
    ("423", "rescue teams in Odisha"),
]

TIMELINE = [
    ("OVERNIGHT", "Crimean Bridge hit again"),
    ("EARLY", "Trump: no rush on Iran"),
    ("MORNING", "Justice Varma letter lands"),
    ("MIDDAY", "Akvan landfall, Gopalpur"),
    ("AFTERNOON", "EU-UK summit, Brussels"),
    ("LATE", "GTA VI tops $1.8bn"),
]

DATE_CHECK = (
    "DATE CHECK: the ICJ verdict, the Shenzhen trilateral, the Riyadh tower "
    "strike and the Kyiv embassy strikes are labelled 19 NOV above. Voyager "
    "crossed one light-day on 18 Nov, the IAEA's Yongbyon report came 18 Nov, "
    "Hayabusa2's new target was set 17 Nov. All else happened, or was first "
    "reported, on Friday 20 November 2026."
)

FOOTER = (
    "Every story here happened, or was first reported, on Friday 20 November 2026, "
    "except the stories labelled 19 NOV, 18 NOV and 17 NOV above. Sources: Reuters, "
    "AP, AFP, BBC, The Hindu, NDTV. Original drawings. Contested claims are "
    "attributed, not stated as fact."
)

# ---------------------------------------------------------------- scenes
# Each scene returns a padded RGBA image (w+40, h+40); the artwork lives
# strictly inside the middle (w, h) box. All radii <= min(w, h)//2 - 2.
PAD = 20


def canvas(w, h):
    w, h = int(w), int(h)
    img = Image.new("RGBA", (w + 2 * PAD, h + 2 * PAD), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img), PAD, PAD


def scene_ok(img, w, h):
    bb = img.getbbox()
    if bb is None:
        return True
    return (bb[0] >= PAD and bb[1] >= PAD
            and bb[2] <= PAD + int(w) and bb[3] <= PAD + int(h))


def _bg(d, ox, oy, w, h, color):
    d.rectangle([ox, oy, ox + w - 1, oy + h - 1], fill=color)


def scene_cyclone(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (216, 228, 238, 255))
    cx, cy = ox + w // 2, oy + h // 2
    rmax = min(w, h) // 2 - 2
    dark = (24, 62, 110, 255)
    for k in range(5):
        r = rmax - k * (rmax // 5)
        if r < 3:
            break
        a0 = 20 + k * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + 250,
              fill=dark, width=max(2, rmax // 9))
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    return img


def scene_calendar(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (240, 238, 230, 255))
    pw, ph = int(w * 0.42), int(h * 0.86)
    px, py = ox + (w - pw) // 2, oy + (h - ph) // 2
    d.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255, 255),
                outline=INK, width=1)
    d.rectangle([px, py, px + pw, py + int(ph * 0.28)], fill=RED)
    d.text((px + 6, py + 2), "2027", font=serifb(max(10, int(ph * 0.24))),
           fill=(255, 255, 255, 255))
    cols, rows = 7, 3
    cw, ch = pw // cols, int(ph * 0.6) // rows
    for i in range(cols * rows):
        cx0 = px + (i % cols) * cw
        cy0 = py + int(ph * 0.34) + (i // cols) * ch
        d.rectangle([cx0 + 1, cy0 + 1, cx0 + cw - 1, cy0 + ch - 1],
                    outline=(200, 200, 200, 255))
    d.ellipse([px + pw - 12, py + ph - 12, px + pw - 2, py + ph - 2],
              outline=RED, width=2)
    d.text((ox + 6, oy + h - 12), "NO RUSH", font=sansb(9), fill=NAVY)
    return img


def scene_kafd(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (226, 214, 196, 255))
    base = oy + h - 4
    towers = [(0.06, 0.55), (0.22, 0.78), (0.40, 0.45), (0.58, 0.66),
              (0.74, 0.52), (0.88, 0.70)]
    for fx, fh in towers:
        twd = max(6, int(w * 0.10))
        tx = ox + int(fx * w)
        th = int(fh * h)
        d.rectangle([tx, base - th, tx + twd, base], fill=(52, 52, 58, 255))
        for wy in range(base - th + 4, base - 4, 6):
            d.line([tx + 2, wy, tx + twd - 2, wy], fill=(240, 220, 140, 255))
    d.rectangle([ox, base, ox + w - 1, base + 3], fill=(40, 40, 44, 255))
    return img


def scene_scales(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (238, 234, 222, 255))
    cx = ox + w // 2
    top = oy + 3
    beam_y = oy + int(h * 0.30)
    half = int(w * 0.36)
    gold = (176, 138, 40, 255)
    d.line([cx - half, beam_y, cx + half, beam_y], fill=gold, width=3)
    d.line([cx, top, cx, beam_y], fill=gold, width=3)
    d.ellipse([cx - 3, top - 3, cx + 3, top + 3], fill=gold)
    for sx in (cx - half, cx + half):
        d.line([sx, beam_y, sx - 8, beam_y + 12], fill=gold, width=2)
        d.line([sx, beam_y, sx + 8, beam_y + 12], fill=gold, width=2)
        d.arc([sx - 10, beam_y + 6, sx + 10, beam_y + 18], 0, 180,
              fill=gold, width=2)
    d.rectangle([cx - 3, beam_y, cx + 3, oy + h - 6], fill=gold)
    d.rectangle([cx - 12, oy + h - 6, cx + 12, oy + h - 2], fill=gold)
    return img


def scene_summit(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (224, 230, 236, 255))
    fw, fh = int(w * 0.24), int(h * 0.34)
    gap = int(w * 0.05)
    x0 = ox + int(w * 0.10)
    y0 = oy + 3
    # US flag
    d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(255, 255, 255, 255),
                outline=INK, width=1)
    for i in range(5):
        d.rectangle([x0, y0 + i * (fh // 5), x0 + fw, y0 + (i + 1) * (fh // 5)],
                    fill=RED if i % 2 == 0 else (255, 255, 255, 255))
    d.rectangle([x0, y0, x0 + int(fw * 0.4), y0 + int(fh * 0.55)], fill=NAVY)
    # China flag
    cx0 = x0 + fw + gap
    d.rectangle([cx0, y0, cx0 + fw, y0 + fh], fill=(222, 41, 16, 255))
    d.ellipse([cx0 + 3, y0 + 3, cx0 + 8, y0 + 8], fill=(255, 222, 89, 255))
    # Russia flag
    rx0 = cx0 + fw + gap
    d.rectangle([rx0, y0, rx0 + fw, y0 + fh], fill=(255, 255, 255, 255),
                outline=INK, width=1)
    d.rectangle([rx0, y0, rx0 + fw, y0 + fh // 3], fill=(255, 255, 255, 255))
    d.rectangle([rx0, y0 + fh // 3, rx0 + fw, y0 + 2 * fh // 3], fill=NAVY)
    d.rectangle([rx0, y0 + 2 * fh // 3, rx0 + fw, y0 + fh], fill=RED)
    # three seated figures
    fy = oy + h - 4
    for i, fx in enumerate((0.16, 0.50, 0.84)):
        fx0 = ox + int(fx * w)
        d.ellipse([fx0 - 5, fy - 22, fx0 + 5, fy - 12], fill=INK)
        d.polygon([(fx0 - 9, fy), (fx0 + 9, fy), (fx0 + 5, fy - 12),
                   (fx0 - 5, fy - 12)], fill=(70, 70, 76, 255))
    return img


def scene_europe(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (210, 222, 238, 255))
    cx, cy = ox + int(w * 0.30), oy + h // 2
    r = min(w, h) // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY)
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = cx + int(math.cos(a) * (r - 5))
        sy = cy + int(math.sin(a) * (r - 5))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=GOLD)
    bx = ox + int(w * 0.58)
    bw, bh = int(w * 0.34), int(h * 0.62)
    by = oy + (h - bh) // 2
    d.rectangle([bx, by, bx + bw, by + bh], fill=(240, 240, 236, 255),
                outline=INK, width=1)
    for i in range(4):
        d.rectangle([bx + 4 + i * (bw // 4), by + 4, bx + 8 + i * (bw // 4),
                     by + bh - 4], fill=NAVY)
    return img


def scene_kyiv(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (222, 230, 238, 255))
    base = oy + h - 3
    cx = ox + int(w * 0.28)
    rd = max(3, int(h * 0.18))
    cw = min(int(w * 0.20), 4 * rd + 8)
    ch = int(h * 0.40)
    d.rectangle([cx - cw // 2, base - ch, cx + cw // 2, base],
                fill=(238, 236, 228, 255), outline=INK, width=1)
    d.pieslice([cx - rd, base - ch - rd, cx + rd, base - ch + rd],
               180, 360, fill=GOLD)
    d.line([cx, base - ch - 2 * rd - 4, cx, base - ch - 2 * rd],
           fill=INK, width=2)
    d.line([cx - 3, base - ch - 2 * rd - 2, cx + 3, base - ch - 2 * rd - 2],
           fill=INK, width=2)
    # quadcopter, large, right side
    qx, qy = ox + int(w * 0.68), oy + h // 2
    arm = int(w * 0.14)
    d.line([qx - arm, qy - 6, qx + arm, qy + 6], fill=INK, width=2)
    d.line([qx - arm, qy + 6, qx + arm, qy - 6], fill=INK, width=2)
    d.ellipse([qx - 7, qy - 4, qx + 7, qy + 4], fill=(60, 60, 66, 255))
    for dx, dy in ((-arm, -6), (arm, 6), (-arm, 6), (arm, -6)):
        rx, ry = qx + dx, qy + dy
        d.line([rx - 7, ry, rx + 7, ry], fill=INK, width=2)
    return img


def scene_bridge(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (206, 224, 238, 255))
    midy = oy + int(h * 0.45)
    d.line([ox, midy, ox + w - 1, midy], fill=(70, 70, 76, 255), width=3)
    d.arc([ox + 6, midy - int(h * 0.30), ox + w - 6, midy + int(h * 0.30)],
          180, 360, fill=(70, 70, 76, 255), width=2)
    for fx in (0.15, 0.5, 0.85):
        px = ox + int(fx * w)
        d.line([px, midy, px, oy + h - 8], fill=(70, 70, 76, 255), width=2)
    for wy in range(oy + h - 8, oy + h - 2, 3):
        d.line([ox + 4, wy, ox + w - 4, wy], fill=(120, 160, 200, 255))
    return img


def scene_atom(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (228, 232, 238, 255))
    cx, cy = ox + w // 2, oy + h // 2
    rx, ry = int(w * 0.38), min(w, h) // 2 - 2
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=NAVY, width=2)
    d.ellipse([cx - rx, cy - ry // 2, cx + rx, cy + ry // 2],
              outline=NAVY, width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    d.ellipse([cx + rx - 3, cy - 3, cx + rx + 3, cy + 3], fill=NAVY)
    return img


def scene_flags(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (240, 238, 230, 255))
    fw, fh = int(w * 0.30), int(h * 0.58)
    y0 = oy + 2
    x0 = ox + int(w * 0.12)
    d.rectangle([x0, y0, x0 + fw, y0 + fh], fill=(255, 255, 255, 255),
                outline=INK, width=1)
    for i in range(5):
        d.rectangle([x0, y0 + i * (fh // 5), x0 + fw, y0 + (i + 1) * (fh // 5)],
                    fill=RED if i % 2 == 0 else (255, 255, 255, 255))
    d.rectangle([x0, y0, x0 + int(fw * 0.4), y0 + int(fh * 0.55)], fill=NAVY)
    vx0 = ox + int(w * 0.58)
    d.rectangle([vx0, y0, vx0 + fw, y0 + fh], fill=(255, 255, 255, 255),
                outline=INK, width=1)
    d.rectangle([vx0, y0, vx0 + fw, y0 + fh // 3], fill=(252, 209, 22, 255))
    d.rectangle([vx0, y0 + fh // 3, vx0 + fw, y0 + 2 * fh // 3], fill=NAVY)
    d.rectangle([vx0, y0 + 2 * fh // 3, vx0 + fw, y0 + fh], fill=RED)
    d.text((ox + 6, oy + h - 11), "DEAL SIGNED", font=sansb(9), fill=NAVY)
    return img


def scene_gavel(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (238, 234, 222, 255))
    # gavel head, left
    hx, hy = ox + int(w * 0.16), oy + int(h * 0.42)
    hw, hh = int(w * 0.20), int(h * 0.34)
    d.rectangle([hx, hy, hx + hw, hy + hh], fill=(120, 82, 40, 255))
    d.rectangle([hx - 3, hy - 3, hx + hw + 3, hy + 2], fill=(90, 60, 28, 255))
    d.rectangle([hx - 3, hy + hh - 2, hx + hw + 3, hy + hh + 3],
                fill=(90, 60, 28, 255))
    d.line([hx + hw, hy + hh // 2, ox + int(w * 0.52), hy + hh // 2 + 6],
           fill=(120, 82, 40, 255), width=3)
    # sound block
    bx = ox + int(w * 0.52)
    d.rectangle([bx, oy + h - 10, bx + int(w * 0.12), oy + h - 4],
                fill=(90, 60, 28, 255))
    # taegeuk circle, top right, clear of the head
    cx, cy = ox + int(w * 0.84), oy + h // 2
    r = min(w, h) // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=1)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=RED)
    d.pieslice([cx - r, cy - r, cx + r, cy + r], 270, 90, fill=NAVY)
    return img


def scene_drought(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (240, 228, 200, 255))
    cx, cy = ox + int(w * 0.80), oy + h // 2
    r = min(w, h) // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 160, 40, 255))
    base = oy + h - 4
    d.rectangle([ox, base - 6, ox + w - 1, base], fill=(196, 160, 110, 255))
    d.line([ox + 10, base - 6, ox + 30, base - 14], fill=(140, 100, 60, 255),
           width=2)
    d.line([ox + 30, base - 14, ox + 55, base - 6], fill=(140, 100, 60, 255),
           width=2)
    d.line([ox + int(w * 0.55), base - 6, ox + int(w * 0.70), base - 13],
           fill=(140, 100, 60, 255), width=2)
    return img


def scene_voyager(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (16, 22, 40, 255))
    import random
    rnd = random.Random(7)
    for _ in range(14):
        sx = ox + rnd.randint(2, w - 3)
        sy = oy + rnd.randint(2, h - 3)
        d.ellipse([sx, sy, sx + 1, sy + 1], fill=(255, 255, 255, 255))
    cx, cy = ox + int(w * 0.30), oy + h // 2
    d.polygon([(cx - 10, cy - 3), (cx + 10, cy - 3), (cx + 4, cy + 3),
               (cx - 4, cy + 3)], fill=(220, 220, 220, 255))
    d.line([cx - 14, cy, cx - 10, cy], fill=(220, 220, 220, 255), width=2)
    d.arc([cx + 12, cy - 10, cx + 34, cy + 10], 270, 90, fill=GOLD, width=2)
    d.text((ox + int(w * 0.55), oy + h - 12), "1 LIGHT-DAY", font=sansb(9),
           fill=(255, 255, 255, 255))
    return img


def scene_asteroid(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (18, 20, 36, 255))
    cx, cy = ox + int(w * 0.30), oy + h // 2
    r = min(w, h) // 2 - 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 140, 130, 255))
    d.ellipse([cx - r // 2, cy - r // 3, cx - r // 4, cy], fill=(110, 100, 90, 255))
    d.ellipse([cx + r // 4, cy + r // 4, cx + r // 2, cy + r // 2],
              fill=(110, 100, 90, 255))
    px = ox + int(w * 0.72)
    d.polygon([(px - 8, cy - 3), (px + 8, cy - 3), (px + 3, cy + 3),
               (px - 3, cy + 3)], fill=(220, 220, 220, 255))
    d.line([px - 12, cy, px - 8, cy], fill=(220, 220, 220, 255), width=2)
    return img


def scene_gta(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (42, 28, 58, 255))
    base = oy + h - 3
    for i, fh in enumerate((0.45, 0.70, 0.55, 0.85, 0.60)):
        bw = int(w * 0.16)
        bx = ox + int(i * w * 0.19) + 2
        th = int(fh * h)
        d.rectangle([bx, base - th, bx + bw, base], fill=(24, 16, 34, 255))
        for wy in range(base - th + 4, base - 4, 6):
            d.line([bx + 2, wy, bx + bw - 2, wy], fill=(250, 210, 90, 255))
    d.text((ox + int(w * 0.68), oy + 2), "VI", font=serifb(max(12, int(h * 0.55))),
           fill=(250, 210, 90, 255))
    return img


def scene_chip(w, h):
    img, d, ox, oy = canvas(w, h)
    _bg(d, ox, oy, w, h, (222, 228, 234, 255))
    s = min(w, h) - 8
    cx, cy = ox + w // 2, oy + h // 2
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(30, 30, 36, 255))
    inner = s // 2
    d.rectangle([cx - inner // 2, cy - inner // 2, cx + inner // 2,
                 cy + inner // 2], fill=(40, 90, 140, 255))
    for i in range(4):
        off = -s // 2 + 4 + i * (s // 3)
        d.line([cx + off, cy - s // 2 - 3, cx + off, cy - s // 2], fill=INK,
               width=2)
        d.line([cx + off, cy + s // 2, cx + off, cy + s // 2 + 3], fill=INK,
               width=2)
    return img


SCENES = [scene_cyclone, scene_calendar, scene_kafd, scene_scales,
          scene_summit, scene_europe, scene_kyiv, scene_bridge,
          scene_atom, scene_flags, scene_gavel, scene_drought,
          scene_voyager, scene_asteroid, scene_gta, scene_chip]

# ---------------------------------------------------------------- map
# Coarse continent outlines as (lon, lat) lists, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-100, 73), (-85, 70), (-80, 73),
     (-70, 62), (-60, 55), (-65, 45), (-75, 35), (-80, 26), (-85, 30),
     (-95, 29), (-97, 26), (-105, 22), (-110, 28), (-115, 32), (-125, 40),
     (-125, 49), (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-75, -10), (-80, -15), (-75, -25),
     (-70, -35), (-65, -45), (-68, -52), (-65, -55), (-60, -45), (-55, -35),
     (-50, -25), (-45, -15), (-40, -5), (-35, -8), (-45, -2), (-55, 5),
     (-65, 8), (-75, 10)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (45, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (9, -5),
     (9, 4), (0, 5), (-8, 4), (-13, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (28, 65),
     (25, 70), (20, 70), (15, 68), (12, 65), (10, 62), (5, 58), (0, 55),
     (-5, 50), (-10, 45)],
    [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 76), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 66), (162, 60), (158, 55), (150, 60), (142, 55), (140, 45),
     (135, 35), (130, 33), (127, 35), (122, 38), (120, 30), (115, 25),
     (110, 20), (108, 12), (105, 8), (100, 10), (95, 15), (90, 22),
     (85, 20), (80, 15), (75, 10), (72, 20), (68, 25), (62, 25), (58, 26),
     (55, 26), (52, 28), (50, 30), (48, 30), (45, 28), (42, 20), (40, 15),
     (38, 12), (35, 10), (32, 15), (30, 20), (30, 30), (30, 36), (30, 42),
     (35, 45), (30, 50), (28, 55)],
    [(113, -22), (114, -30), (115, -35), (120, -35), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -25),
     (146, -20), (142, -15), (140, -12), (135, -12), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20)],
]

OFFSETS = [(0, 0), (12, 0), (-12, 0), (0, 12), (0, -12), (18, 8), (-18, 8),
           (18, -8), (-18, -8), (26, 0), (-26, 0), (0, 26), (0, -26),
           (34, 12), (-34, 12), (34, -12), (-34, -12), (44, 0), (-44, 0),
           (0, 44), (0, -44), (56, 16), (-56, 16), (56, -16), (-56, -16),
           (68, 0), (-68, 0), (0, 68), (0, -68), (76, 20), (-76, 20),
           (76, -20), (-76, -20)]


def project(lon, lat, mx, my, mw, mh):
    x = int(mx + (lon + 180.0) / 360.0 * mw)
    y = int(my + (78.0 - lat) / 133.0 * mh)
    return x, y


# ---------------------------------------------------------------- layout
def region_counts():
    counts = {}
    for s in STORIES + BRIEFS:
        counts[s[1]] = counts.get(s[1], 0) + 1
    return counts


def draw_card(d, x, y, w, h, story, scene_w, scene_h, hf, df, lf,
              max_head=2, max_deck=2):
    num, region, field, head, deck, date = story[:6]
    img = SCENES[num - 1](scene_w, scene_h)
    paste = img.crop((PAD, PAD, PAD + scene_w, PAD + scene_h))
    return paste, num, region, field, head, deck, date


def render():
    img = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    counts = region_counts()
    # masthead
    d.rectangle([0, 0, W, 4], fill=RED)
    title = "Friday 20 November 2026"
    tf = serifb(40)
    d.text(((W - tw(d, title, tf)) // 2, 10), title, font=tf, fill=INK)
    kick = "THE WORLD IN ONE PAGE  —  52 STORIES, 7 REGIONS"
    kf = sansb(11)
    d.text(((W - tw(d, kick, kf)) // 2, 56), kick, font=kf, fill=NAVY)
    d.line([24, 74, W - 24, 74], fill=RULEC, width=1)
    # region bar
    regions = ["ASIA", "EUROPE", "AMERICAS", "WORLD", "OCEANIA", "MIDEAST",
               "AFRICA"]
    cw = (W - 48 - 6 * 4) // 7
    for i, rg in enumerate(regions):
        x0 = 24 + i * (cw + 4)
        d.rectangle([x0, 80, x0 + cw, 102], fill=LIGHT, outline=RULEC)
        label = "%s %d" % (rg, counts.get(rg, 0))
        lf = sansb(11)
        d.text((x0 + (cw - tw(d, label, lf)) // 2, 86), label, font=lf,
               fill=NAVY)
    # numbers strip
    nw = (W - 48 - 5 * 6) // 6
    for i, (val, cap) in enumerate(NUMBERS):
        x0 = 24 + i * (nw + 6)
        vf = serifb(20)
        d.text((x0 + (nw - tw(d, val, vf)) // 2, 108), val, font=vf, fill=RED)
        cf = sans(9)
        lines = wrap(d, cap, cf, nw)
        block(d, x0, 132, lines, cf, INK, 11, 2, "num%d" % i)
    d.line([24, 150, W - 24, 150], fill=RULEC, width=1)
    # timeline
    tf2 = sansb(11)
    d.text((24, 156), "THE DAY IN UTC", font=tf2, fill=RED)
    twd = (W - 48 - 5 * 6) // 6
    for i, (lab, txt) in enumerate(TIMELINE):
        x0 = 24 + i * (twd + 6)
        d.text((x0, 172), lab, font=sansb(9), fill=NAVY)
        lines = wrap(d, txt, sans(9), twd)
        block(d, x0, 183, lines, sans(9), INK, 11, 1, "tl%d" % i)
    d.line([24, 192, W - 24, 192], fill=RULEC, width=1)
    # leads 2x2
    lw = (W - 48 - 10) // 2
    lh = 122
    for idx in range(4):
        r, c = divmod(idx, 2)
        x0 = 24 + c * (lw + 10)
        y0 = 198 + r * (lh + 8)
        s = STORIES[idx]
        paste, num, region, field, head, deck, date = draw_card(
            d, x0, y0, lw, lh, s, lw, 50, None, None, None)
        img.paste(paste, (x0, y0))
        yy = y0 + 54
        lab = "%d  %s  ·  %s" % (num, region, field)
        d.text((x0, yy), lab, font=sansb(10), fill=NAVY)
        if date:
            cx0 = x0 + tw(d, lab, sansb(10)) + 6
            d.rectangle([cx0, yy, cx0 + 42, yy + 12], fill=RED)
            d.text((cx0 + 4, yy + 1), date, font=sansb(8),
                   fill=(255, 255, 255, 255))
        yy += 14
        block(d, x0, yy, wrap(d, head, serifb(15), lw), serifb(15), INK,
              17, 2, "lead%d-head" % num)
        yy += 32
        block(d, x0, yy, wrap(d, deck, sans(11), lw), sans(11), GREY,
              13, 2, "lead%d-deck" % num)
    # mids 4x3
    mw = (W - 48 - 3 * 8) // 4
    mh = 80
    for idx in range(12):
        r, c = divmod(idx, 4)
        x0 = 24 + c * (mw + 8)
        y0 = 454 + r * (mh + 6)
        s = STORIES[4 + idx]
        paste, num, region, field, head, deck, date = draw_card(
            d, x0, y0, mw, mh, s, mw, 26, None, None, None)
        img.paste(paste, (x0, y0))
        yy = y0 + 28
        lab = "%d %s" % (num, region)
        d.text((x0, yy), lab, font=sansb(9), fill=NAVY)
        if date:
            cx0 = x0 + tw(d, lab, sansb(9)) + 4
            d.rectangle([cx0, yy, cx0 + 34, yy + 10], fill=RED)
            d.text((cx0 + 3, yy), date, font=sansb(7),
                   fill=(255, 255, 255, 255))
        yy += 11
        block(d, x0, yy, wrap(d, head, serifb(11), mw), serifb(11), INK,
              13, 2, "mid%d-head" % num)
        yy += 24
        block(d, x0, yy, wrap(d, deck, sans(9), mw), sans(9), GREY,
              11, 2, "mid%d-deck" % num)
    # map
    d.text((24, 706), "THE WORLD — WHERE IT HAPPENED", font=sansb(11),
           fill=RED)
    mx, my, mw2, mh2 = 24, 722, W - 48, 112
    d.rectangle([mx, my, mx + mw2, my + mh2], fill=SEA, outline=RULEC)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw2, mh2) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(180, 172, 150, 255))
    placed = []
    pin_pos = {}
    for s in STORIES:
        num, lat, lon = s[0], s[6], s[7]
        px, py = project(lon, lat, mx, my, mw2, mh2)
        chosen = None
        for ox, oy in OFFSETS:
            cx, cy = px + ox, py + oy
            if all((cx - qx) ** 2 + (cy - qy) ** 2 >= 17 ** 2
                   for qx, qy in placed):
                chosen = (cx, cy)
                break
        if chosen is None:
            chosen = (px + OFFSETS[-1][0], py + OFFSETS[-1][1])
        placed.append(chosen)
        pin_pos[num] = (chosen, (px, py))
    for num, ((cx, cy), (px, py)) in pin_pos.items():
        if (cx, cy) != (px, py):
            d.line([px, py, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=(255, 255, 255, 255))
        nf = sansb(9)
        t = str(num)
        d.text((cx - tw(d, t, nf) // 2, cy - 5), t, font=nf,
               fill=(255, 255, 255, 255))
    # briefs, 3 columns x 12 rows
    bw = (W - 48 - 2 * 8) // 3
    bf = sans(9)
    for i, b in enumerate(BRIEFS):
        col, row = divmod(i, 12)
        x0 = 24 + col * (bw + 8)
        y0 = 842 + row * 9
        pre = "%d %s  " % (b[0], b[1])
        d.text((x0, y0), pre, font=sansb(8), fill=NAVY)
        d.text((x0 + tw(d, pre, sansb(8)), y0), b[2], font=bf, fill=INK)
    # DATE CHECK
    d.rectangle([24, 954, W - 24, 988], outline=RED, width=1)
    d.text((30, 958), "DATE CHECK", font=sansb(9), fill=RED)
    lines = wrap(d, DATE_CHECK, sans(10), W - 48 - 12)
    block(d, 30, 958, lines, sans(10), INK, 12, 2, "datecheck")
    # footer
    lines = wrap(d, FOOTER, sans(9), W - 48)
    block(d, 24, 992, lines, sans(9), GREY, 11, 2, "footer")
    return img, pin_pos


def main():
    # scene-bounds check first
    bad = []
    for i, fn in enumerate(SCENES, start=1):
        for (sw, sh) in ((483, 50), (238, 26)):
            im = fn(sw, sh)
            if not scene_ok(im, sw, sh):
                bad.append((i, sw, sh, im.getbbox()))
    print("BOUNDS spill=%s" % ("NONE" if not bad else bad))
    img, pin_pos = render()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.convert("RGB").save(out, "PNG")
    # pin check: red pixels near each placed pin centre
    px = img.convert("RGB")
    missing = []
    for num, ((cx, cy), _) in pin_pos.items():
        found = 0
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                r, g, b = px.getpixel((cx + dx, cy + dy))
                if r > 150 and g < 90 and b < 90:
                    found += 1
        if found == 0:
            missing.append(num)
    print("PINS missing=%s" % ("NONE" if not missing else missing))
    ov = STATS["overflow"]
    print("WRAP overflow=%s" % ("NONE" if not ov else ov))
    print("COUNTS %s total=%d" % (region_counts(),
                                  sum(region_counts().values())))
    print("SAVED %s" % out)


if __name__ == "__main__":
    main()
