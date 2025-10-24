#!/bin/bash
# SREChat API curl请求示例

echo "========================================================================"
echo "SREChat API 调用示例"
echo "========================================================================"
echo ""

# 示例1: 检测当前时间最近15分钟的异常
echo "示例1: 检测当前时间（最近15分钟）"
echo "------------------------------------------------------------------------"
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%S+08:00" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S+08:00")
echo "检测时间: $CURRENT_TIME"
echo ""
echo "curl命令:"
cat << 'EOF'
curl -XPOST http://192.168.1.6:28522/api/v1/srechat \
  -H 'Accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "threadId": "thread_'$(date +%s)'_test",
    "runId": "run_'$(date +%s)'_test",
    "messages": [{
      "role": "user",
      "content": "Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. ('$(date +"%Y-%m-%dT%H:%M:%S+08:00")')",
      "id": "msg_'$(date +%s)'_test"
    }],
    "state": {},
    "tools": [],
    "context": [],
    "forwardedProps": {}
  }'
EOF
echo ""
echo ""

# 示例2: 检测18:05时间点
echo "示例2: 检测18:05时间点（17:50-18:05）"
echo "------------------------------------------------------------------------"
echo "检测时间: 2025-10-14T18:05:00+08:00"
echo ""
echo "curl命令:"
cat << 'EOF'
curl -XPOST http://192.168.1.6:28522/api/v1/srechat \
  -H 'Accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "threadId": "thread_1805_analysis",
    "runId": "run_1805_analysis",
    "messages": [{
      "role": "user",
      "content": "Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. (2025-10-14T18:05:00+08:00)",
      "id": "msg_1805_test"
    }],
    "state": {},
    "tools": [],
    "context": [],
    "forwardedProps": {}
  }'
EOF
echo ""
echo ""

# 示例3: 检测17:35时间点（之前CPU故障时间）
echo "示例3: 检测17:35时间点（17:20-17:35，之前的CPU故障时间）"
echo "------------------------------------------------------------------------"
echo "检测时间: 2025-10-14T17:35:00+08:00"
echo ""
echo "curl命令:"
cat << 'EOF'
curl -XPOST http://192.168.1.6:28522/api/v1/srechat \
  -H 'Accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "threadId": "thread_1735_analysis",
    "runId": "run_1735_analysis",
    "messages": [{
      "role": "user",
      "content": "Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. (2025-10-14T17:35:00+08:00)",
      "id": "msg_1735_test"
    }],
    "state": {},
    "tools": [],
    "context": [],
    "forwardedProps": {}
  }'
EOF
echo ""
echo ""

# 示例4: 保存输出到文件
echo "示例4: 保存输出到文件"
echo "------------------------------------------------------------------------"
cat << 'EOF'
# 保存完整输出
curl -XPOST http://192.168.1.6:28522/api/v1/srechat \
  -H 'Accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "threadId": "thread_'$(date +%s)'",
    "runId": "run_'$(date +%s)'",
    "messages": [{
      "role": "user",
      "content": "Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. ('$(date +"%Y-%m-%dT%H:%M:%S+08:00")')",
      "id": "msg_'$(date +%s)'"
    }],
    "state": {},
    "tools": [],
    "context": [],
    "forwardedProps": {}
  }' > srechat_output.txt

# 查看文件内容
cat srechat_output.txt
EOF
echo ""
echo ""

# 示例5: 格式化JSON输出
echo "示例5: 使用jq格式化输出（如果安装了jq）"
echo "------------------------------------------------------------------------"
cat << 'EOF'
curl -XPOST http://192.168.1.6:28522/api/v1/srechat \
  -H 'Accept: text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "threadId": "thread_formatted",
    "runId": "run_formatted",
    "messages": [{
      "role": "user",
      "content": "Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. ('$(date +"%Y-%m-%dT%H:%M:%S+08:00")')",
      "id": "msg_formatted"
    }],
    "state": {},
    "tools": [],
    "context": [],
    "forwardedProps": {}
  }' | grep -o '{.*}' | jq .
EOF
echo ""
echo ""

# 提供简化的一行命令
echo "========================================================================"
echo "快捷命令（直接复制使用）"
echo "========================================================================"
echo ""

echo "1️⃣ 检测当前时间最近15分钟："
echo ""
echo 'curl -XPOST http://192.168.1.6:28522/api/v1/srechat -H "Accept: text/event-stream" -H "Content-Type: application/json" -d "{\"threadId\":\"thread_$(date +%s)\",\"runId\":\"run_$(date +%s)\",\"messages\":[{\"role\":\"user\",\"content\":\"Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. ($(date +"%Y-%m-%dT%H:%M:%S+08:00"))\",\"id\":\"msg_$(date +%s)\"}],\"state\":{},\"tools\":[],\"context\":[],\"forwardedProps\":{}}"'
echo ""
echo ""

echo "2️⃣ 检测18:05时间点："
echo ""
echo 'curl -XPOST http://192.168.1.6:28522/api/v1/srechat -H "Accept: text/event-stream" -H "Content-Type: application/json" -d "{\"threadId\":\"thread_1805\",\"runId\":\"run_1805\",\"messages\":[{\"role\":\"user\",\"content\":\"Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. (2025-10-14T18:05:00+08:00)\",\"id\":\"msg_1805\"}],\"state\":{},\"tools\":[],\"context\":[],\"forwardedProps\":{}}"'
echo ""
echo ""

echo "3️⃣ 检测17:35时间点（之前CPU故障）："
echo ""
echo 'curl -XPOST http://192.168.1.6:28522/api/v1/srechat -H "Accept: text/event-stream" -H "Content-Type: application/json" -d "{\"threadId\":\"thread_1735\",\"runId\":\"run_1735\",\"messages\":[{\"role\":\"user\",\"content\":\"Check if there are any application response slowdowns or latency anomalies in the system in the last 15 minutes, and analyze the causes. (2025-10-14T17:35:00+08:00)\",\"id\":\"msg_1735\"}],\"state\":{},\"tools\":[],\"context\":[],\"forwardedProps\":{}}"'
echo ""
echo ""

echo "========================================================================"
echo "💡 提示："
echo "========================================================================"
echo "1. 返回结果是流式输出（text/event-stream）"
echo "2. 可以使用 | tee output.txt 同时显示和保存"
echo "3. API地址: http://192.168.1.6:28522/api/v1/srechat"
echo "4. 如需修改时间，替换日期时间字符串即可"
echo ""




