# Basic example from README
from RCAEval.e2e.baro import baro
from RCAEval.utility import download_data, read_data

# download a sample data to data.csv
download_data()

# read data from data.csv
data = read_data("data.csv")
anomaly_detected_timestamp = 1692569339

# perform root cause analysis
root_causes = baro(data, anomaly_detected_timestamp)["ranks"]

# print the top 5 root causes
print("Top 5 root causes:", root_causes[:5])
print("\n✅ 项目运行成功！")
print("这是一个根因分析(RCA)工具，用于诊断微服务系统中的故障。")
print("上面显示了前5个最可能的根本原因。")


