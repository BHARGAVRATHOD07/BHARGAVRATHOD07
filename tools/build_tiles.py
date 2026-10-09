#!/usr/bin/env python3
"""Generates the animated SVG tiles in assets/readme/. Edit the CONTENT section, run:  python tools/build_tiles.py"""
import os, random, textwrap
from xml.sax.saxutils import escape as esc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "readme")
os.makedirs(OUT, exist_ok=True)

# ============================ CONTENT (edit me) ============================
NAME = "Bhargav Rathod"
PHRASES = ["Solving DSA problems in C++", "Building web & backend projects", "Learning machine learning & AI"]
LINE1 = "B.Tech CSE · CHARUSAT · Gujarat, India"
STATUS = "open to SDE internships"
BUTTONS = [("Portfolio", "#FF9F43"), ("LinkedIn", "#38BDF8"), ("LeetCode", "#FF9F43"), ("GitHub", "#a78bfa")]
QUOTE = ["Learn by building.", "Understand by breaking.", "Improve by repeating."]
WHOAMI = [("$ whoami", 0), ("bhargav-rathod · cs-undergrad @ charusat", 1), ("", 2),
          ("$ status", 0), ("role     : software-developer-in-progress", 1), ("focus    : dsa · web · backend apis", 1),
          ("learning : machine learning · system design", 1), ("location : gujarat, india", 1),
          ("seeking  : sde / software dev internship", 1)]
SECTIONS = [("I", "About", "who I am and how I think"), ("II", "Projects", "things I built and what they solve"),
            ("III", "Craft", "the tools behind the work"), ("IV", "Orbit", "where my attention is right now"),
            ("V", "Signal", "activity, streaks and practice")]
PROJECTS = [("Git Club Event Website", "Harry Potter-themed event website for the Grow with Git Club at CHARUSAT.", ["HTML", "CSS", "JavaScript"], "#a78bfa"),
            ("Hadoop Matrix Multiplication", "Matrix multiplication with MapReduce, run on HDFS and YARN.", ["Hadoop", "MapReduce", "HDFS", "YARN"], "#38BDF8"),
            ("Used Car Price Prediction", "A machine-learning model that predicts used-car prices.", ["Python", "NumPy", "Pandas"], "#FF9F43"),
            ("Personal Portfolio", "My own site, built from scratch with plain HTML, CSS and JavaScript.", ["HTML", "CSS", "JavaScript", "GitHub Pages"], "#34d399")]
SHIPPED = [("INTERNSHIP", "Frontend Developer Intern · InternPe", "Four weekly projects in HTML, CSS and JavaScript: calculator, e-commerce site, to-do app and Connect Four.", "#FF9F43"),
           ("LEADERSHIP", "Social Media Lead · Grow with Git Club", "Git & GitHub activities and event coordination at CHARUSAT, working with first-year students.", "#38BDF8")]
CRAFT = [("LANGUAGES", "#FF9F43", ["C", "C++", "Python", "JavaScript"]),
         ("WEB", "#38BDF8", ["HTML", "CSS", "JavaScript", "GitHub Pages"]),
         ("DATA & ML", "#a78bfa", ["NumPy", "Pandas", "Matplotlib", "OpenCV", "MediaPipe"]),
         ("BIG DATA", "#34d399", ["Hadoop", "HDFS", "YARN", "MapReduce"]),
         ("TOOLS", "#f472b6", ["Git", "GitHub", "GitHub Pages"]),
         ("EXPLORING", "#FF9F43", ["System Design", "Cloud Computing", "ML & AI"])]
MARQUEE = ["C", "C++", "Python", "JavaScript", "HTML", "CSS", "Git", "GitHub", "NumPy", "Pandas", "Matplotlib", "OpenCV", "MediaPipe", "Hadoop", "DSA", "LeetCode"]
ORBITS = [(105, 30, False, [(0, "DSA", "#FF9F43"), (180, "Backend APIs", "#38BDF8")]),
          (185, 46, True, [(0, "Web Dev", "#a78bfa"), (120, "Machine Learning", "#34d399"), (240, "Git & GitHub", "#f472b6")]),
          (250, 72, False, [(40, "System Design", "#38BDF8"), (160, "Cloud Computing", "#FF9F43"), (280, "AI", "#a78bfa")])]
