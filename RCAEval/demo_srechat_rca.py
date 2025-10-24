#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SREChat RCA 演示脚本

这个脚本演示如何使用SREChat RCA算法进行根因分析
"""

import os
from datetime import datetime, timedelta
from RCAEval.e2e import srechat_rca


def demo_basic_usage():
    """基本用法演示"""
    print("=" * 80)
    print("示例1: 基本用法 - 使用当前时间")
    print("=" * 80)
    
    # 最简单的用法：使用当前时间
    result = srechat_rca()
    
    print(f"\n检测时间: {result['detect_time']}")
    print(f"\nTop5根因:")
    for i, rc in enumerate(result['ranks'], 1):
        print(f"  {i}. {rc}")
    
    return result


def demo_with_specific_time():
    """指定时间演示"""
    print("\n" + "=" * 80)
    print("示例2: 指定检测时间")
    print("=" * 80)
    
    # 使用特定的时间
    detect_time = "2025-09-23T17:20:42+08:00"
    
    result = srechat_rca(
        detect_time=detect_time,
        time_window_minutes=15
    )
    
    print(f"\n检测时间: {result['detect_time']}")
    print(f"时间窗口: 15分钟")
    print(f"\nTop5根因:")
    for i, rc in enumerate(result['ranks'], 1):
        print(f"  {i}. {rc}")
    
    # 显示部分原始报告
    print(f"\n原始报告预览（前300字符）:")
    print("-" * 80)
    print(result['report'][:300])
    print("-" * 80)
    
    return result


def demo_with_timestamp():
    """使用时间戳演示"""
    print("\n" + "=" * 80)
    print("示例3: 使用时间戳（inject_time）")
    print("=" * 80)
    
    # 使用15分钟前的时间戳
    past_time = datetime.now() - timedelta(minutes=15)
    timestamp = past_time.timestamp()
    
    print(f"时间戳: {timestamp}")
    print(f"对应时间: {past_time}")
    
    result = srechat_rca(inject_time=timestamp)
    
    print(f"\n检测时间: {result['detect_time']}")
    print(f"\nTop5根因:")
    for i, rc in enumerate(result['ranks'], 1):
        print(f"  {i}. {rc}")
    
    return result


def demo_with_custom_api():
    """自定义API配置演示"""
    print("\n" + "=" * 80)
    print("示例4: 自定义API配置")
    print("=" * 80)
    
    # 完整配置所有参数
    result = srechat_rca(
        detect_time="2025-09-23T17:20:42+08:00",
        api_url=os.getenv("SRECHAT_API_URL", "http://192.168.1.6:28522/api/v1/srechat"),
        time_window_minutes=30,
        deepseek_api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    
    print(f"\nAPI地址: {os.getenv('SRECHAT_API_URL', 'http://192.168.1.6:28522/api/v1/srechat')}")
    print(f"时间窗口: 30分钟")
    print(f"DeepSeek配置: {'已配置' if os.getenv('DEEPSEEK_API_KEY') else '未配置（使用简单解析）'}")
    
    print(f"\nTop5根因:")
    for i, rc in enumerate(result['ranks'], 1):
        print(f"  {i}. {rc}")
    
    return result


def demo_error_handling():
    """错误处理演示"""
    print("\n" + "=" * 80)
    print("示例5: 错误处理")
    print("=" * 80)
    
    try:
        # 尝试使用一个无效的API地址
        result = srechat_rca(
            detect_time="2025-09-23T17:20:42+08:00",
            api_url="http://invalid-server:9999/api/v1/srechat"
        )
        
        print("即使API调用失败，算法也会返回结果（使用降级策略）")
        print(f"返回结果: {result['ranks']}")
        
    except Exception as e:
        print(f"捕获到异常: {e}")
        print("建议检查API配置和网络连接")


def compare_with_different_windows():
    """不同时间窗口对比"""
    print("\n" + "=" * 80)
    print("示例6: 不同时间窗口对比")
    print("=" * 80)
    
    detect_time = "2025-09-23T17:20:42+08:00"
    windows = [5, 15, 30]
    
    for window in windows:
        print(f"\n--- 时间窗口: {window}分钟 ---")
        result = srechat_rca(
            detect_time=detect_time,
            time_window_minutes=window
        )
        
        print(f"Top3根因:")
        for i, rc in enumerate(result['ranks'][:3], 1):
            print(f"  {i}. {rc}")


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "SREChat RCA 演示程序" + " " * 38 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # 检查环境变量配置
    print("环境配置检查:")
    print(f"  DEEPSEEK_API_KEY: {'已设置 ✓' if os.getenv('DEEPSEEK_API_KEY') else '未设置 (将使用简单解析)'}")
    print(f"  SRECHAT_API_URL: {os.getenv('SRECHAT_API_URL', '使用默认值')}")
    print()
    
    # 运行各个演示
    try:
        # 1. 基本用法
        demo_basic_usage()
        
        # 2. 指定时间
        demo_with_specific_time()
        
        # 3. 使用时间戳
        demo_with_timestamp()
        
        # 4. 自定义配置
        demo_with_custom_api()
        
        # 5. 错误处理
        # demo_error_handling()  # 可选：需要时取消注释
        
        # 6. 时间窗口对比
        # compare_with_different_windows()  # 可选：需要时取消注释
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("演示完成！")
    print("=" * 80)
    print("\n更多信息请参考: SREChat-RCA使用说明.md")
    print()


if __name__ == "__main__":
    main()




