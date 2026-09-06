# -*- coding: utf-8 -*-
"""Render PNG set + favicon.ico + apple-touch-icon."""
import os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_util import render_html
from PIL import Image

BASE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(BASE, "png")
os.makedirs(PNG, exist_ok=True)


def render_svg(svg_rel, out_rel, w, h):
    import re
    svg = open(os.path.join(BASE, svg_rel), encoding="utf-8").read()
    # scale root to exact target (viewBox handles the mapping)
    svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{w}" height="{h}"', svg, count=1)
    html_path = os.path.join(PNG, "_tmp.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(f'<!doctype html><html><body style="margin:0;background:transparent">{svg}</body></html>')
    out = os.path.join(PNG, out_rel)
    render_html(html_path, out, w, h, timeout=90)
    os.remove(html_path)
    print("png:", out_rel)


def down(src, dst, size):
    im = Image.open(os.path.join(PNG, src)).convert("RGBA")
    im.resize((size, size), Image.LANCZOS).save(os.path.join(PNG, dst))
    print("png:", dst)


# mark renders — big ones direct, small ones downscaled from 512 (crisper AA)
render_svg("svg/logo-mark.svg", "logo-mark-1024.png", 1024, 1024)
render_svg("svg/logo-mark.svg", "logo-mark-512.png", 512, 512)
for s in (256, 128, 64, 48, 32, 24, 16):
    down("logo-mark-512.png", f"logo-mark-{s}.png", s)

render_svg("svg/logo-mark-dark.svg", "logo-mark-dark-512.png", 512, 512)
render_svg("svg/logo-mark-mono.svg", "logo-mark-mono-512.png", 512, 512)

hw = round(349 / 70 * 210)
render_svg("svg/logo-horizontal.svg", "logo-horizontal-210.png", hw, 210)
render_svg("svg/logo-horizontal-dark.svg", "logo-horizontal-dark-210.png", hw, 210)
render_svg("svg/logo-stack.svg", "logo-stack-2x.png", 424, 286)

# favicon renders (dedicated bold favicon.svg)
render_svg("svg/favicon.svg", "favicon-256.png", 256, 256)
for s in (48, 32, 16):
    down("favicon-256.png", f"favicon-{s}.png", s)

# favicon.ico (16+32+48)
imgs = [Image.open(os.path.join(PNG, f"favicon-{s}.png")).convert("RGBA") for s in (48, 32, 16)]
imgs[0].save(os.path.join(BASE, "favicon.ico"), sizes=[(48, 48), (32, 32), (16, 16)],
             append_images=imgs[1:])
print("favicon.ico written")

# apple-touch-icon: solid paper-backed 180px (iOS dislikes transparency)
im = Image.open(os.path.join(PNG, "logo-mark-512.png")).convert("RGBA")
bg = Image.new("RGBA", (512, 512), "#FFFDF5")
bg.alpha_composite(im)
bg.resize((180, 180), Image.LANCZOS).convert("RGB").save(
    os.path.join(PNG, "apple-touch-icon.png"))
print("apple-touch-icon.png written")

# og images from banners (already rendered at exact 1200x630)
for lang in ("zh", "en"):
    Image.open(os.path.join(PNG, f"banner-{lang}-r2.png")).save(
        os.path.join(PNG, f"og-image{'-en' if lang == 'en' else ''}.png"))
print("og images written")
