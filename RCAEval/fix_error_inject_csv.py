#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 error_inject.csv 的 time 列空值

这个脚本会填充 time 列的 NaN 值，使其等于 inject_time - 30分钟
"""

import pandas as pd
import sys

def main():
    print("=" * 80)
    print("修复 error_inject.csv 的 time 列")
    print("=" * 80)
    
    # 1. 备份原文件
    print("\n步骤1: 读取原文件...")
    try:
        df = pd.read_excel("error_inject.csv")
        print(f"✓ 成功读取，共 {len(df)} 行")
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        sys.exit(1)
    
    # 2. 显示当前状况
    print("\n步骤2: 分析当前数据...")
    na_count = df['time'].isna().sum()
    print(f"  time 列空值数量: {na_count}/{len(df)} ({na_count/len(df)*100:.1f}%)")
    
    if na_count == 0:
        print("\n✓ time 列没有空值，无需修复！")
        return
    
    # 3. 显示修复方案
    print("\n步骤3: 修复方案...")
    print("  策略: time = inject_time - 30分钟")
    print("  影响行数:", na_count)
    
    # 4. 确认
    print("\n是否继续？这将修改 error_inject.csv 文件")
    print("  [y] 继续")
    print("  [n] 取消")
    print("  [b] 先备份再继续")
    
    choice = input("\n请选择 (y/n/b): ").strip().lower()
    
    if choice == 'n':
        print("\n已取消")
        return
    
    # 5. 备份（如果需要）
    if choice == 'b':
        backup_file = "error_inject.csv.backup"
        print(f"\n步骤4: 备份到 {backup_file}...")
        try:
            df.to_excel(backup_file, index=False)
            print(f"✓ 备份成功")
        except Exception as e:
            print(f"✗ 备份失败: {e}")
            sys.exit(1)
    
    # 6. 修复
    print("\n步骤5: 修复 time 列...")
    
    # 记录修复前的值
    before = df['time'].copy()
    
    # 填充策略：inject_time - 30分钟
    df['time'] = df.apply(
        lambda row: row['inject_time'] - pd.Timedelta(minutes=30) 
        if pd.isna(row['time']) else row['time'],
        axis=1
    )
    
    # 统计修复的行
    fixed_count = (before.isna() & df['time'].notna()).sum()
    print(f"✓ 已修复 {fixed_count} 行")
    
    # 7. 保存
    print("\n步骤6: 保存文件...")
    try:
        df.to_excel("error_inject.csv", index=False)
        print("✓ 保存成功")
    except Exception as e:
        print(f"✗ 保存失败: {e}")
        sys.exit(1)
    
    # 8. 验证
    print("\n步骤7: 验证修复结果...")
    df_verify = pd.read_excel("error_inject.csv")
    na_after = df_verify['time'].isna().sum()
    
    print(f"  修复前空值: {na_count}")
    print(f"  修复后空值: {na_after}")
    print(f"  修复数量: {na_count - na_after}")
    
    if na_after == 0:
        print("\n" + "=" * 80)
        print("✓ 修复完成！所有 time 列空值已填充")
        print("=" * 80)
        print("\n现在可以运行测试脚本了:")
        print("  python3 test_srechat_with_error_inject.py")
    else:
        print(f"\n⚠️  仍有 {na_after} 个空值未修复")
    
    # 9. 显示示例
    print("\n修复示例（前5行）:")
    print(df[['time', 'inject_time', 'service', 'error']].head())


if __name__ == "__main__":
    main()


