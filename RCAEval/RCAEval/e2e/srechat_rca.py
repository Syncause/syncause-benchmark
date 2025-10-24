"""
SREChat RCA算法
这是一种基于远程API调用和大模型解析的RCA算法
只需要提供检测时间，算法会自己获取数据并返回根因
"""

import os
import json
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any
import warnings

warnings.filterwarnings("ignore")


def _infer_reason_suffix(report_text: str, service_name: str) -> str:
    """Infer a short reason suffix (e.g., cpu/mem/latency/disk/loss/socket) for a given service
    based on keywords in the report text around global context.

    The fallback is 'latency' to align with README examples.
    """
    text = (report_text or "").lower()

    # Common categories observed across the project
    # Prioritize more specific signals first
    if "memory" in text or "mem" in text:
        return "mem"
    if "cpu" in text or "runq" in text or "epoll" in text:
        return "cpu"
    if "disk" in text or "i/o" in text or "io " in text or "file i/o" in text:
        return "disk"
    if "packet loss" in text or "loss" in text:
        return "loss"
    if "socket" in text:
        return "socket"
    if "network" in text or "rtt" in text or "bandwidth" in text:
        # Some baselines use 'socket', but many examples show 'latency'
        # Prefer 'latency' unless socket explicitly appears
        return "latency"
    if "slow" in text or "delay" in text or "latency" in text or "response time" in text:
        return "latency"
    # Default fallback
    return "latency"


def _format_service_reasons(services: List[str], report_text: str) -> List[str]:
    formatted: List[str] = []
    seen = set()
    for svc in services:
        base = str(svc)
        if base in seen:
            continue
        seen.add(base)
        suffix = _infer_reason_suffix(report_text, base)
        formatted.append(f"{base}_{suffix}")
    return formatted


def _extract_rca_from_report(report_text: str) -> Dict[str, Any]:
    """Extract RCA summary, detailed report markdown, and services from the RCA table
    that was embedded into report_text when the stream contained AgentToolDisplay.

    Return keys:
      - rca_summary: Optional[str]
      - rca_report_markdown: Optional[str]
      - rca_services_from_table: List[str]
    """
    summary = None
    detailed = None
    services: List[str] = []
    if not report_text:
        return {
            "rca_summary": summary,
            "rca_report_markdown": detailed,
            "rca_services_from_table": services,
        }

    text = report_text
    # Try to extract the block we inserted
    # SUMMARY:
    if "SUMMARY:" in text:
        start = text.find("SUMMARY:") + len("SUMMARY:")
        # end before DETAILED REPORT or Original Response divider
        end = text.find("\n\nDETAILED REPORT:", start)
        if end == -1:
            end = text.find("\n\n===", start)
        if end == -1:
            end = start + 2000
        summary = text[start:end].strip()

    # DETAILED REPORT:
    if "DETAILED REPORT:" in text:
        dstart = text.find("DETAILED REPORT:") + len("DETAILED REPORT:")
        dend = text.find("\n\n===", dstart)
        if dend == -1:
            dend = dstart + 20000
        detailed = text[dstart:dend].strip()

    # Extract services from the markdown table (| ts-...service | ... |)
    lines = text.splitlines()
    for ln in lines:
        ln_stripped = ln.strip()
        if ln_stripped.startswith("|") and "service" in ln_stripped.lower():
            # header line, skip
            continue
        if ln_stripped.startswith("|") and ("ts-" in ln_stripped or "service" in ln_stripped.lower()):
            # try to capture the first cell as service name
            try:
                cells = [c.strip() for c in ln_stripped.strip('|').split('|')]
                if cells:
                    candidate = cells[0]
                    # backticks or plain
                    candidate = candidate.replace('`', '').strip()
                    # 更宽松的匹配：包含service或者ts-开头
                    if (candidate.endswith("service") or candidate.startswith("ts-")) and candidate not in services:
                        services.append(candidate)
            except Exception:
                pass
    
    # 如果表格解析失败，尝试正则表达式提取
    if not services:
        import re
        # 匹配 | ts-xxx-service | 格式
        table_pattern = r'\|\s*(ts-[a-z0-9-]+service)\s*\|'
        table_matches = re.findall(table_pattern, text, re.IGNORECASE)
        if table_matches:
            for svc in table_matches:
                if svc not in services:
                    services.append(svc)
    
    # 可选调试：打印解析结果（仅在verbose=True时）
    # if not services and "ts-" in text:
    #     print(f"DEBUG: 表格解析失败，文本中包含ts-: {text.count('ts-')}次")
    # elif services:
    #     print(f"DEBUG: 成功解析表格服务: {services}")

    return {
        "rca_summary": summary,
        "rca_report_markdown": detailed,
        "rca_services_from_table": services,
    }


