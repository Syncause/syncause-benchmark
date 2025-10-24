# error_inject.csv 使用说明

## 📖 简介

`error_inject.csv` 是一个故障注入测试数据集，用于测试和评估根因分析（RCA）算法的性能。本文档说明如何使用这个数据集测试 `srechat_rca` 算法。

## 📂 数据集结构

### 文件信息
- **文件名**: `error_inject.csv`
- **格式**: Microsoft Excel 2007+ (虽然后缀是.csv)
- **大小**: 6行数据（案例数）
- **编码**: Excel二进制格式

### 数据字段

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `time` | datetime | 测试开始时间 | 2025-10-20 00:02:13 |
| `inject_time` | datetime | 故障注入的时间点 | 2025-10-20 00:32:13 |
| `error_end_time` | datetime | 故障结束时间 | - |
| `service` | string | 发生故障的服务名称 | checkoutservice |
| `error` | string | 故障类型 | cpu-stress, memory_leak |

### 当前数据集统计

```
总案例数: 6
服务分布:
  - checkoutservice: 6个案例

故障类型分布:
  - cpu-stress: 3个案例
  - memory_leak: 3个案例
```

## 🚀 快速开始

### 方式1: 使用快速测试脚本（最简单）

```bash
# 测试第一个案例，快速验证环境
python quick_test_error_inject.py
```

这个脚本会：
- ✅ 读取 error_inject.csv 的第一个案例
- ✅ 自动格式化时间和参数
- ✅ 调用 srechat_rca 进行根因分析
- ✅ 评估结果是否正确
- ✅ 显示友好的输出和建议

### 方式2: 使用完整测试脚本（推荐）

```bash
# 测试所有案例
python test_srechat_with_error_inject.py

# 只测试前2个案例
python test_srechat_with_error_inject.py --max-cases 2

# 测试单个案例（第1个，索引从0开始）
python test_srechat_with_error_inject.py --case-index 0

# 显示详细输出
python test_srechat_with_error_inject.py --verbose

# 组合使用
python test_srechat_with_error_inject.py --case-index 0 --verbose
```

### 方式3: 在Python代码中使用

```python
import pandas as pd
from RCAEval.e2e import srechat_rca

# 读取数据（注意使用 read_excel 而不是 read_csv）
df = pd.read_excel("error_inject.csv")

# 获取第一个案例
row = df.iloc[0]

# 格式化时间
detect_time = row['inject_time'].strftime("%Y-%m-%dT%H:%M:%S+08:00")

# 调用RCA
result = srechat_rca(
    detect_time=detect_time,
    time_window_minutes=15
)

# 查看结果
print("Top 5 根因:", result['ranks'])

# 检查是否找到正确服务
service = row['service']
found = any(service.lower() in rc.lower() for rc in result['raw_ranks'])
print(f"找到故障服务: {found}")
```

## 🔧 环境配置

### 必需的Python包

```bash
pip install pandas openpyxl requests
```

或者安装项目依赖：
```bash
pip install -r requirements.txt
```

### SREChat API 配置

```bash
# 设置API地址（如果不是默认值）
export SRECHAT_API_URL="http://192.168.1.6:28522/api/v1/srechat"

# 设置LLM API密钥（用于解析报告）
export LLM_API_KEY="sk-your-api-key"
export LLM_MODEL_NAME="qwen-plus"
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

### 验证配置

```bash
# 检查文件是否存在
ls -lh error_inject.csv

# 检查环境变量
echo $SRECHAT_API_URL
echo $LLM_API_KEY

# 测试API连接
curl -X POST $SRECHAT_API_URL \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "test"}]}'
```

## 📊 测试输出说明

### 快速测试脚本输出

```
================================================================================
快速测试: 使用 error_inject.csv 测试 SREChat RCA
================================================================================

步骤1: 读取 error_inject.csv...
✓ 成功读取，共 6 个测试案例
  列名: ['time', 'inject_time', 'error_end_time', 'service', 'error']

步骤2: 查看第一个测试案例...
  测试开始时间: 2025-10-20 00:02:13
  故障注入时间: 2025-10-20 00:32:13
  故障服务: checkoutservice
  故障类型: cpu-stress

