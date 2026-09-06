# -*- coding: utf-8 -*-
"""Brand sheet — single-page HTML spec of the AgentBoot identity."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_util import render_html, INK, INK8, INK6, INK4, PAPER, SUN, GREEN, GREEN_D, CORAL

BASE = os.path.dirname(os.path.abspath(__file__))


def read(name):
    return open(os.path.join(BASE, "svg", name), encoding="utf-8").read()


MARK = read("logo-mark.svg")
MARK_DARK = read("logo-mark-dark.svg")
MARK_MONO = read("logo-mark-mono.svg")
GLYPH = read("logo-glyph.svg")
WORDMARK = read("wordmark.svg")
HORIZ = read("logo-horizontal.svg")
HORIZ_DARK = read("logo-horizontal-dark.svg")
STACK = read("logo-stack.svg")


def size(svg, s):
    return svg.replace('width="64" height="64"', f'width="{s}" height="{s}"')


def sized(svg, w, h):
    import re
    svg = re.sub(r'width="[\d.]+"', f'width="{w}"', svg, count=1)
    svg = re.sub(r'height="[\d.]+"', f'height="{h}"', svg, count=1)
    return svg


# clearspace diagram: mark 120 + guides
CS = 30  # 1/4 of 120
clear = f"""
<div class="clearwrap">
  <div class="clearbox" style="width:{120 + 2 * CS}px;height:{120 + 2 * CS}px">
    <div class="csmark x"></div><div class="csmark y"></div>
    {size(MARK, 120)}
  </div>
  <p class="cap">净空 = 图标高度的 1/4（x），最小可用尺寸 16px</p>
