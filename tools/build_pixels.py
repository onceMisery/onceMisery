"""把 assets/avatar.jpg 降采样成像素风色块数据。

参考项目的卡片左侧是 ASCII art 肖像，链接按钮是像素精灵 —— 头像也走同一条
复古颗粒路线：先把图缩到 GRID x GRID，再把每个像素放大成一个硬边方块。

为什么需要浏览器：本仓库不引入 Pillow / ImageMagick 之类的图像依赖，
而 JPEG 解码最省事的办法是让本机 Chrome/Edge 用 canvas 的 getImageData 读一遍。
图片以 data URI 内联进 HTML（同源，canvas 不会被跨域污染），headless 的
--dump-dom 再把像素数组吐回来。

**这是一次性的素材加工脚本，只在换头像时本地跑一次。** 产物
assets/avatar-pixels.json 会提交进仓库，所以 GitHub Actions 里的
build_card.py 只需要读 JSON，既不用浏览器也不用解码 JPEG。

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
import sys
import tempfile
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "avatar.jpg"
OUT = ROOT / "assets" / "avatar-pixels.json"
SVG_OUT = ROOT / "assets" / "avatar-pixel.svg"

GRID = 44          # 44x44 个色块，放大后就是明显的像素画
QUANT = 12         # 每通道量化步长：压到有限色阶，又不至于让灰色背景偏紫偏绿


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


def quantize(v: int) -> int:
    return min(255, max(0, round(v / QUANT) * QUANT))


def hex_color(rgb) -> str:
    return "#%02x%02x%02x" % tuple(quantize(v) for v in rgb)


def rle(row: list[int]) -> list[tuple[int, int, int]]:
    """把一行里连续同色的格子合成 (起点, 长度, 色号)，减少 SVG 节点数。"""
    runs, start, prev = [], 0, row[0]
    for x in range(1, len(row)):
        if row[x] != prev:
            runs.append((start, x - start, prev))
            start, prev = x, row[x]
    runs.append((start, len(row) - start, prev))
    return runs


def write_svg(rows: list[list[int]], palette: list[str]) -> None:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="440" height="440" '
        f'viewBox="0 0 {GRID} {GRID}" shape-rendering="crispEdges">',
        f'<rect width="{GRID}" height="{GRID}" fill="#0f1b22"/>',
    ]
    for y, row in enumerate(rows):
        for x, length, idx in rle(row):
            parts.append(
                f'<rect x="{x}" y="{y}" width="{length}" height="1" fill="{palette[idx]}"/>'
            )
    parts.append("</svg>")
    SVG_OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")


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
    print(f"source  : {data['width']}x{data['height']} -> {GRID}x{GRID} pixels")

    palette: list[str] = []
    lookup: dict[str, int] = {}
    rows: list[list[int]] = []
    for y in range(GRID):
        row = []
        for x in range(GRID):
            color = hex_color(data["pixels"][y * GRID + x])
            if color not in lookup:
                lookup[color] = len(palette)
                palette.append(color)
            row.append(lookup[color])
        rows.append(row)

    OUT.write_text(
        json.dumps({"source": SRC.name, "w": GRID, "h": GRID,
                    "palette": palette, "rows": rows}, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    write_svg(rows, palette)
    runs = sum(len(rle(row)) for row in rows)
    print(f"palette : {len(palette)} colors | {GRID*GRID} cells -> {runs} SVG rects")
    print(f"wrote   : {OUT.name} ({OUT.stat().st_size:,} bytes)")
    print(f"wrote   : {SVG_OUT.name} ({SVG_OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
