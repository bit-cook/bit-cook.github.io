# -*- coding: utf-8 -*-
"""AgentBoot logo concepts: 5 candidates on one comparison board."""
import math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_util import render_html, INK, PAPER, SUN, GREEN, CORAL

BASE = os.path.dirname(os.path.abspath(__file__))
CONCEPTS = os.path.join(BASE, "concepts")
os.makedirs(CONCEPTS, exist_ok=True)


def squircle(n=5.0, a=29.0, c=32.0, steps=90):
    """Superellipse path centered at c, half-size a, exponent n."""
    pts = []
    for i in range(steps):
        t = -math.pi / 2 + (2 * math.pi) * i / steps
        ct, st = math.cos(t), math.sin(t)
        x = c + a * (abs(ct) ** (2 / n)) * (1 if ct >= 0 else -1)
        y = c + a * (abs(st) ** (2 / n)) * (1 if st >= 0 else -1)
        pts.append((x, y))
    d = f"M {pts[0][0]:.2f} {pts[0][1]:.2f} " + " ".join(
        f"L {x:.2f} {y:.2f}" for x, y in pts[1:]) + " Z"
    return d


SQ = squircle()

DEFS = f"""
<defs>
  <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFE370"/>
    <stop offset=".55" stop-color="#FFD84D"/>
    <stop offset="1" stop-color="#FFC53A"/>
  </linearGradient>
  <linearGradient id="hi" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".42"/>
    <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="lo" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#A65E00" stop-opacity=".16"/>
    <stop offset="1" stop-color="#A65E00" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="tile"><path d="{SQ}"/></clipPath>
</defs>"""


def tile(inner, size=64, outline=INK, ow=4.5):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="{size}" height="{size}">
{DEFS if size == 64 else ''}
<g>
  <path d="{SQ}" fill="url(#sun)"/>
  <g clip-path="url(#tile)">
    <path d="{SQ}" fill="url(#hi)"/>
    <path d="{SQ}" fill="url(#lo)"/>
  </g>
  {inner}
  <path d="{SQ}" fill="none" stroke="{outline}" stroke-width="{ow}"/>
</g>
</svg>"""


def glyph_path(pts, sw, color=INK, cap="round", join="round"):
    d = "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{join}"/>')


def centered(paths, pad=3.0, cx=32.0, cy=32.4, dy=0):
    """Wrap stroke paths so their stroked bbox is optically centered."""
    import re
    xs, ys = [], []
    for p in paths:
        geo = p.split('d="')[1].split('"')[0] if 'd="' in p else None
        if geo:
            for m in re.finditer(r'(-?\d+\.?\d*) (-?\d+\.?\d*)', geo):
                x, y = float(m.group(1)), float(m.group(2))
                xs += [x - pad, x + pad]; ys += [y - pad, y + pad]
        else:
            g = lambda attr: float(re.search(attr + r'="(-?\d+\.?\d*)"', p).group(1))
            x, y, w, h = g('x'), g('y'), g('width'), g('height')
            xs += [x - pad, x + w + pad]; ys += [y - pad, y + h + pad]
    bx = (min(xs) + max(xs)) / 2; by = (min(ys) + max(ys)) / 2
    return f'<g transform="translate({cx - bx:.2f} {cy - by + dy:.2f})">' + "".join(paths) + "</g>"


SW = 6.0
# A: classic prompt (refined current) — symmetric chevron + short cursor
A = centered([glyph_path([(20, 19.5), (31.5, 31.5), (20, 43.5)], SW),
              glyph_path([(39, 43.5), (48.5, 43.5)], SW)])
# B: same, coral cursor (accent tie to site orbit-dot)
B = centered([glyph_path([(20, 19.5), (31.5, 31.5), (20, 43.5)], SW),
              glyph_path([(39, 43.5), (48.5, 43.5)], SW, color=CORAL)])
# C: launch pad — chevron above full ground line
C = centered([glyph_path([(21, 16.5), (32, 28), (21, 39.5)], 5.6),
              glyph_path([(15.5, 46.5), (48.5, 46.5)], 5.6)])
# D: boot profile — steeper shaft, longer flat toe, on ground line
D = centered([glyph_path([(24.5, 14.5), (33.5, 26.5), (13.5, 41.5)], 5.6),
              glyph_path([(15.5, 46.5), (48.5, 46.5)], 5.6)])
# E: doubled chevron (fast-forward ready) + cursor
E = centered([glyph_path([(15.5, 21), (25, 31.5), (15.5, 42)], 5.4),
              glyph_path([(25.5, 21), (35, 31.5), (25.5, 42)], 5.4),
              glyph_path([(41, 43.2), (49, 43.2)], 5.4)])

VARIANTS = {k: tile(g) for k, g in {"A": A, "B": B, "C": C, "D": D, "E": E}.items()}
NAMES = {
    "A": "A · 经典提示符（进化版）",
    "B": "B · 珊瑚光标（点缀活力）",
    "C": "C · 发射台（靴子站上线）",
    "D": "D · 靴形箭头（双关 Boot）",
    "E": "E · 双箭头（快进就位）",
}

for k, svg in VARIANTS.items():
    with open(os.path.join(CONCEPTS, f"tile-{k}.svg"), "w", encoding="utf-8") as f:
        f.write(svg)

# comparison board
cells = ""
for k in "ABCDE":
    svg = VARIANTS[k]
    cells += f"""
  <div class="cell">
    <div class="big">{svg.replace('width="64" height="64"', 'width="148" height="148"')}</div>
    <h3>{NAMES[k]}</h3>
    <div class="sizes">
      <span>{svg.replace('width="64" height="64"', 'width="40" height="40"')}</span>
      <span>{svg.replace('width="64" height="64"', 'width="24" height="24"')}</span>
      <span>{svg.replace('width="64" height="64"', 'width="16" height="16"')}</span>
      <span>{svg.replace('width="64" height="64"', 'width="12" height="12"')}</span>
    </div>
  </div>"""

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin:0; box-sizing:border-box; }}
body {{ background:{PAPER}; font-family:'Segoe UI',sans-serif; padding:34px 30px; color:{INK}; }}
h1 {{ font-size:21px; margin-bottom:6px; }}
p.sub {{ color:{INK}; opacity:.62; font-size:13px; margin-bottom:26px; }}
.grid {{ display:flex; gap:18px; }}
.cell {{ width:214px; text-align:center; }}
.big {{ background:#fff; border:1.5px solid rgba(18,37,29,.14); border-radius:18px;
        padding:20px 0 12px; display:flex; justify-content:center; }}
.cell h3 {{ font-size:13.5px; margin:12px 0 8px; font-weight:600; }}
.sizes {{ display:flex; gap:12px; justify-content:center; align-items:flex-end; height:44px; }}
.sizes span {{ display:flex; align-items:flex-end; }}
</style></head><body>
<h1>AgentBoot · Logo 概念对比</h1>
<p class="sub">同比例缩放检验：148 / 40 / 24 / 16 / 12 px —— 小尺寸必须依然清晰可辨</p>
<div class="grid">{cells}
</div></body></html>"""

with open(os.path.join(CONCEPTS, "board.html"), "w", encoding="utf-8") as f:
    f.write(html)

render_html(os.path.join(CONCEPTS, "board.html"),
            os.path.join(CONCEPTS, "board.png"), 1190, 420, timeout=90)
print("board rendered")
