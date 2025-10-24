#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 error_inject.csv 测试 SREChat RCA 算法

这个脚本从 error_inject.csv 读取故障注入记录，
然后使用 srechat_rca 对每个故障进行根因分析。
"""

import os
import sys
import pandas as pd
from datetime import datetime
from RCAEval.e2e import srechat_rca


def load_error_inject_csv(file_path="error_inject.csv"):
    """
    加载故障注入CSV文件
    
    Args:
        file_path: CSV文件路径
    
    Returns:
        DataFrame包含故障注入记录
    """
    try:
        # 尝试读取Excel格式（因为文件是Microsoft Excel 2007+格式）
        df = pd.read_excel(file_path)
        print(f"✓ 成功加载 {file_path}")
        print(f"  数据形状: {df.shape}")
        print(f"  列名: {df.columns.tolist()}")
        return df
    except Exception as e:
        print(f"✗ 加载失败: {e}")
        return None


def format_time_for_srechat(time_str):
    """
    将时间字符串转换为SREChat API需要的格式
    
    Args:
        time_str: 时间字符串（pandas datetime或字符串）
    
    Returns:
        格式化的时间字符串，如 "2025-10-20T00:32:13+08:00"
    """
    if isinstance(time_str, pd.Timestamp):
        dt = time_str.to_pydatetime()
    elif isinstance(time_str, str):
        dt = pd.to_datetime(time_str)
    else:
        dt = time_str
    
    # 格式化为ISO 8601格式，添加时区
    return dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")


def test_single_case(row, index, verbose=False):
    """
    测试单个故障案例
    
    Args:
        row: DataFrame的一行，包含故障注入信息
        index: 案例索引
        verbose: 是否显示详细信息
    
    Returns:
        测试结果字典
    """
    print("\n" + "=" * 80)
    print(f"案例 {index + 1}: {row['service']} - {row['error']}")
    print("=" * 80)
    
    # 提取信息
    inject_time = row['inject_time']
    error_end_time = row['error_end_time']
    service = row['service']
    error_type = row['error']
    
    # 使用 error_end_time 作为检测时间
    detect_time = format_time_for_srechat(error_end_time)
    
    print(f"故障注入时间: {inject_time}")
    print(f"故障结束时间: {error_end_time}")
    print(f"检测时间: {detect_time}")
    print(f"故障服务: {service}")
    print(f"故障类型: {error_type}")
    
    # 使用固定的时间窗口：error_end_time - 15分钟 到 error_end_time
    time_window = 15  # 15分钟窗口，从故障结束往前推15分钟
    
    print(f"时间窗口: {time_window} 分钟 (error_end_time - 15分钟 到 error_end_time)")
    
    try:
        # 调用SREChat RCA
        print("\n正在调用 SREChat RCA...")
        result = srechat_rca(
            detect_time=detect_time,
            time_window_minutes=time_window,
            verbose=verbose
        )
        
        # 显示结果
        print("\n" + "-" * 80)
        print("根因分析结果:")
        print("-" * 80)
        
        ranks = result.get('ranks', [])
        raw_ranks = result.get('raw_ranks', [])
        
        print(f"\nTop {len(ranks)} 根因 (格式化):")
        for i, rc in enumerate(ranks, 1):
            print(f"  {i}. {rc}")
        
        if raw_ranks and raw_ranks != ranks:
            print(f"\nTop {len(raw_ranks)} 根因 (原始):")
            for i, rc in enumerate(raw_ranks, 1):
                print(f"  {i}. {rc}")
        
        # 检查是否找到了正确的服务
        found = False
        rank_position = -1
        for i, rc in enumerate(raw_ranks or ranks, 1):
            if service.lower() in rc.lower():
                found = True
                rank_position = i
                break
        
        print("\n" + "-" * 80)
        print("评估:")
        print("-" * 80)
        if found:
            print(f"✓ 找到故障服务 '{service}' (排名: {rank_position})")
        else:
            print(f"✗ 未找到故障服务 '{service}'")
        
        # 显示RCA详细信息（如果有）
        if verbose and 'rca_summary' in result and result['rca_summary']:
            print("\n" + "-" * 80)
            print("RCA摘要:")
            print("-" * 80)
            print(result['rca_summary'][:500])  # 显示前500字符
        
        return {
            'index': index,
            'service': service,
            'error_type': error_type,
            'detect_time': detect_time,
            'found': found,
            'rank_position': rank_position,
            'ranks': ranks,
            'raw_ranks': raw_ranks,
            'success': True
        }
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        if verbose:
            traceback.print_exc()
        
        return {
            'index': index,
            'service': service,
            'error_type': error_type,
            'detect_time': detect_time,
            'found': False,
            'rank_position': -1,
            'error': str(e),
            'success': False
        }


def test_all_cases(df, verbose=False, max_cases=None):
    """
    测试所有故障案例
    
    Args:
        df: 故障注入DataFrame
        verbose: 是否显示详细信息
        max_cases: 最大测试案例数（None表示全部测试）
    
    Returns:
        所有测试结果的列表
    """
    results = []
    
    total_cases = len(df) if max_cases is None else min(max_cases, len(df))
    
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "开始批量测试 SREChat RCA" + " " * 39 + "║")
    print("╚" + "═" * 78 + "╝")
    print(f"\n总共 {total_cases} 个测试案例\n")
    
    for i, row in df.head(total_cases).iterrows():
        result = test_single_case(row, i, verbose=verbose)
        results.append(result)
        
        # 短暂暂停，避免API调用过快
        import time
        time.sleep(2)
    
    return results


def print_summary(results):
    """
    打印测试摘要
    
    Args:
        results: 测试结果列表
    """
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "测试摘要" + " " * 40 + "║")
    print("╚" + "═" * 78 + "╝")
    
    total = len(results)
    successful = sum(1 for r in results if r['success'])
    found = sum(1 for r in results if r['found'])
    
    print(f"\n总测试数: {total}")
    print(f"成功执行: {successful} ({successful/total*100:.1f}%)")
    print(f"找到根因: {found} ({found/total*100:.1f}%)")
    
    # 按排名统计
    top1 = sum(1 for r in results if r['rank_position'] == 1)
    top3 = sum(1 for r in results if 1 <= r['rank_position'] <= 3)
    top5 = sum(1 for r in results if 1 <= r['rank_position'] <= 5)
    
    print(f"\n准确率统计:")
    print(f"  Top-1: {top1}/{total} ({top1/total*100:.1f}%)")
    print(f"  Top-3: {top3}/{total} ({top3/total*100:.1f}%)")
    print(f"  Top-5: {top5}/{total} ({top5/total*100:.1f}%)")
    
    # 详细结果
    print("\n详细结果:")
    print("-" * 80)
    for r in results:
        status = "✓" if r['found'] else "✗"
        rank = f"#{r['rank_position']}" if r['found'] else "未找到"
        print(f"  {status} 案例{r['index']+1}: {r['service']:20s} {r['error_type']:15s} {rank:8s}")
    
    print("-" * 80)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="使用error_inject.csv测试SREChat RCA")
    parser.add_argument("--file", type=str, default="error_inject.csv", 
                       help="error_inject.csv文件路径")
    parser.add_argument("--max-cases", type=int, default=None,
                       help="最大测试案例数（默认全部）")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="显示详细信息")
    parser.add_argument("--case-index", type=int, default=None,
                       help="只测试指定索引的案例（从0开始）")
    args = parser.parse_args()
    
    # 检查环境配置
    print("\n环境配置检查:")
    print(f"  LLM_API_KEY: {'已设置 ✓' if os.getenv('LLM_API_KEY') or os.getenv('DEEPSEEK_API_KEY') else '未设置 (将使用简单解析)'}")
    print(f"  SRECHAT_API_URL: {os.getenv('SRECHAT_API_URL', '使用默认值')}")
    
    # 加载数据
    df = load_error_inject_csv(args.file)
    if df is None:
        sys.exit(1)
    
    # 测试
    if args.case_index is not None:
        # 测试单个案例
        if args.case_index >= len(df):
            print(f"✗ 案例索引 {args.case_index} 超出范围（共 {len(df)} 个案例）")
            sys.exit(1)
        
        row = df.iloc[args.case_index]
        result = test_single_case(row, args.case_index, verbose=True)
        results = [result]
    else:
        # 测试所有案例
        results = test_all_cases(df, verbose=args.verbose, max_cases=args.max_cases)
    
    # 打印摘要
    print_summary(results)
    
    print("\n测试完成！\n")


if __name__ == "__main__":
    main()

