#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展示CPU故障分析结果
"""

import sys
sys.path.insert(0, '/Users/jundi/PycharmProjects/RCAEval')

print("=" * 80)
print("📊 SREChat RCA - CPU故障分析结果")
print("=" * 80)

# 直接调用算法
from RCAEval.e2e.srechat_rca import srechat_rca
from datetime import datetime

detect_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
print(f"\n⏰ 检测时间: {detect_time}")

try:
    result = srechat_rca(detect_time=detect_time, time_window_minutes=15)
    
    print("\n" + "=" * 80)
    print("🎯 检测结果")
    print("=" * 80)
    
    ranks = result.get('ranks', [])
    report = result.get('report', '')
    
    print(f"\n受影响的服务Top5:")
    for i, svc in enumerate(ranks, 1):
        print(f"  {i}. {svc}")
    
    # 解析完整报告
    import json
    try:
        data = json.loads(report)
        all_services = data.get('service', [])
        
        print(f"\n所有受影响的服务 (共{len(all_services)}个):")
        print("-" * 80)
        
        # 按服务类型分类
        service_groups = {
            '基础服务': [],
            '订单服务': [],
            '行程服务': [],
            '路线服务': [],
            '其他服务': []
        }
        
        for svc in all_services:
            if 'basic' in svc or 'config' in svc or 'gateway' in svc:
                service_groups['基础服务'].append(svc)
            elif 'order' in svc:
                service_groups['订单服务'].append(svc)
            elif 'travel' in svc:
                service_groups['行程服务'].append(svc)
            elif 'route' in svc:
                service_groups['路线服务'].append(svc)
            else:
                service_groups['其他服务'].append(svc)
        
        for group_name, svcs in service_groups.items():
            if svcs:
                print(f"\n【{group_name}】 ({len(svcs)}个)")
                for svc in svcs:
                    is_top5 = svc in ranks
                    marker = " ⭐" if is_top5 else ""
                    print(f"  • {svc}{marker}")
        
        print("\n" + "=" * 80)
        print("💡 分析建议")
        print("=" * 80)
        
        print("\n1. 你注入的CPU故障在哪个服务？")
        print("   请告诉我具体的服务名称，我可以检查它是否在检测结果中\n")
        
        print("2. 如果故障服务在Top5中 → ✅ 算法工作正常")
        print("   如果故障服务不在Top5中 → ⚠️  可能需要调整参数或使用DeepSeek解析\n")
        
        print("3. 配置DeepSeek获得更智能的分析:")
        print("   export DEEPSEEK_API_KEY='your-key'")
        print("   python3 verify_cpu_fault.py\n")
        
    except json.JSONDecodeError:
        print(f"\n原始报告:\n{report}")

except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)




