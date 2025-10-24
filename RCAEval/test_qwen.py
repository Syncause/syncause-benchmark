#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试使用Qwen-Plus模型解析RCA报告（README风格：仅一行输出）
"""

import sys, importlib.util
module_path = '/Users/jundi/PycharmProjects/RCAEval/RCAEval/e2e/srechat_rca.py'
spec = importlib.util.spec_from_file_location('srechat_rca', module_path)
srechat_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(srechat_module)  # type: ignore
srechat_rca = srechat_module.srechat_rca

import os

# 通过环境变量配置，避免额外提示
os.environ["LLM_API_KEY"] = "sk-1d400129fbb147458679b2f01f612612"
os.environ["LLM_MODEL_NAME"] = "qwen-plus"
os.environ["LLM_BASE_URL"] = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# 测试时间
detect_time = "2025-10-14T18:20:00+08:00"

result = srechat_rca(
    detect_time=detect_time,
    time_window_minutes=15,
    verbose=True,
)

ranks = result.get('ranks', [])
print("Top 5 root causes:", ranks[:5])

