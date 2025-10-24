"""
将 RE2-OB metrics 转换为 VictoriaMetrics 格式
支持多种导出格式：
1. Prometheus Remote Write (JSON)
2. InfluxDB Line Protocol
3. VictoriaMetrics Import (JSON Lines)
"""
import os
import json
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
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
                'node': node_name
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


def convert_to_influxdb_line_protocol(
    metrics_df: pd.DataFrame,
    k8s_info: Dict,
    case_name: str,
    output_file: str
):
    """
    转换为 InfluxDB Line Protocol 格式
    格式: measurement,tag1=value1,tag2=value2 field1=value1,field2=value2 timestamp
    """
    print(f"\n🔄 转换为 InfluxDB Line Protocol 格式...")
    
    lines = []
    metric_cols = [col for col in metrics_df.columns if col != 'time']
    
    for idx, row in metrics_df.iterrows():
        timestamp_ns = int(row['time'] * 1e9)  # 转换为纳秒
        
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
            
            # 构建标签
            tags = [
                f'case="{case_name}"',
                f'service="{service}"',
                f'metric_type="{metric_type}"'
            ]
            
            # 添加 K8s 信息
            if service in k8s_info.get('pod_to_node', {}):
                k8s_data = k8s_info['pod_to_node'][service]
                tags.append(f'pod="{k8s_data["pod"]}"')
                tags.append(f'node="{k8s_data["node"]}"')
            
            # 构建 line protocol
            # measurement,tag1=val1,tag2=val2 field=value timestamp
            line = f"{metric_type},{','.join(tags)} value={value} {timestamp_ns}"
            lines.append(line)
        
        if (idx + 1) % 100 == 0:
            print(f"  处理进度: {idx + 1}/{len(metrics_df)} 行")
    
    # 写入文件
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ InfluxDB Line Protocol 格式已保存: {output_file}")
    print(f"   总行数: {len(lines)}")


def convert_to_victoriametrics_json(
    metrics_df: pd.DataFrame,
    k8s_info: Dict,
    case_name: str,
    output_file: str
):
    """
    转换为 VictoriaMetrics Import 格式 (JSON Lines)
    每行是一个 JSON 对象
    """
    print(f"\n🔄 转换为 VictoriaMetrics JSON 格式...")
    
    lines = []
    metric_cols = [col for col in metrics_df.columns if col != 'time']
    
    for idx, row in metrics_df.iterrows():
        timestamp_ms = int(row['time'] * 1000)  # 转换为毫秒
        
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
            
            # 构建 labels
            labels = {
                'case': case_name,
                'service': service,
                'metric_type': metric_type,
                '__name__': metric_type  # VictoriaMetrics 要求
            }
            
            # 添加 K8s 信息
            if service in k8s_info.get('pod_to_node', {}):
                k8s_data = k8s_info['pod_to_node'][service]
                labels['pod'] = k8s_data['pod']
                labels['node'] = k8s_data['node']
            
            # 构建 JSON 对象
            metric_obj = {
                'metric': labels,
                'values': [value],
                'timestamps': [timestamp_ms]
            }
            
            lines.append(json.dumps(metric_obj))
        
        if (idx + 1) % 100 == 0:
            print(f"  处理进度: {idx + 1}/{len(metrics_df)} 行")
    
    # 写入文件
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ VictoriaMetrics JSON 格式已保存: {output_file}")
    print(f"   总行数: {len(lines)}")


