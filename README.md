<div align="center">

<a href="https://github.com/onceMisery">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/main/dark_mode.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/main/light_mode.svg">
    <img alt="onceMisery · 后端开发 / 分布式系统 / Apache 开源贡献者" src="https://raw.githubusercontent.com/onceMisery/onceMisery/main/light_mode.svg" width="100%">
  </picture>
</a>

<p align="left"><a href="https://github.com/onceMisery"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/main/link_github_dark.svg"><img alt="GitHub" width="33.3%" src="https://raw.githubusercontent.com/onceMisery/onceMisery/main/link_github_light.svg"></picture></a><a href="https://oncemisery.github.io/learning-hub"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/main/link_hub_dark.svg"><img alt="Learning Hub" width="33.3%" src="https://raw.githubusercontent.com/onceMisery/onceMisery/main/link_hub_light.svg"></picture></a><a href="https://github.com/onceMisery/onceMisery/issues"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/main/link_issues_dark.svg"><img alt="Issues" width="33.3%" src="https://raw.githubusercontent.com/onceMisery/onceMisery/main/link_issues_light.svg"></picture></a></p>

<p>
  <img src="https://github.com/onceMisery/onceMisery/actions/workflows/profile-card.yml/badge.svg" alt="Profile Card workflow" />
  <img src="https://github.com/onceMisery/onceMisery/actions/workflows/main.yml/badge.svg" alt="Snake workflow" />
  <img src="https://komarev.com/ghpvc/?username=onceMisery&label=Profile%20views&color=0e75b6&style=flat" alt="Profile views" />
</p>

> **Make a little progress every day.** —— 像潮汐一样，不必一次涨满，但从不退回去。

</div>

---

## 🧭 目录

