"""把 assets/avatar.jpg 转成 CRT 半色调点阵数据。

风格参照 yetone 的 profile README：荧光屏里的人像不是彩色实心方块，而是
「亮部连成水平条块 + 暗部细密网点」，整幅再叠水平扫描线与辉光。

流程：
  1. 借本机 Chrome/Edge 的 canvas getImageData 解码 JPEG（data URI 内联，
     避免 canvas 跨域污染，--dump-dom 把像素数组吐回来）；
  2. 转灰度、按 2% / 98% 分位做对比度拉伸；
  3. 用 4x4 Bayer 有序抖动打散量化边界，得到 4 档亮度等级；
  4. 写 assets/avatar-pixels.json，并另存一份可单独引用的
     assets/avatar-pixel.svg。

等级 0/1/2/3 分别渲染成 空 / 小点 / 大点 / 满格，相邻满格自然连成水平条块，
小点自然形成网点 —— 这正是参考图的质感来源。

**这是一次性的素材加工脚本，只在换头像时本地跑一次。** 像素等级数据会提交
进仓库，所以 GitHub Actions 里的 build_card.py 只读 JSON，不需要浏览器或图像库。

用法：
    python tools/build_pixels.py            # 自动找 Chrome / Edge
    CHROME_BIN=/path/to/chrome python tools/build_pixels.py
"""

from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import tempfile
from html import unescape
from pathlib import Path

from build_card import CRT_BG, CRT_COLORS, render_halftone, scanlines

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "avatar.jpg"
OUT = ROOT / "assets" / "avatar-pixels.json"
SVG_OUT = ROOT / "assets" / "avatar-pixel.svg"

GRID = 64             # 64x64 的点阵格，比实心像素画更细，才有「细密网点」
DITHER = 0.30         # Bayer 抖动强度，打散色阶边界
CUTS = (0.22, 0.46, 0.80)   # 亮度分级阈值；第三档调高，避免白雾过曝连成整片

BAYER = (
    (0, 8, 2, 10),
    (12, 4, 14, 6),
    (3, 11, 1, 9),
    (15, 7, 13, 5),
)


def find_chrome() -> str:
    env = os.environ.get("CHROME_BIN")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "chrome", "chromium", "msedge"):
        hit = shutil.which(name)
        if hit:
            return hit
    for p in (
        "C:/Program Files/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
        "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
    ):
        if Path(p).exists():
            return p
    raise SystemExit("找不到 Chrome/Edge，请设置 CHROME_BIN 指向浏览器可执行文件")


def page_source() -> str:
    uri = "data:image/jpeg;base64," + base64.b64encode(SRC.read_bytes()).decode("ascii")
    return f"""<!doctype html><meta charset="utf-8"><body>
<img id="src" src="{uri}">
<canvas id="cv" width="{GRID}" height="{GRID}"></canvas>
<pre id="out"></pre>
<script>
const img = document.getElementById('src');
const cv = document.getElementById('cv');
const ctx = cv.getContext('2d', {{ willReadFrequently: true }});
function emit() {{
  ctx.imageSmoothingEnabled = false;
  ctx.drawImage(img, 0, 0, {GRID}, {GRID});
  const d = ctx.getImageData(0, 0, {GRID}, {GRID}).data;
  const px = [];
  for (let i = 0; i < d.length; i += 4) px.push([d[i], d[i+1], d[i+2]]);
  document.getElementById('out').textContent = JSON.stringify({{
    width: img.naturalWidth, height: img.naturalHeight, pixels: px
  }});
}}
if (img.complete) emit(); else img.onload = emit;
</script></body>"""


def luma(rgb) -> float:
    r, g, b = rgb
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255.0


def levels_from(pixels: list) -> list[list[int]]:
    values = sorted(luma(p) for p in pixels)
    lo = values[int(len(values) * 0.02)]
    hi = values[int(len(values) * 0.98)]
    span = max(hi - lo, 1e-6)

    out = []
    for y in range(GRID):
        row = []
        for x in range(GRID):
            norm = min(1.0, max(0.0, (luma(pixels[y * GRID + x]) - lo) / span))
            threshold = (BAYER[y % 4][x % 4] + 0.5) / 16.0
            q = norm + (threshold - 0.5) * DITHER
            row.append(sum(q >= cut for cut in CUTS))  # 0..3
        out.append(row)
    return out


def write_svg(levels: list[list[int]]) -> None:
    """另存一份可单独引用的 CRT 半色调头像，与卡片内的渲染完全一致。"""
    SVG_OUT.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="440" '
        f'viewBox="0 0 {GRID} {GRID}" shape-rendering="crispEdges">\n'
        f'<rect width="{GRID}" height="{GRID}" fill="{CRT_BG}"/>\n'
        f'{render_halftone(levels, CRT_COLORS, GRID, GRID)}\n'
        f'{scanlines(GRID, GRID)}\n</svg>\n',
        encoding="utf-8",
    )


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"缺少头像原图：{SRC}")
    chrome = find_chrome()
    print(f"browser : {chrome}")

    with tempfile.TemporaryDirectory() as tmp:
        html = Path(tmp) / "pixelize.html"
        html.write_text(page_source(), encoding="utf-8")
        proc = subprocess.run(
            [chrome, "--headless", "--no-sandbox", "--disable-gpu",
             "--virtual-time-budget=5000", "--dump-dom", html.as_uri()],
            capture_output=True, text=True, timeout=90,
        )
        dom = proc.stdout
    match = re.search(r'<pre id="out">(.*?)</pre>', dom, re.S)
    if not match or not match.group(1).strip():
        raise SystemExit("未能从浏览器取回像素数据（检查 --dump-dom 输出）")
    data = json.loads(unescape(match.group(1)))
    print(f"source  : {data['width']}x{data['height']} -> {GRID}x{GRID} halftone cells")

    levels = levels_from(data["pixels"])
    counts = [sum(row.count(i) for row in levels) for i in range(4)]

    OUT.write_text(
        json.dumps({"source": SRC.name, "mode": "crt-halftone",
                    "w": GRID, "h": GRID, "levels": levels}, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    write_svg(levels)
    print(f"levels  : empty={counts[0]} dot={counts[1]} big={counts[2]} solid={counts[3]}")
    print(f"wrote   : {OUT.name} ({OUT.stat().st_size:,} bytes)")
    print(f"wrote   : {SVG_OUT.name} ({SVG_OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