FOOT = ["Build it. Break it.", "Understand it."]
# ===========================================================================

BG = "#0B0F19"; PANEL = "#0f1626"; LINE = "#1f2a44"; WHITE = "#F8FAFC"; GREY = "#8b95ad"
PURPLE = "#7C3AED"; LP = "#a78bfa"; BLUE = "#38BDF8"; ORANGE = "#FF9F43"; GREEN = "#34d399"
MONO = "'JetBrains Mono','SF Mono',Consolas,'Courier New',monospace"
SANS = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
W = 1200

DEFS = f'''<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ORANGE}"/><stop offset=".55" stop-color="{LP}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<linearGradient id="gl" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{PURPLE}" stop-opacity="0"/><stop offset=".5" stop-color="{LP}"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#161d30" stroke-width="1"/></pattern>
<radialGradient id="o1"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".30"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
<radialGradient id="o2"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".45"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
<radialGradient id="o3"><stop offset="0" stop-color="{BLUE}" stop-opacity=".28"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'''

_uid = [0]
def uid(p="c"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"

def save(name, w, h, body, grid=True):
    g = f'<rect width="{w}" height="{h}" fill="url(#grid)"/>' if grid else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
           f'<defs>{DEFS}</defs><rect width="{w}" height="{h}" fill="{BG}"/>{g}{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{name:24s}{len(svg)/1024:6.1f} KB")

def text(x, y, s, size, fill, family=SANS, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'

def typed(x, y, s, size, begin, fill, dur=None):
    """one-shot typewriter line (monospace)"""
    cid = uid(); n = len(s); w = n * size * 0.6; dur = dur or max(.4, n * .035)
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y-size}" width="0" height="{size*1.5}">'
            f'<animate attributeName="width" from="0" to="{w}" begin="{begin}s" dur="{dur}s" fill="freeze"/></rect></clipPath>'
            f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" textLength="{w}" lengthAdjust="spacing" '
            f'xml:space="preserve" clip-path="url(#{cid})">{esc(s)}</text>')

def fade(begin, dur=.6):
    return f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'

def sweep_line(x1, x2, y, dur=5):
    return (f'<rect x="{x1}" y="{y}" width="{x2-x1}" height="2" fill="url(#gl)" opacity=".7"/>'
            f'<circle cy="{y+1}" r="4" fill="{ORANGE}"><animate attributeName="cx" values="{x1};{x2}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" dur="{dur}s" repeatCount="indefinite"/></circle>')

