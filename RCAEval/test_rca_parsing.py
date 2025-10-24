#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试RCA解析逻辑
"""

import json

# 你提供的JSON数据
test_json = """data: {"type":"CUSTOM","name":"AgentToolDisplay","value":{"toolCallName":"result","title":"Root Cause Analysis Result","content":{"title":"Root Cause Analysis","fields":[{"key":"summary","label":"Summary","children":"### System Summary\\nThe system is degraded due to response slowdowns and latency issues in three key services during the last 15 minutes. Three main root causes were found, linked to high CPU usage from application code handling external dependencies and increased network delays. This led to slower seat bookings, route planning, and travel plan processing, affecting user requests without any error logs.\\n\\n### Root Cause Report\\n| Node / Service | Evidence | RootCause | Impact | Recommended Actions |\\n|----------------|----------|-----------|--------|---------------------|\\n| ts-seat-service | CPU usage rose to 15.52% (from 12.48% average) with slight network delay increase to 0.002s. | 🔍 High CPU from application code issues in handling dependencies → processing delays. | Slower seat booking responses for users. | 🛠️ Check code for excessive nesting and consider version rollback; scale CPU resources by 20%. |\\n| ts-route-plan-service | Network round-trip time spiked to 0.010s (10x average) with CPU up to 9.67% (from 7.91%). | 🔍 Elevated network delays from poor quality → amplified by CPU strain in dependency calls. ⚠️ Minor thread bottlenecks. | Delays in route planning features. | 🛠️ Tune connection pools and profile memory; add circuit breakers for dependencies. |\\n| ts-travel-plan-service | CPU increased to 10.42% (from 7.81%) and network delay to 0.002s (from 0.0007s). | 🔍 High CPU from code processing dependencies → overall latency rise. ⚠️ Moderate I/O pressure. | Slowdowns in travel plan generation. | 🛠️ Refactor high-latency calls and increase thread pools; monitor I/O and set latency alerts. |\\n\\n*Data analyzed from system metrics and traces over the last inspection window. View the full evidence chain and detailed metrics in the right panel for the complete analysis report! 📊*"},{"key":"report","label":"RCA Report","children":"# Root Cause Analysis Report: Application Response Slowdowns and Latency Anomalies (Last 15 Minutes)\\n\\n**Report Overview** 📋  \\nThis report analyzes latency anomalies and response slowdowns in the ts-seat-service, ts-route-plan-service, and ts-travel-plan-service applications during the period from 2025-10-14T18:05:00+08:00 to 2025-10-14T18:20:00+08:00. Based on eBPF data, metrics, logs, and traces, the primary issues stem from abnormal external call latencies, indicating dependency problems. Metrics show elevated CPU usage and network RTT across services, with no log errors. Traces confirm delays in inter-service calls but are secondary to metrics. Each service is analyzed independently, prioritizing metrics (CPU and RTT anomalies) as root causes, followed by traces for correlation. No TPS data is available, so request overload is not assumed. Root causes focus on high CPU usage (potentially from code logic handling dependencies) and network-related delays (due to RTT increases), pointing to downstream service interactions without direct network packet loss evidence.\\n\\n## Root Cause Identification 🔍\\n\\n### ts-seat-service\\n- **Failure Occurrence Time**: 2025-10-14T18:05:00+08:00 to 2025-10-14T18:20:00+08:00 (consistent exceedance of historical averages in net and epoll threads).  \\n- **Root Cause Component**: ts-seat-service application threads (net and epoll primarily).  \\n- **Root Cause**: High CPU usage combined with abnormal external call latency, likely due to dependency issues in downstream services causing processing delays. 📈 (100% net threads and 88.89% epoll threads affected; CPU anomaly low at 0.20% but metrics show 15.52% average CPU increase).  \\n\\n### ts-route-plan-service\\n- **Failure Occurrence Time**: 2025-10-14T18:05:00+08:00 to 2025-10-14T18:20:00+08:00 (sudden onset in majority threads).  \\n- **Root Cause Component**: ts-route-plan-service application threads (net and epoll dominant).  \\n- **Root Cause**: Elevated network RTT and high CPU usage from abnormal external calls to dependencies, leading to thread latency spikes. 📈 (95.65% net and epoll threads affected; CPU at 9.67% average increase, RTT from 0.001s to 0.010s).  \\n\\n### ts-travel-plan-service\\n- **Failure Occurrence Time**: 2025-10-14T18:05:00+08:00 to 2025-10-14T18:20:00+08:00 (persistent in net/epoll, moderate in CPU/runq).  \\n- **Root Cause Component**: ts-travel-plan-service application threads (net, epoll, and CPU).  \\n- **Root Cause**: Increased CPU load and network RTT due to dependency call delays, resulting in overall response slowdowns. 📈 (94.44% net and epoll threads affected; CPU at 10.42% average increase, moderate 6.80% CPU thread anomaly).  \\n\\n## Analysis Logic 📝\\n\\n### ts-seat-service\\n➡️ **Metrics First**: CPU usage rose 15.52% above average (12.48%), correlating with net thread latency anomalies (100% affected) and slight RTT increase (0.002s vs. 0.001s avg), suggesting high CPU from inefficient code handling external dependencies. Receive bandwidth up 0.08MB indicates minor I/O pressure but not primary.  \\n➡️ **Logs Second**: No errors in 50 logs, ruling out explicit failures like timeouts; anomalies likely from resource saturation not captured in error logs.  \\n➡️ **Traces Last**: Average latency 18,500ns (max 45,000ns) with 85 calls shows no errors but confirms dependency delays propagating to this service. Overall, metrics-derived root cause: dependency-induced CPU strain, not pure network (RTT minor). No multi-app interaction prioritized here.  \\n\\n### ts-route-plan-service\\n➡️ **Metrics First**: Network RTT spiked to 0.010s (10x average), alongside 9.67% CPU increase (from 7.91%), tying to high net/epoll anomalies (95.65% threads); low runq/file impacts suggest processing bottlenecks from external calls.  \\n➡️ **Logs Second**: Zero errors in 50 logs, indicating issues like memory leaks (preliminary direction) manifest as latency without loggable events.  \\n➡️ **Traces Last**: High average latency 450,000ns (max 1,161,000ns) over 25 calls, with delays in calls to ts-travel-service (e.g., 316,000ns to 800,000ns), but metrics prioritize RTT/CPU as root (network congestion amplifying dependencies). Single-app focus: internal code logic exacerbating dependency waits.  \\n\\n### ts-travel-plan-service\\n➡️ **Metrics First**: CPU up 10.42% (from 7.81%) and RTT to 0.002s (from 0.0007s), aligning with moderate CPU/runq anomalies (6.80%/10.48% threads) and high net/epoll (94.44%); no file anomalies, pointing to CPU-driven slowdowns from dependency processing.  \\n➡️ **Logs Second**: No errors in 100 logs, consistent with network I/O bottlenecks (preliminary) not triggering errors but causing saturation.  \\n➡️ **Traces Last**: Elevated latency 650,000ns average (max 1,704,000ns) over 60 calls, including spans to ts-seat-service exceeding 100,000ns in 20% of traces; however, metrics emphasize CPU/RTT as core, with traces showing propagation. Root derived: dependency issues via high CPU, not isolated network.  \\n\\n## Root Cause Evidence Chain 📊\\n\\n### ts-seat-service\\n- 📈 **Key Evidence**: eBPF shows 100% net thread latency anomaly and 88.89% epoll, with CPU metrics at 15.52% (up from 12.48%); RTT 0.002s (slight increase); traces confirm 18,500ns avg latency but no errors. Logs: 0 errors/50 total.  \\n- 📋 **Metrics Summary Table** (Time Range: 18:05-18:20):  \\n\\n| Metric/Time | Value | Historical Avg | Anomaly Icon |\\n|-------------|-------|----------------|--------------|\\n| 📈 CPU Usage (Avg) | 15.52% | 12.48% | 🚨 High |\\n| 🌐 Network RTT (Avg) | 0.002s | 0.001s | ⚠️ Moderate |\\n| 💾 Receive Bandwidth | 0.08MB | 0.064MB | ⚠️ Moderate |\\n| ⏱️ Avg Latency (Traces) | 18,500ns | N/A | 📊 Elevated |\\n\\n- 🔍 **Chain**: Metrics (CPU/RTT spikes) ➡️ Indicate dependency load ➡️ Traces show call delays ➡️ No log errors confirm non-fatal saturation.  \\n\\n### ts-route-plan-service\\n- 📈 **Key Evidence**: eBPF net/epoll anomalies at 95.65%; CPU 9.67% (up from 7.91%); RTT 0.010s spike; traces reveal 450,000ns avg latency with dependency call increases (316,000ns+). Logs: 0 errors/50 total.  \\n- 📋 **Metrics Summary Table** (Time Range: 18:05-18:20):  \\n\\n| Metric/Time | Value | Historical Avg | Anomaly Icon |\\n|-------------|-------|----------------|--------------|\\n| 📈 CPU Usage (Avg) | 9.67% | 7.91% | 🚨 High |\\n| 🌐 Network RTT (Avg) | 0.010s | 0.001s | 🚨 High |\\n| ⏱️ Max Latency (Traces) | 1,161,000ns | N/A | 📊 Severe |\\n| ⚡ Runq Thread Anomaly | 4.46% affected | N/A | ⚠️ Low |\\n\\n- 🔍 **Chain**: Metrics (RTT/CPU elevation) ➡️ Point to external call issues ➡️ Traces correlate with service spans ➡️ Clean logs rule out code crashes.  \\n\\n### ts-travel-plan-service\\n- 📈 **Key Evidence**: eBPF 94.44% net/epoll anomalies, 6.80% CPU threads; metrics CPU 10.42% (up from 7.81%), RTT 0.002s; traces 650,000ns avg with 20% spans >100,000ns to ts-seat-service. Logs: 0 errors/100 total.  \\n- 📋 **Metrics Summary Table** (Time Range: 18:05-18:20):  \\n\\n| Metric/Time | Value | Historical Avg | Anomaly Icon |\\n|-------------|-------|----------------|--------------|\\n| 📈 CPU Usage (Avg) | 10.42% | 7.81% | 🚨 High |\\n| 🌐 Network RTT (Avg) | 0.002s | 0.0007s | 🚨 High |\\n| ⏱️ Avg Latency (Traces) | 650,000ns | N/A | 📊 Elevated |\\n| ⚡ CPU Thread Anomaly | 6.80% affected | N/A | ⚠️ Moderate |\\n\\n- 🔍 **Chain**: Metrics (CPU/RTT rises) ➡️ Suggest dependency processing overhead ➡️ Traces highlight inter-call delays ➡️ No logs indicate subtle I/O bottlenecks.  \\n\\n## Recommended Actions 💡\\n\\n### ts-seat-service\\n- 🛠️ **Repair Suggestions**: Optimize code logic for external calls (e.g., add caching for seat queries to reduce CPU load); scale CPU resources temporarily by 20% to handle current saturation. Investigate downstream dependencies for quick fixes.  \\n- 🛡️ **Prevention**: Implement real-time CPU and RTT monitoring alerts (threshold: >15% CPU or >0.002s RTT); conduct periodic dependency health checks to avoid latency propagation.  \\n\\n### ts-route-plan-service\\n- 🛠️ **Repair Suggestions**: Tune connection pools for external calls to mitigate RTT spikes; profile memory usage to address potential leaks, reducing CPU strain during route planning. Restart service if latency persists beyond 5 minutes.  \\n- 🛡️ **Prevention**: Set up automated alerts for RTT >0.005s and CPU >9%; add circuit breakers for dependency calls to isolate failures early.  \\n\\n### ts-travel-plan-service\\n- 🛠️ **Repair Suggestions**: Refactor high-latency spans to ts-seat-service (e.g., batch queries); increase thread pool for CPU-bound tasks to alleviate 10%+ usage. Monitor and throttle I/O if bandwidth trends continue.  \\n- 🛡️ **Prevention**: Deploy latency thresholds in traces (>500,000ns) for alerts; perform regular code reviews for dependency handling to prevent CPU amplification in travel planning.  \\n\\n**Final Notes** 📌: Data is sufficient for this analysis, but configuration files (e.g., connection pool sizes) would aid deeper code-level insights. Total anomalies resolved via dependency focus; no single root cause across all, but patterns suggest shared downstream issues without direct multi-app association in this report. Contact for follow-up if issues recur."},{"key":"evidence","label":"Evidence","children":"# eBPF Analysis Results for Latency Anomalies (Last 15 Minutes)\\n\\n## Application Anomalies 📋\\n\\n### ts-seat-service\\n- 📈 **Net Thread Latency**: High anomaly (100% threads affected, majority anomalous).\\n- 📈 **Epoll Thread Latency**: Significant anomaly (88.89% threads affected).\\n- ⚡ **CPU Thread Latency**: Low anomaly (0.20% threads affected, only 1 thread anomalous).\\n- ⏱️ **Runq Thread Latency**: Notable anomaly (60% threads affected).\\n- 💾 **File Thread Latency**: Minimal anomaly (7.89% threads affected).\\n- 🌐 **Network RTT**: Normal (no anomalies).\\n\\n### ts-route-plan-service\\n- 📈 **Net Thread Latency**: High anomaly (95.65% threads affected).\\n- 📈 **Epoll Thread Latency**: High anomaly (95.65% threads affected).\\n- ⚡ **CPU Thread Latency**: Low anomaly (4.77% threads affected).\\n- ⏱️ **Runq Thread Latency**: Low anomaly (4.46% threads affected).\\n- 💾 **File Thread Latency**: No anomalies (0% affected).\\n- 🌐 **Network RTT**: Normal (no anomalies).\\n\\n### ts-travel-plan-service\\n- 📈 **Net Thread Latency**: High anomaly (94.44% threads affected).\\n- 📈 **Epoll Thread Latency**: High anomaly (94.44% threads affected).\\n- ⚡ **CPU Thread Latency**: Moderate anomaly (6.80% threads affected).\\n- ⏱️ **Runq Thread Latency**: Moderate anomaly (10.48% threads affected).\\n- 💾 **File Thread Latency**: No anomalies (0% affected).\\n- 🌐 **Network RTT**: Normal (no anomalies).\\n\\n**Note**: All services show conclusions of \\"External call latency is abnormal, likely a dependency issue\\" from eBPF data, indicating downstream dependencies as a primary cause despite preliminary directions.\\n\\n## Anomaly Statistics 📊\\n- **Total Anomalies**: 3 services affected.\\n- **Types of Anomalies**: Predominantly Net (100% services), Epoll (100% services), Runq (100% services), CPU (100% services but low ratios except ts-travel-plan-service), File (33% services with minimal impact).\\n- **Trend Changes**: Across the time range (2025-10-14T18:05:00+08:00 to 2025-10-14T18:20:00+08:00), net and epoll latencies show consistent exceedance of 20% over historical averages in majority threads, indicating sudden onset of slowdowns. CPU anomalies are sporadic and low-impact except in ts-travel-plan-service. No RTT spikes observed, suggesting internal processing or dependency delays.\\n\\n## Supporting Evidence 📚\\n- **ts-seat-service**:\\n  - **CPU Report**: [report1](#/cause/report/aea0011f1ecc4117913266492216aa49/2634d782b219a979?mutatedType=cpu_time), [report2](#/cause/report/aea0011f1ecc4117e58671fc2216aa49/44b10735aa46a979?mutatedType=cpu_time), [report3](#/cause/report/aea0011faed241172dff7b3a2516aa49/8ad2eff78c46a979?mutatedType=cpu_time)\\n  - **Network Report**: [report1](#/cause/report/410c7cde05a445304072d8a703877107/9056f4b7f318a979?mutatedType=network_time), [report2](#/cause/report/410c7cde65a54530f2cf3fa003877107/1a2371b6f418a979?mutatedType=network_time), [report3](#/cause/report/aea0011fa8d24117396b89712216aa49/dac3dbb9b219a979?mutatedType=network_time)\\n  - **Scheduling Report**: [report1](#/cause/report/aea0011f1ecc4117913266492216aa49/2634d782b219a979?mutatedType=scheduling_time), [report2](#/cause/report/410c7cde18a44530e234966e04877107/a4681e784145a979?mutatedType=scheduling_time),"}]}}}"""

def test_parsing():
    print("测试RCA解析逻辑")
    print("=" * 80)
    
    # 模拟SSE解析过程
    line_text = test_json
    if line_text.startswith("data: "):
        data_text = line_text[6:]  # 移除 "data: " 前缀
        print(f"提取的JSON数据长度: {len(data_text)}")
        
        try:
            data = json.loads(data_text)
            print(f"JSON解析成功，类型: {type(data)}")
            
            # 检查是否是Root Cause Analysis结果
            if isinstance(data, dict):
                print(f"data.type: {data.get('type')}")
                print(f"data.name: {data.get('name')}")
                
                if (data.get('type') == 'CUSTOM' and 
                    data.get('name') == 'AgentToolDisplay'):
                    
                    print("✅ 匹配到AgentToolDisplay")
                    value = data.get('value', {})
                    print(f"value.title: {value.get('title')}")
                    
                    if value.get('title') == 'Root Cause Analysis Result':
                        print("✅ 匹配到Root Cause Analysis Result")
                        content = value.get('content', {})
                        fields = content.get('fields', [])
                        print(f"fields数量: {len(fields)}")
                        
                        rca_results = []
                        # 提取summary和report
                        for field in fields:
                            print(f"field.key: {field.get('key')}")
                            if field.get('key') == 'summary':
                                print("✅ 找到summary字段")
                                rca_results.append({
                                    'type': 'summary',
                                    'content': field.get('children', '')
                                })
                            elif field.get('key') == 'report':
                                print("✅ 找到report字段")
                                rca_results.append({
                                    'type': 'report',
                                    'content': field.get('children', '')
                                })
                        
                        print(f"\n最终rca_results数量: {len(rca_results)}")
                        for i, result in enumerate(rca_results):
                            print(f"  {i+1}. {result['type']}: {len(result['content'])} 字符")
                        
                        if rca_results:
                            print("\n🎉 成功找到RCA结果！")
                            return True
                        else:
                            print("\n❌ 没有找到RCA结果")
                            return False
                    else:
                        print(f"❌ title不匹配: {value.get('title')}")
                        return False
                else:
                    print("❌ 不是AgentToolDisplay")
                    return False
            else:
                print("❌ 不是字典类型")
                return False
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析失败: {e}")
            return False
    else:
        print("❌ 不是SSE格式")
        return False

if __name__ == "__main__":
    success = test_parsing()
    print(f"\n测试结果: {'成功' if success else '失败'}")



