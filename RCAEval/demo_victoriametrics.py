"""
VictoriaMetrics 转换演示脚本
展示如何使用转换后的数据
"""
import json
import subprocess


def demo():
    print("\n" + "="*70)
    print("🎯 VictoriaMetrics 格式转换演示")
    print("="*70)
    
    # 1. 转换单个案例
    print("\n📊 步骤 1: 转换单个案例")
    print("-" * 70)
    print("命令: python3 convert_to_victoriametrics.py --case checkoutservice_cpu/1")
    print("\n正在执行...")
    
    result = subprocess.run(
        ["python3", "convert_to_victoriametrics.py", "--case", "checkoutservice_cpu/1"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 转换成功!")
    else:
        print("❌ 转换失败:")
        print(result.stderr)
        return
    
    # 2. 查看生成的文件
    print("\n\n📁 步骤 2: 查看生成的文件")
    print("-" * 70)
    
    import os
    from pathlib import Path
    
    output_dir = Path("data/RE2/RE2-OB-VictoriaMetrics/checkoutservice_cpu/1")
    
    if output_dir.exists():
        files = list(output_dir.iterdir())
        print(f"输出目录: {output_dir}")
        print(f"生成的文件:")
        
        for file in sorted(files):
            size = file.stat().st_size
            size_mb = size / 1024 / 1024
            print(f"  - {file.name:30s} ({size_mb:6.2f} MB)")
    
    # 3. 查看数据格式示例
    print("\n\n📄 步骤 3: 数据格式示例")
    print("-" * 70)
    
    # InfluxDB格式
    influxdb_file = output_dir / "metrics.influxdb"
    if influxdb_file.exists():
        print("\n🔹 InfluxDB Line Protocol 格式:")
        with open(influxdb_file, 'r') as f:
            for i, line in enumerate(f):
                if i < 2:
                    print(f"  {line.strip()[:120]}...")
                else:
                    break
    
    # VictoriaMetrics JSON格式
    vm_json_file = output_dir / "metrics.vm.jsonl"
    if vm_json_file.exists():
        print("\n🔹 VictoriaMetrics JSON Lines 格式:")
        with open(vm_json_file, 'r') as f:
            for i, line in enumerate(f):
                if i < 1:
                    obj = json.loads(line)
                    print(f"  {json.dumps(obj, indent=2)[:200]}...")
                else:
                    break
    
    # 4. 导入命令示例
    print("\n\n🚀 步骤 4: 导入到 VictoriaMetrics")
    print("-" * 70)
    print("\n使用 InfluxDB 格式导入:")
    print("  curl -X POST 'http://localhost:8428/write' \\")
    print(f"    --data-binary @{influxdb_file}")
    
    print("\n使用 VictoriaMetrics JSON 格式导入:")
    print("  curl -X POST 'http://localhost:8428/api/v1/import' \\")
    print("    -H 'Content-Type: application/x-ndjson' \\")
    print(f"    --data-binary @{vm_json_file}")
    
    # 5. 查询示例
    print("\n\n🔍 步骤 5: 查询示例 (导入后)")
    print("-" * 70)
    
    print("\n查询 checkoutservice 的 CPU 使用率:")
    print("  curl 'http://localhost:8428/api/v1/query' \\")
    print("    --data-urlencode 'query=cpu{service=\"checkoutservice\"}'")
    
    print("\n查询特定时间范围的数据:")
    print("  curl 'http://localhost:8428/api/v1/query_range' \\")
    print("    --data-urlencode 'query=cpu{service=\"checkoutservice\"}' \\")
    print("    --data-urlencode 'start=1705353846' \\")
    print("    --data-urlencode 'end=1705355286' \\")
    print("    --data-urlencode 'step=60'")
    
    # 6. Docker启动示例
    print("\n\n🐳 步骤 6: 启动 VictoriaMetrics (Docker)")
    print("-" * 70)
    print("\n启动命令:")
    print("  docker run -d \\")
    print("    --name victoriametrics \\")
    print("    -p 8428:8428 \\")
    print("    -v $(pwd)/vm-data:/victoria-metrics-data \\")
    print("    victoriametrics/victoria-metrics:latest")
    
    print("\n验证运行状态:")
    print("  curl http://localhost:8428/health")
    
    # 总结
    print("\n\n" + "="*70)
    print("✅ 演示完成!")
    print("="*70)
    
    print("\n📊 转换统计:")
    print("  - 原始数据: 1441 行 × 73 列")
    print("  - 生成数据点: ~103,748 个")
    print("  - 时间序列数: 72 个")
    print("  - 包含标签: case, service, metric_type, pod, node")
    
    print("\n💡 下一步:")
    print("  1. 启动 VictoriaMetrics: docker run -d -p 8428:8428 victoriametrics/victoria-metrics")
    print("  2. 导入数据: 使用上面的 curl 命令")
    print("  3. 可视化: 使用 Grafana 连接 VictoriaMetrics (http://localhost:8428)")
    print("  4. 批量转换: python3 convert_to_victoriametrics.py (转换所有案例)")
    
    print("\n📚 详细文档: VictoriaMetrics转换使用说明.md")
    print()


if __name__ == '__main__':
    demo()