# ------------------------------------------------------------------ hero ----
def hero():
    H = 440; random.seed(7)
    b = (f'<circle r="220" fill="url(#o1)"><animate attributeName="cx" values="180;420;180" dur="14s" repeatCount="indefinite"/><animate attributeName="cy" values="90;300;90" dur="14s" repeatCount="indefinite"/></circle>'
         f'<circle r="280" fill="url(#o2)"><animate attributeName="cx" values="1020;780;1020" dur="17s" repeatCount="indefinite"/><animate attributeName="cy" values="330;100;330" dur="17s" repeatCount="indefinite"/></circle>'
         f'<circle r="200" fill="url(#o3)"><animate attributeName="cx" values="640;900;640" dur="19s" repeatCount="indefinite"/><animate attributeName="cy" values="40;260;40" dur="19s" repeatCount="indefinite"/></circle>')
    for _ in range(26):
        x, y, r = random.randint(20, 1180), random.randint(20, 420), random.choice([1, 1.3, 1.8])
        d = random.uniform(3, 7)
        b += (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff"><animate attributeName="opacity" values=".1;.9;.1" dur="{d:.1f}s" repeatCount="indefinite"/>'
              f'<animate attributeName="cy" values="{y};{y-24};{y}" dur="{d*2:.1f}s" repeatCount="indefinite"/></circle>')
    # right-side rotating rings
    b += '<g transform="translate(985 215)">'
    for r, dur, rev, dash in [(150, 40, False, "2 10"), (105, 28, True, "14 8"), (62, 18, False, "4 6")]:
        to = -360 if rev else 360
        b += (f'<circle r="{r}" fill="none" stroke="{LP}" stroke-opacity=".45" stroke-dasharray="{dash}"><animateTransform attributeName="transform" type="rotate" from="0" to="{to}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    b += (f'<g><circle cx="150" r="7" fill="{ORANGE}"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></g>'
          f'<g><circle cx="-105" r="6" fill="{BLUE}"/><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="9s" repeatCount="indefinite"/></g>'
          f'<g><circle cx="62" r="5" fill="{GREEN}"/><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="6s" repeatCount="indefinite"/></g>'
          f'<circle r="24" fill="url(#gb)"><animate attributeName="r" values="20;28;20" dur="3s" repeatCount="indefinite"/></circle></g>')
    b += text(80, 110, "<hello world />", 18, LP, MONO)
    b += text(80, 215, NAME, 86, "url(#gb)", SANS, 800, extra='opacity="0"') .replace('opacity="0">', 'opacity="0">' + fade(0.2, 1.2), 1)
    D, n = 12, len(PHRASES)
    for i, p in enumerate(PHRASES):
        w = len(p) * 26 * 0.6; a = i / n
        k = f"0;{a};{a+.12};{a+.26};{a+.30};1"
        b += (f'<clipPath id="hp{i}"><rect x="80" y="262" width="0" height="40"><animate attributeName="width" values="0;0;{w};{w};0;0" keyTimes="{k}" dur="{D}s" repeatCount="indefinite"/></rect></clipPath>'
              f'<text x="80" y="288" font-family="{MONO}" font-size="26" fill="{WHITE}" textLength="{w}" lengthAdjust="spacing" clip-path="url(#hp{i})">{esc(p)}</text>'
              f'<g><animate attributeName="opacity" values="1;0;1" dur=".9s" repeatCount="indefinite"/><rect x="80" y="266" width="12" height="28" fill="{ORANGE}" opacity="0">'
              f'<animate attributeName="x" values="80;80;{80+w};{80+w};80;80" keyTimes="{k}" dur="{D}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;1;1;1;0;0" keyTimes="{k}" dur="{D}s" repeatCount="indefinite"/></rect></g>')
    b += text(80, 352, LINE1, 17, GREY, MONO)
    b += (f'<circle cx="88" cy="387" r="5" fill="{GREEN}"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.4;1" dur="2s" repeatCount="indefinite"/></circle>'
          + text(104, 393, STATUS, 17, GREEN, MONO))
    save("hero.svg", W, H, b)

# --------------------------------------------------------------- buttons ----
def buttons():
    for i, (label, col) in enumerate(BUTTONS):
        cid = uid("b")
        b = (f'<clipPath id="{cid}"><rect x="10" y="10" width="280" height="60" rx="30"/></clipPath>'
             f'<rect x="10" y="10" width="280" height="60" rx="30" fill="{PANEL}" stroke="url(#gb)" stroke-opacity=".7" stroke-width="1.5"/>'
             f'<g clip-path="url(#{cid})"><rect y="0" width="50" height="80" fill="#fff" opacity=".09" transform="skewX(-20)">'
             f'<animate attributeName="x" values="-120;340" dur="4s" begin="{i*.7}s" repeatCount="indefinite"/></rect></g>'
             f'<circle cx="52" cy="40" r="4" fill="{col}"><animate attributeName="opacity" values="1;.3;1" dur="2s" begin="{i*.4}s" repeatCount="indefinite"/></circle>'
             + text(150, 47, label, 19, WHITE, MONO, 600, "middle") + text(246, 47, "↗", 20, col, MONO, 700, "middle"))
        save(f"btn-{label.lower()}.svg", 300, 80, b)

