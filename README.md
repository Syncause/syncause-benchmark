# AgentSRE Benchmark

[中文版 / Chinese Version](README_CN.md)

## Project Introduction

This project aims to record and evaluate benchmark testing of SynCause platform's AI agent - AgentSRE in the field of system root cause analysis. Through standardized testing procedures, we can objectively compare the performance of different models in fault diagnosis tasks, including Top-1, Top-3, Top-5 accuracy rates and cost-effectiveness analysis.

## Test Dataset Source and Testing Methodology

### Dataset Description
The test dataset is sourced from the [RCAEval](https://github.com/phamquiluan/RCAEval) project, using the methodology provided by this project and paper to inject failures, and generating datasets using the SynCause platform.
The dataset is located in the `backupdata` directory and includes:

- **Failure Scenarios**: Covering various failure types including Kubernetes, microservices, networking, storage, etc.
- **Log Data**: Including system logs, application logs, error logs, etc.
- **Metrics Data**: Performance metrics, resource utilization, etc.
- **Annotation Information**: Expert-annotated ground truth root causes and solutions

## Testing Methodology
We completely used the [RCAEval](https://github.com/phamquiluan/RCAEval) project for standardized testing, adding a new root cause analysis algorithm (agentsre analysis method) to this project, with RCAEval initiating the tests and generating test reports.

## Test Results

### Model Accuracy Comparison

| Model | Top-1 Accuracy | Top-3 Accuracy | Top-5 Accuracy | Total Tests | Success Rate |
|-------|----------------|----------------|----------------|-------------|--------------|
| gpt-4o | 52% | 78% | 89% | 105 | 🟡 52% |
| claude-3.5-sonnet | 82% | 94% | 98% | 105 | 🟢 82% |
| gpt-4.1 | 67% | 85% | 93% | 105 | 🟡 67% |
| gpt-5 | 74% | 88% | 95% | 105 | 🟡 74% |
| deepseek-v3.1 | 75% | 89% | 96% | 105 | 🟡 75% |
| qwen3-next-80b | 55% | 79% | 90% | 105 | 🟡 55% |

### Model Cost Comparison

| Model | Tests | Avg Cost | Min Cost | Max Cost | Total Cost |
|-------|-------|----------|----------|----------|------------|
| gpt-4o | 93 | $0.18 | $0.03 | $1.00 | $16.67 |
| claude-3.5-sonnet | 95 | $0.25 | $0.06 | $1.01 | $22.85 |
| gpt-4.1 | 94 | $0.11 | $0.02 | $0.66 | $10.68 |
| gpt-5 | 94 | $0.19 | $0.02 | $0.59 | $17.43 |
| deepseek-v3.1 | 95 | $0.08 | $0.01 | $0.35 | $7.60 |
| qwen3-next-80b | 95 | $0.06 | $0.01 | $0.28 | $5.70 |

### Model Latency Comparison

| Model | Avg (s) | Min (s) | Max (s) | P50 (s) | P95 (s) |
|-------|---------|---------|---------|---------|---------|
| gpt-4o | 26.6 | 8.0 | 67.1 | 25.9 | 55.3 |
| claude-3.5-sonnet | 48.9 | 9.8 | 263.9 | 43.4 | 100.8 |
| gpt-4.1 | 40.7 | 5.5 | 645.1 | 25.4 | 51.7 |
| gpt-5 | 138.5 | 17.4 | 859.1 | 81.6 | 752.3 |
| deepseek-v3.1 | 75.5 | 21.1 | 221.1 | 68.2 | 145.3 |
| qwen3-next-80b | 45.2 | 12.3 | 156.7 | 38.9 | 89.4 |

### Accuracy by Failure Type

## Reproduction Steps

### 1. Environment Setup

```bash
# 1. Enter test directory
cd RCAEval

# 2. Install dependencies
pip install -r requirements.txt
```

### 2. Data Preparation

```bash
# Access SynCause platform
# 1. Open https://syn-cause.com/
# 2. Follow the web instructions to install SynCause platform

# Import test data
cd backupscript
./backup_scripts/victoriametrics_import.sh vm_backup_20241024_110000.tar.gz
./backup_scripts/clickhouse_import.sh clickhouse_backup_20241024_110000.tar.gz apo_restore
```

### 3. Run Benchmark

```bash
# Run RCAEval benchmark
python test_srechat_with_error_inject.py
```

### 4. Get Results

#### Get Accuracy from Logs
```bash
# View test logs
tail -f logs/benchmark.log

# Extract accuracy information
grep "Accuracy" logs/benchmark.log
grep "Top-1" logs/benchmark.log
grep "Top-3" logs/benchmark.log
grep "Top-5" logs/benchmark.log
```

#### Get Cost Information from Braintrust
```bash
# View Braintrust experiment results
# Visit: https://www.braintrust.dev/app/your-org/p/AgentSRE-Benchmark
# In the experiment page, check:
# - Total Cost
# - Average Cost
# - Cost per Test
```


## Project Structure

```
agentsre-benchmark/
├── README.md                 # Project documentation (English)
├── README_CN.md             # 项目说明文档 (Chinese)
├── requirements.txt          # Python dependencies
├── run_benchmark.py         # Main benchmark script
├── testdata/                # Test data directory
│   ├── import_data.py       # Data import script
│   └── syncause_dataset.json # SynCause dataset
├── results/                 # Test results directory
│   ├── benchmark_results.json
│   └── braintrust_data.json
├── reports/                 # Reports directory
│   └── benchmark_report.html
└── logs/                   # Logs directory
    └── benchmark.log
```

## Contributing

We welcome contributions of new test cases and improvement suggestions!

1. Fork this project
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: Benchmark results are updated regularly, please check for the latest version.