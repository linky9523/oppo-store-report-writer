#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPPO 门店周报聚合脚本

功能：扫描本周（周一~周六）的日报存档，提取每份日报末尾的 <!--metrics ...--> 块，
累加 10 项业绩 KPI，并汇总各日典型案例与收获思考，输出供周报生成的结构化结果。

存档约定（见 daily-report-schema.md）：
  目录: ~/.workbuddy/skills/oppo-store-report-writer/data/daily/{YYYY}/W{ISO周数}/
  文件: {MM-DD}.md
  每份日报末尾包含 metrics 块，例如:
    <!--metrics phone=1 iot=0 paid_film=0 trade_in=0 ent_wechat=5 dianping=1 map_review=0 free_film=2 douyin=0 xiaohongshu=0-->

用法:
  python3 aggregate_weekly.py                  # 默认基于"今天"所在周
  python3 aggregate_weekly.py --week-date 2026-09-13   # 指定该周内任一天

输出（JSON，打印到 stdout）：
  {
    "week_mon": "2026-09-07", "week_sat": "2026-09-12", "iso_week": 37,
    "reports": [ {"date":"09-07","path":"...","metrics":{...},"has_case":true} , ...],
    "totals": {"phone":..,"iot":..,...},          # 周一~周六累计
    "missing_days": ["09-07",...],                # 缺失日报的日期
    "notes": "..."
  }
"""

import argparse
import datetime as dt
import json
import os
import re
import sys

SKILL_DIR = os.path.expanduser("~/.workbuddy/skills/oppo-store-report-writer")
DATA_ROOT = os.path.join(SKILL_DIR, "data", "daily")

# 10 项 KPI 键名（顺序与周报表头一致）
METRIC_KEYS = [
    "phone", "iot", "paid_film", "trade_in", "ent_wechat",
    "dianping", "map_review", "free_film", "douyin", "xiaohongshu",
]


def week_bounds(ref: dt.date):
    """返回 ref 所在周的周一与周六（ISO: Monday=0 ... Sunday=6）。"""
    monday = ref - dt.timedelta(days=ref.weekday())
    saturday = monday + dt.timedelta(days=5)
    return monday, saturday


def metrics_from_text(text: str):
    """从日报文本提取 metrics 块并返回 dict。无则返回空 dict。"""
    m = re.search(r"<!--metrics\s+(.*?)-->", text, re.S)
    if not m:
        return {}
    out = {}
    for k, v in re.findall(r"(\w+)=(-?\d+)", m.group(1)):
        out[k] = int(v)
    return out


def aggregate(ref: dt.date):
    monday, saturday = week_bounds(ref)
    iso_week = monday.isocalendar()[1]
    year = monday.year
    week_dir = os.path.join(DATA_ROOT, str(year), f"W{iso_week:02d}")

    reports = []
    totals = {k: 0 for k in METRIC_KEYS}
    missing = []

    d = monday
    while d <= saturday:
        fname = f"{d.month:02d}-{d.day:02d}.md"
        fpath = os.path.join(week_dir, fname)
        if os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                text = f.read()
            m = metrics_from_text(text)
            for k in METRIC_KEYS:
                totals[k] += m.get(k, 0)
            reports.append({
                "date": fname[:-3],
                "path": fpath,
                "metrics": m,
                "has_case": "【典型案例】" in text,
                "has_reflection": "【收获与思考】" in text,
            })
        else:
            missing.append(fname[:-3])
        d += dt.timedelta(days=1)

    return {
        "week_mon": monday.isoformat(),
        "week_sat": saturday.isoformat(),
        "iso_week": iso_week,
        "week_dir": week_dir,
        "reports": reports,
        "totals": totals,
        "missing_days": missing,
        "report_count": len(reports),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week-date", default=None,
                    help="该周内任一天 YYYY-MM-DD，默认今天")
    args = ap.parse_args()

    if args.week_date:
        try:
            ref = dt.date.fromisoformat(args.week_date)
        except ValueError:
            print(json.dumps({"error": f"无效日期: {args.week_date}"}))
            sys.exit(1)
    else:
        ref = dt.date.today()

    result = aggregate(ref)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