步骤3: 格式化时间...
  检测时间: 2025-10-20T00:32:13+08:00
  时间窗口: 30 分钟

步骤4: 调用 SREChat RCA...
✓ 调用成功!

步骤5: 分析结果...

--------------------------------------------------------------------------------
根因分析结果:
--------------------------------------------------------------------------------

Top 5 根因:
  1. checkoutservice_cpu
  2. ts-order-service_latency
  3. ts-payment-service_latency
  4. ts-config-service_cpu
  5. ts-user-service_mem

--------------------------------------------------------------------------------
结果评估:
--------------------------------------------------------------------------------
✓ 成功找到故障服务 'checkoutservice'
  排名位置: #1
  评价: 优秀！正确识别为首要根因

================================================================================
测试完成!
================================================================================
```

### 完整测试脚本输出

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                              测试摘要                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

总测试数: 6
成功执行: 6 (100.0%)
找到根因: 5 (83.3%)

准确率统计:
  Top-1: 4/6 (66.7%)
  Top-3: 5/6 (83.3%)
  Top-5: 5/6 (83.3%)

详细结果:
--------------------------------------------------------------------------------
  ✓ 案例1: checkoutservice      cpu-stress      #1      
  ✓ 案例2: checkoutservice      cpu-stress      #1      
  ✓ 案例3: checkoutservice      cpu-stress      #2      
  ✓ 案例4: checkoutservice      memory_leak     #1      
  ✓ 案例5: checkoutservice      memory_leak     #3      
  ✗ 案例6: checkoutservice      memory_leak     未找到  
--------------------------------------------------------------------------------
```

## 🎯 使用场景

### 场景1: 验证算法是否正常工作

```bash
# 快速测试单个案例
python quick_test_error_inject.py
```

**目的**: 确保 srechat_rca 算法能正常调用和返回结果

### 场景2: 评估算法准确率

```bash
# 测试所有案例并查看统计
python test_srechat_with_error_inject.py
```

**目的**: 评估算法在不同故障类型下的表现

### 场景3: 调试特定案例

```bash
# 详细查看某个案例的分析过程
python test_srechat_with_error_inject.py --case-index 0 --verbose
```

**目的**: 深入了解算法的分析逻辑和中间结果

### 场景4: 参数调优

```python
# 测试不同时间窗口的影响
for window in [10, 15, 30, 60]:
    result = srechat_rca(
        detect_time=detect_time,
        time_window_minutes=window
    )
    # 比较结果...
```

**目的**: 找到最优的参数配置

### 场景5: 集成到CI/CD

```bash
# 在CI/CD管道中运行测试
python test_srechat_with_error_inject.py --max-cases 3
if [ $? -eq 0 ]; then
    echo "RCA tests passed"
else
    echo "RCA tests failed"
    exit 1
fi
```

**目的**: 自动化测试和质量保证

## 🔍 常见问题

### Q1: 为什么要用 `pd.read_excel()` 而不是 `pd.read_csv()`？

**A**: 虽然文件名是 `.csv`，但实际上是 Excel 格式（Microsoft Excel 2007+）。使用 `read_csv()` 会报错：
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x87
```

**解决方案**:
```python
# ✗ 错误
df = pd.read_csv("error_inject.csv")

# ✓ 正确
df = pd.read_excel("error_inject.csv")
```

### Q2: SREChat API 调用失败怎么办？

**A**: 检查以下几点：

1. **API 服务是否运行**:
   ```bash
   curl http://192.168.1.6:28522/api/v1/srechat
   ```

2. **网络连接**:
   ```bash
   ping 192.168.1.6
   ```

3. **环境变量配置**:
   ```bash
   export SRECHAT_API_URL="http://正确的地址:端口/api/v1/srechat"
   ```

### Q3: 为什么没有找到正确的故障服务？

**A**: 可能的原因：

1. **未配置 LLM API**: 没有配置 `LLM_API_KEY` 时，使用简单规则解析，准确率较低
   
   **解决**: 配置 LLM API
   ```bash
   export LLM_API_KEY="your-api-key"
   ```

2. **时间窗口不合适**: 窗口太短可能数据不足，太长可能引入噪音
   
   **解决**: 调整 `time_window_minutes` 参数
   ```python
   result = srechat_rca(detect_time=dt, time_window_minutes=30)
   ```

3. **SREChat 返回数据质量**: API 返回的报告中没有明确的根因信息
   
   **解决**: 查看原始报告，使用 `--verbose` 选项

### Q4: 如何添加更多测试案例？

**A**: 编辑 `error_inject.csv` 文件（使用Excel打开）：

1. 添加新行
2. 填写字段：
   - `time`: 测试开始时间
   - `inject_time`: 故障注入时间
   - `service`: 故障服务名称
   - `error`: 故障类型

或者用Python添加：
```python
import pandas as pd

