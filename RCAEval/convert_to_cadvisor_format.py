"""
将 RE2-OB metrics 转换为 cAdvisor Prometheus 格式
模拟 cAdvisor 的指标命名和标签结构
"""
import os
import json
import pandas as pd
import argparse
from pathlib import Path
from typing import Dict, List


def load_k8s_info(case_dir: str) -> Dict:
    """加载 K8s 集群信息"""
    case_path = Path(case_dir)
    
    # 读取 pod-node 映射
    pod_node_files = list(case_path.glob('pod-node-*.csv'))
    pod_to_node = {}
    
    if pod_node_files:
        df = pd.read_csv(pod_node_files[0])
        for _, row in df.iterrows():
            pod_name = row['POD']
            node_name = row['NODE_NAME']
            service_name = '-'.join(pod_name.split('-')[:-2])
            pod_to_node[service_name] = {
                'pod': pod_name,
                'pod_name': pod_name,
                'node': node_name,
                'namespace': 'default',  # RE2-OB 使用默认命名空间
                'container': service_name,  # 容器名通常和服务名一致
            }
    
    # 读取 cluster info
    cluster_info = {}
    cluster_info_file = case_path / 'cluster_info.json'
    if cluster_info_file.exists():
        with open(cluster_info_file, 'r') as f:
            cluster_info = json.load(f)
    
    return {
        'pod_to_node': pod_to_node,
        'cluster_info': cluster_info
    }


def convert_to_cadvisor_prometheus(
    metrics_df: pd.DataFrame,
    k8s_info: Dict,
    case_name: str,
    output_file: str
):
    """
    转换为 cAdvisor Prometheus 格式
    
    cAdvisor 指标格式:
    - container_cpu_usage_seconds_total
    - container_memory_working_set_bytes
    - container_network_receive_bytes_total
    - container_fs_io_time_seconds_total
    
    标签:
    - namespace
    - pod
    - container
    - name (容器名称)
    - image
    """
    print(f"\n🔄 转换为 cAdvisor Prometheus 格式...")
    
    lines = []
    metric_cols = [col for col in metrics_df.columns if col != 'time']
    
    # cAdvisor 指标映射
    metric_mapping = {
        'cpu': {
            'name': 'container_cpu_usage_seconds_total',
            'type': 'counter',
            'help': 'Cumulative cpu time consumed in seconds',
            'unit': 'seconds',
            'is_cumulative': True
        },
        'mem': {
            'name': 'container_memory_working_set_bytes',
            'type': 'gauge',
            'help': 'Current working set of the container in bytes',
            'unit': 'bytes',
            'is_cumulative': False
        },
        'diskio': {
            'name': 'container_fs_io_time_seconds_total',
            'type': 'counter',
            'help': 'Cumulative count of seconds spent doing I/Os',
            'unit': 'seconds',
            'is_cumulative': True
        },
        'socket': {
            'name': 'container_sockets',
            'type': 'gauge',
            'help': 'Number of open sockets',
            'unit': 'sockets',
            'is_cumulative': False
        },
        'workload': {
            'name': 'container_requests_total',
            'type': 'counter',
            'help': 'Total number of requests',
            'unit': 'requests',
            'is_cumulative': True
        },
        'latency-50': {
            'name': 'container_request_duration_seconds',
            'type': 'gauge',
            'help': 'Request duration in seconds (p50)',
            'unit': 'seconds',
            'is_cumulative': False,
            'quantile': '0.5'
        },
        'latency-90': {
            'name': 'container_request_duration_seconds',
            'type': 'gauge',
            'help': 'Request duration in seconds (p90)',
            'unit': 'seconds',
            'is_cumulative': False,
            'quantile': '0.9'
        },
        'error': {
            'name': 'container_request_errors_total',
            'type': 'counter',
            'help': 'Total number of request errors',
            'unit': 'errors',
            'is_cumulative': True
        }
    }
    
    # 写入 HELP 和 TYPE 注释
    help_written = set()
    
    # 累积值跟踪（用于 counter 类型）
    cumulative_values = {}
    
    for idx, row in metrics_df.iterrows():
        timestamp_sec = int(row["time"])  # 转换为毫秒
        
        for metric_col in metric_cols:
            value = row[metric_col]
            
            # 跳过 NaN 值
            if pd.isna(value):
                continue
            
            # 解析 metric 名称和服务
            parts = metric_col.split('_')
            if len(parts) < 2:
                continue
            
            service = '_'.join(parts[:-1])
            metric_type = parts[-1]
            
            # 获取映射的 cAdvisor 指标名
            if metric_type not in metric_mapping:
                continue
            
            metric_info = metric_mapping[metric_type]
            cadvisor_metric_name = metric_info['name']
            
            # 写入 HELP 和 TYPE（每个指标只写一次）
            if cadvisor_metric_name not in help_written:
                lines.append(f"# HELP {cadvisor_metric_name} {metric_info['help']}")
                lines.append(f"# TYPE {cadvisor_metric_name} {metric_info['type']}")
                help_written.add(cadvisor_metric_name)
            
            # 构建标签
            labels = [
                f'namespace="default"',
                f'container="{service}"',
                f'name="{service}"',
            ]
            
            # 添加 K8s 信息
            if service in k8s_info.get('pod_to_node', {}):
                k8s_data = k8s_info['pod_to_node'][service]
                labels.append(f'pod="{k8s_data["pod"]}"')
                labels.append(f'node="{k8s_data["node"]}"')
                labels.append(f'image="{service}:latest"')  # 假设镜像名
            
            # 添加分位数标签（如果是延迟指标）
            if 'quantile' in metric_info:
                labels.append(f'quantile="{metric_info["quantile"]}"')
            
            # 处理累积值（counter 类型）
            if metric_info['is_cumulative']:
                key = f"{cadvisor_metric_name}_{service}"
                if key not in cumulative_values:
                    cumulative_values[key] = 0
                
                # CPU: 百分比转换为累积秒数
                if metric_type == 'cpu':
                    # 假设每个采样间隔是 1 秒，CPU 百分比累加
                    cumulative_values[key] += value / 100  # 转换为秒
                    final_value = cumulative_values[key]
                # 其他累积指标直接累加
                else:
                    cumulative_values[key] += value
                    final_value = cumulative_values[key]
            else:
                # Gauge 类型直接使用当前值
                if metric_type == 'mem':
                    final_value = value  # 内存已经是字节
                elif 'latency' in metric_type:
                    final_value = value  # 延迟已经是秒
                else:
                    final_value = value
            
            # 构建 Prometheus 格式
            # metric_name{label1="value1",label2="value2"} value timestamp
            label_str = ','.join(labels)
            line = f"{cadvisor_metric_name}{{{label_str}}} {final_value} {timestamp_sec}"
            lines.append(line)
        
        if (idx + 1) % 100 == 0:
            print(f"  处理进度: {idx + 1}/{len(metrics_df)} 行")
    
    # 写入文件
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ cAdvisor Prometheus 格式已保存: {output_file}")
    print(f"   总行数: {len(lines)}")
    print(f"   指标类型: {len(help_written)}")


