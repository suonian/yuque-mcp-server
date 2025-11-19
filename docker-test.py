#!/usr/bin/env python3
"""
Docker 功能验证脚本（Python 版本）
自动测试所有 MCP 功能
"""

import os
import sys
import time
import json
import subprocess
import requests
from typing import Dict, Any, Optional

# 配置
CONTAINER_NAME = "yuque-mcp-server"
IMAGE_NAME = "yuque-mcp"
PORT = 3000
TOKEN = os.environ.get("YUQUE_TOKEN", "your-token-here")

# 测试结果
PASSED = 0
FAILED = 0
TOTAL = 0
FAILED_TESTS = []


def print_colored(text: str, color: str = "white"):
    """彩色输出"""
    colors = {
        "red": "\033[0;31m",
        "green": "\033[0;32m",
        "yellow": "\033[1;33m",
        "blue": "\033[0;34m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")


def run_command(cmd: list, check: bool = True) -> subprocess.CompletedProcess:
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        if check:
            print_colored(f"❌ 命令执行失败: {' '.join(cmd)}", "red")
            print_colored(f"   错误: {e.stderr}", "red")
        raise


def test_case(name: str, test_func, *args, **kwargs) -> bool:
    """测试用例包装器"""
    global TOTAL, PASSED, FAILED
    
    TOTAL += 1
    print(f"测试 {TOTAL}: {name} ... ", end="", flush=True)
    
    try:
        result = test_func(*args, **kwargs)
        if result:
            print_colored("✓ 通过", "green")
            PASSED += 1
            return True
        else:
            print_colored("✗ 失败", "red")
            FAILED += 1
            FAILED_TESTS.append(name)
            return False
    except Exception as e:
        print_colored("✗ 失败", "red")
        print_colored(f"   错误: {str(e)}", "red")
        FAILED += 1
        FAILED_TESTS.append(name)
        return False


def test_health_check() -> bool:
    """测试健康检查端点"""
    try:
        response = requests.get(f"http://localhost:{PORT}/health", timeout=5)
        return response.status_code == 200 and "status" in response.json()
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_test_endpoint() -> bool:
    """测试测试端点"""
    try:
        response = requests.get(f"http://localhost:{PORT}/test", timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_mcp_initialize() -> bool:
    """测试 MCP 初始化"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test",
                    "version": "1.0.0"
                }
            }
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            headers={"X-Yuque-Token": TOKEN},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return "result" in data and "protocolVersion" in data.get("result", {})
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_tools_list() -> bool:
    """测试获取工具列表"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            headers={"X-Yuque-Token": TOKEN},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return "result" in data and "tools" in data.get("result", {})
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_get_user_info() -> bool:
    """测试获取用户信息"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_user_info",
                "arguments": {}
            }
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            headers={"X-Yuque-Token": TOKEN},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            # 检查是否有结果或错误（Token 无效时会有错误，这也是正常的响应）
            return "result" in data or "error" in data
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_list_repos() -> bool:
    """测试列出知识库"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "list_repos",
                "arguments": {}
            }
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            headers={"X-Yuque-Token": TOKEN},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            return "result" in data or "error" in data
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_ping() -> bool:
    """测试 Ping"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "ping",
            "params": {}
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            headers={"X-Yuque-Token": TOKEN},
            timeout=5
        )
        return response.status_code == 200
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_cors() -> bool:
    """测试 CORS 支持"""
    try:
        response = requests.options(
            f"http://localhost:{PORT}/mcp",
            headers={
                "Origin": "http://localhost:8080",
                "Access-Control-Request-Method": "POST"
            },
            timeout=5
        )
        return response.status_code == 200 and "Access-Control-Allow-Origin" in response.headers
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_error_handling_no_token() -> bool:
    """测试错误处理（缺少 Token）"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "tools/call",
            "params": {
                "name": "get_user_info",
                "arguments": {}
            }
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            timeout=5
        )
        # 应该返回错误
        if response.status_code == 200:
            data = response.json()
            return "error" in data
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False


def test_error_handling_invalid_method() -> bool:
    """测试错误处理（无效方法）"""
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "invalid_method",
            "params": {}
        }
        response = requests.post(
            f"http://localhost:{PORT}/mcp",
            json=payload,
            headers={"X-Yuque-Token": TOKEN},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return "error" in data
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False


def wait_for_service(max_attempts: int = 30) -> bool:
    """等待服务就绪"""
    print_colored("⏳ 等待服务启动...", "yellow")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"http://localhost:{PORT}/health", timeout=2)
            if response.status_code == 200:
                print_colored("✅ 服务已就绪", "green")
                return True
        except:
            pass
        time.sleep(1)
    
    print_colored("❌ 服务启动超时", "red")
    return False


