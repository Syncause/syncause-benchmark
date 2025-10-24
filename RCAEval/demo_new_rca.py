#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示新的SREChat RCA解析器
专门解析Root Cause Analysis结果
"""

import sys, importlib.util
module_path = '/Users/jundi/PycharmProjects/RCAEval/RCAEval/e2e/srechat_rca.py'
spec = importlib.util.spec_from_file_location('srechat_rca', module_path)
srechat_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srechat_module)  # type: ignore
srechat_rca = srechat_module.srechat_rca
from datetime import datetime

print("=" * 80)
print("🎯 SREChat RCA - 简洁输出演示（README风格）")
print("=" * 80)

# 可以测试不同的时间点
# 方式1: 直接测试18:20（会分析18:05-18:20这15分钟的数据）
test_times = [
    ("18:20", "2025-10-14T18:20:00+08:00"),
]

# 方式2: 测试18:05-18:20区间内的多个时间点
# test_times = [
#     ("18:05", "2025-10-14T18:05:00+08:00"),  # 分析17:50-18:05
#     ("18:10", "2025-10-14T18:10:00+08:00"),  # 分析17:55-18:10
#     ("18:15", "2025-10-14T18:15:00+08:00"),  # 分析18:00-18:15
#     ("18:20", "2025-10-14T18:20:00+08:00"),  # 分析18:05-18:20
# ]

for label, detect_time in test_times:
    result = srechat_rca(
        detect_time=detect_time,
        time_window_minutes=15,
        verbose=False,
    )
    root_causes = result.get("ranks", [])
    print("Top 5 root causes:", root_causes[:5])

print("=" * 80)
print("✅ 演示完成")
print("=" * 80)

print("\n💡 使用说明:")
print("  新的解析器会自动提取Root Cause Analysis结果")
print("  包括:")
print("  • Summary - 问题摘要") 
print("  • Root Cause Report Table - 根因分析表格")
print("  • Detailed Report - 详细分析报告")
print()
print("📄 详细文档: NEW_PARSER_SUMMARY.md")
print()

