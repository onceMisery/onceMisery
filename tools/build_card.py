"""生成 neofetch 风格的主页卡片 dark_mode.svg / light_mode.svg。

参考项目的做法是把「肖像 ASCII art + 终端信息面板」做成一张主题感知的 SVG。
这里保留同样的骨架，但换成自己的东西：

- 左侧是用户提供的头像经 tools/build_pixels.py 降采样后的 44x44 像素画，
  硬边色块、有限色阶，与参考项目的像素精灵同一路数；
  像素数据存在 assets/avatar-pixels.json，所以这里不需要浏览器或图像库；
- 右侧是纯 ASCII 的终端面板，数值来自 cache/stats.json；
- 调色板取自头像本身：深板岩灰 + 青蓝水花 + 白色泡沫。
  CJK 字符在等宽字体里是双宽的，会破坏点线对齐，
  所以卡片内一律使用 ASCII，中文叙述全部放在 README 正文里。

用法：
    python tools/build_card.py
"""

from __future__ import annotations

import base64
import html
import json
import mimetypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AVATAR = ROOT / "assets" / "avatar.jpg"
PIXELS = ROOT / "assets" / "avatar-pixels.json"
STATS = ROOT / "cache" / "stats.json"

CARD_W = 1000
CARD_H = 460
# 左侧像素画方框：直角、硬边，刻意为之（圆形照片会破坏像素感）
ART_X, ART_Y, ART_SIZE = 38, 100, 240
PANEL_X = 320
PANEL_COLS = 30           # 键 + 点线引导符占的字符数
FONT = 15
LINE_H = 23
FIRST_Y = 48

# 头像取色：深板岩灰底、青蓝水花、白色泡沫。
THEMES = {
    "dark": {
        "bg": "#0f1b22", "bg2": "#16313d", "card": "#12232c",
        "fg": "#dceff5", "key": "#48d2e8", "value": "#a9e2f0",
        "dot": "#335663", "rule": "#2a4d5b", "ring": "#48d2e8",
        "wave": "#1d4a5b", "prompt": "#48d2e8", "caption": "#4b8296",
    },
    "light": {
        "bg": "#eef8fb", "bg2": "#d8eef5", "card": "#f7fcfe",
        "fg": "#17323d", "key": "#0b7fa3", "value": "#155e75",
        "dot": "#a8cad6", "rule": "#c6e3ec", "ring": "#0b90b5",
        "wave": "#c4e6ef", "prompt": "#0b7fa3", "caption": "#5a8a9b",
    },
}

TITLE = "onceMisery@deep-ocean"


def esc(text: str) -> str:
    return html.escape(str(text), quote=False)


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def shown(value) -> str:
    """数值缺失时退化成 `--`，绝不编造。"""
    if value is None:
        return "--"
    return f"{value:,}" if isinstance(value, int) else str(value)


def rows(st: dict) -> list[tuple]:
    # 刻意不设 Uptime：账号注册时间不是「这一年做了什么」，卡片只放有效信息。
    return [
        ("title", TITLE),
        ("rule", "-" * 60),
        ("kv", ("OS", "Linux / macOS / Windows")),
        ("kv", ("Host", "Shanghai, China")),
        ("kv", ("Kernel", "Backend / Distributed / OSS")),
        ("kv", ("Shell", "Java, Rust, TypeScript, Python")),
        ("kv", ("Editor", "VS Code, Cursor, Zed")),
        ("kv", ("Motto", "Make a little progress every day.")),
        ("blank", ""),
        ("section", "- Last 12 Months"),
        ("kv", ("PRs", f"{shown(st.get('prs'))}   {{ merged {shown(st.get('merged'))} }}")),
        ("kv", ("Repos", f"{shown(st.get('active_repos'))} active / {shown(st.get('repos'))} public")),
        ("kv", ("Top.Repo", f"t8y2/dbx ({shown(st.get('dbx_prs'))} PRs)")),
        ("kv", ("Apache", f"{shown(st.get('apache_prs'))} PRs  seatunnel/pulsar/dubbo")),
        ("kv", ("Stars", f"{shown(st.get('stars'))}  |  Followers {shown(st.get('followers'))}")),
        ("blank", ""),
        ("prompt", "> "),
    ]


def render_line(kind: str, payload, y: int) -> str:
    if kind == "title":
        return f'<text x="{PANEL_X}" y="{y}" class="title">{esc(payload)}</text>'
    if kind in ("rule", "section"):
        return f'<text x="{PANEL_X}" y="{y}" class="{kind}">{esc(payload)}</text>'
    if kind == "blank":
        return ""
    if kind == "prompt":
        # calcMode="discrete" 让光标像真终端一样硬闪，而不是淡入淡出。
        return (
            f'<text x="{PANEL_X}" y="{y}" class="prompt">{esc(payload)}'
            f'<tspan class="cursor">&#9608;'
            f'<animate attributeName="opacity" values="1;0" dur="1.06s" '
            f'calcMode="discrete" repeatCount="indefinite"/>'
            f'</tspan></text>'
        )
    key, value = payload
    dots = "." * max(2, PANEL_COLS - len(key) - 1)
    return (
        f'<text x="{PANEL_X}" y="{y}">'
        f'<tspan class="key">{esc(key)}</tspan>'
        f'<tspan class="dot"> {esc(dots)} </tspan>'
        f'<tspan class="value">{esc(value)}</tspan>'
        f'</text>'
    )


def rle(row: list[int]) -> list[tuple[int, int, int]]:
    """合并一行里连续同色的格子，减少 SVG 节点数。"""
    runs, start, prev = [], 0, row[0]
    for x in range(1, len(row)):
        if row[x] != prev:
            runs.append((start, x - start, prev))
            start, prev = x, row[x]
    runs.append((start, len(row) - start, prev))
    return runs