def convert_to_cadvisor_json(
    metrics_df: pd.DataFrame,
    k8s_info: Dict,
    case_name: str,
    output_file: str
):
    """
    转换为 cAdvisor JSON 格式（用于 remote write）
    """
    print(f"\n🔄 转换为 cAdvisor JSON 格式...")
    
    lines = []
    metric_cols = [col for col in metrics_df.columns if col != 'time']
    
    # 指标映射（同上）
    metric_mapping = {
        'cpu': 'container_cpu_usage_seconds_total',
        'mem': 'container_memory_working_set_bytes',
        'diskio': 'container_fs_io_time_seconds_total',
        'socket': 'container_sockets',
        'workload': 'container_requests_total',
        'latency-50': 'container_request_duration_seconds',
        'latency-90': 'container_request_duration_seconds',
        'error': 'container_request_errors_total'
    }
    
    cumulative_values = {}
    
    for idx, row in metrics_df.iterrows():
        timestamp_sec = int(row["time"])
        
        for metric_col in metric_cols:
            value = row[metric_col]
            
            if pd.isna(value):
                continue
            
            parts = metric_col.split('_')
            if len(parts) < 2:
                continue
            
            service = '_'.join(parts[:-1])
            metric_type = parts[-1]
            
            if metric_type not in metric_mapping:
                continue
            
            cadvisor_metric_name = metric_mapping[metric_type]
            
            # 构建 labels
            labels = {
                '__name__': cadvisor_metric_name,
                'namespace': 'default',
                'container': service,
                'name': service
            }
            
            # 添加 K8s 信息
            if service in k8s_info.get('pod_to_node', {}):
                k8s_data = k8s_info['pod_to_node'][service]
                labels['pod'] = k8s_data['pod']
                labels['node'] = k8s_data['node']
                labels['image'] = f"{service}:latest"
            
            # 添加分位数
            if 'latency' in metric_type:
                labels['quantile'] = '0.5' if '50' in metric_type else '0.9'
            
            # 处理累积值
            if metric_type in ['cpu', 'diskio', 'workload', 'error']:
                key = f"{cadvisor_metric_name}_{service}"
                if key not in cumulative_values:
                    cumulative_values[key] = 0
                
                if metric_type == 'cpu':
                    cumulative_values[key] += value / 100
                else:
                    cumulative_values[key] += value
                final_value = cumulative_values[key]
            else:
                final_value = value
            
            # 构建 JSON 对象
            metric_obj = {
                'metric': labels,
                'values': [final_value],
                'timestamps': [timestamp_sec]
            }
            
            lines.append(json.dumps(metric_obj))
        
        if (idx + 1) % 100 == 0:
            print(f"  处理进度: {idx + 1}/{len(metrics_df)} 行")
    
    # 写入文件
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ cAdvisor JSON 格式已保存: {output_file}")
    print(f"   总行数: {len(lines)}")


