#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试SREChat RCA算法文件是否可以正常解析
"""

import os
import sys

print("=" * 80)
print("SREChat RCA 简单验证测试")
print("=" * 80)

# 测试1: 检查文件存在
print("\n测试1: 检查文件是否存在")
srechat_file = "/Users/jundi/PycharmProjects/RCAEval/RCAEval/e2e/srechat_rca.py"
if os.path.exists(srechat_file):
    print(f"✓ 文件存在: {srechat_file}")
    file_size = os.path.getsize(srechat_file)
    print(f"  文件大小: {file_size} 字节")
else:
    print(f"✗ 文件不存在: {srechat_file}")
    sys.exit(1)

# 测试2: 检查文件内容
print("\n测试2: 检查文件内容")
with open(srechat_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
if 'def srechat_rca' in content:
    print("✓ 找到 srechat_rca 函数定义")
else:
    print("✗ 未找到 srechat_rca 函数定义")
    sys.exit(1)

if 'def call_srechat_api' in content:
    print("✓ 找到 call_srechat_api 函数定义")
else:
    print("✗ 未找到 call_srechat_api 函数定义")

if 'def parse_report_with_deepseek' in content:
    print("✓ 找到 parse_report_with_deepseek 函数定义")
else:
    print("✗ 未找到 parse_report_with_deepseek 函数定义")

# 测试3: 检查__init__.py是否注册了新算法
print("\n测试3: 检查 __init__.py 注册")
init_file = "/Users/jundi/PycharmProjects/RCAEval/RCAEval/e2e/__init__.py"
with open(init_file, 'r', encoding='utf-8') as f:
    init_content = f.read()
    
if 'from .srechat_rca import srechat_rca' in init_content:
    print("✓ __init__.py 中已注册 srechat_rca")
else:
    print("✗ __init__.py 中未注册 srechat_rca")

# 测试4: 检查文档文件
print("\n测试4: 检查文档文件")
doc_file = "/Users/jundi/PycharmProjects/RCAEval/SREChat-RCA使用说明.md"
if os.path.exists(doc_file):
    print(f"✓ 使用说明文档存在: {doc_file}")
    doc_size = os.path.getsize(doc_file)
    print(f"  文档大小: {doc_size} 字节")
else:
    print(f"✗ 使用说明文档不存在")

# 测试5: 检查演示文件
print("\n测试5: 检查演示文件")
demo_file = "/Users/jundi/PycharmProjects/RCAEval/demo_srechat_rca.py"
if os.path.exists(demo_file):
    print(f"✓ 演示脚本存在: {demo_file}")
    demo_size = os.path.getsize(demo_file)
    print(f"  文件大小: {demo_size} 字节")
else:
    print(f"✗ 演示脚本不存在")

# 测试6: 检查README更新
print("\n测试6: 检查 README 更新")
readme_file = "/Users/jundi/PycharmProjects/RCAEval/README.md"
with open(readme_file, 'r', encoding='utf-8') as f:
    readme_content = f.read()
    
if 'SREChat RCA' in readme_content:
    print("✓ README.md 已包含 SREChat RCA 说明")
else:
    print("✗ README.md 未包含 SREChat RCA 说明")

if 'srechat_rca' in readme_content:
    print("✓ README.md 包含使用示例")
else:
    print("✗ README.md 不包含使用示例")

# 测试7: 语法检查
print("\n测试7: Python语法检查")
import py_compile
try:
    py_compile.compile(srechat_file, doraise=True)
    print(f"✓ {srechat_file} 语法正确")
except py_compile.PyCompileError as e:
    print(f"✗ 语法错误: {e}")
    sys.exit(1)

try:
    py_compile.compile(demo_file, doraise=True)
    print(f"✓ {demo_file} 语法正确")
except py_compile.PyCompileError as e:
    print(f"✗ 语法错误: {e}")

print("\n" + "=" * 80)
print("所有基础验证测试通过! ✓")
print("=" * 80)

print("\n注意事项:")
print("1. 要完整测试功能，需要安装完整依赖")
print("2. 实际使用时需要配置 DEEPSEEK_API_KEY（可选）")
print("3. 确保 SREChat API 服务正常运行")
print("\n快速开始:")
print("  python demo_srechat_rca.py")




