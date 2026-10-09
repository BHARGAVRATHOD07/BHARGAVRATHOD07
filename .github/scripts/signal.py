#!/usr/bin/env python3
"""Renders the Signal panels (GitHub activity + LeetCode) as animated SVGs. Standard library only.
Usage: signal.py --user NAME --leetcode HANDLE --out dist [--prev prev-cache.json] [--demo]
If a source is unreachable, the last good values from the previous cache.json are reused."""
import argparse, json, os, re, sys, urllib.request
from datetime import date, timedelta
from xml.sax.saxutils import escape as esc

BG = "#0B0F19"; PANEL = "#0f1626"; LINE = "#1f2a44"; WHITE = "#F8FAFC"; GREY = "#8b95ad"
LP = "#a78bfa"; BLUE = "#38BDF8"; ORANGE = "#FF9F43"; GREEN = "#34d399"; RED = "#f87171"
MONO = "'JetBrains Mono','SF Mono',Consolas,'Courier New',monospace"
SANS = "Inter,'Segoe UI',Helvetica,Arial,sans-serif"
LEVELS = ["#151b2d", "#2a2350", "#4b3f9e", "#8b7cf6", "#c4b5fd"]
W = 1200

def http(url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", "replace")

def fetch_github(user, token):
    q = """query($login:String!){ user(login:$login){ followers{totalCount}
      repositories(ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){ totalCount }
      contributionsCollection{ contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } } } }"""
    raw = http("https://api.github.com/graphql", json.dumps({"query": q, "variables": {"login": user}}).encode(),
               {"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-signal"})
    u = json.loads(raw)["data"]["user"]; cal = u["contributionsCollection"]["contributionCalendar"]
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    return {"total": cal["totalContributions"], "days": days, "repos": u["repositories"]["totalCount"], "followers": u["followers"]["totalCount"]}

def fetch_leetcode(handle):
    q = """query u($username:String!){ matchedUser(username:$username){ profile{ranking} submitStatsGlobal{ acSubmissionNum{ difficulty count } } } }"""
    raw = http("https://leetcode.com/graphql", json.dumps({"query": q, "variables": {"username": handle}}).encode(),
               {"Content-Type": "application/json", "Referer": f"https://leetcode.com/u/{handle}/", "User-Agent": "Mozilla/5.0 profile-signal"})
    m = json.loads(raw)["data"]["matchedUser"]
    ac = {x["difficulty"]: x["count"] for x in m["submitStatsGlobal"]["acSubmissionNum"]}
    return {"total": ac.get("All", 0), "easy": ac.get("Easy", 0), "medium": ac.get("Medium", 0), "hard": ac.get("Hard", 0), "rank": m["profile"]["ranking"]}

def streaks(days):
    counts = [c for _, c in days]
    best = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0; best = max(best, run)
    cur = 0; i = len(counts) - 1
    if i >= 0 and counts[i] == 0: i -= 1          # today may not have contributions yet
    while i >= 0 and counts[i] > 0: cur += 1; i -= 1
    return cur, best

def text(x, y, s, size, fill, family=SANS, weight=400, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(str(s))}</text>'

def save(path, w, h, body):
    defs = (f'<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ORANGE}"/><stop offset=".55" stop-color="{LP}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
            '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#161d30" stroke-width="1"/></pattern>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"><defs>{defs}</defs>'
           f'<rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#grid)"/>{body}</svg>')
    open(path, "w", encoding="utf-8").write(svg)

def level(c):
    return 0 if c == 0 else 1 if c < 4 else 2 if c < 7 else 3 if c < 10 else 4

def render_overview(path, gh):
    H = 360; b = ""
    if not gh:
        save(path, W, H, text(600, 190, "GitHub activity loading…", 20, GREY, MONO, 400, "middle")); return
    cur, best = streaks(gh["days"])
    stats = [("Contributions (12 mo)", gh["total"]), ("Current streak", f"{cur}d"), ("Longest streak", f"{best}d"),
             ("Public repos", gh["repos"]), ("Followers", gh["followers"])]
    for i, (label, val) in enumerate(stats):
        x = 40 + i * 226
        b += (f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{i*.15}s" dur=".6s" fill="freeze"/>'
              f'<rect x="{x}" y="30" width="206" height="96" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
              + text(x + 22, 78, val, 36, "url(#gb)", SANS, 800) + text(x + 22, 106, label, 12, GREY, MONO) + '</g>')
    days = gh["days"][-371:]
    start = date.fromisoformat(days[0][0]); offset = (start.weekday() + 1) % 7   # Sunday-first rows
    pitch, x0, y0 = 18, 123, 160
    cols = {}
    for k, (d, c) in enumerate(days):
        idx = k + offset; cols.setdefault(idx // 7, []).append((idx % 7, c, d))
    for ci, cells in cols.items():
        b += f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{.6+ci*.03:.2f}s" dur=".5s" fill="freeze"/>'
        for row, c, d in cells:
            b += f'<rect x="{x0+ci*pitch}" y="{y0+row*pitch}" width="14" height="14" rx="3" fill="{LEVELS[level(c)]}"><title>{d}: {c}</title></rect>'
        b += '</g>'
    b += text(123, 322, "contributions over the last 12 months", 12, GREY, MONO)
    lx = 1077 - 5 * 18
    b += text(lx - 40, 322, "less", 12, GREY, MONO)
    for i, col in enumerate(LEVELS): b += f'<rect x="{lx+i*18}" y="311" width="14" height="14" rx="3" fill="{col}"/>'
    b += text(lx + 5 * 18 + 6, 322, "more", 12, GREY, MONO)
    save(path, W, H, b)

def render_leetcode(path, lc, handle):
    H = 240
    if not lc:
        save(path, W, H, text(600, 125, "LeetCode stats loading…", 20, GREY, MONO, 400, "middle")); return
    b = (f'<rect x="40" y="20" width="1120" height="200" rx="16" fill="{PANEL}" stroke="{LINE}"/>'
         + text(80, 62, "LEETCODE", 13, ORANGE, MONO, 600, extra='letter-spacing="3"')
         + text(80, 140, lc["total"], 72, "url(#gb)", SANS, 800) + text(80, 172, "problems solved", 14, GREY, MONO)
         + text(80, 198, f"@{handle}", 12, GREY, MONO))
    mx = max(lc["easy"], lc["medium"], lc["hard"], 1)
    for i, (name, key, col) in enumerate([("Easy", "easy", GREEN), ("Medium", "medium", ORANGE), ("Hard", "hard", RED)]):
        y = 70 + i * 44; wmax = 480; w = max(6, wmax * lc[key] / mx)
        b += (text(380, y + 17, name, 14, WHITE, MONO, 500)
              + f'<rect x="460" y="{y}" width="{wmax}" height="22" rx="11" fill="#151b2d"/>'
              f'<rect x="460" y="{y}" width="0" height="22" rx="11" fill="{col}"><animate attributeName="width" from="0" to="{w:.0f}" begin="{i*.25}s" dur="1.2s" fill="freeze"/></rect>'
              + text(460 + wmax + 20, y + 17, lc[key], 15, WHITE, MONO, 600))
    b += text(1120, 62, f"global rank #{lc['rank']:,}" if lc.get("rank") else "", 14, GREY, MONO, 400, "end")
    save(path, W, H, b)

def patch_snake(path):
    if not os.path.exists(path): return
    s = open(path, encoding="utf-8").read()
    m = re.search(r"<svg[^>]*>", s)
    if m and "profile-bg" not in s:
        s = s[:m.end()] + f'<rect id="profile-bg" x="-2000" y="-2000" width="6000" height="6000" fill="{BG}"/>' + s[m.end():]
        open(path, "w", encoding="utf-8").write(s)

def demo():
    import random; random.seed(3); t = date.today(); days = []
    for i in range(371, 0, -1):
        d = t - timedelta(days=i); days.append((d.isoformat(), random.choice([0, 0, 0, 1, 2, 3, 5, 8, 12])))
    return {"total": sum(c for _, c in days), "days": days, "repos": 14, "followers": 9}, {"total": 120, "easy": 70, "medium": 44, "hard": 6, "rank": 1234567}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user"); ap.add_argument("--leetcode"); ap.add_argument("--out", default="dist")
    ap.add_argument("--prev"); ap.add_argument("--demo", action="store_true")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    prev = {}
    if a.prev and os.path.exists(a.prev):
        try: prev = json.load(open(a.prev))
        except Exception: prev = {}
    if a.demo: gh, lc = demo()
    else:
        gh = lc = None
        try: gh = fetch_github(a.user, os.environ.get("GITHUB_TOKEN", ""))
        except Exception as e: print("github fetch failed:", e, file=sys.stderr); gh = prev.get("gh")
        try: lc = fetch_leetcode(a.leetcode)
        except Exception as e: print("leetcode fetch failed:", e, file=sys.stderr); lc = prev.get("lc")
    render_overview(os.path.join(a.out, "signal-overview.svg"), gh)
    render_leetcode(os.path.join(a.out, "signal-leetcode.svg"), lc, a.leetcode or "")
    patch_snake(os.path.join(a.out, "signal-snake.svg"))
    json.dump({"gh": gh, "lc": lc}, open(os.path.join(a.out, "cache.json"), "w"))

if __name__ == "__main__":
    main()
