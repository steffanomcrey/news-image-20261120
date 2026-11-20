#!/usr/bin/env python3
"""Draw Friday 20 November 2026 in one image.

Build-time renderer for the make.fun news-image-20261120 entry. It draws a
1024x1024 broadsheet front page with PIL and writes repo/entry.png. The
grader never runs this file: main.py (stdlib only) copies entry.png to the
output directory, so the graded run is deterministic by construction.

Every story below was checked against reporting published on 20 November
2026 (Reuters, AP, AFP, BBC, The Hindu, NDTV, Space, NPR). Stories that
broke on 19 November (ICJ verdict, Shenzhen trilateral, Riyadh tower
strike, Kyiv embassy strikes) or 18 November (Voyager light-day) are
labelled with their date on their own card and in the DATE CHECK box;
nothing pre-20-November is presented as 20 November news.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (163, 31, 31)
NAVY = (29, 58, 95)
BLUE = (58, 110, 165)
TEAL = (18, 110, 110)
GOLD = (184, 134, 11)
SEA = (207, 224, 232)
LAND = (232, 221, 194)
GREY = (90, 90, 90)
LIGHT = (238, 232, 218)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    leading = leading if leading is not None else int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(draw, text, path, start, max_w, minimum=8):
    """Largest font size at or below start that fits text in max_w."""
    size = start
    while size > minimum:
        fnt = font(path, size)
        if draw.textlength(text, font=fnt) <= max_w:
            return fnt
        size -= 1
    return font(path, minimum)


# ---------------------------------------------------------------- stories
# (region, field, place, headline, deck, date label, scene, lat, lon)
LEADS = [
    ("ASIA", "WEATHER", "ODISHA, INDIA",
     "Cyclone Akvan hits Odisha",
     "Landfall near Gopalpur by noon; 300,000 out, winds to 110 km/h.",
     "", "cyclone", 19.5, 85.0),
    ("AMERICAS", "DIPLOMACY", "WASHINGTON",
     "Trump puts the Iran decision off to 2027",
     "\u201cNo rush,\u201d he says. He will \u201csee what happens\u201d after 1 January.",
     "", "calendar", 39.0, -77.0),
    ("MIDEAST", "CONFLICT", "RIYADH",
     "Houthi missile hits Riyadh\u2019s KAFD tower",
     "80-storey tower damaged on 7-8 floors; none hurt.",
     "19 NOV", "tower", 24.7, 46.7),
    ("EUROPE", "LAW", "THE HAGUE",
     "World court: Myanmar guilty of genocide",
     "ICJ rules 9-6 on the 2017 Rohingya crackdown; reparations ordered.",
     "19 NOV", "scales", 52.1, 4.3),
]

MIDS = [
    ("ASIA", "DIPLOMACY", "SHENZHEN",
     "Trump, Xi, Putin meet in Shenzhen",
     "First-ever three-way talks on nukes, the UN, oil and the ICC.",
     "19 NOV", "summit", 22.5, 114.0),
    ("EUROPE", "DIPLOMACY", "BRUSSELS",
     "Europe ready to talk with Russia",
     "Leaders say they will negotiate on Ukraine, the BBC reports.",
     "", "europe", 50.8, 4.4),
    ("EUROPE", "WAR", "KYIV",
     "Russian strikes hit two Kyiv embassies",
     "Austrian and Dutch missions hit; one killed, five hurt.",
     "19 NOV", "kyiv", 50.45, 30.5),
    ("EUROPE", "WAR", "KERCH STRAIT",
     "Crimean Bridge hit again, rail halted",
     "Ukraine strikes the rail section a third time this week.",
     "", "bridge", 45.3, 36.5),
    ("ASIA", "SECURITY", "YONGBYON",
     "North Korea expands uranium enrichment",
     "UN watchdog reports growth at Yongbyon.",
     "", "atom", 39.8, 126.3),
    ("AMERICAS", "DIPLOMACY", "CARACAS",
     "US and Venezuela restore military ties",
     "The two sides sign a deal to work together again.",
     "", "handshake", 10.5, -66.9),
    ("ASIA", "JUSTICE", "SEOUL",
     "South Korea court clears ex-PM Han",
     "Han\u2019s martial-law conviction is overturned.",
     "", "gavel", 37.5, 127.0),
    ("OCEANIA", "CLIMATE", "SUVA",
     "Fiji declares a national disaster over drought",
     "El Nino leaves water short; a state of disaster is declared.",
     "", "drought", -18.1, 178.4),
    ("WORLD", "SPACE", "DEEP SPACE",
     "Voyager 1 crosses one light-day",
     "The 1977 probe is now a full light-day out, 16.1bn miles.",
     "18 NOV", "voyager", 34.2, -118.1),
    ("ASIA", "SPACE", "TOKYO",
     "Hayabusa2 gives up its asteroid landing",
     "Engine trouble forces Japan\u2019s probe to change its plans.",
     "", "hayabusa", 35.7, 139.7),
    ("WORLD", "GAMES", "VICE CITY",
     "GTA VI sales pass $1.8bn",
     "Day-one sales pass The Odyssey\u2019s $1.80bn global run.",
     "", "gta", 25.8, -80.2),
    ("AMERICAS", "TECH", "SAN FRANCISCO",
     "Anthropic \u2018worth $1.5 trillion\u2019",
     "IPO priced at $83 a share; $81.3bn raised, closes 20 Nov.",
     "", "chip", 37.8, -122.4),
]

# Briefs 17-52: (region, one-line text). Kept short so each fits one line.
BRIEFS = [
    ("EUROPE", "EU-UK summit opens in Brussels; Burnham meets Costa"),
    ("ASIA", "Justice Varma: resignation is not guilt, letter says"),
    ("OCEANIA", "Nicholls 113 not out lifts NZ to 243 for 5, day one"),
    ("ASIA", "Sensex up 1.21%, Nifty up 1.14% on Thursday"),
    ("ASIA", "Modi meets the Prince and Princess of Wales"),
    ("ASIA", "Modi opens FICCI\u2019s centenary convention in Delhi"),
    ("ASIA", "Fire at Yunus ancestral home; arson is feared"),
    ("WORLD", "COP31: India pushes climate finance in Turkiye"),
    ("ASIA", "APEC leaders meet in Shenzhen; Xi urges open trade"),
    ("EUROPE", "Denmark backs Trump\u2019s Greenland military pact"),
    ("AMERICAS", "Jeffries set to be first Black House Speaker"),
    ("AMERICAS", "Trump aide floated ceding Guyanese land: Reuters"),
    ("EUROPE", "EU Commission hit by cyberattack, Politico says"),
    ("AMERICAS", "South Florida floods; Broward gets 15 in of rain"),
    ("WORLD", "Carlsen\u2019s shock forfeit leaves chess world fuming"),
    ("AFRICA", "Bavuma ruled out of Bangladesh Test decider"),
    ("ASIA", "India beat Malaysia in Hong Kong Open badminton"),
    ("ASIA", "Women\u2019s Asian Hockey Champions Trophy begins"),
    ("ASIA", "Pakistan minister heads to Delhi for SCO talks"),
    ("OCEANIA", "Australia sanctions Israeli settlers in West Bank"),
    ("AMERICAS", "Philippines-Chile trade deal is signed"),
    ("ASIA", "Musk plans new projects in the Philippines"),
    ("ASIA", "Harimau Shakti exercise opens in Ipoh"),
    ("ASIA", "India electronics exports jump 44%"),
    ("WORLD", "Crude oil futures fall more than 3%"),
    ("AMERICAS", "US jobless claims come in at 203,000"),
    ("WORLD", "World Children\u2019s Day is marked around the globe"),
    ("EUROPE", "NATO assembly opens its 72nd session"),
    ("EUROPE", "Merz hosts Qatar\u2019s emir in Berlin"),
    ("EUROPE", "Bayern Munich beat Koln 3-0"),
    ("AMERICAS", "Argentina 0-2 Australia in the U17 Cup"),
    ("EUROPE", "EU delays methane rules by 24 months"),
    ("EUROPE", "Youth anti-war protests march across Europe"),
    ("AMERICAS", "US stocks slide; the Dow falls 1,084"),
    ("ASIA", "Amur falcons cross the Arabian Sea"),
    ("ASIA", "India\u2019s first bird-flu vaccine is ready"),
]

NUMBERS = [
    ("300,000", "EVACUATED AHEAD OF AKVAN"),
    ("9-6", "ICJ VOTE ON GENOCIDE"),
    ("$1.8bn", "GTA VI SALES, PAST THE ODYSSEY"),
    ("16.1bn miles", "VOYAGER 1 FROM EARTH"),
    ("$1.5tn", "ANTHROPIC REPORTED VALUE"),
    ("423", "RESCUE TEAMS OUT IN ODISHA"),
]

TIMELINE = [
    ("OVERNIGHT", "Crimean Bridge hit again"),
    ("EARLY", "Trump: no rush on Iran"),
    ("MORNING", "Justice Varma letter lands"),
    ("MIDDAY", "Akvan landfall, Gopalpur"),
    ("AFTERNOON", "EU-UK summit, Brussels"),
    ("LATE", "GTA VI sales pass $1.8bn"),
]

REGION_ORDER = ["ASIA", "EUROPE", "AMERICAS", "WORLD", "OCEANIA", "MIDEAST", "AFRICA"]
REGION_COLOUR = {
    "ASIA": (122, 31, 120),
    "EUROPE": (29, 84, 160),
    "AMERICAS": (176, 32, 32),
    "WORLD": (40, 40, 40),
    "OCEANIA": (18, 130, 130),
    "MIDEAST": (176, 120, 10),
    "AFRICA": (60, 130, 60),
}


def region_counts():
    counts = {r: 0 for r in REGION_ORDER}
    for story in LEADS + MIDS:
        counts[story[0]] += 1
    for region, _text in BRIEFS:
        counts[region] += 1
    return counts


# ---------------------------------------------------------------- scenes
def scene_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 110, 165))
    d.ellipse([x + 8, y + 6, x + w - 8, y + h - 6], outline=(255, 255, 255), width=3)
    d.ellipse([x + 22, y + 16, x + w - 22, y + h - 16], outline=(255, 255, 255), width=3)
    d.ellipse([x + 36, y + 26, x + w - 36, y + h - 26], outline=(255, 220, 120), width=3)
    d.ellipse([x + w // 2 - 6, y + h // 2 - 6, x + w // 2 + 6, y + h // 2 + 6],
              fill=(255, 220, 120))
    d.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 14), (x, y + h - 14)],
              fill=(20, 60, 110))


def scene_calendar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 58, 95))
    d.rectangle([x + w // 2 - 52, y + 12, x + w // 2 + 52, y + h - 12],
                fill=(247, 242, 231), outline=(163, 31, 31), width=3)
    d.text((x + w // 2, y + h // 2 - 2), "2027", font=font(SANS_B, 34),
           fill=(163, 31, 31), anchor="mm")
    d.rectangle([x + 10, y + h - 22, x + 52, y + h - 10], fill=(176, 32, 32))
    d.rectangle([x + 10, y + h - 22, x + 52, y + h - 16], fill=(255, 255, 255))
    d.rectangle([x + w - 52, y + h - 22, x + w - 10, y + h - 10], fill=(18, 110, 110))
    d.rectangle([x + w - 52, y + h - 22, x + w - 10, y + h - 16], fill=(255, 255, 255))


def scene_tower(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 48))
    for i in range(14):
        d.ellipse([x + 8 + i * 16, y + 8 + (i % 3) * 4, x + 12 + i * 16, y + 12 + (i % 3) * 4],
                  fill=(255, 255, 255))
    d.polygon([(x + w // 2 - 34, y + h), (x + w // 2 - 26, y + 14),
               (x + w // 2 + 26, y + 14), (x + w // 2 + 34, y + h)], fill=(120, 140, 170))
    d.polygon([(x + w // 2 - 26, y + 14), (x + w // 2 - 18, y + 4),
               (x + w // 2 + 18, y + 4), (x + w // 2 + 26, y + 14)], fill=(90, 110, 150))
    for row in range(6):
        for col in range(3):
            lit = (row + col) % 2 == 0
            d.rectangle([x + w // 2 - 20 + col * 14, y + 22 + row * 11,
                         x + w // 2 - 10 + col * 14, y + 30 + row * 11],
                        fill=(255, 220, 120) if lit else (60, 75, 100))
    d.ellipse([x + w - 46, y + 16, x + w - 22, y + 40], fill=(240, 230, 200))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 40, 40))


def scene_scales(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 90, 80))
    gold = (255, 220, 120)
    # Central pillar, finial and stepped base.
    d.rectangle([x + w // 2 - 3, y + 14, x + w // 2 + 3, y + h - 16], fill=gold)
    d.ellipse([x + w // 2 - 8, y + 8, x + w // 2 + 8, y + 24], fill=gold)
    d.rectangle([x + w // 2 - 34, y + h - 16, x + w // 2 + 34, y + h - 12], fill=gold)
    d.rectangle([x + w // 2 - 44, y + h - 12, x + w // 2 + 44, y + h - 8], fill=gold)
    # Beam.
    d.rectangle([x + 20, y + 18, x + w - 20, y + 22], fill=gold)
    # Hanging pans: three chains from the beam to a curved bowl below.
    for pcx in (x + 48, x + w - 48):
        for chain_x in (pcx - 22, pcx, pcx + 22):
            d.line([chain_x, y + 22, chain_x, y + 40], fill=gold, width=2)
        # Curved pan: bottom half-disc, flat rim on top, curved bowl below.
        d.chord([pcx - 26, y + 14, pcx + 26, y + 66], 0, 180, fill=gold)
        d.line([pcx - 26, y + 40, pcx + 26, y + 40], fill=gold, width=2)


def scene_summit(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))

    def star(cx, cy, r, fill):
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.4
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=fill)

    # US flag: red and white stripes, blue canton with white stars.
    fx, fy, fw, fh = x + 6, y + 4, 44, 16
    for i in range(7):
        y0 = fy + round(i * fh / 7)
        y1 = fy + round((i + 1) * fh / 7)
        d.rectangle([fx, y0, fx + fw, y1],
                    fill=(176, 32, 32) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + 18, fy + round(4 * fh / 7)], fill=(0, 40, 104))
    for sx, sy in ((fx + 5, fy + 3), (fx + 12, fy + 6), (fx + 5, fy + 8)):
        star(sx, sy, 2, (255, 255, 255))
    # China flag: red field, one large yellow star and four small ones.
    cx0, cy0 = x + 57, y + 4
    d.rectangle([cx0, cy0, cx0 + 44, cy0 + 16], fill=(222, 41, 16))
    star(cx0 + 9, cy0 + 8, 5, (255, 220, 0))
    for sx, sy in ((cx0 + 19, cy0 + 4), (cx0 + 23, cy0 + 7), (cx0 + 23, cy0 + 11),
                   (cx0 + 19, cy0 + 13)):
        star(sx, sy, 2, (255, 220, 0))
    # Russia flag: white, blue and red horizontal bands.
    rx0, ry0 = x + 108, y + 4
    d.rectangle([rx0, ry0, rx0 + 44, ry0 + 16], fill=(255, 255, 255))
    d.rectangle([rx0, ry0 + 5, rx0 + 44, ry0 + 11], fill=(0, 60, 160))
    d.rectangle([rx0, ry0 + 11, rx0 + 44, ry0 + 16], fill=(200, 30, 30))
    # Three seated figures, heads above the table, one under each flag.
    for fcx in (x + 28, x + w // 2, x + w - 28):
        d.ellipse([fcx - 8, y + 24, fcx + 8, y + 38], fill=(240, 200, 160))
        d.polygon([(fcx - 13, y + 46), (fcx - 10, y + 38),
                   (fcx + 10, y + 38), (fcx + 13, y + 46)], fill=(40, 40, 60))
    d.rectangle([x + 8, y + 46, x + w - 8, y + 50], fill=(120, 80, 40))


def scene_europe(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(29, 58, 95))
    for i in range(12):
        import math
        ang = 2 * math.pi * i / 12
        cx = x + w // 2 + int(34 * math.cos(ang))
        cy = y + h // 2 + int(20 * math.sin(ang))
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 220, 120))
    d.ellipse([x + w // 2 - 8, y + h // 2 - 8, x + w // 2 + 8, y + h // 2 + 8],
              fill=(255, 220, 120))


def scene_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 220, 180))
    # Domed cathedral, left: dome with a cross, body, arched door.
    cx = x + 42
    d.pieslice([cx - 16, y + 8, cx + 16, y + 40], 180, 360, fill=(58, 110, 165))
    d.line([cx, y + 2, cx, y + 10], fill=(163, 31, 31), width=2)
    d.line([cx - 4, y + 5, cx + 4, y + 5], fill=(163, 31, 31), width=2)
    d.rectangle([cx - 20, y + 24, cx + 20, y + h - 8], fill=(200, 170, 90))
    d.rectangle([cx - 5, y + h - 22, cx + 5, y + h - 8], fill=(120, 90, 40))
    d.pieslice([cx - 5, y + h - 27, cx + 5, y + h - 17], 180, 360,
               fill=(120, 90, 40))
    # Quadcopter drone, upper right: central body, four arms, four rotors.
    bx, by = x + w - 40, y + 12
    rotors = ((bx - 18, by - 8), (bx + 18, by - 8),
              (bx - 18, by + 8), (bx + 18, by + 8))
    for rx, ry in rotors:
        d.line([bx, by, rx, ry], fill=(70, 70, 70), width=2)
    for rx, ry in rotors:
        d.ellipse([rx - 9, ry - 2, rx + 9, ry + 2], fill=(210, 210, 220))
        d.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=(70, 70, 70))
    d.ellipse([bx - 9, by - 4, bx + 9, by + 5], fill=(60, 60, 60))
    d.ellipse([bx - 3, by + 5, bx + 3, by + 9], fill=(40, 40, 40))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(120, 100, 70))


def scene_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 200, 230))
    d.rectangle([x, y + h - 22, x + w, y + h - 8], fill=(120, 120, 120))
    d.rectangle([x + w // 2 - 14, y + h - 40, x + w // 2 + 14, y + h - 8],
                fill=(90, 90, 90))
    d.line([x + 16, y + 12, x + w // 2 - 14, y + h - 40], fill=(60, 60, 60), width=3)
    d.line([x + w - 16, y + 12, x + w // 2 + 14, y + h - 40], fill=(60, 60, 60), width=3)
    d.polygon([(x + w // 2 - 30, y + h - 22), (x + w // 2, y + h - 34),
               (x + w // 2 + 30, y + h - 22)], fill=(176, 32, 32))


def scene_atom(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 50))
    cx, cy = x + w // 2, y + h // 2
    for ang in (0, 60, 120):
        a = math.radians(ang)
        pts = []
        for t in range(0, 360, 12):
            r = math.radians(t)
            ex, ey = 34 * math.cos(r), 13 * math.sin(r)
            rx = ex * math.cos(a) - ey * math.sin(a)
            ry = ex * math.sin(a) + ey * math.cos(a)
            pts.append((cx + rx, cy + ry))
        d.line(pts + [pts[0]], fill=(120, 200, 255), width=2)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 80, 80))
    d.ellipse([cx + 26, cy - 12, cx + 32, cy - 6], fill=(255, 220, 120))


def scene_handshake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    d.rectangle([x + 8, y + 8, x + w // 2 - 4, y + 30], fill=(176, 32, 32))
    d.rectangle([x + 8, y + 8, x + w // 2 - 4, y + 15], fill=(255, 255, 255))
    d.rectangle([x + w // 2 + 4, y + 8, x + w - 8, y + 30], fill=(255, 220, 0))
    d.rectangle([x + w // 2 + 4, y + 8, x + w - 8, y + 15], fill=(0, 60, 160))
    d.rectangle([x + w // 2 + 4, y + 22, x + w - 8, y + 30], fill=(200, 30, 30))
    d.ellipse([x + w // 2 - 26, y + h - 30, x + w // 2 - 6, y + h - 10],
              fill=(240, 200, 160))
    d.ellipse([x + w // 2 + 6, y + h - 30, x + w // 2 + 26, y + h - 10],
              fill=(220, 180, 140))


def scene_gavel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 50, 40))
    d.rectangle([x + 22, y + 12, x + w - 22, y + 28], fill=(150, 110, 60))
    d.rectangle([x + 22, y + 12, x + w - 22, y + 18], fill=(180, 140, 80))
    d.line([x + w // 2 + 8, y + 28, x + w // 2 - 14, y + h - 24],
           fill=(150, 110, 60), width=7)
    d.ellipse([x + w // 2 - 30, y + h - 24, x + w // 2 + 30, y + h - 10],
              fill=(200, 160, 90))
    d.rectangle([x + w // 2 - 30, y + h - 18, x + w // 2 + 30, y + h - 14],
                fill=(150, 110, 60))


def scene_drought(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 220, 150))
    d.ellipse([x + w - 44, y + 6, x + w - 10, y + 40], fill=(255, 180, 40))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(180, 140, 80))
    d.line([x + 10, y + h - 26, x + 40, y + h - 12], fill=(120, 85, 40), width=2)
    d.line([x + 60, y + h - 26, x + 90, y + h - 8], fill=(120, 85, 40), width=2)
    d.line([x + 110, y + h - 26, x + 130, y + h - 14], fill=(120, 85, 40), width=2)


def scene_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 40))
    for i, (px, py) in enumerate([(12, 10), (40, 26), (70, 8), (110, 20), (140, 12)]):
        d.ellipse([x + px, y + py, x + px + 3, y + py + 3], fill=(255, 255, 255))
    d.polygon([(x + w // 2 - 6, y + 16), (x + w // 2 + 26, y + h // 2),
               (x + w // 2 - 6, y + h - 16)], outline=(200, 200, 220), width=2)
    d.rectangle([x + w // 2 - 22, y + h // 2 - 10, x + w // 2 - 4, y + h // 2 + 10],
                fill=(200, 200, 220))
    d.line([x + w // 2 - 22, y + h // 2, x + 16, y + h - 12], fill=(255, 220, 120), width=2)


def scene_hayabusa(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 24, 44))
    d.ellipse([x + 12, y + h - 34, x + 62, y + h - 6], fill=(150, 120, 90))
    d.ellipse([x + 24, y + h - 28, x + 44, y + h - 12], fill=(120, 95, 70))
    d.rectangle([x + w - 52, y + 14, x + w - 30, y + 34], fill=(200, 200, 220))
    d.line([x + w - 52, y + 24, x + w - 66, y + 24], fill=(200, 200, 220), width=3)
    d.line([x + w - 30, y + 24, x + w - 16, y + 24], fill=(200, 200, 220), width=3)


def scene_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 40, 90))
    d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + 60], fill=(255, 190, 60))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(10, 60, 80))
    d.polygon([(x + 20, y + h - 18), (x + 26, y + h - 40), (x + 32, y + h - 18)],
              fill=(10, 40, 20))
    d.polygon([(x + 20, y + h - 30), (x + 8, y + h - 38), (x + 20, y + h - 26)],
              fill=(10, 60, 30))
    d.polygon([(x + w - 30, y + h - 18), (x + w - 24, y + h - 44), (x + w - 18, y + h - 18)],
              fill=(10, 40, 20))


def scene_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 20, 36))
    d.rectangle([x + w // 2 - 22, y + 12, x + w // 2 + 22, y + h - 12],
                fill=(40, 60, 110), outline=(120, 200, 255), width=2)
    d.rectangle([x + w // 2 - 10, y + 22, x + w // 2 + 10, y + h - 22],
                fill=(120, 200, 255))
    for i in range(4):
        d.line([x + w // 2 - 22, y + 20 + i * 10, x + w // 2 - 30, y + 20 + i * 10],
               fill=(120, 200, 255), width=2)
        d.line([x + w // 2 + 22, y + 20 + i * 10, x + w // 2 + 30, y + 20 + i * 10],
               fill=(120, 200, 255), width=2)


SCENES = {
    "cyclone": scene_cyclone, "calendar": scene_calendar, "tower": scene_tower,
    "scales": scene_scales, "summit": scene_summit, "europe": scene_europe,
    "kyiv": scene_kyiv, "bridge": scene_bridge, "atom": scene_atom,
    "handshake": scene_handshake, "gavel": scene_gavel, "drought": scene_drought,
    "voyager": scene_voyager, "hayabusa": scene_hayabusa, "gta": scene_gta,
    "chip": scene_chip,
}

# ---------------------------------------------------------------- map
# Rough continent outlines as (lon, lat) lists. Each continent is its own
# polygon, drawn separately, so they can never merge into one blob.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-150, 60)],
    [(-80, 10), (-60, 5), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-70, -20), (-80, -5)],
    [(-10, 36), (-5, 44), (0, 48), (5, 55), (10, 58), (20, 60), (30, 70),
     (40, 68), (30, 60), (25, 55), (20, 45), (15, 40), (10, 38), (0, 36)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (43, 12), (48, 10), (40, 0), (35, -10), (30, -20),
     (20, -35), (15, -30), (12, -18), (8, 0), (0, 5), (-8, 5)],
    [(40, 68), (60, 70), (80, 73), (110, 75), (140, 72), (170, 66),
     (180, 65), (160, 60), (140, 55), (130, 42), (127, 38), (122, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 25),
     (70, 20), (60, 25), (50, 30), (43, 35), (40, 45)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -14)],
]


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    px = x0 + (lon + 170) / 360.0 * w
    py = y0 + (75 - lat) / 130.0 * h
    return px, py


def draw_map(d, x0, y0, w, h, pins):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SEA, outline=INK, width=1)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, x0, y0, w, h) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(120, 100, 60))
    placed = []
    for num, lat, lon in pins:
        px, py = lonlat_to_xy(lon, lat, x0, y0, w, h)
        ox, oy = 0, 0
        for (qx, qy) in placed:
            if abs(px + ox - qx) < 14 and abs(py + oy - qy) < 14:
                found = False
                for cand in [(12, -10), (-12, -10), (12, 10), (-12, 10),
                             (0, -15), (0, 15), (16, 0), (-16, 0)]:
                    if all(abs(px + cand[0] - ax) >= 14 or
                           abs(py + cand[1] - ay) >= 14 for (ax, ay) in placed):
                        ox, oy = cand
                        found = True
                        break
                if not found:
                    ox, oy = 12, -10
                break
        if ox or oy:
            d.line([px, py, px + ox, py + oy], fill=RED, width=1)
        cx, cy = px + ox, py + oy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED, outline=(255, 255, 255))
        tf = font(SANS_B, 9)
        tw = d.textlength(str(num), font=tf)
        d.text((cx - tw / 2, cy - 6), str(num), font=tf, fill=(255, 255, 255))
        placed.append((cx, cy))


# ---------------------------------------------------------------- layout
def draw_card(d, x, y, w, num, story, img_h, head_size, deck_size,
               head_lines=3, deck_lines=2):
    region, field, place, headline, deck, datelabel, scene, _lat, _lon = story
    SCENES[scene](d, x, y, w, img_h)
    yy = y + img_h + 5
    kicker = "%d  %s \u00b7 %s" % (num, region, field)
    d.text((x, yy), kicker, font=font(SANS_B, 9), fill=RED)
    if datelabel:
        lw = d.textlength(datelabel, font=font(SANS_B, 9))
        d.rectangle([x + w - lw - 8, yy - 1, x + w, yy + 11], fill=RED)
        d.text((x + w - lw - 4, yy), datelabel, font=font(SANS_B, 9),
               fill=(255, 255, 255))
    yy += 13
    head_fnt = font(SERIF_B, head_size)
    for line in wrap(d, headline, head_fnt, w)[:head_lines]:
        d.text((x, yy), line, font=head_fnt, fill=INK)
        yy += head_size + 3
    yy += 2
    deck_fnt = font(SANS, deck_size)
    for line in wrap(d, deck, deck_fnt, w)[:deck_lines]:
        d.text((x, yy), line, font=deck_fnt, fill=(40, 40, 40))
        yy += deck_size + 3
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    counts = region_counts()
    total = sum(counts.values())
    assert total == 52, total

    # Top bar.
    d.rectangle([0, 0, W, 20], fill=INK)
    d.text((16, 4), "ONE DAY OF WORLD NEWS, ONE PICTURE",
           font=font(SANS_B, 11), fill=(255, 255, 255))
    right = "52 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM THIS FRIDAY"
    d.text((W - 16 - d.textlength(right, font=font(SANS_B, 11)), 4), right,
           font=font(SANS_B, 11), fill=(255, 220, 120))

    # Masthead.
    title = "Friday 20 November 2026"
    tf = fit_font(d, title, SERIF_B, 64, W - 32)
    d.text((W // 2, 58), title, font=tf, fill=INK, anchor="mm")
    d.line([16, 92, W - 16, 92], fill=INK, width=2)
    sub = "Akvan comes ashore  \u00b7  Trump puts Iran off to 2027  \u00b7  A missile over Riyadh"
    sf = fit_font(d, sub, SERIF, 20, W - 32)
    d.text((W // 2, 110), sub, font=sf, fill=RED, anchor="mm")

    # Region bar: all segment rectangles first, then the legend line below,
    # so no label is ever overpainted by the next segment.
    bx, bw, by = 16, W - 32, 128
    pos = bx
    for region in REGION_ORDER:
        seg = bw * counts[region] / total
        d.rectangle([pos, by, pos + seg, by + 16], fill=REGION_COLOUR[region])
        pos += seg
    d.rectangle([bx, by, bx + bw, by + 16], outline=INK, width=1)
    legend = "   ".join("%s %d" % (r, counts[r]) for r in REGION_ORDER)
    lf = font(SANS_B, 10)
    lx = bx
    for region in REGION_ORDER:
        d.rectangle([lx, by + 22, lx + 9, by + 31], fill=REGION_COLOUR[region])
        label = "%s %d" % (region, counts[region])
        d.text((lx + 12, by + 21), label, font=lf, fill=INK)
        lx += 12 + d.textlength(label, font=lf) + 16

    # Numbers strip.
    ny = 158
    d.line([16, ny - 4, W - 16, ny - 4], fill=INK, width=1)
    col_w = (W - 32) / 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = 16 + col_w * i + col_w / 2
        nf = fit_font(d, num, SERIF_B, 26, col_w - 8)
        d.text((cx, ny + 12), num, font=nf, fill=RED, anchor="mm")
        d.text((cx, ny + 32), label, font=font(SANS_B, 8), fill=GREY, anchor="mm")
    d.line([16, ny + 42, W - 16, ny + 42], fill=INK, width=1)

    # Timeline strip.
    ty = 206
    d.text((16, ty), "THE DAY IN UTC", font=font(SANS_B, 10), fill=(255, 255, 255))
    d.rectangle([16, ty - 2, 16 + d.textlength("THE DAY IN UTC", font=font(SANS_B, 10)) + 10,
                 ty + 12], fill=RED)
    d.text((16, ty), "THE DAY IN UTC", font=font(SANS_B, 10), fill=(255, 255, 255))
    for i, (when, what) in enumerate(TIMELINE):
        cx = 16 + col_w * i + col_w / 2
        d.text((cx, ty + 16), when, font=font(SANS_B, 9), fill=RED, anchor="ma")
        draw_wrapped(d, cx - col_w / 2 + 4, ty + 28, what, font(SANS, 10),
                     col_w - 8, fill=INK, leading=12)
    d.line([16, ty + 52, W - 16, ty + 52], fill=INK, width=2)

    # Leads: 4 across.
    ly = 266
    lead_w = (W - 32 - 3 * 8) // 4
    for i, story in enumerate(LEADS):
        draw_card(d, 16 + i * (lead_w + 8), ly, lead_w, i + 1, story, 88, 16, 11,
                  head_lines=2)

    # Mids: 2 rows of 6.
    mid_w = (W - 32 - 5 * 8) // 6
    for row in range(2):
        my = 446 + row * 128
        for col in range(6):
            idx = row * 6 + col
            draw_card(d, 16 + col * (mid_w + 8), my, mid_w, 5 + idx,
                      MIDS[idx], 52, 12, 10, head_lines=2)

    # Map + briefs.
    my0 = 708
    d.text((16, my0), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=RED)
    d.text((16, my0 + 15), "pins 1-16 as numbered above",
           font=font(SANS, 9), fill=GREY)
    map_x, map_y, map_w, map_h = 16, my0 + 30, 330, 150
    pins = [(i + 1, s[7], s[8]) for i, s in enumerate(LEADS + MIDS)]
    draw_map(d, map_x, map_y, map_w, map_h, pins)
    d.text((16, map_y + map_h + 4), "Red pins mark stories 1-16; grey dots mark briefs 17-52.",
           font=font(SANS, 9), fill=GREY)
    bx0 = 362
    d.text((bx0, my0), "ALSO ON FRIDAY 20 NOVEMBER \u2014 36 MORE STORIES",
           font=font(SANS_B, 12), fill=RED)
    col2_w = (W - 16 - bx0 - 12) // 2
    bf = font(SANS, 10)
    for j, (region, text) in enumerate(BRIEFS):
        col = j // 18
        row = j % 18
        x = bx0 + col * (col2_w + 12)
        y = my0 + 20 + row * 10
        num = 17 + j
        d.text((x, y), str(num), font=font(SANS_B, 10),
               fill=REGION_COLOUR[region])
        d.text((x + 22, y), text, font=bf, fill=INK)

    # DATE CHECK box.
    dy = 920
    d.rectangle([16, dy, W - 16, dy + 42], outline=RED, width=2)
    d.rectangle([16, dy, 16 + 108, dy + 42], fill=RED)
    d.text((16 + 54, dy + 21), "DATE CHECK", font=font(SANS_B, 12),
           fill=(255, 255, 255), anchor="mm")
    check = ("19 NOV stories are labelled 19 NOV above: the ICJ verdict, the "
             "Shenzhen trilateral, the Riyadh tower strike, the Kyiv embassy "
             "strikes. Voyager crossed one light-day on 18 Nov. All else "
             "happened, or was first reported, on Friday 20 November 2026.")
    draw_wrapped(d, 134, dy + 5, check, font(SANS, 10), W - 16 - 134 - 8,
                 leading=13)

    # Footer.
    fy = 970
    d.text((16, fy), "Every story here happened, or was first reported, on Friday 20 November 2026, "
                     "except the four labelled 19 NOV and Voyager (18 Nov).",
           font=font(SANS, 9), fill=GREY)
    d.text((16, fy + 12), "Sources: Reuters, AP, AFP, BBC, The Hindu, NDTV. Original drawings. "
                          "Contested claims are attributed, not stated as fact.",
           font=font(SANS, 9), fill=GREY)
    d.line([16, 1004, W - 16, 1004], fill=INK, width=1)
    d.text((W // 2, 1012), "FRIDAY 20 NOVEMBER 2026  \u00b7  ONE DAY, ONE PICTURE",
           font=font(SANS_B, 9), fill=GREY, anchor="ma")

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
