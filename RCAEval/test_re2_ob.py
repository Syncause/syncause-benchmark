"""
RE2-OB 数据集测试脚本
使用 BARO 方法进行根因分析评估
"""
import subprocess
import sys

print("=" * 60)
print("🚀 开始在 RE2-OB 数据集上运行根因分析评估")
print("=" * 60)
print()
print("📊 数据集信息:")
print("  - 名称: RE2-OB (Online Boutique)")
print("  - 案例数: 90")
print("  - 故障类型: CPU、MEM、DISK、SOCKET、DELAY、LOSS")
print("  - 方法: BARO (Bayesian Online Change Point Detection)")
print()
print("-" * 60)
print()

# 运行完整评估
result = subprocess.run(
    [sys.executable, "main.py", "--method", "baro", "--dataset", "re2-ob"],
    capture_output=False,
    text=True
)

print()
print("=" * 60)
print("✅ 评估完成！")
print("=" * 60)
print()
print("📈 结果说明:")
print("  - Avg@5-CPU:    CPU故障的平均Top-5准确率")
print("  - Avg@5-MEM:    内存故障的平均Top-5准确率")
print("  - Avg@5-DISK:   磁盘I/O故障的平均Top-5准确率")
print("  - Avg@5-SOCKET: Socket故障的平均Top-5准确率")
print("  - Avg@5-DELAY:  网络延迟故障的平均Top-5准确率")
print("  - Avg@5-LOSS:   网络丢包故障的平均Top-5准确率")
print("  - Avg speed:    每个案例的平均处理时间（秒）")
print()
print("💡 提示:")
print("  - 可以尝试其他方法: circa, rcd, microcause, e_diagnosis 等")
print("  - 使用 --test 参数可以只测试前2个案例进行快速验证")
print()
print("示例: python3 main.py --method circa --dataset re2-ob --test")
print()


