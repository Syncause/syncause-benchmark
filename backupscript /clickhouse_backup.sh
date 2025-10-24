#!/bin/bash

# ClickHouse 备份脚本
# 使用 clickhouse-backup 工具进行备份和恢复

set -e

# 配置变量
BACKUP_DIR="./clickhouse_backups"
CONFIG_FILE="./clickhouse-backup-config.yml"
BACKUP_TOOL="./clickhouse-backup"

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

# 检查工具是否存在
check_tool() {
    if [ ! -f "$BACKUP_TOOL" ]; then
        log_error "clickhouse-backup 工具不存在: $BACKUP_TOOL"
        log_info "请下载 clickhouse-backup 工具到当前目录"
        log_info "下载地址: https://github.com/Altinity/clickhouse-backup/releases"
        exit 1
    fi
    
    if [ ! -x "$BACKUP_TOOL" ]; then
        log_info "设置 clickhouse-backup 执行权限..."
        chmod +x "$BACKUP_TOOL"
    fi
}

# 检查配置文件
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        log_warning "配置文件不存在，创建默认配置..."
        create_default_config
    fi
}

# 创建默认配置文件
create_default_config() {
    cat > "$CONFIG_FILE" << 'EOF'
general:
  remote_storage: local
  max_file_size: 1073741824
  disable_progress_bar: false
  backups_to_keep_local: 5
  backups_to_keep_remote: 0
  log_level: info
  allow_empty_backups: false

clickhouse:
  username: default
  password: ''
  host: localhost
  port: 9000
  secure: false
  skip_verify: false
  sync_replicated_tables: true
  log_sql_queries: false
  config_dir: /etc/clickhouse-server/
  restart_command: 'systemctl restart clickhouse-server'
  ignore_databases: []
  ignore_tables: []
  skip_check_parts_columns: false
  timeout: 5m
  freeze_by_part: false

local:
  path: ./clickhouse_backups/
EOF
    log_success "已创建默认配置文件: $CONFIG_FILE"
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
    echo "ClickHouse 备份恢复工具"
    echo ""
    echo "用法: $0 [命令] [选项]"
    echo ""
    echo "命令:"
    echo "  backup [名称]     创建备份"
    echo "  restore [名称]    恢复备份"
    echo "  list             列出所有备份"
    echo "  delete [名称]    删除备份"
    echo "  clean            清理旧备份"
    echo "  status           检查 ClickHouse 连接状态"
    echo "  help             显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 backup                    # 创建带时间戳的备份"
    echo "  $0 backup my_backup         # 创建指定名称的备份"
    echo "  $0 restore my_backup        # 恢复指定备份"
    echo "  $0 list                     # 列出所有备份"
    echo "  $0 delete old_backup        # 删除指定备份"
    echo "  $0 clean                    # 清理7天前的备份"
}

# 检查 ClickHouse 连接
check_clickhouse() {
    log_info "检查 ClickHouse 连接状态..."
    if $BACKUP_TOOL --config "$CONFIG_FILE" list > /dev/null 2>&1; then
        log_success "ClickHouse 连接正常"
        return 0
    else
        log_error "无法连接到 ClickHouse"
        log_info "请检查:"
        log_info "1. ClickHouse 服务是否运行"
        log_info "2. 配置文件中的连接参数是否正确"
        log_info "3. 网络连接是否正常"
        return 1
    fi
}

# 创建备份
create_backup() {
    local backup_name="$1"
    
    if [ -z "$backup_name" ]; then
        backup_name="backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    log_info "开始创建备份: $backup_name"
    
    if $BACKUP_TOOL --config "$CONFIG_FILE" create "$backup_name"; then
        log_success "备份创建成功: $backup_name"
        
        # 显示备份信息
        log_info "备份详情:"
        $BACKUP_TOOL --config "$CONFIG_FILE" list | grep "$backup_name" || true
    else
        log_error "备份创建失败"
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
    
    # 检查备份是否存在
    if ! $BACKUP_TOOL --config "$CONFIG_FILE" list | grep -q "$backup_name"; then
        log_error "备份不存在: $backup_name"
        log_info "使用 '$0 list' 查看可用备份"
        exit 1
    fi
    
    log_warning "即将恢复备份: $backup_name"
    log_warning "这将覆盖当前数据库中的数据！"
    read -p "确认继续吗？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "开始恢复备份: $backup_name"
        
        if $BACKUP_TOOL --config "$CONFIG_FILE" restore "$backup_name"; then
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
    $BACKUP_TOOL --config "$CONFIG_FILE" list
}

# 删除备份
delete_backup() {
    local backup_name="$1"
    
    if [ -z "$backup_name" ]; then
        log_error "请指定要删除的备份名称"
        log_info "使用 '$0 list' 查看可用备份"
        exit 1
    fi
    
    # 检查备份是否存在
    if ! $BACKUP_TOOL --config "$CONFIG_FILE" list | grep -q "$backup_name"; then
        log_error "备份不存在: $backup_name"
        exit 1
    fi
    
    log_warning "即将删除备份: $backup_name"
    read -p "确认删除吗？(y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if $BACKUP_TOOL --config "$CONFIG_FILE" delete "$backup_name"; then
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
    
    if $BACKUP_TOOL --config "$CONFIG_FILE" delete --older-than "${days}d"; then
        log_success "旧备份清理完成"
    else
        log_warning "清理过程中可能遇到问题，请检查日志"
    fi
}

# 主函数
main() {
    local command="$1"
    local param="$2"
    
    # 检查工具和配置
    check_tool
    check_config
    create_backup_dir
    
    case "$command" in
        "backup")
            create_backup "$param"
            ;;
        "restore")
            restore_backup "$param"
            ;;
        "list")
            list_backups
            ;;
        "delete")
            delete_backup "$param"
            ;;
        "clean")
            clean_old_backups "$param"
            ;;
        "status")
            check_clickhouse
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
