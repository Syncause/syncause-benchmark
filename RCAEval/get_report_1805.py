#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取18:05左右的完整报告
"""

import sys
sys.path.insert(0, '/Users/jundi/PycharmProjects/RCAEval')

from RCAEval.e2e.srechat_rca import srechat_rca
from datetime import datetime
import json
import re

print("=" * 80)
print("📄 获取 18:05 左右的完整报告")
print("=" * 80)

# 指定18:05的时间
detect_time = "2025-10-14T18:05:00+08:00"
print(f"\n⏰ 检测时间: {detect_time}")
print(f"📊 时间窗口: 最近15分钟 (17:50 - 18:05)\n")

print("正在调用API，请稍候...")
print("-" * 80)

result = srechat_rca(detect_time=detect_time, time_window_minutes=15)

report = result.get('report', '')
print(f"\n✅ 报告获取成功！")
print(f"   报告长度: {len(report):,} 字符")

# 保存原始报告
raw_file = "report_1805_raw.txt"
with open(raw_file, 'w', encoding='utf-8') as f:
    f.write(f"检测时间: {detect_time}\n")
    f.write(f"获取时间: {datetime.now()}\n")
    f.write(f"报告长度: {len(report)} 字符\n")
    f.write("=" * 80 + "\n")
    f.write(report)

print(f"   原始报告已保存: {raw_file}")

# 解析JSON对象
print("\n" + "=" * 80)
print("解析报告中的JSON对象...")
print("=" * 80)

json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
matches = re.findall(json_pattern, report)

print(f"\n检测到 {len(matches)} 个JSON对象\n")

# 提取关键信息
key_objects = {
    'intention': None,
    'all_services': None,
    'abnormal_services': None,
    'causal_graph': None,
    'cpu_info': None,
}

for i, match in enumerate(matches, 1):
    try:
        obj = json.loads(match)
        if not isinstance(obj, dict):
            continue
        
        # 分类JSON对象
        if 'intention' in obj and 'classify' in obj:
            key_objects['intention'] = obj
        elif 'service' in obj and isinstance(obj['service'], list) and len(obj['service']) > 5:
            key_objects['all_services'] = obj
        elif 'abnormalServices' in obj:
            key_objects['abnormal_services'] = obj
        elif 'causal' in obj:
            key_objects['causal_graph'] = obj
        elif 'affected_services_info' in obj:
            key_objects['cpu_info'] = obj
            
    except:
        pass

# 显示关键信息
print("━" * 80)
print("📋 1. 意图识别")
print("━" * 80)
if key_objects['intention']:
    print(json.dumps(key_objects['intention'], indent=2, ensure_ascii=False))
else:
    print("未找到")

print("\n" + "━" * 80)
print("🎯 2. 异常服务列表 (abnormalServices)")
print("━" * 80)
if key_objects['abnormal_services']:
    print(json.dumps(key_objects['abnormal_services'], indent=2, ensure_ascii=False))
    
    services = key_objects['abnormal_services'].get('abnormalServices', [])
    print(f"\n检测到 {len(services)} 个异常服务:")
    for i, svc in enumerate(services, 1):
        print(f"  {i}. 🔴 {svc}")
else:
    print("未找到异常服务")

print("\n" + "━" * 80)
print("💻 3. CPU异常信息 (affected_services_info)")
print("━" * 80)
if key_objects['cpu_info']:
    print(json.dumps(key_objects['cpu_info'], indent=2, ensure_ascii=False))
    
    affected = key_objects['cpu_info'].get('affected_services_info', [])
    print(f"\n检测到 {len(affected)} 个CPU异常服务:")
    for i, info in enumerate(affected, 1):
        svc = info.get('service', '?')
        direction = info.get('direction', '?')
        count = info.get('count', 0)
        level = info.get('level', 0)
        severity = "🔥" * level
        print(f"\n  {i}. {svc}")
        print(f"     类型: {direction.upper()}")
        print(f"     异常次数: {count}")
        print(f"     严重等级: {severity} (Level {level})")
else:
    print("未找到CPU异常信息")

print("\n" + "━" * 80)
print("🧠 4. 因果关系图 (causal graph)")
print("━" * 80)
if key_objects['causal_graph']:
    causal_edges = key_objects['causal_graph'].get('causal', [])
    print(f"因果关系数量: {len(causal_edges)}\n")
    
    # 按置信度排序
    sorted_edges = sorted(causal_edges, key=lambda x: x.get('confidence', 0), reverse=True)
    
    print("Top 10 因果关系 (按置信度排序):")
    print(f"{'排名':<6} {'源服务':<30} {'→':<3} {'目标服务':<30} {'置信度':<10}")
    print("-" * 85)
    
    for i, edge in enumerate(sorted_edges[:10], 1):
        from_svc = edge.get('from', '?')
        to_svc = edge.get('to', '?')
        confidence = edge.get('confidence', 0)
        print(f"{i:<6} {from_svc:<30} {'→':<3} {to_svc:<30} {confidence:>6.1%}")
    
    # 统计作为源头的次数
    from_counts = {}
    for edge in causal_edges:
        from_svc = edge.get('from')
        if from_svc:
            from_counts[from_svc] = from_counts.get(from_svc, 0) + 1
    
    print(f"\n根因服务分析 (作为因果源头的次数):")
    sorted_sources = sorted(from_counts.items(), key=lambda x: x[1], reverse=True)
    for i, (svc, count) in enumerate(sorted_sources[:5], 1):
        print(f"  {i}. {svc:<30} → {count} 次")
else:
    print("未找到因果关系图")

print("\n" + "━" * 80)
print("📊 5. 所有受影响服务")
print("━" * 80)
if key_objects['all_services']:
    services = key_objects['all_services'].get('service', [])
    print(f"总计: {len(services)} 个服务\n")
    
    for i, svc in enumerate(services, 1):
        print(f"  {i:2d}. {svc}")
else:
    print("未找到服务列表")

# 保存格式化的关键信息
summary_file = "report_1805_summary.json"
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump({
        'detect_time': detect_time,
        'report_length': len(report),
        'json_objects_count': len(matches),
        'key_objects': key_objects
    }, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print("✅ 完成！")
print("=" * 80)
print(f"\n📁 生成的文件:")
print(f"  1. {raw_file} - 完整原始报告")
print(f"  2. {summary_file} - 关键信息摘要")
print()




