"""生成卡片下方的三枚链接按钮 link_<name>_<theme>.svg。

参考项目把按钮做成各自独立的 SVG：GitHub 的 README 通过 <img> 展示 SVG，
SVG 内部既不可点击也不响应 hover，所以「一个链接包一张图」是唯一可靠的做法。
这里沿用这一点，但把像素风图标换成深海配色的字母徽记，并让三张图合起来
恰好等于卡片宽度（间隙画在图片内部），从而左右边缘与卡片、贡献图对齐。

用法：
    python tools/build_links.py
"""

from __future__ import annotations

import html
from pathlib import Path

from build_card import CARD_W, THEMES

ROOT = Path(__file__).resolve().parent.parent

GAP = 14
SLOT_W = CARD_W / 3
BUTTON_W = (CARD_W - 2 * GAP) / 3
HEIGHT = 56
LABEL_FONT = 16

# (文件名, 按钮上的字, 左侧字母徽记, 强调色取自主题中的哪个字段)
LINKS = (
    ("github", "GITHUB", "GH", "key"),
    ("hub", "LEARNING HUB", "LH", "value"),
    ("issues", "ISSUES", "IS", "key"),
)


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def build(theme: str, slot: int) -> str:
    c = THEMES[theme]
    _, label, monogram, accent_key = LINKS[slot]
    accent = c[accent_key]

    # 第 i 张图从第 i 个 1/3 槽位开始；按钮相对槽位内缩 i * GAP/3，
    # 于是三枚按钮之间恰好留出两个 GAP，最左与最右贴齐卡片。
    x = slot * GAP / 3
    badge_r = 15
    badge_cx = x + 12 + badge_r
    mid = HEIGHT / 2

    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" width="{SLOT_W:.3f}px" height="{HEIGHT}px"
     viewBox="0 0 {SLOT_W:.3f} {HEIGHT}"
     font-family="ConsolasFallback,Consolas,Menlo,DejaVu Sans Mono,monospace">
<style>
@font-face {{
  src: local('Consolas'), local('Menlo'), local('DejaVu Sans Mono');
  font-family: 'ConsolasFallback';
  font-display: swap;
  size-adjust: 109%;
}}
text {{white-space: pre;}}
.label {{font-size: {LABEL_FONT}px; font-weight: bold; fill: {c['fg']};}}
.mono {{font-size: 12px; font-weight: bold; fill: {c['bg']};}}
</style>
<rect x="{x + 1:.3f}" y="1" width="{BUTTON_W - 2:.3f}" height="{HEIGHT - 2}" rx="10"
      fill="{c['card']}" stroke="{c['rule']}" stroke-width="1"/>
<rect x="{x + 12:.3f}" y="{HEIGHT - 4}" width="{BUTTON_W - 24:.3f}" height="2"
      fill="{accent}" opacity="0.85"/>
<circle cx="{badge_cx:.3f}" cy="{mid:g}" r="{badge_r}" fill="{accent}"/>
<text x="{badge_cx:.3f}" y="{mid + 4:g}" text-anchor="middle" class="mono">{esc(monogram)}</text>
<text x="{badge_cx + badge_r + 14:.3f}" y="{mid + 5:g}" class="label">{esc(label)}</text>
</svg>
"""


def main() -> None:
    print(f"row: {CARD_W}px = 3 x {BUTTON_W:g}px buttons + 2 x {GAP}px gaps")
    for theme in THEMES:
        for slot, (name, *_) in enumerate(LINKS):
            out = ROOT / f"link_{name}_{theme}.svg"
            out.write_text(build(theme, slot), encoding="utf-8")
            print(f"wrote {out.name} ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
