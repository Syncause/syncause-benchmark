
# Syncause Benchmark

[中文版 / Chinese Version](README_CN.md)

**Syncause Benchmark** provides a standardized evaluation framework to measure the performance of the **Syncause RCA** (Root Cause Analysis) method in system fault diagnosis tasks.
This project aims to openly demonstrate the problem-solving capability of Syncause in the AI SRE Agent domain and to promote reproducible, comparable, and transparent research for AI-driven incident analysis.

## Syncause RCA Method Overview

In the fields of RCA and AIOps, numerous approaches have achieved partial success on specific datasets, **yet challenges remain in terms of accuracy and real-world applicability**.
Traditional machine learning–based RCA solutions often face the following challenges:

- **Long training cycles**: Model training and fine-tuning in production environments typically take several weeks.

- **Lack of interpretability**: The generated results often lack transparent reasoning paths and interpretability, making it difficult for users to trust the outputs.

With the rapid advancement of Large Language Models (LLMs), new opportunities have emerged to address these challenges.
Syncause leverages LLMs to build an intelligent RCA Agent capable of delivering higher accuracy and faster response in root cause analysis tasks. Empirical results show that combining conventional observability signals (metrics, logs, and traces) with [**eBPF data**](https://syn-cause.com/blog/35e631d5-28fa-4c46-9f44-54f84707a2a4/) significantly improves diagnostic reliability and precision.

By utilizing the reasoning capabilities of LLMs, Syncause makes RCA a **white-box process**—its inference logic and decision paths are fully visible to users.
Recognizing that no RCA model is 100% accurate, Syncause introduces a trust-oriented approach: every output is grounded in real system observations. Even when the exact root cause is not immediately identified, the system visualizes intermediate hypotheses, validation paths, and **findings**. These findings provide valuable investigative clues, reduce repetitive work, and significantly shorten incident resolution time.

This benchmark will continue to track and update the accuracy and behavior of different LLMs under diverse test scenarios, gradually expanding the evaluation dimensions to reflect Syncause’s performance across varied environments.
The current results are based on the **Syncause Beta** version, and subsequent releases will be published and versioned in this repository.

## Dataset and Evaluation Methodology

### Dataset Description

The test dataset is based on the [**RCAEval**](https://github.com/phamquiluan/RCAEval) project and has been extended with **Syncause-specific eBPF metrics**.

The dataset includes:

* **Failure Scenarios**: Covers Kubernetes, microservices, networking, and storage fault types
* **Log Data**: System, application, and error logs
* **Metric Data**: Performance metrics and resource utilization
* **Trace Data**: Distributed tracing data
* **Annotations**: Expert-labeled ground-truth root causes and resolutions

## Evaluation Method

All experiments are conducted using the standardized framework provided by [**RCAEval**](https://github.com/phamquiluan/RCAEval).
A new algorithm named **Syncause RCA** was added to the RCAEval framework, and all benchmark runs and reports are generated through it.

### Accuracy Metric: AC@k (Accuracy@k)

`AC@k` represents the probability that the true root cause appears within the top `k` ranked predictions produced by an RCA method.
In simple terms, it answers: *“If I only check the top `k` suspects recommended by the model, what is the chance that I’ll find the actual cause?”*

The score ranges from 0 to 1. A higher value (closer to 1) indicates that the RCA approach can rank the correct root cause closer to the top, reflecting stronger diagnostic precision.

## Evaluation Results

### Train Ticket Scenario
Evaluation Date: 2025-11-07

#### Root Cause Service Identification Accuracy

For services `ts-travel-service`, `ts-train-service`, and `ts-route-service` with CPU increase, memory increase, network delay, and packet loss faults injected, the accuracy **with Syncause eBPF data assistance** is as follows:

| Model | Cases | AC@1 Accuracy | AC@3 Accuracy | AC@5 Accuracy |
| --- | --- | --- | --- | --- |
| grok-4-fast-non-reasoning | 30 | 86.67% (20/30) | 96.67% (29/30) |  \ |
| qwen-plus | 30 | 90% (27/30) | 96.67% (29/30) |  \ |

For comparison, without Syncause eBPF data assistance, the accuracy is as follows:

| Model | Cases | AC@1 Accuracy | AC@3 Accuracy | AC@5 Accuracy |
| --- | --- | --- | --- | --- |
| grok-4-fast-non-reasoning | 30 | 60% (18/30) | 93.33% (28/30) |  \ |
| qwen-plus | 30 | 60% (18/30) | 90% (27/30) |  \ |

> **Note:** Results will be continuously updated as models and methods evolve. Future versions will include additional scenarios and model comparisons.


### Cost Efficiency

Average **token consumption** and **execution latency** per case: 

| Model | LLM Calls | Input Tokens | Output Tokens | Total Cost (USD) | Latency (s) |
| --- | --- | --- | --- | --- | --- |
| grok-4-fast-non-reasoning | 37 | 209,678 | 12,234 | $0.041 | 138s |
| qwen-plus | 25 | 139,279 | 7,324 | $0.056 | 154s |


## Reproduction Guide

### 1. Environment Setup

```bash
# Enter the RCAEval directory
cd RCAEval

# Install dependencies
pip install -r requirements.txt
```

### 2. Data Preparation

```bash
# Access the Syncause platform
# 1. Visit https://syn-cause.com/
# 2. Follow the on-screen instructions to install the Syncause platform

# Import benchmark datasets (Contact us for datasets)
cd backupscript
./backup_scripts/victoriametrics_import.sh vm_backup_20241024_110000.tar.gz
./backup_scripts/clickhouse_import.sh clickhouse_backup_20241024_110000.tar.gz apo_restore
```

### 3. Run the Benchmark

```bash
# Execute RCAEval benchmark
python test_srechat_with_error_inject.py
```

### 4. Retrieve Results

#### From Log Files

```bash
# View benchmark logs
tail -f logs/benchmark.log

# Extract accuracy metrics
grep "Accuracy" logs/benchmark.log
grep "Top-1" logs/benchmark.log
grep "Top-3" logs/benchmark.log
grep "Top-5" logs/benchmark.log
```

#### From Braintrust Dashboard

```bash
# View Braintrust experiment results
# URL: https://www.braintrust.dev/app/your-org/p/Syncause-Benchmark
# Metrics available:
# - Total Cost
# - Average Cost
# - Cost per Test
```

## Contribution Guidelines

Contributions are welcome — including new test cases, data extensions, or algorithm improvements.

1. Fork this repository
2. Create a feature branch
3. Commit your changes
4. Submit a Pull Request

## License

This project is released under the [MIT License](LICENSE).
