# -*- coding: utf-8 -*-
"""Shape 'AgentBoot' with HarfBuzz, export combined SVG path."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


def shape_to_path(font_path, text, size=100.0, tracking=0.0, pair_fix=None):
    """Return (path_d, width, cap_height, x_height, ascender, descender).
    pair_fix: {(left_char, right_char): extra_advance_in_font_units}"""
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    upem = face.upem
    font.scale = (upem, upem)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, {"kern": True, "liga": True})

    infos, positions = buf.glyph_infos, buf.glyph_positions
    tt = TTFont(font_path)
    glyph_set = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    glyph_chars = [text[info.cluster] if info.cluster < len(text) else "" for info in infos]

    s = size / upem
    x = 0.0
    parts = []
    for i, (info, pos) in enumerate(zip(infos, positions)):
        gname = order[info.codepoint]
        pen = SVGPathPen(glyph_set)
        tpen = TransformPen(pen, Transform(s, 0, 0, -s, (x + pos.x_offset) * s, -pos.y_offset * s))
        glyph_set[gname].draw(tpen)
        d = pen.getCommands()
        if d:
            parts.append(d)
        adv = pos.x_advance
        if pair_fix and i + 1 < len(infos):
            k = (glyph_chars[i], glyph_chars[i + 1])
            if k in pair_fix:
                adv += pair_fix[k]
        x += adv + tracking * upem
    width = x * s

    cap = tt["OS/2"].sCapHeight * s if hasattr(tt["OS/2"], "sCapHeight") else size * 0.7
    xh = tt["OS/2"].sxHeight * s if hasattr(tt["OS/2"], "sxHeight") else size * 0.5
    asc = tt["hhea"].ascender * s
    desc = tt["hhea"].descender * s
    return " ".join(parts), width, cap, xh, asc, desc


if __name__ == "__main__":
    for fp in ["fonts/Nunito-800.ttf", "fonts/Baloo2-700.ttf"]:
        d, w, cap, xh, asc, desc = shape_to_path(fp, "AgentBoot", 100)
        print(f"{fp}: width={w:.1f} cap={cap:.1f} xh={xh:.1f} pathlen={len(d)}")
