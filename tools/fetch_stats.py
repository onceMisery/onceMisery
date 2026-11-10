"""把近一年的公开 GitHub 数据写进 cache/stats.json。

与 build_card.py 分开是刻意的：这一半是慢的、受速率限制的网络部分，
失败时不应让主页卡片一起挂掉。build_card.py 在缺少缓存时会退化为占位符，
而本脚本在单个接口失败时会保留上一次成功抓取的数值（见 merge_previous）。

只统计公开数据，不需要 PAT；设置 GITHUB_TOKEN 可以获得更高的速率上限
（GitHub Actions 内置的 token 就够用）。

口径说明：
- PR 数量用 GitHub Search 的 total_count，限定 author + type:pr + created 区间；
- "活跃仓库" 指 pushed_at 落在最近 365 天内的公开仓库；
- stars 只累加本人自有（非 fork）仓库，避免把上游项目的星重复算进来；
- 不统计 commit 总数。fork 会继承上游提交历史，Search API 的
  author: 会把这些提交重复计入，得到的数字没有意义。

用法：
    python tools/fetch_stats.py
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATS_OUT = ROOT / "cache" / "stats.json"

LOGIN = os.environ.get("GH_LOGIN", "onceMisery")
WINDOW_DAYS = 365
BASE = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN")


def get(path: str, params: dict | None = None) -> dict | list:
    url = BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": f"profile-card/{LOGIN}",
        "Accept": "application/vnd.github+json",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def search_count(query: str) -> int:
    return int(get("/search/issues", {"q": query, "per_page": 1})["total_count"])


def merge_previous(stats: dict) -> dict:
    """接口失败时沿用上次成功的值，避免卡片某一天突然出现 `--`。"""
    if not STATS_OUT.exists():
        return stats
    try:
        prev = json.loads(STATS_OUT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return stats
    for key, value in stats.items():
        if value is None and key in prev:
            stats[key] = prev[key]
    return stats


def main() -> None:
    now = datetime.now(timezone.utc)
    since = (now - timedelta(days=WINDOW_DAYS)).date().isoformat()
    window = f"{since} .. {now.date().isoformat()}"
    print(f"fetching {LOGIN} | window {window}")

    stats: dict = {
        "updated": now.isoformat(timespec="seconds"),
        "window": window,
        "login": LOGIN,
    }

    try:
        user = get(f"/users/{LOGIN}")
        stats["repos"] = user["public_repos"]
        stats["followers"] = user["followers"]
    except Exception as exc:  # noqa: BLE001 - 单个接口失败不应中断整次刷新
        print(f"  ! user endpoint: {exc}")
        stats.update({"repos": None, "followers": None})

    try:
        repos = get(f"/users/{LOGIN}/repos", {"per_page": 100, "type": "owner"})
        cutoff = now - timedelta(days=WINDOW_DAYS)
        active = 0
        for repo in repos:
            pushed = datetime.fromisoformat(repo["pushed_at"].replace("Z", "+00:00"))
            if pushed >= cutoff:
                active += 1
        stats["active_repos"] = active
        stats["stars"] = sum(r["stargazers_count"] for r in repos if not r["fork"])
    except Exception as exc:  # noqa: BLE001
        print(f"  ! repos endpoint: {exc}")
        stats.update({"active_repos": None, "stars": None})

    prefix = f"author:{LOGIN} type:pr created:>={since}"
    queries = {
        "prs": prefix,
        "merged": prefix + " is:merged",
        "apache_prs": prefix + " org:apache",
        "dbx_prs": prefix + " repo:t8y2/dbx",
    }
    for key, query in queries.items():
        try:
            stats[key] = search_count(query)
        except Exception as exc:  # noqa: BLE001
            print(f"  ! search {key}: {exc}")
            stats[key] = None

    stats = merge_previous(stats)
    STATS_OUT.parent.mkdir(exist_ok=True)
    STATS_OUT.write_text(json.dumps(stats, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(stats, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
