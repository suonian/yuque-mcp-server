#!/usr/bin/env python3
"""
语雀 MCP 代理自动启动包装器
功能：在收到请求时自动检测并启动服务
"""

import os
import sys
import time
import subprocess
import socket
import requests
from pathlib import Path

# 配置
SCRIPT_DIR = Path(__file__).parent.absolute()
SERVER_SCRIPT = SCRIPT_DIR / "yuque-proxy.js"
PORT = int(os.environ.get("PORT", 3000))
HOST = "localhost"
CHECK_INTERVAL = 2  # 检查间隔（秒）
MAX_WAIT = 30  # 最大等待时间（秒）

def is_port_open(host, port):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def is_server_running():
    """检查服务是否运行"""
    if not is_port_open(HOST, PORT):
        return False
    
    # 尝试访问健康检查端点
    try:
        response = requests.get(f"http://{HOST}:{PORT}/test", timeout=2)
        return response.status_code == 200
    except Exception:
        return False

def start_server():
    """启动服务器"""
    print(f"🚀 正在启动语雀 MCP 代理服务器...")
    print(f"   脚本: {SERVER_SCRIPT}")
    print(f"   端口: {PORT}")
    
    # 启动服务器（后台运行）
    try:
        process = subprocess.Popen(
            [sys.executable, str(SERVER_SCRIPT)],
            cwd=str(SCRIPT_DIR),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True
        )
        
        # 等待服务启动
        print(f"⏳ 等待服务启动...")
        for i in range(MAX_WAIT // CHECK_INTERVAL):
            time.sleep(CHECK_INTERVAL)
            if is_server_running():
                print(f"✅ 服务启动成功！")
                print(f"   PID: {process.pid}")
                print(f"   地址: http://{HOST}:{PORT}")
                return True
        
        print(f"❌ 服务启动超时")
        return False
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        return False

def ensure_server_running():
    """确保服务器正在运行"""
    if is_server_running():
        return True
    
    return start_server()

def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # 仅检查模式
        if is_server_running():
            print("✅ 服务正在运行")
            sys.exit(0)
        else:
            print("❌ 服务未运行")
            sys.exit(1)
    
    # 自动启动模式
    if ensure_server_running():
        print(f"\n📝 服务管理:")
        print(f"   启动脚本: ./start_server.sh start")
        print(f"   停止脚本: ./start_server.sh stop")
        print(f"   查看状态: ./start_server.sh status")
        print(f"   查看日志: ./start_server.sh logs")
        sys.exit(0)
    else:
        print(f"\n❌ 无法启动服务，请手动检查")
        sys.exit(1)

if __name__ == "__main__":
    main()

