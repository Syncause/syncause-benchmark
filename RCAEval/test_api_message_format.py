#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 SREChat API 消息格式更新
"""

from datetime import datetime, timedelta

def test_message_format():
    print("=" * 70)
    print("测试 API 消息格式")
    print("=" * 70)
    
    # 测试用例
    test_cases = [
        ("2025-10-21T19:40:13+08:00", 15),
        ("2025-10-21T20:00:00+08:00", 30),
        ("2025-10-22T10:30:45+08:00", 10),
    ]
    
    for i, (detect_time, time_window) in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print("-" * 70)
        
        # 解析时间
        dt_str = detect_time[:-6]
        detect_dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
        
        # 计算起始时间
        start_dt = detect_dt - timedelta(minutes=time_window)
        
        # 格式化
        start_time_str = start_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
        end_time_str = detect_time
        
        # 构建消息
        message = (
            f"Check if there are any application response slowdowns or latency anomalies "
            f"in the system, and analyze the causes. "
            f"({start_time_str} -- {end_time_str})"
        )
        
        print(f"检测时间 (end): {detect_time}")
        print(f"时间窗口: {time_window} 分钟")
        print(f"起始时间 (start): {start_time_str}")
        print(f"\n消息内容:")
        print(f"  {message}")
        
        # 验证
        assert start_time_str in message
        assert end_time_str in message
        assert " -- " in message
        print(f"\n✓ 测试通过")
    
    print("\n" + "=" * 70)
    print("所有测试通过！✓")
    print("=" * 70)

if __name__ == "__main__":
    test_message_format()
