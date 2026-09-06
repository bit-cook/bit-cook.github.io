# -*- coding: utf-8 -*-
"""Build the complete AgentBoot logo family as optimized SVGs."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_util import INK, INK8, INK6, INK4, PAPER, SUN, GREEN, GREEN_D, CORAL
from concepts import squircle, glyph_path
from wordmark import shape_to_path

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "svg")
os.makedirs(OUT, exist_ok=True)

SQ = squircle()

# ---------------- glyph geometry (final, A2) ----------------
SW = 6.2
CHEVRON = [(18.6, 18.2), (30.8, 31.0), (18.6, 43.8)]
CURSOR = [(38.6, 43.8), (48.4, 43.8)]
PAD = SW / 2
CX, CY = 32.0, 32.4

def glyph_group(color=INK, sw=SW):
    return (f'<g transform="translate({CX - 33.5:.2f} {CY - 31.0:.2f})">'
            + glyph_path(CHEVRON, sw, color) + glyph_path(CURSOR, sw, color) + "</g>")

# tight bbox of translated glyph: x 14.0..50.0, y 16.5..48.3 (hand-computed)
GLYPH_VB = (13.0, 15.5, 38.0, 33.8)  # x y w h with ~1u breathing room

DEFS_SUN = f"""<defs>
  <linearGradient id="abSun" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFE370"/>
    <stop offset=".52" stop-color="#FFD84D"/>
    <stop offset="1" stop-color="#FFC33A"/>
  </linearGradient>
  <linearGradient id="abHi" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".40"/>
    <stop offset=".6" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="abLo" x1="0" y1="1" x2="0" y2="0">
    <stop offset="0" stop-color="#A65E00" stop-opacity=".14"/>
    <stop offset=".45" stop-color="#A65E00" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="abTile"><path d="{SQ}"/></clipPath>
</defs>"""

def svg(body, vb="0 0 64 64", w=64, h=64):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'width="{w}" height="{h}">{body}</svg>')

# ---------------- 1. primary mark ----------------
mark = svg(f"""{DEFS_SUN}
<path d="{SQ}" fill="url(#abSun)"/>
<g clip-path="url(#abTile)"><path d="{SQ}" fill="url(#abHi)"/><path d="{SQ}" fill="url(#abLo)"/></g>
{glyph_group()}
<path d="{SQ}" fill="none" stroke="{INK}" stroke-width="4.5"/>""")

# ---------------- 2. dark mark ----------------
DEFS_DARK = f"""<defs>
  <linearGradient id="abInk" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2A4A3C"/>
    <stop offset="1" stop-color="#12251D"/>
  </linearGradient>
  <linearGradient id="abSunD" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFE370"/>
    <stop offset="1" stop-color="#FFC33A"/>
  </linearGradient>
  <linearGradient id="abHiD" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".09"/>
    <stop offset=".5" stop-color="#FFFFFF" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="abTileD"><path d="{SQ}"/></clipPath>
</defs>"""

mark_dark = svg(f"""{DEFS_DARK}
<path d="{SQ}" fill="url(#abInk)"/>
<g clip-path="url(#abTileD)"><path d="{SQ}" fill="url(#abHiD)"/></g>
{glyph_group(color="url(#abSunD)")}
<path d="{SQ}" fill="none" stroke="#0A1712" stroke-width="3"/>""")

# ---------------- 3. mono mark (currentColor) ----------------
mark_mono = svg(f"""
<path d="{SQ}" fill="none" stroke="currentColor" stroke-width="4.5"/>
{glyph_group(color="currentColor")}""")

# ---------------- 4. bare glyph ----------------
gx, gy, gw, gh = GLYPH_VB
mark_glyph = svg(f"""{glyph_group()}""", vb=f"{gx} {gy} {gw} {gh}", w=96, h=86)

# ---------------- 5. favicon (bold, simplified) ----------------
SW_F = 7.0
fav_glyph = (f'<g transform="translate({CX - 33.5:.2f} {CY - 31.0:.2f})">'
             + glyph_path(CHEVRON, SW_F, INK) + glyph_path(CURSOR, SW_F, INK) + "</g>")
favicon = svg(f"""<defs>
  <linearGradient id="s" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FFE370"/><stop offset="1" stop-color="#FFC33A"/>
  </linearGradient>