def pixel_art(c: dict) -> str:
    """用 assets/avatar-pixels.json 渲染硬边像素画；缺失时回退成原图圆形头像。"""
    data = load_json(PIXELS)
    if data.get("rows") and data.get("palette"):
        w, h = data["w"], data["h"]
        palette, grid = data["palette"], data["rows"]
        scale = ART_SIZE / w
        cells = "\n".join(
            f'<rect x="{x}" y="{y}" width="{length}" height="1" fill="{palette[idx]}"/>'
            for y, row in enumerate(grid)
            for x, length, idx in rle(row)
        )
        art = (
            f'<g transform="translate({ART_X},{ART_Y}) scale({scale:.6f})" '
            f'shape-rendering="crispEdges">{cells}</g>'
        )
        frame = (
            f'<rect x="{ART_X - 5}" y="{ART_Y - 5}" width="{ART_SIZE + 10}" '
            f'height="{ART_SIZE + 10}" fill="none" stroke="{c["ring"]}" stroke-width="2"/>'
            f'<rect x="{ART_X - 10}" y="{ART_Y - 10}" width="{ART_SIZE + 20}" '
            f'height="{ART_SIZE + 20}" fill="none" stroke="{c["rule"]}" '
            f'stroke-width="1" stroke-dasharray="3 5"/>'
        )
        return (
            f'<rect x="{ART_X}" y="{ART_Y}" width="{ART_SIZE}" height="{ART_SIZE}" '
            f'fill="{c["bg"]}"/>{art}{frame}'
        )

    # 素材丢失时的兜底：至少不让整张卡片变成空白。
    if AVATAR.exists():
        mime = mimetypes.guess_type(AVATAR.name)[0] or "image/jpeg"
        uri = "data:" + mime + ";base64," + base64.b64encode(AVATAR.read_bytes()).decode("ascii")
        cx, cy, r = ART_X + ART_SIZE / 2, ART_Y + ART_SIZE / 2, ART_SIZE / 2
        return (
            f'<clipPath id="face"><circle cx="{cx:g}" cy="{cy:g}" r="{r:g}"/></clipPath>'
            f'<image x="{ART_X}" y="{ART_Y}" width="{ART_SIZE}" height="{ART_SIZE}" '
            f'preserveAspectRatio="xMidYMid slice" clip-path="url(#face)" '
            f'href="{uri}"/>'
            f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" fill="none" '
            f'stroke="{c["ring"]}" stroke-width="2"/>'
        )
    r = ART_SIZE / 2
    return (
        f'<rect x="{ART_X}" y="{ART_Y}" width="{ART_SIZE}" height="{ART_SIZE}" '
        f'fill="{c["bg2"]}" stroke="{c["ring"]}" stroke-width="2"/>'
        f'<text x="{ART_X + r}" y="{ART_Y + r}" text-anchor="middle" '
        f'class="caption">NO AVATAR</text>'
    )


def build(theme: str) -> str:
    c = THEMES[theme]
    st = load_json(STATS)

    lines = "\n".join(
        out
        for i, (kind, payload) in enumerate(rows(st))
        if (out := render_line(kind, payload, FIRST_Y + i * LINE_H))
    )

    waves = "\n".join(
        f'<path d="M0 {360 + i * 26} Q 90 {340 + i * 26}, 180 {360 + i * 26} '
        f'T 360 {360 + i * 26}" fill="none" stroke="{c["wave"]}" '
        f'stroke-width="1.2" opacity="{0.55 - i * 0.12:.2f}"/>'
        for i in range(3)
    )

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" width="{CARD_W}px" height="{CARD_H}px"
     viewBox="0 0 {CARD_W} {CARD_H}"
     font-family="ConsolasFallback,Consolas,Menlo,DejaVu Sans Mono,monospace">
<title>onceMisery - GitHub profile card</title>
<defs>
  <linearGradient id="sea" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{c['bg']}"/>
    <stop offset="1" stop-color="{c['bg2']}"/>
  </linearGradient>
</defs>
<style>
@font-face {{
  src: local('Consolas'), local('Menlo'), local('DejaVu Sans Mono');
  font-family: 'ConsolasFallback';
  font-display: swap;
  size-adjust: 109%;
}}
text {{font-size: {FONT}px; white-space: pre;}}
.key {{fill: {c['key']}; font-weight: bold;}}
.value {{fill: {c['value']};}}
.dot {{fill: {c['dot']};}}
.title {{fill: {c['key']}; font-weight: bold; font-size: 17px;}}
.section {{fill: {c['key']}; font-weight: bold;}}
.rule {{fill: {c['rule']};}}
.prompt {{fill: {c['prompt']};}}
.cursor {{fill: {c['value']};}}
.caption {{fill: {c['caption']}; font-size: 11px; letter-spacing: 2px;}}
</style>
<rect width="{CARD_W}" height="{CARD_H}" rx="16" fill="url(#sea)"/>
<rect x="1" y="1" width="{CARD_W - 2}" height="{CARD_H - 2}" rx="16"
      fill="none" stroke="{c['rule']}" stroke-width="1"/>
{waves}
{pixel_art(c)}
<text x="{ART_X + ART_SIZE / 2}" y="{ART_Y + ART_SIZE + 32}" text-anchor="middle"
      class="caption">// TIDE &amp; NEURONS //</text>
<line x1="{PANEL_X - 24}" y1="30" x2="{PANEL_X - 24}" y2="{CARD_H - 30}"
      stroke="{c['rule']}" stroke-width="1"/>
{lines}
</svg>
"""


def main() -> None:
    for name in THEMES:
        out = ROOT / f"{name}_mode.svg"
        out.write_text(build(name), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
