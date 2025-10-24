#!/bin/bash

# VictoriaMetrics 备份恢复脚本
# 使用 vmctl 专业工具进行 VictoriaMetrics 的备份和恢复

set -e

# 配置变量
BACKUP_DIR="./victoriametrics_backups"
VMCTL_TOOL="./vmctl"
VM_ADDR="http://localhost:8428"
VM_USER=""
VM_PASSWORD=""
BACKUP_FORMAT="prometheus"  # 支持 prometheus, influxdb, csv

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 vmctl 工具
check_vmctl() {
    if [ ! -f "$VMCTL_TOOL" ]; then
        log_error "vmctl 工具不存在: $VMCTL_TOOL"
        log_info "请下载 vmctl 工具到当前目录"
        log_info "下载地址: https://github.com/VictoriaMetrics/VictoriaMetrics/releases"
        exit 1
    fi
    
    if [ ! -x "$VMCTL_TOOL" ]; then
        log_info "设置 vmctl 执行权限..."
        chmod +x "$VMCTL_TOOL"
    fi
}

# 检查 VictoriaMetrics 连接
check_vm_connection() {
    log_info "检查 VictoriaMetrics 连接状态..."
    
    local check_url="${VM_ADDR}/api/v1/status/config"
    if command -v curl >/dev/null 2>&1; then
        if curl -s "$check_url" >/dev/null 2>&1; then
            log_success "VictoriaMetrics 连接正常"
            return 0
        fi
    elif command -v wget >/dev/null 2>&1; then
        if wget -q --spider "$check_url" 2>/dev/null; then
            log_success "VictoriaMetrics 连接正常"
            return 0
        fi
    fi
    
    log_error "无法连接到 VictoriaMetrics: $VM_ADDR"
    log_info "请检查:"
    log_info "1. VictoriaMetrics 服务是否运行"
    log_info "2. 地址和端口是否正确"
    log_info "3. 网络连接是否正常"
    return 1
}

# 创建备份目录
create_backup_dir() {
    if [ ! -d "$BACKUP_DIR" ]; then
        log_info "创建备份目录: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"
    fi
}

# 显示帮助信息
show_help() {
    echo "VictoriaMetrics 备份恢复工具"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  backup [名称] [时间范围]    创建备份"
    echo "  restore [名称]             恢复备份"
    echo "  list                      列出所有备份"
    echo "  delete [名称]             删除备份"
    echo "  clean                     清理旧备份"
    echo "  status                    检查 VictoriaMetrics 连接状态"
    echo "  export [查询] [时间范围]   导出特定查询数据"
    echo "  import [文件]             导入数据文件"
    echo "  help                     显示此帮助信息"
    echo ""
    echo "时间范围格式:"
    echo "  -1h                       过去1小时"
    echo "  -1d                       过去1天"
    echo "  -1w                       过去1周"
    echo "  -1M                       过去1个月"
    echo "  2023-01-01T00:00:00Z      具体时间"
    echo ""
    echo "示例:"
    echo "  $0 backup                    # 创建带时间戳的备份"
    echo "  $0 backup my_backup -1d      # 创建过去1天的备份"
    echo "  $0 restore my_backup         # 恢复指定备份"
    echo "  $0 export 'up' -1h           # 导出 up 指标过去1小时数据"
    echo "  $0 import data.prom          # 导入 Prometheus 格式数据"
}

# 创建备份
create_backup() {
    local backup_name="$1"
    local time_range="${2:--1d}"
    
    if [ -z "$backup_name" ]; then
        backup_name="vm_backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    local backup_path="$BACKUP_DIR/$backup_name"
    
    log_info "开始创建 VictoriaMetrics 备份: $backup_name"
    log_info "时间范围: $time_range"
    
    # 创建备份目录
    mkdir -p "$backup_path"
    
    # 构建 vmctl 命令
    local vmctl_cmd="$VMCTL_TOOL export"
    vmctl_cmd="$vmctl_cmd --addr=$VM_ADDR"
    vmctl_cmd="$vmctl_cmd --format=$BACKUP_FORMAT"
    vmctl_cmd="$vmctl_cmd --range=$time_range"
    
    if [ -n "$VM_USER" ]; then
        vmctl_cmd="$vmctl_cmd --username=$VM_USER"
    fi
    
    if [ -n "$VM_PASSWORD" ]; then
        vmctl_cmd="$vmctl_cmd --password=$VM_PASSWORD"
    fi
    
    vmctl_cmd="$vmctl_cmd --output=$backup_path/data.$BACKUP_FORMAT"
    
    log_info "执行命令: $vmctl_cmd"
    
    if eval "$vmctl_cmd"; then
        # 保存备份元数据
        cat > "$backup_path/metadata.json" << EOF
{
    "backup_name": "$backup_name",
    "created_at": "$(date -Iseconds)",
    "time_range": "$time_range",
    "format": "$BACKUP_FORMAT",
    "vm_addr": "$VM_ADDR",
    "vmctl_version": "$($VMCTL_TOOL --version 2>&1 | head -1)"
}
EOF
        
        # 计算备份大小
        local backup_size=$(du -sh "$backup_path" | cut -f1)
        
        log_success "备份创建成功: $backup_name"
        log_info "备份路径: $backup_path"
        log_info "备份大小: $backup_size"
        log_info "时间范围: $time_range"
    else
        log_error "备份创建失败"
        rm -rf "$backup_path"
        exit 1
    fi
}

