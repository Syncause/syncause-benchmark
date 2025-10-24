#!/usr/bin/env python3
import sys
sys.path.insert(0, '/Users/jundi/PycharmProjects/RCAEval')

from RCAEval.e2e.srechat_rca import srechat_rca
from datetime import datetime

print("🔍 快速测试 SREChat RCA")
print("=" * 60)

detect_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
print(f"检测时间: {detect_time}\n")

result = srechat_rca(detect_time=detect_time, time_window_minutes=15)

print("Top5根因:")
for i, rc in enumerate(result['ranks'], 1):
    marker = "🔴 " if i == 1 else "   "
    print(f"{marker}{i}. {rc}")

print("\n" + "=" * 60)
print("✅ 测试完成！")
print("\n请告诉我你注入CPU故障的具体服务名称，")
print("我可以验证它是否被正确检测到。")




