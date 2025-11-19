#!/bin/bash

# Docker 功能验证脚本
# 自动测试所有 MCP 功能

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置
CONTAINER_NAME="yuque-mcp-server"
IMAGE_NAME="yuque-mcp"
PORT=3000
TOKEN="${YUQUE_TOKEN:-your-token-here}"

# 计数器
PASSED=0
FAILED=0
TOTAL=0

# 测试函数
test_case() {
    local name="$1"
    local command="$2"
    local expected_status="${3:-200}"
    
    TOTAL=$((TOTAL + 1))
    echo -n "测试 $TOTAL: $name ... "
    
    if eval "$command" > /tmp/test_output.json 2>&1; then
        local status_code=$(cat /tmp/test_output.json | grep -oP '(?<=HTTP/1.1 )\d+' | tail -1 || echo "0")
        if [ "$status_code" = "$expected_status" ] || [ -z "$status_code" ]; then
            # 检查 JSON 响应
            if grep -q "jsonrpc" /tmp/test_output.json || grep -q "status" /tmp/test_output.json; then
                echo -e "${GREEN}✓ 通过${NC}"
                PASSED=$((PASSED + 1))
                return 0
            fi
        fi
    fi
    
    echo -e "${RED}✗ 失败${NC}"
    echo "  输出: $(cat /tmp/test_output.json | head -5)"
    FAILED=$((FAILED + 1))
    return 1
}

# 等待服务就绪
wait_for_service() {
    echo "⏳ 等待服务启动..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker exec "$CONTAINER_NAME" curl -sf http://localhost:3000/health > /dev/null 2>&1; then
            echo "✅ 服务已就绪"
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    
    echo "❌ 服务启动超时"
    return 1
}

# 检查容器状态
check_container() {
    if ! docker ps | grep -q "$CONTAINER_NAME"; then
        echo "❌ 容器未运行"
        return 1
    fi
    return 0
}

# 主函数
main() {
    echo "=========================================="
    echo "🐳 Docker 功能验证测试"
    echo "=========================================="
    echo ""
    
    # 检查 Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker 未安装"
        exit 1
    fi
    
    # 检查 Token
    if [ "$TOKEN" = "your-token-here" ]; then
        echo -e "${YELLOW}⚠️  警告: 未设置 YUQUE_TOKEN 环境变量${NC}"
        echo "   使用测试 Token，某些功能可能失败"
        echo "   设置方式: export YUQUE_TOKEN=your-token"
        echo ""
    fi
    
    # 构建镜像
    echo "📦 构建 Docker 镜像..."
    docker build -t "$IMAGE_NAME" . || {
        echo "❌ 镜像构建失败"
        exit 1
    }
    echo "✅ 镜像构建成功"
    echo ""
    
    # 停止并删除旧容器
    echo "🧹 清理旧容器..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
    echo ""
    
    # 启动容器
    echo "🚀 启动容器..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p "$PORT:3000" \
        -e YUQUE_TOKEN="$TOKEN" \
        -e PORT=3000 \
        "$IMAGE_NAME" || {
        echo "❌ 容器启动失败"
        exit 1
    }
    echo "✅ 容器启动成功"
    echo ""
    
    # 等待服务就绪
    wait_for_service || exit 1
    echo ""
    
    # 开始测试
    echo "=========================================="
    echo "🧪 开始功能测试"
    echo "=========================================="
    echo ""
    
    # 1. 健康检查
    test_case "健康检查端点" \
        "curl -s -w '\n%{http_code}' http://localhost:$PORT/health"
    
    # 2. 测试端点
    test_case "测试端点" \
        "curl -s -w '\n%{http_code}' http://localhost:$PORT/test"
    
    # 3. MCP 初始化
    test_case "MCP 初始化 (initialize)" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -H 'X-Yuque-Token: $TOKEN' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2024-11-05\",\"capabilities\":{},\"clientInfo\":{\"name\":\"test\",\"version\":\"1.0.0\"}}}'"
    
    # 4. 获取工具列表
    test_case "获取工具列表 (tools/list)" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -H 'X-Yuque-Token: $TOKEN' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\",\"params\":{}}'"
    
    # 5. 获取用户信息
    test_case "获取用户信息 (get_user_info)" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -H 'X-Yuque-Token: $TOKEN' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"get_user_info\",\"arguments\":{}}}'"
    
    # 6. 列出知识库
    test_case "列出知识库 (list_repos)" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -H 'X-Yuque-Token: $TOKEN' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":4,\"method\":\"tools/call\",\"params\":{\"name\":\"list_repos\",\"arguments\":{}}}'"
    
    # 7. Ping 测试
    test_case "Ping 测试" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -H 'X-Yuque-Token: $TOKEN' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":5,\"method\":\"ping\",\"params\":{}}'"
    
    # 8. CORS 测试
    test_case "CORS 支持" \
        "curl -s -X OPTIONS http://localhost:$PORT/mcp \
        -H 'Origin: http://localhost:8080' \
        -H 'Access-Control-Request-Method: POST' \
        -w '\n%{http_code}'"
    
    # 9. 错误处理测试（无 Token）
    test_case "错误处理（缺少 Token）" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":6,\"method\":\"tools/call\",\"params\":{\"name\":\"get_user_info\",\"arguments\":{}}}'"
    
    # 10. 无效方法测试
    test_case "错误处理（无效方法）" \
        "curl -s -X POST http://localhost:$PORT/mcp \
        -H 'Content-Type: application/json' \
        -H 'X-Yuque-Token: $TOKEN' \
        -d '{\"jsonrpc\":\"2.0\",\"id\":7,\"method\":\"invalid_method\",\"params\":{}}'"
    
    echo ""
    echo "=========================================="
    echo "📊 测试结果汇总"
    echo "=========================================="
    echo "总测试数: $TOTAL"
    echo -e "${GREEN}通过: $PASSED${NC}"
    echo -e "${RED}失败: $FAILED${NC}"
    echo ""
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}✅ 所有测试通过！${NC}"
        echo ""
        echo "容器信息:"
        docker ps | grep "$CONTAINER_NAME"
        echo ""
        echo "查看日志: docker logs $CONTAINER_NAME"
        echo "停止容器: docker stop $CONTAINER_NAME"
        echo "删除容器: docker rm $CONTAINER_NAME"
        exit 0
    else
        echo -e "${RED}❌ 部分测试失败${NC}"
        echo ""
        echo "查看日志: docker logs $CONTAINER_NAME"
        exit 1
    fi
}

# 清理函数
cleanup() {
    echo ""
    echo "🧹 清理资源..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
}

# 捕获退出信号
trap cleanup EXIT

# 运行主函数
main "$@"

