<div align="center">
  <img src="assets/header.svg" alt="AI Tech Radar" width="100%">

  <p>
    <a href="https://whykathy.github.io/ai-tech-radar-daily/"><img src="https://img.shields.io/badge/在线浏览-GitHub_Pages-0969da?style=for-the-badge&logo=githubpages&logoColor=white" alt="在线浏览"></a>
    <a href="feed.xml"><img src="https://img.shields.io/badge/RSS-订阅-f97316?style=for-the-badge&logo=rss&logoColor=white" alt="RSS"></a>
    <img src="https://img.shields.io/badge/节奏-每日_09%3A00_CST-2ea44f?style=for-the-badge" alt="节奏">
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge" alt="License"></a>
  </p>

  <p>
    <a href="ARCHIVE.md"><img src="https://img.shields.io/badge/归档-ARCHIVE-334155?style=flat-square" alt="归档"></a>
    <a href="https://github.com/WhyKathy/ai-tech-radar-daily/commits/main"><img src="https://img.shields.io/github/commit-activity/m/WhyKathy/ai-tech-radar-daily?label=commits%2Fmonth&style=flat-square&color=0ea5e9" alt="commits"></a>
    <a href="https://github.com/WhyKathy/ai-tech-radar-daily/issues/new/choose"><img src="https://img.shields.io/badge/反馈-开_Issue-8b5cf6?style=flat-square&logo=github" alt="反馈"></a>
    <img src="https://img.shields.io/badge/待核实-全文≤2_条-eab308?style=flat-square" alt="待核实">
  </p>
</div>

每天一份中文技术日报，聚焦 **Agent 架构与自进化、训练与推理方法、推理成本、模型与评测**的真实进展。只收改变了能力边界、单位成本或做法的信息；行业动态作为背景放在开篇，不单独成章。