# 恢复备份
restore_backup() {
    local backup_name="$1"
    
    if [ -z "$backup_name" ]; then
        log_error "请指定要恢复的备份名称"
        log_info "使用 '$0 list' 查看可用备份"
        exit 1
    fi
    
    local backup_path="$BACKUP_DIR/$backup_name"
    
    # 检查备份是否存在
    if [ ! -d "$backup_path" ]; then
        log_error "备份不存在: $backup_name"
        log_info "使用 '$0 list' 查看可用备份"
        exit 1
    fi
    
    # 检查备份文件
    local data_file="$backup_path/data.$BACKUP_FORMAT"
    if [ ! -f "$data_file" ]; then
        log_error "备份数据文件不存在: $data_file"
        exit 1
    fi
    
    log_warning "即将恢复备份: $backup_name"
    log_warning "这将向 VictoriaMetrics 导入数据！"
    read -p "确认继续吗？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "开始恢复备份: $backup_name"
        
        # 构建 vmctl 导入命令
        local vmctl_cmd="$VMCTL_TOOL import"
        vmctl_cmd="$vmctl_cmd --addr=$VM_ADDR"
        vmctl_cmd="$vmctl_cmd --format=$BACKUP_FORMAT"
        
        if [ -n "$VM_USER" ]; then
            vmctl_cmd="$vmctl_cmd --username=$VM_USER"
        fi
        
        if [ -n "$VM_PASSWORD" ]; then
            vmctl_cmd="$vmctl_cmd --password=$VM_PASSWORD"
        fi
        
        vmctl_cmd="$vmctl_cmd --input=$data_file"
        
        log_info "执行命令: $vmctl_cmd"
        
        if eval "$vmctl_cmd"; then
            log_success "备份恢复成功: $backup_name"
        else
            log_error "备份恢复失败"
            exit 1
        fi
    else
        log_info "取消恢复操作"
    fi
}

