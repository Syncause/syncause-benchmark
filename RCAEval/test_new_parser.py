#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试新的Root Cause Analysis解析器
"""

import sys
sys.path.insert(0, '/Users/jundi/PycharmProjects/RCAEval')

from RCAEval.e2e.srechat_rca import srechat_rca
from datetime import datetime

print("=" * 80)
print("🧪 测试新的Root Cause Analysis解析器")
print("=" * 80)

# 测试18:15时间点（你提供的示例时间）
detect_time = "2025-10-14T18:15:00+08:00"
print(f"\n⏰ 检测时间: {detect_time}")
print(f"   (分析18:00-18:15时间窗口)\n")

print("正在调用API...")
print("-" * 80)

result = srechat_rca(
    detect_time=detect_time,
    time_window_minutes=15
)

print("\n" + "=" * 80)
print("📊 解析结果")
print("=" * 80)

ranks = result.get('ranks', [])
report = result.get('report', '')

print(f"\n🎯 Top5根因服务:")
for i, svc in enumerate(ranks, 1):
    print(f"  {i}. {svc}")

print(f"\n📄 报告预览（前1000字符）:")
print("-" * 80)
print(report[:1000])
if len(report) > 1000:
    print(f"... (还有 {len(report) - 1000} 字符)")
print("-" * 80)

# 检查是否包含Root Cause Analysis
if "Root Cause Analysis" in report:
    print("\n✅ 成功提取Root Cause Analysis内容！")
    
    # 提取summary部分
    if "SUMMARY:" in report:
        summary_start = report.find("SUMMARY:") + 9
        summary_end = report.find("\n\nDETAILED REPORT:")
        if summary_end == -1:
            summary_end = report.find("\n\n===")
        
        summary = report[summary_start:summary_end].strip()
        print("\n📋 摘要:")
        print("-" * 80)
        print(summary[:500])
        if len(summary) > 500:
            print(f"... (摘要共 {len(summary)} 字符)")
        print("-" * 80)
    
    # 检查是否有表格
    if "| Node / Service |" in report or "| ts-" in report:
        print("\n✅ 检测到根因分析表格")
else:
    print("\n⚠️  未检测到Root Cause Analysis格式")

# 保存完整报告
output_file = f"test_rca_report_{datetime.now().strftime('%H%M%S')}.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"检测时间: {detect_time}\n")
    f.write(f"解析时间: {datetime.now()}\n")
    f.write("=" * 80 + "\n")
    f.write("Top5根因:\n")
    for i, rc in enumerate(ranks, 1):
        f.write(f"{i}. {rc}\n")
    f.write("\n" + "=" * 80 + "\n")
    f.write("完整报告:\n")
    f.write("=" * 80 + "\n")
    f.write(report)

print(f"\n💾 完整报告已保存: {output_file}")

print("\n" + "=" * 80)
print("✅ 测试完成")
print("=" * 80)




