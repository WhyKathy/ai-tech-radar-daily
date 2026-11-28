#!/usr/bin/env python3
"""日报轻量质检：结构完整性 + 事实标注 + 公开文风。

用法：
  python3 scripts/check_report.py            # 检查最新一期
  python3 scripts/check_report.py 2026-11-28 # 检查指定日期
  python3 scripts/check_report.py --strict   # 警告也视为失败

默认只把结构性缺失当失败（exit 1），警告不阻断发布。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["## 今日一句话", "## 今日判断", "## 覆盖与不确定", "## 附录 · 今日索引"]
BANNED = ["你", "我们", "您", "咱们", "本期", "综上所述", "本节略"]


def check(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    text = path.read_text(encoding="utf-8")
    body = text.split("## 附录 · 今日索引")[0]

    for heading in REQUIRED:
        if heading not in text:
            errors.append(f"缺少章节：{heading}")

    match = re.search(r"^##\s+今日一句话\s*$\n(.*?)(?=^##\s|\Z)", body, re.M | re.S)
    one_liner = ""
    if match:
        for line in match.group(1).splitlines():
            line = line.strip()
            if line and not line.startswith(">"):
                one_liner = line
                break
    if not one_liner:
        errors.append("「今日一句话」为空")
    elif len(one_liner) < 30:
        warnings.append("「今日一句话」过短，建议给出具体事实与数字")

    links = re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", body)
    if len(links) < 3:
        warnings.append(f"正文来源链接仅 {len(links)} 条，建议至少 3 条可核验链接")

    pending = body.count("待核实")
    if pending > 2:
        errors.append(f"「待核实」出现 {pending} 次，超过口径上限 2 次")

    # 引号内多为论文原话或术语（如「你错了」），不算公开文风违规。
    unquoted = re.sub(r"「[^」]*」|『[^』]*』|《[^》]*》", "", body)
    for word in BANNED:
        if word in unquoted:
            warnings.append(f"正文出现公开文风禁用词：{word}")

    return errors, warnings


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    strict = "--strict" in sys.argv
    daily = ROOT / "daily"
    if args:
        date = args[0].removesuffix(".md")
        path = daily / f"{date}.md"
        if not path.exists():
            path = ROOT / f"{date}.md"  # 兼容定时任务仍写根目录的过渡期
    else:
        dates = sorted(p.stem for p in daily.glob("????-??-??.md"))
        if not dates:
            dates = sorted(p.stem for p in ROOT.glob("????-??-??.md"))
        if not dates:
            raise SystemExit("未找到日报")
        path = daily / f"{dates[-1]}.md"
        if not path.exists():
            path = ROOT / f"{dates[-1]}.md"
    if not path.exists():
        raise SystemExit(f"文件不存在：{path}")

    errors, warnings = check(path)
    for item in errors:
        print(f"[ERROR] {item}")
    for item in warnings:
        print(f"[WARN]  {item}")
    if not errors and not warnings:
        print(f"[OK] {path.name}: 结构、来源与文风检查通过")
    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