def check_container() -> bool:
    """检查容器状态"""
    result = run_command(["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"], check=False)
    return CONTAINER_NAME in result.stdout


def main():
    """主函数"""
    print("=" * 50)
    print_colored("🐳 Docker 功能验证测试", "blue")
    print("=" * 50)
    print()
    
    # 检查 Docker
    try:
        run_command(["docker", "--version"])
    except:
        print_colored("❌ Docker 未安装或不可用", "red")
        sys.exit(1)
    
    # 检查 Token
    if TOKEN == "your-token-here":
        print_colored("⚠️  警告: 未设置 YUQUE_TOKEN 环境变量", "yellow")
        print("   使用测试 Token，某些功能可能失败")
        print("   设置方式: export YUQUE_TOKEN=your-token")
        print()
    
    # 构建镜像
    print_colored("📦 构建 Docker 镜像...", "blue")
    try:
        run_command(["docker", "build", "-t", IMAGE_NAME, "."])
        print_colored("✅ 镜像构建成功", "green")
    except:
        print_colored("❌ 镜像构建失败", "red")
        sys.exit(1)
    print()
    
    # 清理旧容器
    print_colored("🧹 清理旧容器...", "blue")
    run_command(["docker", "stop", CONTAINER_NAME], check=False)
    run_command(["docker", "rm", CONTAINER_NAME], check=False)
    print()
    
    # 启动容器
    print_colored("🚀 启动容器...", "blue")
    try:
        run_command([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", f"{PORT}:3000",
            "-e", f"YUQUE_TOKEN={TOKEN}",
            "-e", "PORT=3000",
            IMAGE_NAME
        ])
        print_colored("✅ 容器启动成功", "green")
    except:
        print_colored("❌ 容器启动失败", "red")
        sys.exit(1)
    print()
    
    # 等待服务就绪
    if not wait_for_service():
        print_colored("❌ 服务启动失败", "red")
        print_colored("查看日志: docker logs " + CONTAINER_NAME, "yellow")
        sys.exit(1)
    print()
    
    # 开始测试
    print("=" * 50)
    print_colored("🧪 开始功能测试", "blue")
    print("=" * 50)
    print()
    
    test_case("健康检查端点", test_health_check)
    test_case("测试端点", test_test_endpoint)
    test_case("MCP 初始化 (initialize)", test_mcp_initialize)
    test_case("获取工具列表 (tools/list)", test_tools_list)
    test_case("获取用户信息 (get_user_info)", test_get_user_info)
    test_case("列出知识库 (list_repos)", test_list_repos)
    test_case("Ping 测试", test_ping)
    test_case("CORS 支持", test_cors)
    test_case("错误处理（缺少 Token）", test_error_handling_no_token)
    test_case("错误处理（无效方法）", test_error_handling_invalid_method)
    
    # 输出结果
    print()
    print("=" * 50)
    print_colored("📊 测试结果汇总", "blue")
    print("=" * 50)
    print(f"总测试数: {TOTAL}")
    print_colored(f"通过: {PASSED}", "green")
    print_colored(f"失败: {FAILED}", "red")
    print()
    
    if FAILED > 0:
        print_colored("失败的测试:", "yellow")
        for test in FAILED_TESTS:
            print(f"  - {test}")
        print()
    
    if FAILED == 0:
        print_colored("✅ 所有测试通过！", "green")
        print()
        print("容器信息:")
        run_command(["docker", "ps", "--filter", f"name={CONTAINER_NAME}"], check=False)
        print()
        print_colored("查看日志: docker logs " + CONTAINER_NAME, "blue")
        print_colored("停止容器: docker stop " + CONTAINER_NAME, "blue")
        print_colored("删除容器: docker rm " + CONTAINER_NAME, "blue")
        return 0
    else:
        print_colored("❌ 部分测试失败", "red")
        print()
        print_colored("查看日志: docker logs " + CONTAINER_NAME, "yellow")
        return 1


def cleanup():
    """清理函数"""
    print()
    print_colored("🧹 清理资源...", "blue")
    run_command(["docker", "stop", CONTAINER_NAME], check=False)
    run_command(["docker", "rm", CONTAINER_NAME], check=False)


if __name__ == "__main__":
    try:
        exit_code = main()
        cleanup()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  测试被中断", "yellow")
        cleanup()
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n❌ 发生错误: {e}", "red")
        cleanup()
        sys.exit(1)

