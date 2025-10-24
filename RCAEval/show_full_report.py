#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
显示SREChat API返回的完整报告内容
"""

import sys
sys.path.insert(0, '/Users/jundi/PycharmProjects/RCAEval')

from RCAEval.e2e.srechat_rca import srechat_rca
from datetime import datetime
import json

print("=" * 80)
print("📄 SREChat API 完整报告内容")
print("=" * 80)

detect_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
print(f"\n⏰ 检测时间: {detect_time}")
print(f"📊 时间窗口: 最近15分钟\n")

print("正在调用API...")
result = srechat_rca(detect_time=detect_time, time_window_minutes=15)

report = result.get('report', '')
print(f"\n报告长度: {len(report)} 字符")
print("\n" + "=" * 80)
print("完整报告内容:")
print("=" * 80)
print()

# 尝试格式化JSON
try:
    # 如果整个报告是JSON
    data = json.loads(report)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    # 如果不是单个JSON，尝试提取多个JSON对象
    import re
    
    # 查找所有JSON对象
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, report)
    
    if matches:
        print("检测到多个JSON对象，逐个显示:\n")
        for i, match in enumerate(matches, 1):
            print(f"--- JSON对象 #{i} ---")
            try:
                obj = json.loads(match)
                print(json.dumps(obj, indent=2, ensure_ascii=False))
            except:
                print(match)
            print()
    else:
        # 纯文本报告
        print(report)

# 保存到文件
output_file = f"full_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    try:
        data = json.loads(report)
        json.dump(data, f, indent=2, ensure_ascii=False)
    except:
        f.write(report)

print("\n" + "=" * 80)
print(f"✅ 完整报告已保存到: {output_file}")
print("=" * 80)




