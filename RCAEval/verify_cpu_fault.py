#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证CPU故障 - 使用SREChat RCA算法
"""

import os
import sys
from datetime import datetime, timedelta

# 添加路径以便导入RCAEval
sys.path.insert(0, '/Users/jundi/PycharmProjects/RCAEval')

print("=" * 80)
print("🔍 SREChat RCA - CPU故障分析")
print("=" * 80)

# 检查是否配置了API密钥
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
srechat_url = os.getenv("SRECHAT_API_URL", "http://192.168.1.6:28522/api/v1/srechat")

print(f"\n📋 配置信息:")
print(f"  SREChat API: {srechat_url}")
print(f"  DeepSeek API: {'已配置 ✓' if deepseek_key else '未配置 (将使用简单解析)'}")

# 获取当前时间作为检测时间
now = datetime.now()
detect_time = now.strftime("%Y-%m-%dT%H:%M:%S+08:00")

print(f"\n⏰ 检测时间: {detect_time}")
print(f"  (分析最近15分钟的异常)")

# 也提供几个时间选项
print(f"\n可选的检测时间点:")
for i in [5, 10, 15, 30]:
    past_time = now - timedelta(minutes=i)
    print(f"  {i}分钟前: {past_time.strftime('%Y-%m-%dT%H:%M:%S+08:00')}")

print(f"\n如果需要指定其他时间，请按 Ctrl+C 退出，然后运行:")
print(f"  python verify_cpu_fault.py <时间>")
print(f"  例如: python verify_cpu_fault.py '2025-09-23T17:20:42+08:00'")

# 等待用户确认或提供时间
if len(sys.argv) > 1:
    detect_time = sys.argv[1]
    print(f"\n✓ 使用指定时间: {detect_time}")
else:
    print(f"\n⏳ 3秒后开始分析当前时间...")
    import time
    for i in range(3, 0, -1):
        print(f"  {i}...", end='\r')
        time.sleep(1)
    print("  开始分析!")

print("\n" + "=" * 80)
print("🚀 调用SREChat RCA算法...")
print("=" * 80)

try:
    from RCAEval.e2e.srechat_rca import srechat_rca
    
    # 调用算法
    result = srechat_rca(
        detect_time=detect_time,
        api_url=srechat_url,
        time_window_minutes=15,
        deepseek_api_key=deepseek_key
    )
    
    print("\n" + "=" * 80)
    print("📊 分析结果")
    print("=" * 80)
    
    print(f"\n检测时间: {result.get('detect_time', detect_time)}")
    
    # 显示Top5根因
    ranks = result.get('ranks', [])
    print(f"\n🎯 Top5根因:")
    if ranks:
        for i, rc in enumerate(ranks, 1):
            # 高亮CPU相关的根因
            if 'cpu' in rc.lower():
                print(f"  {i}. 🔴 {rc}  <-- CPU相关!")
            else:
                print(f"  {i}. {rc}")
    else:
        print("  (未找到根因)")
    
    # 显示原始报告（摘要）
    report = result.get('report', '')
    if report:
        print(f"\n📄 原始报告摘要 (前500字符):")
        print("-" * 80)
        print(report[:500])
        if len(report) > 500:
            print(f"... (还有 {len(report) - 500} 字符)")
        print("-" * 80)
        
        # 保存完整报告到文件
        report_file = f"cpu_fault_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(f"检测时间: {detect_time}\n")
            f.write(f"分析时间: {datetime.now()}\n")
            f.write("=" * 80 + "\n")
            f.write("Top5根因:\n")
            for i, rc in enumerate(ranks, 1):
                f.write(f"{i}. {rc}\n")
            f.write("=" * 80 + "\n")
            f.write("完整报告:\n")
            f.write(report)
        
        print(f"\n💾 完整报告已保存到: {report_file}")
    
    # 分析结果
    print(f"\n" + "=" * 80)
    print("🔬 分析建议")
    print("=" * 80)
    
    cpu_related = [rc for rc in ranks if 'cpu' in rc.lower()]
    if cpu_related:
        print(f"\n✅ 检测到 {len(cpu_related)} 个CPU相关根因:")
        for rc in cpu_related:
            print(f"  • {rc}")
        print(f"\n💡 建议:")
        print(f"  1. 检查这些服务的CPU使用率")
        print(f"  2. 查看是否有CPU密集型操作")
        print(f"  3. 检查是否需要扩容或优化")
    else:
        print(f"\n⚠️  Top5根因中未直接出现CPU关键词")
        print(f"  但这可能是:")
        print(f"  1. CPU故障的间接影响（如延迟、错误等）")
        print(f"  2. 报告解析需要优化")
        print(f"  3. 检查原始报告中的详细信息")
    
    print(f"\n" + "=" * 80)
    print("✅ 分析完成!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ 错误: {e}")
    import traceback
    traceback.print_exc()
    print(f"\n故障排查建议:")
    print(f"  1. 确认SREChat API服务正常运行:")
    print(f"     curl -XPOST {srechat_url}")
    print(f"  2. 检查网络连接")
    print(f"  3. 查看API返回的错误信息")
    sys.exit(1)

print(f"\n💡 提示:")
print(f"  - 如需分析其他时间点，运行: python verify_cpu_fault.py '<时间>'")
print(f"  - 如需配置DeepSeek以获得更好的解析: export DEEPSEEK_API_KEY='your-key'")
print()




