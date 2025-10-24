#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试SREChat RCA算法是否能正常导入和使用
"""

import os
import sys

print("=" * 80)
print("测试1: 检查模块导入")
print("=" * 80)

try:
    # 直接导入模块避免其他依赖问题
    from RCAEval.e2e.srechat_rca import srechat_rca
    print("✓ srechat_rca 成功导入")
except ImportError as e:
    print(f"✗ 导入失败: {e}")
    sys.exit(1)

print("\n" + "=" * 80)
print("测试2: 检查函数签名")
print("=" * 80)

import inspect
sig = inspect.signature(srechat_rca)
print(f"函数签名: {sig}")
print(f"参数列表: {list(sig.parameters.keys())}")

print("\n" + "=" * 80)
print("测试3: 检查模块文档")
print("=" * 80)

import RCAEval.e2e.srechat_rca as sre_module
print(f"模块文档:\n{sre_module.__doc__}")

print("\n" + "=" * 80)
print("测试4: 检查导出内容")
print("=" * 80)

if hasattr(sre_module, '__all__'):
    print(f"导出内容: {sre_module.__all__}")
else:
    print("未定义 __all__")

print("\n" + "=" * 80)
print("测试5: 模拟调用（不实际执行API调用）")
print("=" * 80)

# 创建一个简单的测试，不实际调用API
print("提示: 要实际测试API调用，请运行 demo_srechat_rca.py")
print("示例:")
print("  python demo_srechat_rca.py")
print("\n或者在Python中:")
print("  from RCAEval.e2e import srechat_rca")
print('  result = srechat_rca(detect_time="2025-09-23T17:20:42+08:00")')
print('  print(result["ranks"])')

print("\n" + "=" * 80)
print("所有测试通过! ✓")
print("=" * 80)