def convert_to_prometheus_json(
    metrics_df: pd.DataFrame,
    k8s_info: Dict,
    case_name: str,
    output_file: str
):
    """
    转换为 Prometheus Remote Write 格式 (JSON)
    这是一个完整的 JSON 对象，包含所有时间序列
    """
    print(f"\n🔄 转换为 Prometheus Remote Write 格式...")
    
    timeseries_map = {}  # key: metric_signature, value: {labels, samples}
    metric_cols = [col for col in metrics_df.columns if col != 'time']
    
    for idx, row in metrics_df.iterrows():
        timestamp_ms = int(row['time'] * 1000)
        
        for metric_col in metric_cols:
            value = row[metric_col]
            
            if pd.isna(value):
                continue
            
            # 解析 metric
            parts = metric_col.split('_')
            if len(parts) < 2:
                continue
            
            service = '_'.join(parts[:-1])
            metric_type = parts[-1]
            
            # 构建 metric 签名（用于去重）
            metric_name = f"{service}_{metric_type}"
            
            # 构建标签
            labels = [
                {'name': '__name__', 'value': metric_name},
                {'name': 'case', 'value': case_name},
                {'name': 'service', 'value': service},
                {'name': 'metric_type', 'value': metric_type}
            ]
            
            # 添加 K8s 信息
            if service in k8s_info.get('pod_to_node', {}):
                k8s_data = k8s_info['pod_to_node'][service]
                labels.append({'name': 'pod', 'value': k8s_data['pod']})
                labels.append({'name': 'node', 'value': k8s_data['node']})
            
            # 创建签名
            label_sig = tuple(sorted([(l['name'], l['value']) for l in labels]))
            
            # 添加样本
            if label_sig not in timeseries_map:
                timeseries_map[label_sig] = {
                    'labels': labels,
                    'samples': []
                }
            
            timeseries_map[label_sig]['samples'].append({
                'value': value,
                'timestamp': timestamp_ms
            })
        
        if (idx + 1) % 100 == 0:
            print(f"  处理进度: {idx + 1}/{len(metrics_df)} 行")
    
    # 构建最终的 JSON 结构
    timeseries_list = []
    for ts_data in timeseries_map.values():
        timeseries_list.append({
            'labels': ts_data['labels'],
            'samples': ts_data['samples']
        })
    
    prometheus_data = {
        'timeseries': timeseries_list
    }
    
    # 写入文件
    with open(output_file, 'w') as f:
        json.dump(prometheus_data, f, indent=2)
    
    print(f"✅ Prometheus JSON 格式已保存: {output_file}")
    print(f"   时间序列数: {len(timeseries_list)}")


def convert_case(
    case_dir: str,
    output_dir: str,
    formats: List[str] = ['influxdb', 'vm-json', 'prometheus']
):
    """
    转换单个案例
    
    Args:
        case_dir: 案例目录
        output_dir: 输出目录
        formats: 要生成的格式列表
    """
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
    if 'influxdb' in formats:
        influxdb_file = output_path / 'metrics.influxdb'
        convert_to_influxdb_line_protocol(
            metrics_df, k8s_info, case_name, str(influxdb_file)
        )
    
    if 'vm-json' in formats:
        vm_json_file = output_path / 'metrics.vm.jsonl'
        convert_to_victoriametrics_json(
            metrics_df, k8s_info, case_name, str(vm_json_file)
        )
    
    if 'prometheus' in formats:
        prom_file = output_path / 'metrics.prometheus.json'
        convert_to_prometheus_json(
            metrics_df, k8s_info, case_name, str(prom_file)
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
    
    print(f"\n✅ 转换完成! 输出目录: {output_path}")


def convert_dataset(
    dataset_dir: str,
    output_base_dir: str,
    formats: List[str],
    limit: int = None
):
    """转换整个数据集"""
    dataset_path = Path(dataset_dir)
    
    print(f"\n{'='*70}")
    print(f"🚀 开始转换数据集到 VictoriaMetrics 格式")
    print(f"{'='*70}")
    print(f"输入: {dataset_dir}")
    print(f"输出: {output_base_dir}")
    print(f"格式: {', '.join(formats)}")
    if limit:
        print(f"限制: 仅转换前 {limit} 个案例")
    print()
    
    # 遍历所有案例
    fault_dirs = [d for d in dataset_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    total_cases = 0
    for fault_dir in sorted(fault_dirs):
        case_dirs = [d for d in fault_dir.iterdir() if d.is_dir() and d.name.isdigit()]
        
        for case_dir in sorted(case_dirs, key=lambda x: int(x.name)):
            if limit and total_cases >= limit:
                break
            
            relative_path = case_dir.relative_to(dataset_path)
            output_dir = Path(output_base_dir) / relative_path
            
            convert_case(str(case_dir), str(output_dir), formats)
            total_cases += 1
        
        if limit and total_cases >= limit:
            break
    
    print(f"\n{'='*70}")
    print(f"✅ 数据集转换完成!")
    print(f"{'='*70}")
    print(f"总案例数: {total_cases}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='将 RE2-OB metrics 转换为 VictoriaMetrics 格式'
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
        default='data/RE2/RE2-OB-VictoriaMetrics',
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
        choices=['influxdb', 'vm-json', 'prometheus', 'all'],
        default=['all'],
        help='输出格式 (可选多个)'
    )
    parser.add_argument(
        '--limit',
        type=int,
        help='限制转换的案例数量'
    )
    
    args = parser.parse_args()
    
    # 处理格式参数
    if 'all' in args.format:
        formats = ['influxdb', 'vm-json', 'prometheus']
    else:
        formats = args.format
    
    if args.case:
        # 转换单个案例
        case_dir = os.path.join(args.input, args.case)
        output_dir = os.path.join(args.output, args.case)
        convert_case(case_dir, output_dir, formats)
    else:
        # 转换整个数据集
        convert_dataset(args.input, args.output, formats, args.limit)


if __name__ == '__main__':
    main()