def convert_case(
    case_dir: str,
    output_dir: str,
    formats: List[str] = ['prometheus', 'json']
):
    """转换单个案例"""
    case_path = Path(case_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*70}")
    print(f"📂 处理案例: {case_path}")
    print(f"{'='*70}")
    
    # 读取数据
    metrics_file = case_path / 'simple_metrics.csv'
    if not metrics_file.exists():
        print(f"⚠️  Metrics 文件不存在: {metrics_file}")
        return
    
    print(f"📊 读取 metrics 数据...")
    metrics_df = pd.read_csv(metrics_file)
    print(f"   数据形状: {metrics_df.shape}")
    
    # 读取 K8s 信息
    print(f"🔗 读取 K8s 信息...")
    k8s_info = load_k8s_info(str(case_path))
    print(f"   服务数: {len(k8s_info.get('pod_to_node', {}))}")
    
    # 获取案例名称
    case_name = case_path.parent.name + '_' + case_path.name
    
    # 转换为各种格式
    if 'prometheus' in formats:
        prom_file = output_path / 'metrics.cadvisor.prom'
        convert_to_cadvisor_prometheus(
            metrics_df, k8s_info, case_name, str(prom_file)
        )
    
    if 'json' in formats:
        json_file = output_path / 'metrics.cadvisor.jsonl'
        convert_to_cadvisor_json(
            metrics_df, k8s_info, case_name, str(json_file)
        )
    
    # 复制其他元数据
    print(f"\n📋 复制元数据文件...")
    import shutil
    for filename in ['inject_time.txt', 'cluster_info.json']:
        src = case_path / filename
        if src.exists():
            dst = output_path / filename
            shutil.copy2(src, dst)
            print(f"   ✓ {filename}")
    
    # 保存 K8s 映射信息
    with open(output_path / 'k8s_mapping.json', 'w') as f:
        json.dump(k8s_info['pod_to_node'], f, indent=2)
    print(f"   ✓ k8s_mapping.json")
    
    print(f"\n✅ 转换完成! 输出目录: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='将 RE2-OB metrics 转换为 cAdvisor Prometheus 格式'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data/RE2/RE2-OB',
        help='输入数据集目录'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/RE2/RE2-OB-cAdvisor',
        help='输出目录'
    )
    parser.add_argument(
        '--case',
        type=str,
        help='只转换指定案例 (例如: checkoutservice_cpu/1)'
    )
    parser.add_argument(
        '--format',
        type=str,
        nargs='+',
        choices=['prometheus', 'json', 'all'],
        default=['all'],
        help='输出格式'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='限制转换的案例数量'
    )
    
    args = parser.parse_args()
    
    # 处理格式参数
    if 'all' in args.format:
        formats = ['prometheus', 'json']
    else:
        formats = args.format
    
    if args.case:
        # 转换单个案例
        case_dir = os.path.join(args.input, args.case)
        output_dir = os.path.join(args.output, args.case)
        convert_case(case_dir, output_dir, formats)
    else:
        # 转换整个数据集
        import glob
        from tqdm import tqdm
        
        print("="*70)
        print("🚀 开始转换数据集到 cAdvisor 格式")
        print("="*70)
        print(f"输入: {args.input}")
        print(f"输出: {args.output}")
        print(f"格式: {', '.join(formats)}")
        if args.limit:
            print(f"限制: 仅转换前 {args.limit} 个案例")
        print()
        
        base_dir = Path(args.input)
        case_dirs = sorted(glob.glob(os.path.join(args.input, '*/*/')))
        
        if args.limit:
            case_dirs = case_dirs[:args.limit]
        
        for case_dir in tqdm(case_dirs, desc="Processing cases"):
            relative_path = Path(case_dir).relative_to(base_dir)
            output_dir = Path(args.output) / relative_path
            convert_case(case_dir, str(output_dir), formats)
        
        print(f"\n{'='*70}")
        print(f"✅ 数据集转换完成!")
        print(f"{'='*70}")
        print(f"总案例数: {len(case_dirs)}")
        print()


if __name__ == '__main__':
    main()





