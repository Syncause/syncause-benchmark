# Syncause Benchmark 

[英文版 / English Version](README.md)

**Syncause Benchmark** 提供了一组标准化的评估结果，用于量化在系统根因分析任务中 Syncause RCA (Root Cause Analysis) 方法的表现。该项目旨在公开 Syncause 在 AI SRE Agent 领域解决问题的能力，推动 AI SRE Agent 的可复现、可对比研究，提升透明度。

## Syncause RCA 方法简介
在根因分析和 AIOps 领域，尽管已有多种方法在特定数据集上取得一定效果，但整体仍面临准确率不足和工程化落地困难的问题。传统基于机器学习的根因分析方案通常存在以下问题：
- **落地周期长**：需要在真实生产环境中花费数周时间完成模型训练与参数微调。
- **缺乏可解释性**：生成的分析结果缺乏透明的推理路径和可解释性，用户难以信任输出内容。

随着大语言模型（Large Language Model, LLMs）能力的快速演进，这些问题出现了新的解决路径。Syncause 基于 LLMs 构建了智能化的 RCA Agent，可在根因分析场景中提供更高准确度和更强时效性的解决方案。实际测试表明，将指标、日志和链路追踪等传统可观测性数据与 [eBPF 数据](https://syn-cause.com/blog/35e631d5-28fa-4c46-9f44-54f84707a2a4/) 结合使用，能够显著提升分析结果的可靠性与精确度。

借助大语言模型的推理能力，Syncause 使根因分析过程实现了“白盒化”：推理逻辑与决策路径对用户完全可见。针对根因分析结果并非始终百分之百准确的现实，Syncause 提供了一种更具信任度的交互方式——系统输出的内容始终基于真实观测数据，即使未直接命中根因，也会以可视化形式呈现推理假设、验证路径及中间发现。这些发现往往能为用户提供关键线索，减少重复性排查工作，并显著缩短问题定位时间。

本项目将持续更新不同大语言模型在各类测试场景下的识别准确率与表现，并不断扩展评测维度，以展示 Syncause 在多样化环境中的性能表现。当前报告结果基于 Syncause Beta 版本，后续版本的优化与测试结果将持续在此项目中发布。

## 测试数据集来源和测试方法

### 数据集描述
测试数据集来源于 [RCAEval](https://github.com/phamquiluan/RCAEval) 项目，并在此基础上扩展了 Syncause 特有的 eBPF 指标。

数据集中包含以下数据：

- **故障场景**: 涵盖Kubernetes、微服务、网络、存储等多种故障类型
- **日志数据**: 包含系统日志、应用日志、错误日志等
- **指标数据**: 性能指标、资源使用情况等
- **标注信息**: 专家标注的真实根因和解决方案

## 测试方法
基于 [RCAEval](https://github.com/phamquiluan/RCAEval) 项目进行测试，该项目提供了标准化地测试与评估框架，我们在该框架中增加了一种新的根因分析算法——Syncause RCA，由RCAEval统一发起测试并生成结果报告。

### 衡量准确度指标：AC@k (Accuracy@k)
`AC@k` 表示该RCA方法所给出的排名前 `k` 个结果中，包含真实根因的概率。
简单来说，该值回答了：如果我只检查该方法推荐的前 `k` 个怀疑对象，我有多大几率能找到真正的故障根源？

`AC@k` 的得分范围为 0 到 1 之间。得分越高（越接近 1），代表该RCA方法的性能越好，这意味着它能更有效地将真实根因排在靠前的位置。

## 测试结果
### 根因服务识别准确度
在测试场景`Online Boutique`中，针对服务`emailservice`, `productcatalogservice`, `recommendationservice`的 11-12 种独立故障类型，基于`grok-4-fast-non-reasoning`模型，使用 Syncause RCA 进行根因分析，得到准确度如下表所示：

| 服务 | 案例数 | AC@1 准确度 | AC@3 准确度 | AC@5 准确度 |
| --- | --- | --- | --- | --- |
| emailservice | 12 | 66.7% | 91.7% | 91.7% |
| productcatalogservice | 11 | 63.6% | 90.9% | 90.9% |
| recommendationservice | 12 | 58.3% | 91.7% | 100% |

**说明**：结果将随着模型与方法更新持续修正。未来版本将补充更多场景与模型对比结果。

### 成本效益（Coming Soon）

后续版本将补充以下维度的评估：
- 每次分析的平均 Token 消耗
- 任务完成的响应时间

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
# 访问Syncause平台
# 1. 打开 https://syn-cause.com/
# 2. 按照网页提示安装Syncause平台

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
# 访问: https://www.braintrust.dev/app/your-org/p/Syncause-Benchmark
# 在实验页面查看:
# - 总成本 (Total Cost)
# - 平均成本 (Average Cost)
# - 每次测试成本 (Cost per Test)
```

## 项目结构

```
syncause-benchmark/
├── README.md                 # 项目说明文档 (英文)
├── README_CN.md             # 项目说明文档 (中文)
├── requirements.txt          # Python依赖
├── run_benchmark.py         # 基准测试主脚本
├── testdata/                # 测试数据目录
│   ├── import_data.py       # 数据导入脚本
│   └── Syncause_dataset.json # Syncause数据集
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

本项目采用 [MIT 许可证](LICENSE)。