</div>"""

swatches = "".join(f"""
  <div class="sw"><div class="chip" style="background:{c};{'border:1.5px solid '+INK if c in ('sun: #FFD84D','') else ''}"></div>
  <b>{name}</b><code>{hexv}</code></div>"""
    for name, hexv, c in [
        ("墨 Ink 950", "#12251D", "#12251D"),
        ("纸 Paper", "#FFFDF5", "#FFFDF5"),
        ("日光 Sun", "#FFD84D", "#FFD84D"),
        ("日光深 Sun Deep", "#FFC33A", "#FFC33A"),
        ("行动绿 Green", "#137A52", "#137A52"),
        ("珊瑚 Coral", "#FF7A59", "#FF7A59"),
    ])

donts = "".join(f"""
  <figure class="dont"><div class="dontbox">{inner}</div>
  <figcaption>✗ {why}</figcaption></figure>"""
    for inner, why in [
        (f'<span style="display:inline-block;transform:scaleX(1.45);transform-origin:center">{size(MARK, 96)}</span>', "不要拉伸变形"),
        (f'<span style="display:inline-block;transform:rotate(14deg)">{size(MARK, 96)}</span>', "不要旋转"),
        (f'<span style="display:inline-block;filter:hue-rotate(140deg)">{size(MARK, 96)}</span>', "不要改变品牌配色"),
        (f'<span style="display:inline-block;filter:drop-shadow(6px 8px 6px rgba(0,0,0,.45))">{size(MARK, 96)}</span>', "不要加投影/立体效果"),
        (f'<span style="display:inline-block;opacity:.45">{size(MARK, 96)}</span>', "不要降低对比度"),
        (f'<span style="display:inline-block;filter:grayscale(1) brightness(1.6)">{size(MARK, 96)}</span>', "不要自行去色（请用 mono 版）"),
    ])

html = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>
* {{ margin:0; box-sizing:border-box; }}
body {{ background:{PAPER}; color:{INK}; font-family:'Segoe UI','Microsoft YaHei',sans-serif; padding:52px 56px; }}
h1 {{ font-size:30px; letter-spacing:-.02em; }}
h2 {{ font-size:19px; margin:46px 0 6px; padding-top:26px; border-top:1.5px solid rgba(18,37,29,.15); }}
p.lede {{ color:{INK6}; font-size:14px; margin-bottom:20px; max-width:72ch; line-height:1.7; }}
.row {{ display:flex; gap:18px; align-items:stretch; flex-wrap:wrap; }}
.card {{ background:#fff; border:1.5px solid rgba(18,37,29,.15); border-radius:18px; padding:24px;
        display:flex; flex-direction:column; align-items:center; justify-content:center; gap:14px; }}
.card .cap {{ font-size:12.5px; color:{INK6}; }}
.grid2 {{ display:grid; grid-template-columns:repeat(4,1fr); gap:18px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
.hero {{ display:flex; gap:36px; align-items:center; background:#fff; border:1.5px solid rgba(18,37,29,.15);
        border-radius:24px; padding:38px 42px; margin-top:26px; }}
.hero .txt h2 {{ border:0; margin:0 0 8px; padding:0; }}
.hero .txt p {{ color:{INK6}; font-size:14px; line-height:1.8; max-width:60ch; }}
.sizes {{ display:flex; align-items:flex-end; gap:26px; }}
.sizes .s {{ display:flex; flex-direction:column; align-items:center; gap:8px; font-size:11.5px; color:{INK6}; }}
.clearwrap {{ display:flex; gap:30px; align-items:center; }}
.clearbox {{ position:relative; border:1.5px dashed #7FA08F; border-radius:24px;
             display:flex; align-items:center; justify-content:center; }}
.csmark {{ position:absolute; background:#7FA08F; }}
.csmark.x {{ left:{CS / 2 - 1}px; top:0; bottom:0; width:2px; }}
.csmark.y {{ top:{CS / 2 - 1}px; left:0; right:0; height:2px; }}
.cap {{ font-size:12.5px; color:{INK6}; max-width:30ch; line-height:1.6; }}
.swatches {{ display:flex; gap:16px; }}
.sw {{ width:150px; }} .sw .chip {{ height:74px; border-radius:14px; border:1.5px solid rgba(18,37,29,.18); }}
.sw b {{ display:block; font-size:13px; margin-top:8px; }}
.sw code {{ font-size:12px; color:{INK6}; }}
.navymock {{ background:{PAPER}; border:1.5px solid rgba(18,37,29,.15); border-radius:16px;
             padding:14px 22px; display:flex; align-items:center; gap:12px; width:680px; }}
.navymock .links {{ margin-left:auto; display:flex; gap:16px; font-size:13.5px; color:{INK8}; }}
.navymock .links b {{ color:{INK}; font-weight:600; }}
.term {{ background:{INK}; color:#E9F2EC; border-radius:16px; padding:18px 22px; width:680px;
         font-family:Consolas,monospace; font-size:14.5px; line-height:2.0; }}
.term .p {{ color:{SUN}; }} .term .ok {{ color:#57D49B; }} .term .dim {{ color:{INK4}; }}
.donts {{ display:grid; grid-template-columns:repeat(6,1fr); gap:14px; }}
.dontbox {{ background:#fff; border:1.5px solid rgba(18,37,29,.15); border-radius:14px; height:128px;
            display:flex; align-items:center; justify-content:center; overflow:hidden; }}
.dont figcaption {{ font-size:12px; color:{INK6}; margin-top:7px; text-align:center; }}
.files td {{ font-size:13px; padding:7px 18px 7px 0; color:{INK8}; }}
.files code {{ color:{INK}; }}
.darkcard {{}}
.foot {{ margin-top:44px; color:{INK4}; font-size:12px; }}
</style></head><body>

<h1>AgentBoot 品牌标识规范</h1>
<p class="lede">设计名「日出提示符 Sunrise Prompt」：日光色圆角方砖上，一道墨色终端提示符 —— 大于号是命令，
下划线是就位的光标。呼应官网的 <code>--sun</code> 品牌锚点色与「一条命令，Agent 就位」的产品叙事；
几何全部由圆角直线构成，可在 CSS/SVG 中重建（DESIGN.md 的品牌符号要求）。</p>

<div class="hero">
  {size(MARK, 148)}
  <div class="txt">
    <h2>主标志 · Primary mark</h2>
    <p>日光渐变方砖（#FFE370 → #FFD84D → #FFC33A）+ 墨色描边（#12251D，4.5/64），
    提示符笔画 6.2/64 圆头圆角。超级椭圆（n=5）砖形，与官网按钮/卡片的圆角语言一致。</p>
  </div>
</div>

<h2>标志家族 · Family</h2>
<div class="grid2">
  <div class="card">{size(MARK, 108)}<span class="cap">彩色（默认）</span></div>
  <div class="card" style="background:#0E1B15">{size(MARK_DARK, 108)}<span class="cap" style="color:{INK4}">暗色背景</span></div>
  <div class="card"><span style="color:{INK}">{size(MARK_MONO, 108)}</span><span class="cap">单色 currentColor</span></div>
  <div class="card">{size(GLYPH, 120)}<span class="cap">裸符号（无砖）</span></div>
</div>

<h2>组合 · Lockups</h2>
<div class="row">
  <div class="card" style="flex:1">{sized(HORIZ, 346, 69)}<span class="cap">横排（主用）</span></div>
  <div class="card" style="flex:1;background:{INK}">{sized(HORIZ_DARK, 346, 69)}<span class="cap" style="color:{INK4}">横排 · 暗底</span></div>
  <div class="card">{sized(STACK, 212, 143)}<span class="cap">竖排</span></div>
</div>

<h2>尺寸阶梯 · Scale</h2>
<div class="card"><div class="sizes">
  <div class="s">{size(MARK, 128)}<span>128</span></div>
  <div class="s">{size(MARK, 64)}<span>64</span></div>
  <div class="s">{size(MARK, 48)}<span>48</span></div>
  <div class="s">{size(MARK, 32)}<span>32</span></div>
  <div class="s">{size(MARK, 24)}<span>24</span></div>
  <div class="s">{size(MARK, 16)}<span>16</span></div>
</div></div>

<h2>净空与最小尺寸 · Clearspace</h2>
<div class="row">{clear}
  <div class="card">{size(MARK.replace('logo-mark', 'favicon-plain') if False else MARK, 16)}<span class="cap">favicon.svg 专版：16px 加粗笔画</span></div>
</div>

<h2>色板 · Palette</h2>
<div class="swatches">{swatches}</div>

<h2>应用示例 · In context</h2>
<div class="row">
  <div>
    <div class="navymock">{size(MARK, 34)}<b style="font-family:'Baloo 2','Segoe UI';font-size:17px">AgentBoot</b>
      <span class="links"><span class="links"><b>安装</b><span>能力</span><span>Agent</span><span>文档</span><span>EN</span></span></span>
    </div>
    <p class="cap" style="margin-top:8px">官网导航条 · 34px 品牌位</p>
    <div class="term" style="margin-top:18px">
      <span class="p">$</span> agentboot<br>
      <span class="dim">检查系统环境与网络…</span><br>
      <span class="ok">✓</span> 选择你想安装的 Agent<br>
      <span class="ok">✓</span> 安装完成，开始创造。
    </div>
    <p class="cap" style="margin-top:8px">终端内的品牌语言：日光提示符 + 行动绿 ✓</p>
  </div>
</div>

<h2>禁例 · Misuse</h2>
<div class="donts">{donts}</div>

<h2>文件清单 · Files</h2>
<table class="files">
<tr><td><code>logo-mark.svg</code></td><td>主标志（彩砖 + 墨描边）</td><td><code>logo-mark-dark.svg</code></td><td>暗色背景版</td></tr>
<tr><td><code>logo-mark-mono.svg</code></td><td>单色版（currentColor）</td><td><code>logo-glyph.svg</code></td><td>裸提示符</td></tr>
<tr><td><code>favicon.svg</code></td><td>站点图标（小尺寸加粗）</td><td><code>wordmark.svg</code></td><td>字标（Baloo 2 Bold 轮廓）</td></tr>
<tr><td><code>logo-horizontal.svg</code></td><td>横排组合</td><td><code>logo-stack.svg</code></td><td>竖排组合</td></tr>
<tr><td><code>banner-zh.svg / banner-en.svg</code></td><td>README / 社交预览 1200×630</td><td><code>favicon.ico</code></td><td>16/32/48 多尺寸</td></tr>
</table>

<p class="foot">AgentBoot Identity · Sunrise Prompt · 2026</p>
</body></html>"""

# favicon-plain: use favicon.svg at 16 in clearspace card
html = html.replace('{size(MARK.replace(\'logo-mark\', \'favicon-plain\') if False else MARK, 16)}',
                    sized(read("favicon.svg"), 16, 16))

with open(os.path.join(BASE, "brand.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("brand.html written", len(html))
PNG = os.path.join(BASE, "png")
render_html(os.path.join(BASE, "brand.html"), os.path.join(PNG, "brand-full.png"),
            1440, 3320, timeout=120)
print("brand rendered")