# -------------------------------------------------------------- sections ----
def sections():
    for n, (num, title, sub) in enumerate(SECTIONS, 1):
        b = (text(80, 50, f"SECTION {num}", 14, BLUE, MONO, 600, extra='letter-spacing="3"')
             + text(80, 94, title, 40, WHITE, SANS, 800, extra='opacity="0"').replace('opacity="0">', 'opacity="0">' + fade(.1), 1)
             + text(1120, 94, sub, 15, GREY, MONO, 400, "end") + sweep_line(80, 1120, 108))
        save(f"sec-0{n}-{title.lower()}.svg", W, 120, b)

# ----------------------------------------------------------------- about ----
def about():
    H = 440; b = ""
    for i, q in enumerate(QUOTE):
        fill = "url(#gb)" if i == 2 else WHITE
        b += text(80, 170 + i * 62, q, 36, fill, SANS, 800, extra='opacity="0"').replace('opacity="0">', 'opacity="0">' + fade(.3 + i * .7, .8), 1)
    b += text(80, 372, "— my working philosophy", 15, GREY, MONO)
    b += (f'<rect x="610" y="50" width="520" height="340" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
          f'<circle cx="638" cy="76" r="6" fill="#ff5f56"/><circle cx="660" cy="76" r="6" fill="#ffbd2e"/><circle cx="682" cy="76" r="6" fill="#27c93f"/>'
          + text(1110, 81, "bhargav@charusat:~", 13, GREY, MONO, 400, "end"))
    y, t = 125, .8
    for s, kind in WHOAMI:
        if s:
            col = {0: BLUE, 1: "#cbd5e1", 2: WHITE}[kind]
            b += typed(640, y, s, 15, round(t, 2), col)
            t += max(.4, len(s) * .035) + .15
        y += 28
    b += (f'<rect x="640" y="{y-14}" width="9" height="18" fill="{ORANGE}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
    save("about.svg", W, H, b)

# ----------------------------------------------------------------- cards ----
def chips(x, y, items, maxw, color, size=13, delay=0.0):
    out, cx, cy = "", x, y
    for i, it in enumerate(items):
        w = len(it) * size * 0.62 + 26
        if cx + w > x + maxw:
            cx, cy = x, cy + 38
        out += (f'<g opacity="0">{fade(delay + i * .12, .5)}<rect x="{cx}" y="{cy}" width="{w:.0f}" height="30" rx="15" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".6"/>'
                + text(cx + w / 2, cy + 20, it, size, WHITE, MONO, 500, "middle") + '</g>')
        cx += w + 10
    return out

def cards():
    for i, (title, desc, stack, col) in enumerate(PROJECTS, 1):
        b = (f'<rect x="20" y="20" width="560" height="280" rx="18" fill="{PANEL}" stroke="{LINE}"/>'
             f'<rect x="20" y="20" width="560" height="4" rx="2" fill="{col}" opacity=".9"/>'
             f'<g transform="translate(505 85)"><circle r="34" fill="none" stroke="{col}" stroke-dasharray="4 8" opacity=".7"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>'
             f'<circle r="6" fill="{col}"><animate attributeName="r" values="5;9;5" dur="2.6s" repeatCount="indefinite"/></circle></g>'
             + text(50, 68, f"No. 0{i}", 14, col, MONO, 600, extra='letter-spacing="2"')
             + text(50, 112, title, 27, WHITE, SANS, 800))
        for j, line in enumerate(textwrap.wrap(desc, 46)[:3]):
            b += text(50, 152 + j * 26, line, 16, "#aab3c7", SANS)
        b += chips(50, 232, stack, 500, col)
        save(f"card-0{i}.svg", 600, 320, b)

def shipped():
    H = 200; b = ""
    for i, (tag, title, desc, col) in enumerate(SHIPPED):
        x = 40 + i * 570
        b += (f'<rect x="{x}" y="20" width="550" height="160" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
              f'<rect x="{x}" y="20" width="4" height="160" fill="{col}"/>'
              + text(x + 28, 56, tag, 13, col, MONO, 600, extra='letter-spacing="3"')
              + text(x + 28, 94, title, 21, WHITE, SANS, 800))
        for j, line in enumerate(textwrap.wrap(desc, 62)[:3]):
            b += text(x + 28, 126 + j * 22, line, 14, "#aab3c7", SANS)
    save("shipped.svg", W, H, b)

# ----------------------------------------------------------------- craft ----
def craft():
    H = 440; b = ""
    for k, (title, col, items) in enumerate(CRAFT):
        x = 40 + (k % 3) * 390; y = 40 + (k // 3) * 190
        b += (f'<rect x="{x}" y="{y}" width="340" height="170" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
              f'<circle cx="{x+26}" cy="{y+34}" r="5" fill="{col}"><animate attributeName="opacity" values="1;.3;1" dur="2.4s" begin="{k*.3}s" repeatCount="indefinite"/></circle>'
              + text(x + 42, y + 39, title, 13, col, MONO, 600, extra='letter-spacing="3"')
              + chips(x + 24, y + 62, items, 292, col, 13, .2 + k * .25))
    save("craft.svg", W, H, b)

def marquee():
    H = 80; items = []; x = 0
    for t in MARQUEE:
        w = len(t) * 12 + 56; items.append((x, w, t)); x += w
    L = x
    row = "".join(f'<g transform="translate({off+ix} 0)"><rect x="8" y="22" width="{w-16}" height="36" rx="18" fill="{PANEL}" stroke="{LINE}"/>'
                  + text(w / 2, 46, t, 16, WHITE, MONO, 500, "middle") + '</g>' for off in (0, L) for ix, w, t in items)
    b = (f'<g>{row}<animateTransform attributeName="transform" type="translate" from="0 0" to="-{L} 0" dur="{L/55:.0f}s" repeatCount="indefinite"/></g>'
         f'<defs><linearGradient id="fl"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="fr"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>'
         f'<rect width="140" height="{H}" fill="url(#fl)"/><rect x="{W-140}" width="140" height="{H}" fill="url(#fr)"/>')
    save("marquee.svg", W, H, b)

# ----------------------------------------------------------------- orbit ----
def orbit():
    H = 560; cx, cy = 600, 280; b = ""
    for r, dur, rev, planets in ORBITS:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-dasharray="3 8"/>'
        inner = ""
        for ang, label, col in planets:
            inner += (f'<g transform="rotate({ang})"><g transform="translate({r} 0)"><g>'
                      f'<circle r="16" fill="{col}" opacity=".18"/><circle r="7" fill="{col}"/>'
                      + text(0, -24, label, 15, WHITE, MONO, 500, "middle")
                      + f'<animateTransform attributeName="transform" type="rotate" from="{-ang}" to="{-ang + (360 if rev else -360)}" dur="{dur}s" repeatCount="indefinite"/></g></g></g>')
        b += (f'<g transform="translate({cx} {cy})"><g>{inner}'
              f'<animateTransform attributeName="transform" type="rotate" from="0" to="{-360 if rev else 360}" dur="{dur}s" repeatCount="indefinite"/></g></g>')
    b += (f'<circle cx="{cx}" cy="{cy}" r="64" fill="url(#o2)"><animate attributeName="r" values="56;76;56" dur="4s" repeatCount="indefinite"/></circle>'
          f'<circle cx="{cx}" cy="{cy}" r="38" fill="{PANEL}" stroke="url(#gb)" stroke-width="2"/>'
          + text(cx, cy + 5, "learning", 13, WHITE, MONO, 600, "middle"))
    save("orbit.svg", W, H, b)

# ---------------------------------------------------------------- footer ----
def footer():
    H = 200
    b = (text(600, 90, FOOT[0], 40, WHITE, SANS, 800, "middle") + text(600, 140, FOOT[1], 40, "url(#gb)", SANS, 800, "middle")
         + sweep_line(300, 900, 164, 6) + text(600, 190, f"{NAME} · Gujarat, India", 13, GREY, MONO, 400, "middle"))
    save("footer.svg", W, H, b)

if __name__ == "__main__":
    hero(); buttons(); sections(); about(); cards(); shipped(); craft(); marquee(); orbit(); footer()