# 读取现有数据
df = pd.read_excel("error_inject.csv")

# 添加新案例
new_case = pd.DataFrame({
    'time': ['2025-10-20 10:00:00'],
    'inject_time': ['2025-10-20 10:30:00'],
    'error_end_time': [''],
    'service': ['paymentservice'],
    'error': ['network-delay']
})

# 合并
df = pd.concat([df, new_case], ignore_index=True)

# 保存（注意：需要安装 openpyxl）
df.to_excel("error_inject.csv", index=False)
```

### Q5: 如何将结果保存到文件？

**A**: 修改测试脚本，添加保存功能：

```python
import json

# 在 test_srechat_with_error_inject.py 中添加
def save_results(results, filename="test_results.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    print(f"结果已保存到: {filename}")

# 在 main() 函数中调用
save_results(results)
```

## 📚 相关文档

- [使用error_inject测试SREChat指南.md](使用error_inject测试SREChat指南.md) - 详细指南
- [SRECHAT_RCA_更改总结.md](SRECHAT_RCA_更改总结.md) - 算法文档
- [demo_srechat_rca.py](demo_srechat_rca.py) - 使用示例
- [README.md](README.md) - 项目主文档

## 🛠️ 脚本文件说明

| 脚本文件 | 用途 | 推荐场景 |
|---------|------|---------|
| `quick_test_error_inject.py` | 快速测试单个案例 | 首次使用、验证环境 |
| `test_srechat_with_error_inject.py` | 完整测试框架 | 批量测试、性能评估 |
| `demo_srechat_rca.py` | 演示各种用法 | 学习API使用方法 |
| `test_srechat.py` | 简单导入测试 | 检查模块是否正常 |

## 💡 最佳实践

1. **首次使用**:
   ```bash
   # 1. 验证环境
   python test_srechat.py
   
   # 2. 快速测试
   python quick_test_error_inject.py
   
   # 3. 详细测试
   python test_srechat_with_error_inject.py --case-index 0 --verbose
   ```

2. **批量测试**:
   ```bash
   # 分批测试，避免API限流
   python test_srechat_with_error_inject.py --max-cases 3
   ```

3. **结果分析**:
   - 查看 Top-1 准确率：算法最重要的指标
   - 查看 Top-3/Top-5：评估候选根因质量
   - 分析失败案例：找出算法弱点

4. **参数优化**:
   - 调整时间窗口
   - 配置不同的 LLM 模型
   - 对比不同配置的结果

## 📈 性能基准

基于当前 6 个测试案例的初步测试（示例数据）：

| 指标 | 预期值 | 说明 |
|------|--------|------|
| Top-1 准确率 | 60-80% | 首位命中率 |
| Top-3 准确率 | 80-90% | 前三命中率 |
| Top-5 准确率 | 85-95% | 前五命中率 |
| 平均响应时间 | 10-30秒 | 包含API调用和解析 |

*注: 实际性能取决于API配置、网络环境和LLM选择*

## 🎉 总结

使用 `error_inject.csv` 测试 `srechat_rca` 的完整流程：

1. ✅ **安装依赖**: `pip install pandas openpyxl requests`
2. ✅ **配置环境**: 设置 API 地址和密钥
3. ✅ **快速验证**: `python quick_test_error_inject.py`
4. ✅ **批量测试**: `python test_srechat_with_error_inject.py`
5. ✅ **分析结果**: 查看准确率和详细报告
6. ✅ **优化参数**: 根据结果调整配置

开始测试吧！🚀


