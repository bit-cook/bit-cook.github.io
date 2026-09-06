"""Shared helpers: SVG arc geometry + headless Edge renderer."""
import math
import os
import subprocess

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PROFILE = os.path.join(os.environ.get("TEMP", "/tmp"), "edge-headless-profile")
BASE = r"C:\Users\Shaun\ZCodeProject\agentboot-logo"

INK = "#12251D"
INK8 = "#294238"
INK6 = "#5B7067"
INK4 = "#91A198"
PAPER = "#FFFDF5"
SUN = "#FFD84D"
GREEN = "#137A52"
GREEN_D = "#0D5E3E"
CORAL = "#FF7A59"


def pt(cx, cy, r, deg):
    """Point on circle; math convention (0=east, CCW+, y-up) -> screen coords."""
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy - r * math.sin(a))


def arc(cx, cy, r, a_start, a_end):
    """SVG path for arc from a_start to a_end (degrees, increasing, may exceed 360).
    Screen-CCW (sweep 0), auto-split into <=180 deg segments."""
    d = []
    a = a_start
    while a < a_end - 1e-6:
        b = min(a + 180, a_end)
        x1, y1 = pt(cx, cy, r, a)
        x2, y2 = pt(cx, cy, r, b)
        d.append(f"M {x1:.2f} {y1:.2f} A {r:.2f} {r:.2f} 0 0 0 {x2:.2f} {y2:.2f}")
        a = b
    return " ".join(d)


def render_html(html_path, png_path, w, h, timeout=60):
    import tempfile, time
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    out = os.path.abspath(png_path)
    before = os.path.getmtime(out) if os.path.exists(out) else 0
    with tempfile.TemporaryDirectory(prefix="edge-prof-", ignore_cleanup_errors=True) as prof:
        cmd = [
            EDGE, "--edge-skip-compat-layer-relaunch", "--headless=new",
            "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", "--force-color-profile=srgb",
            "--no-first-run", "--no-default-browser-check",
            "--disable-extensions", f"--user-data-dir={prof}",
            f"--screenshot={out}", f"--window-size={w},{h}", url,
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=timeout)
    for _ in range(40):
        if os.path.exists(out) and os.path.getmtime(out) > before:
            return
        time.sleep(0.25)
    raise RuntimeError(f"Edge did not write {out}")


def downscale(src_png, out_png, sizes):
    from PIL import Image
    im = Image.open(src_png).convert("RGBA")
    for s in sizes:
        im.resize((s, s), Image.LANCZOS).save(out_png % s)
