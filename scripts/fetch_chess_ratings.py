#!/usr/bin/env python3
import json, os, urllib.request

CHESSCOM_USER = "obstinixx"
LICHESS_USER  = "piyushggs"

FALLBACK = {
    "cc": {"bullet": 1400, "blitz": 1500, "rapid": 1700},
    "lc": {"bullet": 1583, "blitz": 1684, "rapid": 2035, "classical": 2150},
}

def fetch(url):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "obstinix-readme-builder/1.0")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"WARN: {url} failed: {e}")
        return None

def get_cc():
    d = fetch(f"https://api.chess.com/pub/player/{CHESSCOM_USER}/stats")
    if not d:
        return FALLBACK["cc"]
    return {
        "bullet": d.get("chess_bullet", {}).get("last", {}).get("rating", FALLBACK["cc"]["bullet"]),
        "blitz":  d.get("chess_blitz",  {}).get("last", {}).get("rating", FALLBACK["cc"]["blitz"]),
        "rapid":  d.get("chess_rapid",  {}).get("last", {}).get("rating", FALLBACK["cc"]["rapid"]),
    }

def get_lc():
    d = fetch(f"https://lichess.org/api/user/{LICHESS_USER}")
    if not d:
        return FALLBACK["lc"]
    p = d.get("perfs", {})
    return {
        "bullet":    p.get("bullet",    {}).get("rating", FALLBACK["lc"]["bullet"]),
        "blitz":     p.get("blitz",     {}).get("rating", FALLBACK["lc"]["blitz"]),
        "rapid":     p.get("rapid",     {}).get("rating", FALLBACK["lc"]["rapid"]),
        "classical": p.get("classical", {}).get("rating", FALLBACK["lc"]["classical"]),
    }

def y_px(v):
    return round(280 - ((v - 1300) / 1050) * 210, 1)

def bar_h(v):
    return round(280 - y_px(v), 1)

def make_svg(cc, lc):
    def bar(x, v, color):
        if not v:
            return ""
        yp = y_px(v)
        bh = bar_h(v)
        ly = round(yp - 5, 1)
        return (
            f'<rect x="{x}" y="{yp}" width="50" height="{bh}" rx="3" fill="{color}" opacity="0.9"/>'
            f'<text x="{x+25}" y="{ly}" text-anchor="middle" font-family="monospace" font-size="10" fill="{color}">{v}</text>'
        )

    grid = ""
    for r, y in [(1400,260),(1600,220),(1800,180),(2000,140),(2200,100)]:
        grid += f'<line x1="60" y1="{y}" x2="830" y2="{y}" stroke="#21262d" stroke-width="0.5"/>'
        grid += f'<text x="54" y="{y+4}" text-anchor="end" font-family="monospace" font-size="10" fill="#8b949e">{r}</text>\n'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="340" viewBox="0 0 860 340">
<rect width="860" height="340" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="1"/>
<text x="430" y="28" text-anchor="middle" font-family="monospace" font-size="15" fill="#e6edf3" font-weight="bold">&#9823; Chess Ratings &#8212; Chess.com vs Lichess</text>
<text x="430" y="46" text-anchor="middle" font-family="monospace" font-size="11" fill="#8b949e">obstinixx @ chess.com  &#183;  piyushggs @ lichess.org</text>
<rect x="60" y="54" width="12" height="12" rx="2" fill="#FFD700"/>
<text x="76" y="65" font-family="monospace" font-size="11" fill="#8b949e">Chess.com</text>
<rect x="160" y="54" width="12" height="12" rx="2" fill="#00FF9C"/>
<text x="176" y="65" font-family="monospace" font-size="11" fill="#8b949e">Lichess</text>
{grid}
<line x1="60" y1="280" x2="830" y2="280" stroke="#21262d" stroke-width="1"/>
{bar(100, cc.get("bullet"), "#FFD700")}
{bar(160, lc.get("bullet"), "#00FF9C")}
<text x="155" y="300" text-anchor="middle" font-family="monospace" font-size="12" fill="#e6edf3">Bullet</text>
{bar(292, cc.get("blitz"), "#FFD700")}
{bar(352, lc.get("blitz"), "#00FF9C")}
<text x="347" y="300" text-anchor="middle" font-family="monospace" font-size="12" fill="#e6edf3">Blitz</text>
{bar(485, cc.get("rapid"), "#FFD700")}
{bar(545, lc.get("rapid"), "#00FF9C")}
<text x="540" y="300" text-anchor="middle" font-family="monospace" font-size="12" fill="#e6edf3">Rapid</text>
{bar(717, lc.get("classical"), "#00FF9C")}
<text x="732" y="300" text-anchor="middle" font-family="monospace" font-size="12" fill="#e6edf3">Classical</text>
</svg>'''

if __name__ == "__main__":
    cc = get_cc()
    lc = get_lc()
    print("Chess.com:", cc)
    print("Lichess:  ", lc)
    svg = make_svg(cc, lc)
    os.makedirs("assets", exist_ok=True)
    with open("assets/chess-ratings.svg", "w") as f:
        f.write(svg)
    print("Saved assets/chess-ratings.svg")