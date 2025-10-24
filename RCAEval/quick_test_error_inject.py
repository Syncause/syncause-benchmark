#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试：使用 error_inject.csv 的第一个案例测试 SREChat RCA
"""

import pandas as pd
from RCAEval.e2e import srechat_rca

print("=" * 80)
print("快速测试: 使用 error_inject.csv 测试 SREChat RCA")
print("=" * 80)

# 1. 读取数据
print("\n步骤1: 读取 error_inject.csv...")
try:
    df = pd.read_excel("error_inject.csv")
    print(f"✓ 成功读取，共 {len(df)} 个测试案例")
    print(f"  列名: {df.columns.tolist()}")
except Exception as e:
    print(f"✗ 读取失败: {e}")
    print("提示: 确保 error_inject.csv 文件存在且格式正确")
    exit(1)

# 2. 显示第一个案例
print("\n步骤2: 查看第一个测试案例...")
row = df.iloc[0]
print(f"  测试开始时间: {row['time']}")
print(f"  故障注入时间: {row['inject_time']}")
print(f"  故障结束时间: {row['error_end_time']}")
print(f"  故障服务: {row['service']}")
print(f"  故障类型: {row['error']}")

# 3. 格式化时间 - 使用 error_end_time
print("\n步骤3: 格式化时间...")
detect_time = row['error_end_time'].strftime("%Y-%m-%dT%H:%M:%S+08:00")
print(f"  检测时间: {detect_time} (使用 error_end_time)")

# 4. 使用固定的时间窗口：error_end_time - 15分钟 到 error_end_time
time_window = 15  # 15分钟窗口，从故障结束往前推
print(f"  时间窗口: {time_window} 分钟 (error_end_time - 15分钟 到 error_end_time)")

# 5. 调用 SREChat RCA
print("\n步骤4: 调用 SREChat RCA...")
print("  注意: 这可能需要几秒到几十秒...")

try:
    result = srechat_rca(
        detect_time=detect_time,
        time_window_minutes=time_window,
        verbose=False  # 设置为 True 可以看到更多细节
    )
    
    print("✓ 调用成功!")
    
    # 6. 显示结果
    print("\n步骤5: 分析结果...")
    print("\n" + "-" * 80)
    print("根因分析结果:")
    print("-" * 80)
    
    ranks = result.get('ranks', [])
    raw_ranks = result.get('raw_ranks', [])
    
    print(f"\nTop {len(ranks)} 根因:")
    for i, rc in enumerate(ranks, 1):
        print(f"  {i}. {rc}")
    
    # 7. 评估结果
    print("\n" + "-" * 80)
    print("结果评估:")
    print("-" * 80)
    
    service = row['service']
    found = False
    rank_position = -1
    
    for i, rc in enumerate(raw_ranks or ranks, 1):
        if service.lower() in rc.lower():
            found = True
            rank_position = i
            break
    
    if found:
        print(f"✓ 成功找到故障服务 '{service}'")
        print(f"  排名位置: #{rank_position}")
        if rank_position == 1:
            print(f"  评价: 优秀！正确识别为首要根因")
        elif rank_position <= 3:
            print(f"  评价: 良好！在Top-3中")
        elif rank_position <= 5:
            print(f"  评价: 可接受，在Top-5中")
        else:
            print(f"  评价: 排名较低，需要优化")
    else:
        print(f"✗ 未找到故障服务 '{service}'")
        print(f"  建议: 检查API配置或调整时间窗口")
    
    # 8. 显示报告摘要（如果有）
    if 'rca_summary' in result and result['rca_summary']:
        print("\n" + "-" * 80)
        print("RCA摘要（前200字符）:")
        print("-" * 80)
        print(result['rca_summary'][:200])
        print("...")
    
    print("\n" + "=" * 80)
    print("测试完成!")
    print("=" * 80)
    
    print("\n下一步:")
    print("  1. 测试更多案例: python test_srechat_with_error_inject.py")
    print("  2. 查看详细指南: 使用error_inject测试SREChat指南.md")
    print("  3. 调整参数优化结果")
    
except Exception as e:
    print(f"✗ 调用失败: {e}")
    print("\n故障排查:")
    print("  1. 检查 SREChat API 是否运行")
    print("  2. 检查网络连接")
    print("  3. 配置环境变量:")
    print("     export SRECHAT_API_URL='http://your-server:port/api/v1/srechat'")
    print("     export LLM_API_KEY='your-api-key'")
    import traceback
    print("\n详细错误:")
    traceback.print_exc()

print()

