# AgentSRE 基准测试

[English Version](README.md)

## 项目简介

本项目旨在记录和评估SynCause平台的AI智能体-AgentSRE在系统根因分析领域的基准测试。通过标准化的测试流程，我们能够客观地比较不同模型在故障诊断任务中的性能，包括Top-1、Top-3、Top-5准确率以及成本效益分析。
我们认为使用AI智能体配合ebpf数据（todo:链接待完善，指向ebpf数据的作用）进行根因分析将极大提升rca的准确率-在top1准确率做到95%以上、top3准确率做到100…%。为此我们设立了这个测试集来验证目标，并且还将不断扩展测试集。

## 测试数据集来源和测试方法

### 数据集描述
测试数据集来源于 [RCAEval](https://github.com/phamquiluan/RCAEval) 项目，并对数据集进行了拓展，增加了ebpf指标数据。
数据集在backupdata目录,数据集包含：

- **故障场景**: 涵盖Kubernetes、微服务、网络、存储等多种故障类型
- **日志数据**: 包含系统日志、应用日志、错误日志等
- **指标数据**: 性能指标、资源使用情况等
- **标注信息**: 专家标注的真实根因和解决方案

## 测试方法
我们完全使用了[RCAEval](https://github.com/phamquiluan/RCAEval) 项目来进行标准化测试，在该项目增加了一种新的根因分析算法（agentsre分析法），由RCAEval发起测试并生成测试报告。

## 测试结果

### 模型准确率对比

| 模型 | Top-1准确率 | Top-3准确率 | Top-5准确率 | 总测试数 | 成功率 |
|------|-------------|-------------|-------------|----------|--------|
| gpt-4o | 52% | 78% | 89% | 105 | 🟡 52% |
| claude-3.5-sonnet | 82% | 94% | 98% | 105 | 🟢 82% |
| gpt-4.1 | 67% | 85% | 93% | 105 | 🟡 67% |
| gpt-5 | 74% | 88% | 95% | 105 | 🟡 74% |
| deepseek-v3.1 | 75% | 89% | 96% | 105 | 🟡 75% |
| qwen3-next-80b | 55% | 79% | 90% | 105 | 🟡 55% |

### 模型成本对比

| 模型 | 测试数 | 平均成本 | 最小成本 | 最大成本 | 总成本 |
|------|--------|----------|----------|----------|--------|
| gpt-4o | 93 | $0.18 | $0.03 | $1.00 | $16.67 |
| claude-3.5-sonnet | 95 | $0.25 | $0.06 | $1.01 | $22.85 |
| gpt-4.1 | 94 | $0.11 | $0.02 | $0.66 | $10.68 |
| gpt-5 | 94 | $0.19 | $0.02 | $0.59 | $17.43 |
| deepseek-v3.1 | 95 | $0.08 | $0.01 | $0.35 | $7.60 |
| qwen3-next-80b | 95 | $0.06 | $0.01 | $0.28 | $5.70 |

### 模型延迟对比

| 模型 | 平均(秒) | 最小(秒) | 最大(秒) | P50(秒) | P95(秒) |
|------|----------|----------|----------|---------|---------|
| gpt-4o | 26.6 | 8.0 | 67.1 | 25.9 | 55.3 |
| claude-3.5-sonnet | 48.9 | 9.8 | 263.9 | 43.4 | 100.8 |
| gpt-4.1 | 40.7 | 5.5 | 645.1 | 25.4 | 51.7 |
| gpt-5 | 138.5 | 17.4 | 859.1 | 81.6 | 752.3 |
| deepseek-v3.1 | 75.5 | 21.1 | 221.1 | 68.2 | 145.3 |
| qwen3-next-80b | 45.2 | 12.3 | 156.7 | 38.9 | 89.4 |

### 每类故障的准确度

## 复现步骤

### 1. 环境准备

```bash
# 1. 进入测试
cd RCAEval

# 2. 安装依赖
pip install -r requirements.txt

```

### 2. 数据准备

```bash
# 访问SynCause平台
# 1. 打开 https://syn-cause.com/
# 2. 按照网页提示安装SynCause平台

# 导入测试数据
cd backupscript
./backup_scripts/victoriametrics_import.sh vm_backup_20241024_110000.tar.gz
./backup_scripts/clickhouse_import.sh clickhouse_backup_20241024_110000.tar.gz apo_restore
```

### 3. 运行基准测试

```bash
# 运行RCAEval基准测试
python test_srechat_with_error_inject.py
```

### 4. 获取结果

#### 从日志获取准确率
```bash
# 查看测试日志
tail -f logs/benchmark.log

# 提取准确率信息
grep "Accuracy" logs/benchmark.log
grep "Top-1" logs/benchmark.log
grep "Top-3" logs/benchmark.log
grep "Top-5" logs/benchmark.log
```

#### 从Braintrust获取成本信息
```bash
# 查看Braintrust实验结果
# 访问: https://www.braintrust.dev/app/your-org/p/AgentSRE-Benchmark
# 在实验页面查看:
# - 总成本 (Total Cost)
# - 平均成本 (Average Cost)
# - 每次测试成本 (Cost per Test)
```

## 项目结构

```
agentsre-benchmark/
├── README.md                 # 项目说明文档 (英文)
├── README_CN.md             # 项目说明文档 (中文)
├── requirements.txt          # Python依赖
├── run_benchmark.py         # 基准测试主脚本
├── testdata/                # 测试数据目录
│   ├── import_data.py       # 数据导入脚本
│   └── syncause_dataset.json # SynCause数据集
├── results/                 # 测试结果目录
│   ├── benchmark_results.json
│   └── braintrust_data.json
├── reports/                 # 报告目录
│   └── benchmark_report.html
└── logs/                   # 日志目录
    └── benchmark.log
```

## 贡献指南

欢迎提交新的测试用例和改进建议！

1. Fork 本项目
2. 创建特性分支
3. 提交更改
4. 发起 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**注意**: 本基准测试结果会定期更新，请关注最新版本。
