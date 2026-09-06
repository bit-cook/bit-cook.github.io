# -*- coding: utf-8 -*-
"""GitHub social preview / README banners (1200x630), zh + en."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_util import render_html, INK, INK8, INK6, INK4, PAPER, SUN, GREEN, GREEN_D, CORAL
from concepts import squircle, glyph_path
from wordmark import shape_to_path
from build_family import mark
import math

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "svg")
SQ = squircle()


def shape_file(font_path, text, size, tracking=0.0, index=0):
    import uharfbuzz as hb
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.misc.transform import Transform
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob, index)
    font = hb.Font(face)
    upem = face.upem
    font.scale = (upem, upem)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})
    tt = TTFont(font_path, fontNumber=index)
    glyph_set = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    s = size / upem
    x = 0.0
    parts = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        gname = order[info.codepoint]
        pen = SVGPathPen(glyph_set)
        tpen = TransformPen(pen, Transform(s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s))
        glyph_set[gname].draw(tpen)
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += pos.x_advance + tracking * upem
    return " ".join(parts), x * s


YAHEI_B = "C:/Windows/Fonts/msyhbd.ttc"
CONSOLAS = "C:/Windows/Fonts/consola.ttf"

# mark at arbitrary size
def mark_at(x, y, size):
    return (f'<g transform="translate({x} {y})">'
            + mark.replace('width="64" height="64"', f'width="{size}" height="{size}"')
            + "</g>")


def banner(lang):
    if lang == "zh":
        h1 = "一条命令，Agent 就位"
        sub = "免费开源的 AI Agent 启动器 · 15 个 Agent 按需安装"
        foot = "MIT 开源 · Linux / macOS / Windows · 离线可用 · boot.ide.pub"
        cmd = "$ curl -fsSL https://boot.ide.pub/install.sh | sh"
        cmd2 = "$ agentboot"
        ok = "选择 Agent，开始创造"
    else:
        h1 = "One command. Agent ready."
        sub = "Free, open-source launcher for 15 AI coding agents"
        foot = "MIT · Linux / macOS / Windows · Offline packages · boot.ide.pub"
        cmd = "$ curl -fsSL https://boot.ide.pub/install.sh | sh"
        cmd2 = "$ agentboot"
        ok = "Pick your agents, start creating"

    wm_d, wm_w, wm_cap, *_ = shape_to_path("fonts/Baloo2-700.ttf", "AgentBoot", 58, -0.008, pair_fix={("t", "B"): 14.0})
    h1_d, h1_w = shape_file(YAHEI_B, h1, 46, -0.01)
    sub_d, sub_w = shape_file(YAHEI_B, sub, 22, 0)
    foot_d, foot_w = shape_file(YAHEI_B, foot, 19, 0)
    cmd_d, cmd_w = shape_file(CONSOLAS, cmd, 21.5, 0)
    cmd2_d, cmd2_w = shape_file(CONSOLAS, cmd2, 21.5, 0)
    ok_d, ok_w = shape_file(YAHEI_B, ok, 19, 0)

    W, H = 1200, 630
    icon_s = 82
    ix, iy = 68, 62
    wm_x = ix + icon_s + 22
    wm_base = iy + icon_s / 2 + wm_cap / 2 + 2

    card_x, card_y, card_w, card_h = 68, 330, 660, 158
    mx, my, ms = 836, 208, 296
    ring_c = (mx + ms / 2, my + ms / 2)

    check_pts = "M 0 5 L 4.2 9.4 L 12 0"
    body = f"""
<rect width="{W}" height="{H}" fill="{PAPER}"/>
<!-- decor: orbit rings echoing site hero -->
<circle cx="{ring_c[0]}" cy="{ring_c[1]}" r="238" fill="none" stroke="{INK}" stroke-opacity=".10" stroke-width="1.6"/>
<circle cx="{ring_c[0]}" cy="{ring_c[1]}" r="296" fill="none" stroke="{INK}" stroke-opacity=".06" stroke-width="1.6"/>
<circle cx="{ring_c[0] + 238 * math.cos(math.radians(-38)):.1f}" cy="{ring_c[1] - 238 * math.sin(math.radians(-38)):.1f}" r="9" fill="{CORAL}" stroke="{INK}" stroke-width="2.5"/>
<g opacity=".07"><path d="{SQ}" transform="translate(1010 512) scale(2.1)" fill="none" stroke="{INK}" stroke-width="2"/></g>

<!-- lockup -->
<g transform="translate({ix} {iy})">
  {'{MARK}'}
</g>
<g transform="translate({wm_x:.0f} {wm_base:.1f})"><path d="{wm_d}" fill="{INK}"/></g>

<!-- headline -->
<g transform="translate(70 254)"><path d="{h1_d}" fill="{INK}"/></g>
<g transform="translate(72 300)" opacity=".78"><path d="{sub_d}" fill="{INK6}"/></g>

<!-- terminal card -->
<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="18" fill="#FFFFFF" stroke="{INK}" stroke-width="2.5"/>
<circle cx="{card_x + 26}" cy="{card_y + 26}" r="5.5" fill="{CORAL}"/>
<circle cx="{card_x + 46}" cy="{card_y + 26}" r="5.5" fill="{SUN}"/>
<circle cx="{card_x + 66}" cy="{card_y + 26}" r="5.5" fill="{GREEN}"/>
<line x1="{card_x + 1}" y1="{card_y + 44}" x2="{card_x + card_w - 1}" y2="{card_y + 44}" stroke="{INK}" stroke-opacity=".14" stroke-width="1.5"/>
<g transform="translate({card_x + 26} {card_y + 84})"><path d="{cmd_d}" fill="{INK}"/></g>
<g transform="translate({card_x + 26} {card_y + 126})"><path d="{cmd2_d}" fill="{INK}"/></g>
<g transform="translate({card_x + 40 + cmd2_w:.0f} {card_y + 112})">
  <path d="{check_pts}" transform="scale(1.5)" fill="none" stroke="{GREEN}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
</g>
<g transform="translate({card_x + 74 + cmd2_w:.0f} {card_y + 127})"><path d="{ok_d}" fill="{GREEN_D}"/></g>

<!-- big mark right -->
<g transform="translate({mx} {my})">
  {'{MARK_BIG}'}
</g>

<!-- footer -->
<g transform="translate(70 596)" opacity=".9"><path d="{foot_d}" fill="{INK6}"/></g>
"""
    body = body.replace("{MARK}", mark.replace('width="64" height="64"', f'width="{icon_s}" height="{icon_s}"'))
    body = body.replace("{MARK_BIG}", mark.replace('width="64" height="64"', f'width="{ms}" height="{ms}"'))
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{body}</svg>'


for lang in ("zh", "en"):
    p = os.path.join(OUT, f"banner-{lang}.svg")
    with open(p, "w", encoding="utf-8") as f:
        f.write(banner(lang))
    print("wrote", p)