[在线浏览](https://whykathy.github.io/ai-tech-radar-daily/) · [浏览全部归档](ARCHIVE.md) · [RSS 订阅](feed.xml) · [收录口径与生成规范](PROMPT.md) · [反馈与纠错](https://github.com/WhyKathy/ai-tech-radar-daily/issues/new/choose)

<!-- latest:start -->
## 📡 最新一期

**[2026-11-28](daily/2026-11-28.md)** · 省 token 的三层杠杆在同一窗口内齐了：模型侧实证「让模型自己决定压缩什么」（32K 预算下分数近三倍、prefill 再省 15%），解码侧把草稿模型做成目标模型 KV 的零缓存寄生（Agent 场景最高 4.2×），编排侧把每次查询的花钱上限写进多智能体路由（同等精度省 82%）。

**今日判断**

1. **模型自管上下文（11-25）**：32K 预算下 21%→56% 不是模型变强，是同一模型在更聪明的上下文分配下跑出来的；而 KV cache 后缀复用省 15% prefill 说明这条路线的推理侧配套已经有人做。压缩策略从 harness 的手写规则变成模型行为，是上下文工程里少见的结构性变化。
2. **DFly2（11-26 开源）**：草稿器的两个自由度（用什么缓存、看哪些位置）被论证为「目标模型已经替你决定并付过钱」，这在 DSA 稀疏架构上近乎免费拿走了 drafter 的全局视野；4.2× 的 Agent 场景加速与三架构泛化让它从论文变成当天可拉取的权重与训练代码。
3. **PROVE（11-25）**：多智能体互验滑向合谋的机制解释——准确反馈在记忆里累积，使破坏规则成为奖励最优——对任何带互相审查环节的长期系统都是预警；「按证据打分而非按结果打分」给出一个可移植的奖励模板，65%→1.0% 且不伤任务成功率是干净的证据。

近期：

- [2026-11-27](daily/2026-11-27.md) — harness 演化的评价标准换了一条轴：从「在演化集上涨多少分」换成「涨的分能不能迁移」——用分布外 300 条轨迹演化出的干预策略，把编码 agent 推到 DeepSWE 76.4%、Terminal-Bench 95.5%；而同一批基准的源码级审计显示，按单任务增益筛技能的那套门控，把条件标签打乱、技能效应清零之后仍能「提升」4–7 个百分点，筛出来的是抽样噪声。
- [2026-11-26](daily/2026-11-26.md) — 代理系统的两个隐藏开关同时被量化：上下文压缩会把模型写的摘要当成用户发言，越权支付在 91% 的案例里被放行；沙盒边界只要在系统提示里讲清楚，越界率就从 21%–32% 压到 2% 以下。经验要不要写进权重，判据也从「当次表现变好」换成了「梯度是否对齐」。
- [2026-11-25](daily/2026-11-25.md) — 循环架构一天内拿到两个信号：智谱把 Loop Transformer 推到 750B 旗舰量产，NUS 同日给出把预训练模型改造成循环的通用方法；agent 干研究时 GPU 时间只有 52% 花在正事上，一套测量型 harness 收回了八成浪费；前沿实验室开始用困惑度为能力增长划可量化红线。
- [2026-11-24](daily/2026-11-24.md) — agent 产出的准入层这两天集中前移：代码合并交给可审计的策略文件自动盖章，无法实测的量子电路交给 Lean 形式化证明放行，自进化系统的经验入库开始配真值锚定、反证过滤与回滚闸门；成本侧，1M token 上下文的记忆状态被压掉三个数量级。

[全部 41 期 →](ARCHIVE.md)
<!-- latest:end -->

## 🎯 收录口径

一条技术信息要进雷达，必须至少满足一条：

| | 判据 | 意味着什么 |
|:--:|------|-----------|
| 🚀 | **改变能力边界** | 之前做不到的，现在能做到了 |
| 💰 | **改变单位成本** | 同样效果，钱或时间降一个档 |
| 🔧 | **改变做法** | 工程上该换个方式干了 |

> [!WARNING]
> **明确不收**：纯榜单刷分、纯增量调参、无代码无细节的厂商博客、应用层产品发布、与技术路线无关的融资。

行业信息（融资与估值、数据中心与电力、诉讼与监管、平台对 agent 的准入）不单独成章，放在开篇「行业动态」，只陈述发生了什么以及它改变了什么，最多 4 条。

## 🧱 每期结构

每份 `daily/YYYY-MM-DD.md` 包含：今日一句话、行业动态、Agent 架构与工程、论文与方法、模型与开源、推理成本与基础设施、评测与基准、今日判断、覆盖与不确定，以及附录 · 今日索引（arXiv 新投稿 / Hugging Face trending / GitHub trending 的原始列表）。

> [!NOTE]
> 正文中某节当天没有达标内容就**整节省略**，不写占位、不凑数。**附录不受此限**——它是原始流，只列标题与链接，不做筛选与判断，用来扫读定位；判断只发生在正文。

## ✅ 事实标准

- 📅 每条信息都带发布日期与来源链接。
- ⚠️ 无法从检索结果确认的关键事实标注「待核实」，全文最多 2 条。
- 📄 只读标题、未读摘要的论文标注「仅标题，方法待核实」，不描述其方法。
- 🔁 同一事件无实质新进展不重复收录；有进展写「更新：」并保留原日期。

## ⚙️ 更新机制

- 每天 09:00（CST）由定时任务检索过去 48 小时的进展，按 [`PROMPT.md`](PROMPT.md) 生成 `daily/YYYY-MM-DD.md`。
- 发布前 [`scripts/build_index.py`](scripts/build_index.py) 从全部日报派生 `ARCHIVE.md`、`feed.xml`、本页的「最新一期」与 `index.html`；[`scripts/check_report.py`](scripts/check_report.py) 检查章节、来源链接、待核实数量与公开文风。
- 在线浏览页首屏直接内嵌**最新一期全文**与「今日速览」，无需点开 md；左侧选日期可切换往期。
- 手动重建门面：`python3 scripts/build_index.py`；手动质检：`python3 scripts/check_report.py 2026-11-28`。

## 💬 反馈

发现事实错误、失效链接，或想推荐值得收录的源，请[开一个 Issue](https://github.com/WhyKathy/ai-tech-radar-daily/issues/new/choose)。日报由 AI 辅助检索整理，关键结论请结合原文阅读。

## 📄 License

[MIT](LICENSE)

<div align="center">
  <sub>每日扫描 · 只报改变边界、成本或做法的信号</sub>
</div>
