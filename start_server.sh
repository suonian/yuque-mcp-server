#!/bin/bash

# 语雀 MCP 代理服务器启动脚本
# 功能：检测服务是否运行，如果没有则自动启动

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="yuque-proxy.js"
CONFIG_FILE="$SCRIPT_DIR/yuque-config.env"
PORT=${PORT:-3000}
PID_FILE="/tmp/yuque-proxy.pid"
LOG_FILE="/tmp/yuque-proxy.log"

# 加载配置文件（如果存在）
load_config() {
    if [ -f "$CONFIG_FILE" ]; then
        echo "📝 加载配置文件: $CONFIG_FILE"
        # 读取配置文件并导出环境变量（忽略注释和空行）
        set -a
        source "$CONFIG_FILE" 2>/dev/null
        set +a
    fi
}

# 检查服务是否运行
check_server() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            # 检查端口是否被占用
            if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
                return 0  # 服务正在运行
            fi
        fi
        # PID 文件存在但进程不存在，清理
        rm -f "$PID_FILE"
    fi
    return 1  # 服务未运行
}

# 启动服务
start_server() {
    if check_server; then
        echo "✅ 服务已在运行中 (PID: $(cat $PID_FILE))"
        return 0
    fi
    
    # 加载配置文件
    load_config
    
    echo "🚀 正在启动语雀 MCP 代理服务器..."
    cd "$SCRIPT_DIR"
    
    # 检查 Token 配置
    if [ -z "$YUQUE_TOKEN" ]; then
        echo "⚠️  警告: 未设置 YUQUE_TOKEN 环境变量"
        echo "   提示: 可以通过以下方式配置："
        echo "   1. 创建配置文件: $CONFIG_FILE"
        echo "   2. 设置环境变量: export YUQUE_TOKEN=your-token"
        echo "   3. 在 Chatbox 的 HTTP Header 中配置: X-Yuque-Token"
        echo ""
        echo "   继续启动服务（Token 可通过 HTTP Header 提供）..."
    fi
    
    # 启动服务（后台运行，传递环境变量）
    nohup env YUQUE_TOKEN="$YUQUE_TOKEN" PORT="$PORT" python3 "$SCRIPT_NAME" > "$LOG_FILE" 2>&1 &
    PID=$!
    
    # 保存 PID
    echo $PID > "$PID_FILE"
    
    # 等待服务启动
    sleep 2
    
    # 检查是否启动成功
    if check_server; then
        echo "✅ 服务启动成功！"
        echo "   PID: $PID"
        echo "   端口: $PORT"
        echo "   日志: $LOG_FILE"
        echo "   健康检查: http://localhost:$PORT/health"
        return 0
    else
        echo "❌ 服务启动失败，请查看日志: $LOG_FILE"
        rm -f "$PID_FILE"
        return 1
    fi
}

# 停止服务
stop_server() {
    if [ ! -f "$PID_FILE" ]; then
        echo "⚠️  服务未运行"
        return 0
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "🛑 正在停止服务 (PID: $PID)..."
        kill "$PID"
        sleep 1
        
        # 强制杀死（如果还在运行）
        if ps -p "$PID" > /dev/null 2>&1; then
            kill -9 "$PID"
        fi
        
        rm -f "$PID_FILE"
        echo "✅ 服务已停止"
    else
        echo "⚠️  PID 文件存在但进程不存在，清理 PID 文件"
        rm -f "$PID_FILE"
    fi
}

# 查看状态
status_server() {
    # 加载配置文件以显示配置信息
    load_config
    
    if check_server; then
        PID=$(cat "$PID_FILE")
        echo "✅ 服务正在运行"
        echo "   PID: $PID"
        echo "   端口: $PORT"
        echo "   日志: $LOG_FILE"
        
        # 显示 Token 配置状态
        if [ -n "$YUQUE_TOKEN" ]; then
            echo "   Token: 已配置（环境变量）"
        elif [ -f "$CONFIG_FILE" ]; then
            echo "   Token: 已配置（配置文件）"
        else
            echo "   Token: 未配置（需通过 HTTP Header 提供）"
        fi
        
        # 测试健康检查
        if command -v curl > /dev/null 2>&1; then
            echo ""
            echo "📊 健康检查:"
            curl -s http://localhost:$PORT/health | python3 -m json.tool 2>/dev/null || echo "   无法连接"
        fi
    else
        echo "❌ 服务未运行"
    fi
}

# 查看日志
view_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "⚠️  日志文件不存在: $LOG_FILE"
    fi
}

# 主函数
main() {
    case "${1:-start}" in
        start)
            start_server
            ;;
        stop)
            stop_server
            ;;
        restart)
            stop_server
            sleep 1
            start_server
            ;;
        status)
            status_server
            ;;
        logs)
            view_logs
            ;;
        config)
            # 创建配置文件
            if [ -f "$CONFIG_FILE" ]; then
                echo "📝 配置文件已存在: $CONFIG_FILE"
                echo ""
                echo "当前配置:"
                cat "$CONFIG_FILE"
            else
                echo "📝 创建配置文件: $CONFIG_FILE"
                cat > "$CONFIG_FILE" << EOF
# 语雀 MCP 代理配置文件
# 此文件包含敏感信息，请勿提交到代码仓库

# 语雀 Token（必需）
# 获取方式：语雀设置 > 个人设置 > Token
YUQUE_TOKEN=your-token-here

# 服务端口（可选，默认 3000）
PORT=3000
EOF
                chmod 600 "$CONFIG_FILE"
                echo "✅ 配置文件已创建"
                echo "⚠️  请编辑 $CONFIG_FILE 并填入您的 Token"
            fi
            ;;
        *)
            echo "用法: $0 {start|stop|restart|status|logs|config}"
            echo ""
            echo "命令说明:"
            echo "  start   - 启动服务（如果未运行）"
            echo "  stop    - 停止服务"
            echo "  restart - 重启服务"
            echo "  status  - 查看服务状态"
            echo "  logs    - 查看日志（实时）"
            echo "  config  - 创建/查看配置文件"
            exit 1
            ;;
    esac
}

main "$@"