</defs>
<path d="{SQ}" fill="url(#s)"/>
{fav_glyph}
<path d="{SQ}" fill="none" stroke="{INK}" stroke-width="5.4"/>""")

# ---------------- 6. wordmark ----------------
WM_SIZE = 55.0
PAIR_FIX = {("t", "B"): 14.0}
wm_d, wm_w, wm_cap, wm_xh, wm_asc, wm_desc = shape_to_path(
    "fonts/Baloo2-700.ttf", "AgentBoot", WM_SIZE, tracking=-0.008, pair_fix=PAIR_FIX)
print(f"wordmark: w={wm_w:.1f} cap={wm_cap:.1f}")

wordmark = svg(f'<path d="{wm_d}" fill="{INK}"/>',
               vb=f"0 {wm_asc - WM_SIZE * 0:.0f} ...")  # placeholder replaced below

# tight wordmark box: glyphs from -asc? compute: ink top ≈ cap above baseline; descender below
wm_top = -wm_cap - WM_SIZE * 0.06
wm_bot = -wm_desc * 0.88  # g descender
wm_vb = f"-1 {wm_top:.1f} {wm_w + 2:.1f} {wm_bot - wm_top + 1:.1f}"
wordmark = svg(f'<path d="{wm_d}" fill="{INK}"/>', vb=wm_vb,
               w=round(wm_w + 2), h=round(wm_bot - wm_top + 1))

# ---------------- 7. horizontal lockup ----------------
GAP = 16.5
BASE_Y = 48.6  # baseline in tile coords
def lockup(text_fill=INK, bg=None):
    parts = [f'<g transform="translate(0 0)">']
    parts.append(mark)  # 64x64 with viewBox intact
    parts.append(f'<g transform="translate({64 + GAP:.1f} {BASE_Y:.1f})">'
                 f'<path d="{wm_d}" fill="{text_fill}"/></g>')
    parts.append("</g>")
    total_w = 64 + GAP + wm_w
    body = "".join(parts)
    return body, total_w

body_l, w_l = lockup()
PAD_L = 3
logo_h = svg(body_l, vb=f"{-PAD_L} {-PAD_L} {w_l + 2 * PAD_L:.1f} {64 + 2 * PAD_L}",
             w=round(w_l + 2 * PAD_L), h=70)
body_l2, w_l2 = lockup(text_fill=PAPER)
logo_h_dark = svg(body_l2, vb=f"{-PAD_L} {-PAD_L} {w_l2 + 2 * PAD_L:.1f} {64 + 2 * PAD_L}",
                  w=round(w_l2 + 2 * PAD_L), h=70)

# ---------------- 8. stacked lockup ----------------
ST_ICON = 96.0
ST_WM = 40.0
wm_d2, wm_w2, wm_cap2, *_ = shape_to_path("fonts/Baloo2-700.ttf", "AgentBoot", ST_WM, tracking=-0.008, pair_fix={("t", "B"): 14.0})
st_w = max(ST_ICON, wm_w2)
stack_wm_y = ST_ICON + 26 + wm_cap2  # baseline
st_h = ST_ICON + 26 + wm_cap2 + 2
stack = svg(
    f'<g transform="translate({(st_w - ST_ICON) / 2:.1f} 0)">'
    + mark.replace('width="64" height="64"', f'width="{ST_ICON:.0f}" height="{ST_ICON:.0f}"') +
    f'</g><g transform="translate({(st_w - wm_w2) / 2:.1f} {stack_wm_y:.1f})">'
    f'<path d="{wm_d2}" fill="{INK}"/></g>',
    vb=f"0 0 {st_w:.1f} {st_h:.1f}", w=round(st_w), h=round(st_h))

# ---------------- write files ----------------
files = {
    "logo-mark.svg": mark,
    "logo-mark-dark.svg": mark_dark,
    "logo-mark-mono.svg": mark_mono,
    "logo-glyph.svg": mark_glyph,
    "favicon.svg": favicon,
    "wordmark.svg": wordmark,
    "logo-horizontal.svg": logo_h,
    "logo-horizontal-dark.svg": logo_h_dark,
    "logo-stack.svg": stack,
}
for name, content in files.items():
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, f"({len(content)} B)")

# stash pieces for banner/brand scripts
with open(os.path.join(BASE, "_pieces.py"), "w", encoding="utf-8") as f:
    f.write(f"""SQ = {SQ!r}
GLYPH_GROUP = {glyph_group()!r}
FAV_GLYPH = {fav_glyph!r}
WM_D = {wm_d!r}
WM_W = {wm_w:.2f}
WM_CAP = {wm_cap:.2f}
WM_SIZE = {WM_SIZE}
""")
print("pieces stashed")
