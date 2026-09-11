# OPPO 门店日报/周报撰写技能 (oppo-store-report-writer)

为 OPPO 门店导购把零散销售素材，按固定模板撰写成符合品牌口径的日报与周报的 AI Skill（适用于 WorkBuddy / CodeBuddy 等支持 Agent Skills 的客户端）。

## 能力

1. **日报撰写** — 纯文本（微信/群发风格），固定区块：门店数据 / 个人数据 / 典型案例 / 收获思考 / 今日达成 / 明日目标。
2. **周报撰写** — 自动汇总本周一至周六的存档日报，结合周日补充数据，生成 Excel 版式周报（OPPO 绿标题 + 10 项业绩指标表 + 四段长文本 + 下周计划）。
3. **业务校准** — 内置 OPPO 导购业务背景：产品线（Find / Reno / 一加 / A）、10 项 KPI 口径、销售场景与话术、门店观察维度，确保机型、术语、数据口径准确。

## 目录结构

```
oppo-store-report-writer/
├── SKILL.md                          # 主控：触发条件 + 日报/周报工作流
├── references/
│   ├── daily-report-schema.md        # 日报字段结构、所需信息清单、存档约定
│   ├── weekly-report-schema.md       # 周报字段结构、10 项 KPI、自动汇总流程、xlsx 样式规格
│   ├── oppo-sales-context.md         # 产品线、KPI 口径、销售场景、观察维度
│   └── writing-examples.md           # 3 份日报范本 + 1 份周报范本
├── assets/
│   ├── daily-report-template.md      # 日报空白模板（含 metrics 块）
│   └── weekly-report-template.md     # 周报 markdown 结构模板
├── scripts/
│   └── aggregate_weekly.py           # 周报聚合脚本：扫描本周日报、累加 10 项 KPI
└── data/daily/                       # 日报存档（运行时生成，已被 .gitignore 排除）
```

## 安装

复制到用户级技能目录（跨项目可用）：

```bash
# WorkBuddy
cp -r oppo-store-report-writer ~/.workbuddy/skills/

# CodeBuddy
cp -r oppo-store-report-writer ~/.codebuddy/skills/
```

## 使用

触发词：写日报 / 写周报 / 今日日报 / 本周周报 / 门店日报 / 导购日报。

**日报**由用户提供当日素材（门店数据、个人数据、典型案例、收获要点）生成，并自动存档到 `data/daily/{年份}/W{周}/{MM-DD}.md`。

**周报**下指令后自动运行聚合脚本：

```bash
python3 scripts/aggregate_weekly.py            # 默认本周
python3 scripts/aggregate_weekly.py --week-date 2026-09-13
```

输出本周 10 项 KPI 累计、缺失日报日期与各日案例标记，再结合周日补充数据生成周报。

## 隐私说明

`data/daily/` 存放真实门店销售数据、客户企微与客户案例，已在 `.gitignore` 中排除，不会进入版本库。若 fork 本仓库，请勿提交该目录。