def parse_report_with_llm(report_text: str, api_key: str = None, model_name: str = None, base_url: str = None, verbose: bool = False) -> List[str]:
    """
    使用大模型解析根因报告，提取top5根因
    支持多种模型：DeepSeek、Qwen-Plus等
    
    Args:
        report_text: 根因报告文本
        api_key: API密钥
        model_name: 模型名称 (如 'deepseek-chat', 'qwen-plus')
        base_url: API基础URL
    
    Returns:
        top5根因列表
    """
    # 读取配置（优先使用参数，其次环境变量）
    if api_key is None:
        api_key = os.getenv("LLM_API_KEY") or os.getenv("DEEPSEEK_API_KEY")
    
    if model_name is None:
        model_name = os.getenv("LLM_MODEL_NAME", "qwen-plus")
    
    if base_url is None:
        base_url = os.getenv("LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    
    if not api_key:
        if verbose:
            print("警告: 未提供LLM_API_KEY，将尝试简单解析")
        return simple_parse_report(report_text)
    
    try:
        # 构建API URL
        if not base_url.endswith('/'):
            base_url += '/'
        url = base_url + "chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        prompt = f"""请分析以下根因报告，提取出最重要的前5个根因服务。
要求：
1. 只返回服务名称列表，每个服务一行
2. 按照重要性从高到低排序
3. 不要包含任何解释或额外信息
4. 如果根因少于5个，返回所有根因
5. 只返回服务名称，如：ts-order-service

报告内容：
{report_text[:5000]}

请直接返回根因服务列表（每行一个服务名）："""

        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": "你是一个专业的系统根因分析专家。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 500
        }
        
        if verbose:
            print(f"使用模型: {model_name} (URL: {url})")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        
        # 解析返回的根因列表
        root_causes = [line.strip() for line in content.split('\n') if line.strip()]
        # 移除可能的序号前缀（如 "1. ", "- " 等）
        root_causes = [rc.lstrip('0123456789.-) ').strip() for rc in root_causes]
        # 过滤空字符串和非服务名
        root_causes = [rc for rc in root_causes if rc and 'service' in rc.lower()]
        
        # 确保最多返回5个
        return root_causes[:5] if root_causes else simple_parse_report(report_text)
        
    except Exception as e:
        print(f"LLM API调用失败: {e}，使用简单解析")
        return simple_parse_report(report_text)


# 保持向后兼容
def parse_report_with_deepseek(report_text: str, api_key: str = None) -> List[str]:
    """
    使用DeepSeek大模型解析根因报告（兼容旧版本）
    现在实际调用parse_report_with_llm
    """
    return parse_report_with_llm(
        report_text, 
        api_key=api_key,
        model_name="deepseek-chat",
        base_url="https://api.deepseek.com/v1"
    )


def simple_parse_report(report_text: str) -> List[str]:
    """
    简单的报告解析方法，当无法使用大模型时使用
    优先解析Root Cause Analysis表格，然后尝试提取服务名称
    
    Args:
        report_text: 根因报告文本
    
    Returns:
        根因列表
    """
    import json
    import re
    
    root_causes = []
    
    # 优先级1: 从Root Cause Analysis表格中提取
    # 查找类似 "| ts-order-service | CPU usage spiked..." 的行
    table_pattern = r'\|\s*([a-z0-9-]+service)\s*\|[^|]+\|[^|]*🔍[^|]*\|'
    table_matches = re.findall(table_pattern, report_text, re.IGNORECASE)
    if table_matches:
        for svc in table_matches:
            if svc not in root_causes:
                root_causes.append(svc)
        if len(root_causes) >= 5:
            return root_causes[:5]
    
    # 优先级2: 从标题或重点标记中提取 (如 "### 🚨 `ts-order-service`")
    title_pattern = r'###?\s*🚨\s*`?([a-z0-9-]+service)`?'
    title_matches = re.findall(title_pattern, report_text, re.IGNORECASE)
    if title_matches:
        for svc in title_matches:
            if svc not in root_causes:
                root_causes.append(svc)
        if len(root_causes) >= 5:
            return root_causes[:5]
    
    # 优先级3: 尝试解析JSON格式
    json_objects = []
    try:
        # 尝试直接解析整个文本
        data = json.loads(report_text)
        json_objects.append(data)
    except (json.JSONDecodeError, ValueError):
        # 尝试提取多个JSON对象
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, report_text)
        for match in matches:
            try:
                obj = json.loads(match)
                if isinstance(obj, dict):
                    json_objects.append(obj)
            except:
                pass
    
    # 从所有JSON对象中提取根因
    for data in json_objects:
        if not isinstance(data, dict):
            continue
            
        # abnormalServices (明确的异常服务标记)
        if 'abnormalServices' in data and isinstance(data['abnormalServices'], list):
            for svc in data['abnormalServices']:
                if svc not in root_causes:
                    root_causes.append(svc)
        
        # service列表
        if 'service' in data and isinstance(data['service'], list):
            for svc in data['service']:
                if svc not in root_causes:
                    root_causes.append(svc)
        
        # 其他可能的字段
        for key in ['root_causes', 'causes', 'issues', 'problems', 'services']:
            if key in data:
                if isinstance(data[key], list):
                    for item in data[key]:
                        if item not in root_causes:
                            root_causes.append(str(item))
                elif isinstance(data[key], str):
                    if data[key] not in root_causes:
                        root_causes.append(data[key])
    
    if root_causes:
        return root_causes[:5]
    
    # 如果是列表格式
    for data in json_objects:
        if isinstance(data, list):
            return [str(item) for item in data[:5]]
    
    # 常见的根因关键词
    keywords = [
        "cpu", "memory", "disk", "network", "latency", "timeout",
        "error", "exception", "service", "pod", "container", "node"
    ]
    
    # 尝试提取服务名称 (如 ts-xxx-service, xxx-service等)
    service_pattern = r'\b([\w-]+service)\b'
    services = re.findall(service_pattern, report_text.lower())
    if services:
        # 去重并返回前5个
        unique_services = []
        for svc in services:
            if svc not in unique_services:
                unique_services.append(svc)
            if len(unique_services) >= 5:
                return unique_services[:5]
        if unique_services:
            root_causes.extend(unique_services)
    
    # 尝试提取包含关键词的行
    lines = report_text.split('\n')
    for line in lines:
        line_lower = line.lower()
        for keyword in keywords:
            if keyword in line_lower and line.strip():
                # 清理并添加
                cleaned = line.strip().lstrip('*-•123456789. ')
                if cleaned and cleaned not in root_causes:
                    root_causes.append(cleaned)
                    if len(root_causes) >= 5:
                        return root_causes[:5]
    
    # 如果没有找到足够的根因，返回前几行非空内容
    if len(root_causes) < 5:
        for line in lines:
            cleaned = line.strip()
            if cleaned and cleaned not in root_causes:
                root_causes.append(cleaned)
                if len(root_causes) >= 5:
                    break
    
    return root_causes[:5] if root_causes else ["未能解析出根因"]


def call_srechat_api(
    detect_time: str,
    api_url: str = "http://120.26.30.82/:31338/api/v1/srechat",
    thread_id: str = None,
    run_id: str = None,
    time_window_minutes: int = 15,
    verbose: bool = False
) -> str:
    """
    调用SREChat API获取根因报告
    
    Args:
        detect_time: 检测时间，格式如 "2025-09-23T17:20:42+08:00"
        api_url: API地址
        thread_id: 线程ID，如果为None则自动生成
        run_id: 运行ID，如果为None则自动生成
        time_window_minutes: 时间窗口（分钟）
    
    Returns:
        根因报告文本
    """
    import time
    
    # 生成ID
    if thread_id is None:
        thread_id = f"thread_{int(time.time() * 1000)}_{os.urandom(4).hex()}"
    if run_id is None:
        run_id = f"run_{int(time.time() * 1000)}_{os.urandom(4).hex()}"
    
    # 计算时间范围
    from datetime import datetime, timedelta
    
    # 解析 detect_time (格式: "2025-10-21T19:40:13+08:00")
    if detect_time.endswith('+08:00'):
        dt_str = detect_time[:-6]  # 移除 "+08:00"
        detect_dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%S")
    else:
        # 尝试解析其他格式
        detect_dt = datetime.fromisoformat(detect_time.replace('+08:00', ''))
    
    # 计算起始时间
    start_dt = detect_dt - timedelta(minutes=time_window_minutes)
    
    # 格式化时间范围
    start_time_str = start_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
    end_time_str = detect_time  # 使用传入的原始格式
    
    # 构建请求消息
    message_content = (
        f"Check if there are any application response slowdowns or latency anomalies "
        f"in the system, and analyze the causes. "
        f"({start_time_str} -- {end_time_str})"
    )
    
    payload = {
        "threadId": thread_id,
        "runId": run_id,
        "messages": [
            {
                "role": "user",
                "content": message_content,
                "id": f"msg_{int(time.time() * 1000)}_{os.urandom(4).hex()}"
            }
        ],
        "state": {},
        "tools": [],
        "context": [],
        "forwardedProps": {}
    }
    
    headers = {
        "Accept": "text/event-stream",
        "Content-Type": "application/json"
    }
    
    try:
        if verbose:
            print(f"调用SREChat API: {api_url}")
            print(f"时间范围: {start_time_str} -- {end_time_str}")
            print(f"时间窗口: {time_window_minutes}分钟")
            print(f"消息内容: {message_content}")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60,
            stream=True
        )
        response.raise_for_status()
        
        # 处理流式响应
        report_text = ""
        rca_results = []  # 存储Root Cause Analysis结果
        
        for line in response.iter_lines():
            if line:
                line_text = line.decode('utf-8')
                # SSE格式通常是 "data: {...}"
                if line_text.startswith("data: "):
                    data_text = line_text[6:]  # 移除 "data: " 前缀
                    try:
                        data = json.loads(data_text)
                        
                        # 专门提取Root Cause Analysis结果
                        if isinstance(data, dict):
                            # 检查是否是Root Cause Analysis结果
                            if (data.get('type') == 'CUSTOM' and 
                                data.get('name') == 'AgentToolDisplay'):
                                
                                value = data.get('value', {})
                                if value.get('title') == 'Root Cause Analysis Result':
                                    content = value.get('content', {})
                                    fields = content.get('fields', [])
                                    
                                    # 提取summary和report
                                    for field in fields:
                                        if field.get('key') == 'summary':
                                            rca_results.append({
                                                'type': 'summary',
                                                'content': field.get('children', '')
                                            })
                                        elif field.get('key') == 'report':
                                            rca_results.append({
                                                'type': 'report',
                                                'content': field.get('children', '')
                                            })
                            
                            # 保留所有数据用于备用解析
                            for key in ["content", "message", "text", "report", "data"]:
                                if key in data:
                                    report_text += str(data[key])
                        else:
                            report_text += data_text
                    except json.JSONDecodeError:
                        report_text += data_text
                else:
                    report_text += line_text
                report_text += "\n"
        
        # 如果找到了RCA结果，优先使用
        if rca_results:
            formatted_report = "=== Root Cause Analysis ===\n\n"
            for result in rca_results:
                if result['type'] == 'summary':
                    formatted_report += "SUMMARY:\n" + result['content'] + "\n\n"
                elif result['type'] == 'report':
                    formatted_report += "DETAILED REPORT:\n" + result['content'] + "\n\n"
            report_text = formatted_report + "\n\n=== Original Response ===\n" + report_text
            if verbose:
                print("✅ 找到RCA结果，数量:", len(rca_results))
        else:
            if verbose:
                print("⚠️  未找到RCA结果，使用原始响应")
                print(f"原始响应长度: {len(report_text)} 字符")
                print(f"原始响应前200字符: {report_text[:200]}")

        
        if not report_text.strip():
            report_text = "未能获取到有效的报告内容"
        
        return report_text.strip()
        
    except requests.exceptions.RequestException as e:
        print(f"API调用失败: {e}")
        return f"API调用失败: {str(e)}"


def srechat_rca(
    data=None,
    inject_time: str = None,
    dataset: str = None,
    detect_time: str = None,
    api_url: str = None,
    time_window_minutes: int = 15,
    deepseek_api_key: str = None,
    llm_api_key: str = None,
    llm_model_name: str = None,
    llm_base_url: str = None,
    verbose: bool = False,
    **kwargs
) -> Dict[str, Any]:
    """
    SREChat RCA算法
    
    这个算法不需要data参数，只需要检测时间，会自动调用远程API获取根因报告，
    然后使用大模型解析报告获取top5根因。
    
    Args:
        data: 数据（此算法不使用）
        inject_time: 注入时间（兼容性参数）
        dataset: 数据集名称（兼容性参数）
        detect_time: 检测时间，格式如 "2025-09-23T17:20:42+08:00"
                    如果未提供，将使用inject_time或当前时间
        api_url: SREChat API地址，默认为 http://192.168.1.6:28522/api/v1/srechat
        time_window_minutes: 检测时间窗口（分钟），默认15分钟
        deepseek_api_key: DeepSeek API密钥（兼容旧版本）
        llm_api_key: 通用LLM API密钥（推荐）
        llm_model_name: 模型名称，如 'qwen-plus', 'deepseek-chat'
        llm_base_url: API基础URL，如 'https://dashscope.aliyuncs.com/compatible-mode/v1'
        **kwargs: 其他参数
    
    Returns:
        字典，包含 ranks 字段（top5根因列表）
    """
    # 确定检测时间
    if detect_time is None:
        if inject_time is not None:
            # 如果inject_time是时间戳，转换为ISO格式
            if isinstance(inject_time, (int, float)):
                from datetime import datetime
                dt = datetime.fromtimestamp(inject_time)
                detect_time = dt.strftime("%Y-%m-%dT%H:%M:%S+08:00")
            else:
                detect_time = str(inject_time)
        else:
            # 使用当前时间
            from datetime import datetime
            detect_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+08:00")
    
    # 确定API地址
    if api_url is None:
        api_url = os.getenv("SRECHAT_API_URL", "http://120.26.30.82:31338/api/v1/srechat")
    
    # 调用SREChat API获取报告
    if verbose:
        print("步骤1: 调用SREChat API获取根因报告...")
    report_text = call_srechat_api(
        detect_time=detect_time,
        api_url=api_url,
        time_window_minutes=time_window_minutes,
        verbose=verbose
    )

    if verbose:
        print(f"获取到报告，长度: {len(report_text)} 字符")
        print("=" * 80)
        print("报告内容预览:")
        print(report_text[:500] if len(report_text) > 500 else report_text)
        print("=" * 80)
    
    # 使用大模型解析报告
    if verbose:
        print("\n步骤2: 使用大模型解析报告...")
    
    # 支持新的参数名或兼容旧的参数名
    llm_api_key = kwargs.get('llm_api_key') or deepseek_api_key
    llm_model_name = kwargs.get('llm_model_name')
    llm_base_url = kwargs.get('llm_base_url')
    
    root_causes = parse_report_with_llm(
        report_text=report_text,
        api_key=llm_api_key,
        model_name=llm_model_name,
        base_url=llm_base_url,
        verbose=verbose
    )
    
    if verbose:
        print(f"解析出 {len(root_causes)} 个根因:")
        for i, rc in enumerate(root_causes, 1):
            print(f"  {i}. {rc}")

    # Convert to "service_reason" format to align with other algorithms in the project
    ranks_formatted = _format_service_reasons(root_causes, report_text)

    # Extract RCA content from the stream for user display/verification
    rca_info = _extract_rca_from_report(report_text)

    # LLM usage & simple matching with RCA services
    llm_used = bool(llm_api_key or os.getenv("LLM_API_KEY") or os.getenv("DEEPSEEK_API_KEY"))
    rca_services = set(rca_info.get("rca_services_from_table", []) or [])
    llm_services = set(root_causes or [])
    llm_match_count = len(rca_services.intersection(llm_services)) if rca_services else 0
    llm_match = llm_match_count > 0
    
    return {
        "ranks": ranks_formatted,
        "raw_ranks": root_causes,
        "report": report_text,
        "detect_time": detect_time,
        # Newly exposed RCA content and comparison
        "rca_summary": rca_info.get("rca_summary"),
        "rca_report_markdown": rca_info.get("rca_report_markdown"),
        "rca_services_from_table": rca_info.get("rca_services_from_table"),
        "llm_used": llm_used,
        "llm_match": llm_match,
        "llm_match_count": llm_match_count,
    }


# 导出
__all__ = ["srechat_rca"]

