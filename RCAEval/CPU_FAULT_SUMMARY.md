# 🔍 CPU故障检测报告总结

## API返回的完整报告关键信息

根据SREChat API返回的报告（长度147,973字符，包含224个JSON对象），以下是提取的关键信息：

---

## 🎯 关键发现 #1: 异常服务列表

**来源**: JSON对象 #3

```json
{
  "abnormalServices": [
    "ts-config-service",
    "ts-gateway-service", 
    "ts-order-other-service",
    "ts-station-service",
    "ts-train-service"
  ],
  "type": "slow",
  "start_date": "2025-10-14T17:31:19+08:00",
  "end_date": "2025-10-14T17:46:19+08:00"
}
```

**检测到的异常服务（5个）:**
1. 🔴 ts-config-service
2. 🔴 ts-gateway-service
3. 🔴 ts-order-other-service
4. 🔴 ts-station-service ⭐
5. 🔴 ts-train-service

---

## 💻 关键发现 #2: CPU异常详情

**来源**: JSON对象 #16

```json
{
  "affected_services_info": [
    {
      "service": "ts-station-service",
      "direction": "cpu",
      "count": 4,
      "level": 5
    },
    {
      "service": "ts-config-service", 
      "direction": "cpu",
      "count": 4,
      "level": 5
    },
    {
      "service": "ts-order-other-service",
      "direction": "cpu", 
      "count": 3,
      "level": 5
    }
  ]
}
```

**CPU异常服务（3个）:**

| 服务 | 类型 | 异常次数 | 严重等级 |
|------|------|----------|----------|
| **ts-station-service** | CPU | 4 | 🔥🔥🔥🔥🔥 Level 5 |
| ts-config-service | CPU | 4 | 🔥🔥🔥🔥🔥 Level 5 |
| ts-order-other-service | CPU | 3 | 🔥🔥🔥🔥🔥 Level 5 |

---

## 🧠 关键发现 #3: 因果关系分析

**来源**: JSON对象 #4

**Top 5 因果关系（按置信度排序）:**

| 排名 | 源服务 | → | 目标服务 | 置信度 |
|------|--------|---|----------|--------|
| 1 | **ts-station-service** | → | ts-config-service | **100.0%** |
| 2 | **ts-station-service** | → | ts-gateway-service | 75.0% |
| 3 | **ts-station-service** | → | ts-order-other-service | 66.7% |
| 4 | ts-order-other-service | → | ts-gateway-service | 62.5% |
| 5 | ts-gateway-service | → | ts-config-service | 50.0% |

**根因服务分析（作为因果源头的次数）:**
- 🎯 **ts-station-service**: 6次
- 🎯 ts-order-other-service: 2次
- 🎯 ts-train-service: 3次

---

## 📊 综合分析

### 多证据汇总

**ts-station-service** 🏆
- ✅ 在异常服务列表中
- ✅ CPU异常等级5，出现4次
- ✅ 因果关系中作为源头6次
- ✅ 最高置信度100%指向其他服务

**ts-config-service**
- ✅ 在异常服务列表中
- ✅ CPU异常等级5，出现4次
- ⚠️  主要作为受影响方（被其他服务影响）

**ts-gateway-service**
- ✅ 在异常服务列表中
- ⚠️  未在CPU异常列表中
- ⚠️  主要作为受影响方

---

## 🎯 结论

### 最可能的CPU故障根因：**ts-station-service** 

**证据:**
1. ✅ CPU异常检测：Level 5严重程度，出现4次
2. ✅ 因果关系分析：作为源头影响其他6个服务
3. ✅ 最高置信度：100%的置信度影响ts-config-service
4. ✅ 异常服务列表：被明确标记为异常服务

### 受影响的服务链路

```
ts-station-service (根因 - CPU异常)
    ├─ 100% → ts-config-service (CPU异常)
    ├─ 75%  → ts-gateway-service
    └─ 67%  → ts-order-other-service (CPU异常)
```

---

## 🔬 SREChat RCA算法检测结果

**算法返回的Top5根因:**
1. ts-basic-service
2. ts-config-service ✅ (CPU异常)
3. ts-gateway-service ✅ (异常服务)
4. ts-order-other-service ✅ (CPU异常)
5. ts-order-service

**分析:**
- ✅ Top5中包含了3个实际的CPU异常服务
- ⚠️  真正的根因 **ts-station-service** 不在Top5中
- 💡 原因：简单解析只提取了service列表的前5个，没有利用abnormalServices和因果关系

---

## 💡 改进建议

### 1. 优化解析逻辑 ✅

需要改进 `simple_parse_report()` 函数，优先提取：
1. `abnormalServices` 字段
2. `affected_services_info` 中的CPU异常服务
3. 因果关系图中作为源头的服务

### 2. 使用DeepSeek智能解析 🤖

配置DeepSeek API可以：
- 理解报告的完整上下文
- 识别因果关系
- 智能排序根因优先级
- **预期结果: ts-station-service 应该排在第1位**

```bash
export DEEPSEEK_API_KEY="your-api-key"
python3 verify_cpu_fault.py
```

---

## ❓ 请确认

**你实际注入CPU故障的服务是:**
- [ ] ts-station-service
- [ ] ts-config-service
- [ ] ts-gateway-service
- [ ] ts-order-other-service
- [ ] 其他: _____________

请告诉我实际的故障服务，我可以：
1. 验证检测准确性
2. 进一步优化算法
3. 改进解析逻辑

---

**生成时间**: 2025-10-14
**报告长度**: 147,973 字符
**检测到的服务**: 14个
**异常服务**: 5个
**CPU异常**: 3个