| 章节 | 说明 |
| --- | --- |
| [关于我](#about) | 是谁、在哪、这一年把时间花在了哪 |
| [过去一年](#year) | 2025.11 — 2026.11 的真实提交与 PR 复盘 |
| [技术栈](#stack) | 按近一年产出反推的语言与中间件 |
| [活跃项目](#projects) | 主要战场与在做的具体事情 |
| [贡献图](#snake) | 每日自动生成的贡献蛇动画 |
| [仓库结构](#structure) | 文件、像素头像素材与生成脚本 |
| [自动化](#workflow) | 两条工作流与数据口径 |
| [快速开始](#quickstart) | 复刻这份主页到自己账号 |
| [常见问题](#faq) | 卡片不刷新、换头像、图片不显示等 |
| [贡献指南](#contributing) | 纠错与改进 |
| [联系方式](#contact) | GitHub、邮箱与其他渠道 |

---

<a id="about"></a>

## 🌊 关于我

常驻中国上海，写 Java 出身。过去一年把大部分时间交给了 **dbx** —— 一个 Rust + Java + TypeScript 的跨平台数据库客户端：从 SQL 变量替换、JDBC Agent 连接恢复，到 Kafka / Pulsar / ZooKeeper 管理、CSV / XLSX 流式导出、结构化错误契约和插件体系，都在同一个仓库里反复打磨。近一年向 [t8y2/dbx](https://github.com/t8y2/dbx) 提交了 **54 个 PR、合并 50 个**。

另一条线是 Apache 上游：向 SeaTunnel、Pulsar、Dubbo 提交 PR 与 PIP；再一条线是自己的 AI Agent 实验场 —— [seahorse-agent](https://github.com/onceMisery/seahorse-agent)（企业级 RAG / 长期记忆 / 可治理智能体）、[hertz-studio](https://github.com/onceMisery/hertz-studio)（桌面客户端），以及若干 Rust / Python 小项目。

头像是一片浪，[Seahorse](https://github.com/onceMisery/Seahorse) 的副标题写着 *Where neurons meet the tide*，我很喜欢这句话，所以主页用了深海配色：板岩灰作底、青蓝作字、白沫作高光。头像本身被降采样成 **44×44 的硬边像素画**，和卡片右侧的终端面板、下方的像素徽记按钮凑成一套复古颗粒感。信条没变 —— **Make a little progress every day.**

| 维度 | 说明 |
| --- | --- |
| 城市 | 中国上海 |
| 身份 | 后端开发者 / Apache 开源贡献者 |
| 近一年主战场 | dbx 数据库客户端工程化（Rust + Java + TypeScript） |
| 上游开源 | Apache SeaTunnel · Pulsar · Dubbo（PR / PIP） |
| 自己的项目 | seahorse-agent · hertz-studio · Seahorse · learning-hub |
| 正在探索 | AI Agent 记忆引擎、MCP、向量数据库、Rust |
| 可以聊 | Java、JDBC、一致性协议（Raft）、消息中间件、数据库客户端设计 |

---

<a id="year"></a>

## 🗓️ 过去一年：2025.11 — 2026.11

下方数字是本页写作时的**快照（截至 2026-11-10）**，只统计公开数据；顶部卡片里的数值由工作流每日自动刷新。

| 指标 | 数值 | 统计口径 |
| --- | --- | --- |
| Pull Request | **92** 个（合并 **65**，进行中 3） | GitHub Search `author:onceMisery type:pr created:>=2025-11-10` |
| 活跃仓库 | **51** / 95 个公开仓库 | `pushed_at` 落在最近 365 天内 |
| dbx 生态 PR | **67** 个（含 t8y2/dbx 的 54 个、合并 50 个） | dbx / dbx-store / dbx-agents 及其个人 fork |
| Apache 上游 PR | **7** 个（SeaTunnel 4 · Pulsar 2 · Dubbo 1） | `org:apache` |
| 自有仓库 Star | **27**（最高 seahorse-agent，12 ★） | 仅统计非 fork 的 20 个自有仓库 |
| Issue / 讨论 | 10 个 | 含 dubbo#16108、dbx 的 bug 与 feature 反馈 |

> **为什么没有 commit 总数**：fork 会继承上游的提交历史，Search API 的 `author:` 会把这些提交重复计入本人名下，得到的数字没有意义。这里只列可复核的 PR、仓库与 Star。

**这一年的节奏**

| 时段 | 在做什么 |
| --- | --- |
| 2026.02 — 03 | 从 Apache 起步：SeaTunnel MongoDB-CDC NPE 修复与 DaMeng JDBC 单测、Dubbo registry invoker 去重、Pulsar PIP-459（Functions 状态汇总） |
| 2026.06 — 08 | dbx 密集期，两个月 46 个 PR：SQL `@set` 变量替换、ZK / Pulsar / Kafka Agent、DuckDB 子进程、CSV / XLSX 流式导出、后端错误契约、插件与 MCP 配置 |
| 2026.09 — 11 | 收口与自有项目：hertz-studio 的 AI 壁纸 / 桌面歌词 / 局域网一起听、插件市场上架 dbx-store、seahorse-agent 记忆引擎 |

**三条主线（都可点开复核）**

1. **数据库客户端工程化 · dbx** —— [#12495 列元数据可配置](https://github.com/t8y2/dbx/pull/12495)、[#11064 插件浮动窗口](https://github.com/t8y2/dbx/pull/11064)、[#1741 流式导出](https://github.com/t8y2/dbx/pull/1741)、[#1968 连接超时恢复](https://github.com/t8y2/dbx/pull/1968)、[#1834 connect PIP 文档](https://github.com/t8y2/dbx/pull/1834)。从查询正确性一路做到性能、协议与扩展机制。
2. **Apache 上游贡献** —— [SeaTunnel#10825 Pulsar 多表读取](https://github.com/apache/seatunnel/pull/10825)、[SeaTunnel#10477 MongoDB-CDC NPE](https://github.com/apache/seatunnel/pull/10477)、[Pulsar#25299 PIP-459](https://github.com/apache/pulsar/pull/25299)、[Dubbo#16133 registry 去重](https://github.com/apache/dubbo/pull/16133)；另有 [eec#475 线程安全修复](https://github.com/wangguanquan/eec/pull/475) 这类基础库健壮性补丁。
3. **AI Agent 与桌面端** —— [seahorse-agent#1 记忆引擎接入 chat pipeline](https://github.com/onceMisery/seahorse-agent/pull/1)、[hertz-studio 桌面壁纸与歌词舞台](https://github.com/onceMisery/hertz-studio/pull/5)、[插件上架 dbx-store](https://github.com/t8y2/dbx-store/pull/436)、[ragent#29 MQ 换 Pulsar + 记忆系统增强](https://github.com/nageoffer/ragent/pull/29)。

---

<a id="stack"></a>

## 🛠️ 技术栈

下表按**近一年实际提交与 PR 内容**反推，不按"会过"来写。

| 分类 | 近一年实际用到 | 依据 |
| --- | --- | --- |
| 语言 | Java · Rust · TypeScript / JavaScript · Python · SQL | 活跃自有仓库中 Java 7 / Rust 5 / JS 3 / TS 1 / Python 4；dbx 本身横跨 Rust + Java + TS |
| 数据访问 | JDBC、MySQL、PostgreSQL、SQL Server、DaMeng、Doris、DuckDB、MongoDB、Redis | dbx 的 Agent / 连接 / 导出 PR、SeaTunnel DaMeng JDBC 单测 |
| 消息与协调 | Apache Pulsar · Kafka · ZooKeeper · Apache Dubbo | Pulsar 多表 source 与 PIP-459、dbx 的 MQ 管理、Dubbo registry 修复 |
| 数据集成 | Apache SeaTunnel · CSV / XLSX 流式导出 | SeaTunnel Connector-V2 PR、dbx 导出性能系列 PR |
| AI / Agent | RAG、长期记忆、MCP、向量数据库、Spring AI（探索中） | seahorse-agent、dbx 的 MCP 配置、hertz-studio 的 AI 壁纸 |
| 工程基建 | Maven、GitHub Actions、Docker、Linux | 两条工作流、eec / fastjson2 等 Java 生态修复 |

> `go-study`、`python-study` 等是早期学习仓库，近一年无活跃提交，因此 Go 不列入主栈。

<details>
<summary><b>展开：完整徽章墙（含长期积累）</b></summary>

**近一年主力**

<p align="left">
  <img src="https://img.shields.io/badge/Java-%23ED8B00.svg?style=for-the-badge&logo=openjdk&logoColor=white" />
  <img src="https://img.shields.io/badge/Rust-%23000000.svg?style=for-the-badge&logo=rust&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20SeaTunnel-005CB9?style=for-the-badge&logo=apache&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20Pulsar-188FFF?style=for-the-badge&logo=apache-pulsar&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20Dubbo-FF6600?style=for-the-badge&logo=apache-dubbo&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apache-kafka&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
</p>

**长期积累 / 了解**

<p align="left">
  <img src="https://img.shields.io/badge/Spring-%236DB33F.svg?style=for-the-badge&logo=spring&logoColor=white" />
  <img src="https://img.shields.io/badge/MyBatis--Plus-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Maven-C71A36?style=for-the-badge&logo=apache-maven&logoColor=white" />
  <img src="https://img.shields.io/badge/Go-%2300ADD8.svg?style=for-the-badge&logo=go&logoColor=white" />
  <img src="https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20RocketMQ-D42027?style=for-the-badge&logo=apache-rocketmq&logoColor=white" />
  <img src="https://img.shields.io/badge/OceanBase-0067FF?style=for-the-badge&logo=oceanbase&logoColor=white" />
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" />
</p>

</details>

---

<a id="projects"></a>

## 🚢 活跃项目

| 项目 | 角色 | 技术 | 近一年在做什么 |
| --- | --- | --- | --- |
| [t8y2/dbx](https://github.com/t8y2/dbx) | 核心贡献者 | Rust / Java / TypeScript | 54 个 PR：查询、连接恢复、ZK / Pulsar / Kafka Agent、流式导出、插件与 MCP |
| [t8y2/dbx-store](https://github.com/t8y2/dbx-store) · [dbx-agents](https://github.com/t8y2/dbx-agents) | 贡献者 | Java / 插件元数据 | ZooKeeper Agent、hertz-studio 插件上架与版本发布 |
| [apache/seatunnel](https://github.com/apache/seatunnel) · [pulsar](https://github.com/apache/pulsar) · [dubbo](https://github.com/apache/dubbo) | 上游贡献者 | Java | Connector-V2 Pulsar 多表读取、CDC 修复、PIP-459、registry 去重 |
| [onceMisery/seahorse-agent](https://github.com/onceMisery/seahorse-agent) | 作者 | Java | 企业级 RAG / 长期记忆 / 可治理智能体，记忆引擎与 query optimizer（12 ★，本页最高） |
| [onceMisery/hertz-studio](https://github.com/onceMisery/hertz-studio) | 作者 | JavaScript / Rust / 桌面端 | AI 壁纸、桌面歌词舞台、局域网一起听、dbx 插件 |
| [onceMisery/Seahorse](https://github.com/onceMisery/Seahorse) · [rust-study](https://github.com/onceMisery/rust-study) · [NovaHub](https://github.com/onceMisery/NovaHub) | 作者 | Rust | Rust 学习与长期实验 |
| [onceMisery/learning-hub](https://github.com/onceMisery/learning-hub) · [harness-template](https://github.com/onceMisery/harness-template) · [smart-skills](https://github.com/onceMisery/smart-skills) | 作者 | HTML / Python | 知识沉淀、Agent 技能包与工程模板 |

另有 `DocForge`、`api-hub`、`cli-run-ui`、`odoo-java`、`future-partner` 等小型项目，以及 75 个用于阅读源码的 fork（SigNoz、nacos、fastjson2、agentscope-java、deer-flow 等）—— 它们构成了这一年的输入，但没有算进上面的产出数字。

---

<a id="snake"></a>

## 🐍 贡献图动画

由 GitHub Actions 每日生成，并随 GitHub 明暗主题自动切换。

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/output/github-contribution-grid-snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/onceMisery/onceMisery/output/github-contribution-grid-snake.svg">
    <img alt="github contribution grid snake animation" src="https://raw.githubusercontent.com/onceMisery/onceMisery/output/github-contribution-grid-snake.svg">
  </picture>
</div>

<details>
<summary><b>展开：换成星球大战主题</b></summary>

工作流同样会生成 `github-contribution-grid-starwars.svg`，替换上方 `<picture>` 里的地址即可。

```html
<img alt="starwars contribution snake" src="https://raw.githubusercontent.com/onceMisery/onceMisery/output/github-contribution-grid-starwars.svg" />
```

</details>

---

<a id="structure"></a>

## 📦 仓库结构

结构参考了 [ignaciochiappero/ignaciochiappero](https://github.com/ignaciochiappero/ignaciochiappero)：**数据与渲染分离**，卡片是构建产物而不是手写文件，数值由定时任务刷新，主题感知交给 `<picture>`。参考项目左侧是 ASCII art 肖像、按钮是像素精灵，这里把同一套复古像素语言用在了头像本身。

```text
onceMisery/
├── README.md                              # 个人主页展示内容（本文件）
├── dark_mode.svg / light_mode.svg         # 主题感知的 neofetch 风格卡片
├── link_github_*.svg / link_hub_*.svg /
│   └── link_issues_*.svg                  # 三枚链接按钮，各含明暗两套
├── assets/
│   ├── avatar.jpg                         # 头像原图
│   ├── avatar-pixels.json                 # 44x44 像素画数据（有限色阶 + 调色板）
│   └── avatar-pixel.svg                   # 可单独引用的像素风头像
├── cache/
│   └── stats.json                         # 每日刷新的公开统计数据
├── tools/
│   ├── build_pixels.py                    # 头像 → 像素数据（换头像时本地跑一次）
│   ├── fetch_stats.py                     # GitHub REST / Search → cache/stats.json
│   ├── build_card.py                      # 像素数据 + stats → 卡片 SVG
│   └── build_links.py                     # 复用卡片配色 → 链接按钮 SVG
└── .github/workflows/
    ├── profile-card.yml                   # 每日刷新卡片、按钮与统计
    └── main.yml                           # 生成贡献蛇动画 → output 分支

output 分支（由 main.yml 自动写入）:
├── github-contribution-grid-snake.svg
├── github-contribution-grid-snake-dark.svg
└── github-contribution-grid-starwars.svg
```

> `output` 分支由工作流自动推送，请勿手动编辑，下次运行会被覆盖。

---

<a id="workflow"></a>

## ⚙️ 自动化

| 工作流 | 触发 | 做什么 |
| --- | --- | --- |
| `profile-card.yml` | 每天 05:00 UTC、手动、素材或脚本改动时 push | 抓统计 → 重建卡片与按钮 → 提交 `*.svg` 和 `cache/*.json` |
| `main.yml` | 每天 00:00 UTC、手动、push 到 `main` | 用 [Platane/snk](https://github.com/Platane/snk) 生成贡献蛇，推送到 `output` 分支 |

`fetch_stats.py` 只用 Python 标准库，不需要 `pip install`，也不需要 PAT：公开数据即可，内置 `GITHUB_TOKEN` 只是为了提高速率上限。单个接口失败时会沿用上一次成功的值，卡片不会出现 `--` 或整块消失。统计口径见[过去一年](#year)。

**像素数据不参与每日构建**：`build_pixels.py` 借本机 Chrome/Edge 的 canvas 解码 JPEG，属于一次性素材加工，只在换头像时本地运行；产出的 `avatar-pixels.json` 已提交进仓库，所以 Actions 里的 `build_card.py` 既不需要浏览器也不需要图像库。

<details>
<summary><b>展开：卡片配色与像素参数</b></summary>

配色取自头像本身，定义在 `tools/build_card.py` 的 `THEMES` 里。想换成自己的颜色，只改这一处，`build_links.py` 会自动跟着变化。

| 主题 | 背景 | 关键字 | 数值 | 强调 |
| --- | --- | --- | --- | --- |
| dark | `#0f1b22` → `#16313d` | `#48d2e8` | `#a9e2f0` | `#2a4d5b` |
| light | `#eef8fb` → `#d8eef5` | `#0b7fa3` | `#155e75` | `#c6e3ec` |

像素画参数在 `tools/build_pixels.py` 顶部：`GRID = 44`（色块数）、`QUANT = 12`（每通道量化步长，越小越细腻、越大越硬朗）。卡片内的文字刻意全部使用 ASCII：CJK 字符在等宽字体里是双宽的，会破坏点线引导符的对齐；中文叙述都放在 README 正文里。

</details>

---

<a id="quickstart"></a>

## 🚀 快速开始

```bash
# 1. 克隆到自己的同名仓库（<username>/<username>）
git clone https://github.com/onceMisery/onceMisery.git
cd onceMisery

# 2. 全局替换 README 与工作流里的 onceMisery / 仓库地址
#    贡献蛇工作流用 ${{ github.repository_owner }}，无需改动

# 3a. 换头像：把自己的图片放到 assets/avatar.jpg，本地重生成像素数据
python tools/build_pixels.py          # 需要本机 Chrome / Edge，或设置 CHROME_BIN

# 3b. 本地预览生成结果
python tools/fetch_stats.py
python tools/build_card.py
python tools/build_links.py

# 4. 提交并推送，然后在 Actions 页手动触发一次 workflow_dispatch
git add -A && git commit -m "feat: personalize profile card"
git push
```

随后在 **Settings → Actions → General** 确认两条工作流已启用。卡片里的用户名默认由 `GH_LOGIN` 决定（缺省 `onceMisery`），可在工作流里通过环境变量覆盖。

---

<a id="faq"></a>

## ❓ 常见问题

<details>
<summary><b>卡片里的数字没变化？</b></summary>

`profile-card.yml` 每天 05:00 UTC 跑一次。想立刻刷新，进入 **Actions → Update Profile Card → Run workflow** 手动触发。若某次抓取失败，会沿用上一份 `cache/stats.json`，这是刻意设计，不是卡住。

</details>

<details>
<summary><b>想换头像 / 调整像素粒度？</b></summary>

替换 `assets/avatar.jpg` 后本地运行 `python tools/build_pixels.py`，会重新生成 `avatar-pixels.json` 与 `avatar-pixel.svg`，把两者连同新原图一起提交即可。想更粗的颗粒就调小 `GRID`、调大 `QUANT`；改完再跑一次 `python tools/build_card.py` 预览。这个脚本需要本机浏览器，CI 里不会执行它。

</details>

<details>
<summary><b>SVG 显示不出来？</b></summary>

卡片与按钮放在 `main` 分支根目录，通过 `raw.githubusercontent.com` 分发；贡献蛇在 `output` 分支。请确认：

1. 仓库为公开仓库（私有仓库的 raw 链接需要鉴权）；
2. 已把新生成的 `*.svg` 推送到 `main`；
3. README 里的分支名与文件名拼写一致。

</details>

<details>
<summary><b>为什么卡片里没有中文？</b></summary>

等宽字体下 CJK 是双宽字符，会让 `key ...... value` 的点线引导符错位。卡片保留纯 ASCII 的终端观感，中文内容全部在正文中，两者分工。

</details>

---

<a id="contributing"></a>

## 🤝 贡献指南

这是个人主页仓库，欢迎纠错与改进建议：Fork 后新建分支（如 `docs/readme-tweak`），用简洁的提交信息提交，再发 Pull Request 说明改动原因。请特别留意**不要引入未经核实的数字**：主页里的统计都应当能在 GitHub 上复核。

---

<a id="contact"></a>

## 📬 联系方式

| 渠道 | 地址 |
| --- | --- |
| GitHub | [@onceMisery](https://github.com/onceMisery) |
| 邮箱 | [cmiracle@163.com](mailto:cmiracle@163.com) |
| Issues | [提问与建议](https://github.com/onceMisery/onceMisery/issues) |
| 学习驿站 | [learning-hub](https://oncemisery.github.io/learning-hub) |

欢迎就 Java、数据库客户端设计、消息中间件、一致性协议或 Apache 项目参与等话题交流。

---

<div align="center">

感谢看到这里 👋 记得 **Make a little progress every day.**

</div>