# 列出备份
list_backups() {
    log_info "可用备份列表:"
    echo ""
    
    if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR" 2>/dev/null)" ]; then
        log_info "没有找到任何备份"
        return 0
    fi
    
    printf "%-30s %-20s %-15s %-20s %s\n" "备份名称" "创建时间" "大小" "时间范围" "格式"
    printf "%-30s %-20s %-15s %-20s %s\n" "------------------------------" "--------------------" "---------------" "--------------------" "--------"
    
    for backup_dir in "$BACKUP_DIR"/*; do
        if [ -d "$backup_dir" ]; then
            local backup_name=$(basename "$backup_dir")
            local metadata_file="$backup_dir/metadata.json"
            
            if [ -f "$metadata_file" ]; then
                local created_at=$(jq -r '.created_at' "$metadata_file" 2>/dev/null || echo "未知")
                local time_range=$(jq -r '.time_range' "$metadata_file" 2>/dev/null || echo "未知")
                local format=$(jq -r '.format' "$metadata_file" 2>/dev/null || echo "未知")
            else
                local created_at="未知"
                local time_range="未知"
                local format="未知"
            fi
            
            local size=$(du -sh "$backup_dir" | cut -f1)
            
            printf "%-30s %-20s %-15s %-20s %s\n" "$backup_name" "$created_at" "$size" "$time_range" "$format"
        fi
    done
}

# 删除备份
delete_backup() {
    local backup_name="$1"
    
    if [ -z "$backup_name" ]; then
        log_error "请指定要删除的备份名称"
        log_info "使用 '$0 list' 查看可用备份"
        exit 1
    fi
    
    local backup_path="$BACKUP_DIR/$backup_name"
    
    # 检查备份是否存在
    if [ ! -d "$backup_path" ]; then
        log_error "备份不存在: $backup_name"
        exit 1
    fi
    
    log_warning "即将删除备份: $backup_name"
    read -p "确认删除吗？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if rm -rf "$backup_path"; then
            log_success "备份删除成功: $backup_name"
        else
            log_error "备份删除失败"
            exit 1
        fi
    else
        log_info "取消删除操作"
    fi
}

# 清理旧备份
clean_old_backups() {
    local days="${1:-7}"
    
    log_info "清理 $days 天前的备份..."
    
    local cleaned=0
    for backup_dir in "$BACKUP_DIR"/*; do
        if [ -d "$backup_dir" ]; then
            local backup_name=$(basename "$backup_dir")
            local metadata_file="$backup_dir/metadata.json"
            
            if [ -f "$metadata_file" ]; then
                local created_at=$(jq -r '.created_at' "$metadata_file" 2>/dev/null)
                if [ -n "$created_at" ] && [ "$created_at" != "null" ]; then
                    local created_timestamp=$(date -d "$created_at" +%s 2>/dev/null || echo "0")
                    local cutoff_timestamp=$(date -d "$days days ago" +%s 2>/dev/null || echo "0")
                    
                    if [ "$created_timestamp" -lt "$cutoff_timestamp" ]; then
                        log_info "删除过期备份: $backup_name"
                        rm -rf "$backup_dir"
                        ((cleaned++))
                    fi
                fi
            fi
        fi
    done
    
    if [ "$cleaned" -gt 0 ]; then
        log_success "清理完成，删除了 $cleaned 个过期备份"
    else
        log_info "没有找到需要清理的备份"
    fi
}

# 导出特定查询
export_query() {
    local query="$1"
    local time_range="${2:--1h}"
    local output_file="${3:-query_export_$(date +%Y%m%d_%H%M%S).$BACKUP_FORMAT}"
    
    if [ -z "$query" ]; then
        log_error "请指定要导出的查询"
        exit 1
    fi
    
    log_info "导出查询: $query"
    log_info "时间范围: $time_range"
    log_info "输出文件: $output_file"
    
    # 构建 vmctl 命令
    local vmctl_cmd="$VMCTL_TOOL export"
    vmctl_cmd="$vmctl_cmd --addr=$VM_ADDR"
    vmctl_cmd="$vmctl_cmd --format=$BACKUP_FORMAT"
    vmctl_cmd="$vmctl_cmd --range=$time_range"
    vmctl_cmd="$vmctl_cmd --query='$query'"
    
    if [ -n "$VM_USER" ]; then
        vmctl_cmd="$vmctl_cmd --username=$VM_USER"
    fi
    
    if [ -n "$VM_PASSWORD" ]; then
        vmctl_cmd="$vmctl_cmd --password=$VM_PASSWORD"
    fi
    
    vmctl_cmd="$vmctl_cmd --output=$output_file"
    
    log_info "执行命令: $vmctl_cmd"
    
    if eval "$vmctl_cmd"; then
        log_success "查询导出成功: $output_file"
    else
        log_error "查询导出失败"
        exit 1
    fi
}

# 导入数据文件
import_data() {
    local input_file="$1"
    
    if [ -z "$input_file" ]; then
        log_error "请指定要导入的文件"
        exit 1
    fi
    
    if [ ! -f "$input_file" ]; then
        log_error "文件不存在: $input_file"
        exit 1
    fi
    
    log_info "导入数据文件: $input_file"
    
    # 构建 vmctl 命令
    local vmctl_cmd="$VMCTL_TOOL import"
    vmctl_cmd="$vmctl_cmd --addr=$VM_ADDR"
    vmctl_cmd="$vmctl_cmd --format=$BACKUP_FORMAT"
    
    if [ -n "$VM_USER" ]; then
        vmctl_cmd="$vmctl_cmd --username=$VM_USER"
    fi
    
    if [ -n "$VM_PASSWORD" ]; then
        vmctl_cmd="$vmctl_cmd --password=$VM_PASSWORD"
    fi
    
    vmctl_cmd="$vmctl_cmd --input=$input_file"
    
    log_info "执行命令: $vmctl_cmd"
    
    if eval "$vmctl_cmd"; then
        log_success "数据导入成功: $input_file"
    else
        log_error "数据导入失败"
        exit 1
    fi
}

# 主函数
main() {
    local command="$1"
    local param1="$2"
    local param2="$3"
    local param3="$4"
    
    # 检查工具和连接
    check_vmctl
    create_backup_dir
    
    case "$command" in
        "backup")
            create_backup "$param1" "$param2"
            ;;
        "restore")
            restore_backup "$param1"
            ;;
        "list")
            list_backups
            ;;
        "delete")
            delete_backup "$param1"
            ;;
        "clean")
            clean_old_backups "$param1"
            ;;
        "export")
            export_query "$param1" "$param2" "$param3"
            ;;
        "import")
            import_data "$param1"
            ;;
        "status")
            check_vm_connection
            ;;
        "help"|"-h"|"--help"|"")
            show_help
            ;;
        *)
            log_error "未知命令: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@"
