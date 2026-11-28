#!/usr/bin/env python3
"""从每日日报生成仓库门面：归档索引、RSS、README 最新一期。

只做结构化派生，不改写正文；不依赖第三方库。
用法：python3 scripts/build_index.py
"""
from __future__ import annotations

import html
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO_URL = "https://github.com/WhyKathy/ai-tech-radar-daily"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
TODAY_MARKERS = ("<!-- latest:start -->", "<!-- latest:end -->")


def ingest_root_reports() -> int:
    """兼容旧路径：定时任务若仍把日报写在根目录，自动收进 daily/。"""
    daily = ROOT / "daily"
    if not daily.exists():
        daily.mkdir()
    moved = 0
    for path in sorted(ROOT.glob("????-??-??.md")):
        if not DATE_RE.match(path.stem):
            continue
        target = daily / path.name
        if not target.exists():
            path.replace(target)
            moved += 1
    return moved


def load_reports() -> list[dict]:
    reports = []
    for path in sorted((ROOT / "daily").glob("????-??-??.md")):
        if not DATE_RE.match(path.stem):
            continue
        text = path.read_text(encoding="utf-8")
        body = text.split("## 附录 · 今日索引")[0]
        match = re.search(r"^##\s+今日一句话\s*$\n(.*?)(?=^##\s|\Z)", body, re.M | re.S)
        one_liner = ""
        if match:
            for line in match.group(1).splitlines():
                line = line.strip()
                if not line or line.startswith(">"):
                    continue
                one_liner = line
                break
        reports.append(
            {
                "date": path.stem,
                "rel": f"daily/{path.name}",
                "one_liner": one_liner or "（今日一句话缺失）",
                "links": len(re.findall(r"https?://", body)),
                "pending": body.count("待核实"),
            }
        )
    return reports


def write_archive(reports: list[dict]) -> None:
    lines = [
        "# 日报归档",
        "",
        f"共 {len(reports)} 期 · {reports[0]['date']} — {reports[-1]['date']} · 每日更新",
        "",
        "按月份倒序排列，每期标题下是当天的「今日一句话」。点日期进入全文（含正文与原始索引附录）。",
        "",
    ]
    by_month: dict[str, list[dict]] = {}
    for report in reversed(reports):
        by_month.setdefault(report["date"][:7], []).append(report)
    for month, items in by_month.items():
        year, mon = month.split("-")
        lines.append(f"## {year} 年 {int(mon)} 月（{len(items)} 期）")
        lines.append("")
        for item in items:
            lines.append(
                f"- **[{item['date']}]({item['rel']})** — {item['one_liner']}"
            )
        lines.append("")
    (ROOT / "ARCHIVE.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_feed(reports: list[dict]) -> None:
    # 用最新一期日期而非当前时间，避免重复运行产生无意义 diff。
    latest_day = datetime.strptime(reports[-1]["date"], "%Y-%m-%d").replace(
        tzinfo=timezone(timedelta(hours=8))
    )
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        "  <channel>",
        "    <title>AI 技术雷达 · 每日日报</title>",
        f"    <link>{REPO_URL}</link>",
        "    <description>聚焦 Agent 架构与自进化、训练与推理方法、推理成本、模型与评测的真实进展。</description>",
        "    <language>zh-CN</language>",
        f"    <lastBuildDate>{latest_day.strftime('%a, %d %b %Y %H:%M:%S %z')}</lastBuildDate>",
    ]
    for item in reversed(reports):
        day = datetime.strptime(item["date"], "%Y-%m-%d").replace(
            tzinfo=timezone(timedelta(hours=8))
        )
        link = f"{REPO_URL}/blob/main/{item['rel']}"
        lines.extend(
            [
                "    <item>",
                f"      <title>AI 技术雷达 · {item['date']}</title>",
                f"      <link>{link}</link>",
                f"      <guid isPermaLink=\"true\">{link}</guid>",
                f"      <pubDate>{day.strftime('%a, %d %b %Y %H:%M:%S %z')}</pubDate>",
                f"      <description>{html.escape(item['one_liner'])}</description>",
                "    </item>",
            ]
        )
    lines.extend(["  </channel>", "</rss>", ""])
    (ROOT / "feed.xml").write_text("\n".join(lines), encoding="utf-8")


def update_readme(reports: list[dict]) -> None:
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    start, end = TODAY_MARKERS
    if start not in text or end not in text:
        raise SystemExit("README.md 缺少 latest 标记块，无法更新最新一期")
    latest = list(reversed(reports))[:5]
    lines = ["## 最新一期", ""]
    if latest:
        newest = latest[0]
        lines.append(
            f"**[{newest['date']}]({newest['rel']})** · {newest['one_liner']}"
        )
        lines.append("")
        lines.append("近期：")
        lines.append("")
        for item in latest[1:]:
            lines.append(f"- [{item['date']}]({item['rel']}) — {item['one_liner']}")
        lines.append("")
        lines.append(f"[全部 {len(reports)} 期 →](ARCHIVE.md)")
    block = "\n".join(lines).rstrip()
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    path.write_text(f"{head}{start}\n{block}\n{end}{tail}", encoding="utf-8")


def main() -> int:
    moved = ingest_root_reports()
    if moved:
        print(f"ingested: {moved} 份根目录日报已移入 daily/")
    reports = load_reports()
    if not reports:
        raise SystemExit("未找到 YYYY-MM-DD.md 日报")
    write_archive(reports)
    write_feed(reports)
    update_readme(reports)
    print(
        f"built: ARCHIVE.md ({len(reports)} 期), feed.xml, README 最新一期 "
        f"({reports[-1]['date']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
