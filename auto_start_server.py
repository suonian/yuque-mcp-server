#!/usr/bin/env python3
"""
语雀 MCP 服务器自动启动脚本
监听外部请求，自动启动主服务进程
"""

import socket
import subprocess
import time
import threading
import os
import logging
import sys
from typing import Optional, Dict, Any


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoStartServer:
    """自动启动服务器类"""
    
    def __init__(self, listen_port: int = 3000, target_port: int = 3000, target_script: str = "app_async.py"):
        """初始化自动启动服务器
        
        Args:
            listen_port: 监听端口，默认3000
            target_port: 主服务端口，默认3000
            target_script: 主服务脚本，默认app_async.py
        """
        self.listen_port = listen_port
        self.target_port = target_port
        self.target_script = target_script
        self.server_process: Optional[subprocess.Popen] = None
        self.server_running = False
        self.lock = threading.Lock()
        self.listen_socket = None
        
        # 确定主服务脚本的路径
        self.script_path = os.path.join(os.path.dirname(__file__), self.target_script)
        if not os.path.exists(self.script_path):
            logger.error(f"主服务脚本不存在: {self.script_path}")
            sys.exit(1)
    
    def check_server_status(self) -> bool:
        """检查主服务是否正在运行
        
        Returns:
            bool: 主服务是否正在运行
        """
        try:
            # 尝试连接到主服务端口
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(("localhost", self.target_port))
            sock.close()
            return result == 0
        except Exception as e:
            logger.error(f"检查服务状态失败: {e}")
            return False
    
    def start_server(self) -> bool:
        """启动主服务进程
        
        Returns:
            bool: 主服务是否启动成功
        """
        with self.lock:
            if self.server_running:
                logger.info("主服务已经在运行")
                return True
            
            logger.info(f"正在启动主服务: {self.script_path}")
            
            try:
                # 启动主服务进程
                self.server_process = subprocess.Popen(
                    [sys.executable, self.script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # 启动输出读取线程
                threading.Thread(target=self._read_server_output, daemon=True).start()
                
                # 等待服务启动
                logger.info(f"等待主服务在端口 {self.target_port} 上启动...")
                for i in range(10):
                    if self.check_server_status():
                        logger.info(f"主服务已成功启动，端口: {self.target_port}")
                        self.server_running = True
                        return True
                    time.sleep(1)
                
                logger.error(f"主服务启动超时，端口: {self.target_port}")
                return False
            except Exception as e:
                logger.error(f"启动主服务失败: {e}")
                return False
    
    def _read_server_output(self):
        """读取主服务的输出
        
        这个方法在单独的线程中运行，用于读取主服务的输出并记录日志
        """
        if not self.server_process:
            return
        
        try:
            while True:
                # 读取 stdout
                stdout_line = self.server_process.stdout.readline()
                if stdout_line:
                    logger.info(f"[主服务] {stdout_line.strip()}")
                
                # 读取 stderr
                stderr_line = self.server_process.stderr.readline()
                if stderr_line:
                    logger.error(f"[主服务] {stderr_line.strip()}")
                
                # 检查进程是否结束
                if self.server_process.poll() is not None:
                    logger.error(f"主服务进程已结束，退出码: {self.server_process.returncode}")
                    with self.lock:
                        self.server_running = False
                    break
        except Exception as e:
            logger.error(f"读取主服务输出失败: {e}")
    
    def forward_request(self, client_socket: socket.socket):
        """将请求转发到主服务
        
        Args:
            client_socket: 客户端套接字
        """
        try:
            # 创建到主服务的连接
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect(("localhost", self.target_port))
            
            # 接收客户端请求
            request = client_socket.recv(4096)
            if not request:
                return
            
            # 将请求转发到主服务
            server_socket.sendall(request)
            
            # 接收主服务响应
            response = b""
            while True:
                part = server_socket.recv(4096)
                if not part:
                    break
                response += part
            
            # 将响应返回给客户端
            client_socket.sendall(response)
            
            server_socket.close()
        except Exception as e:
            logger.error(f"转发请求失败: {e}")
            # 返回错误响应
            error_response = b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\nInternal Server Error"
            client_socket.sendall(error_response)
        finally:
            client_socket.close()
    
    def handle_client(self, client_socket: socket.socket, address: tuple):
        """处理客户端连接
        
        Args:
            client_socket: 客户端套接字
            address: 客户端地址
        """
        logger.info(f"收到来自 {address} 的请求")
        
        # 检查主服务是否正在运行
        if not self.check_server_status():
            # 启动主服务
            if not self.start_server():
                logger.error("主服务启动失败，无法处理请求")
                error_response = b"HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/plain\r\n\nFailed to start server"
                client_socket.sendall(error_response)
                client_socket.close()
                return
        
        # 转发请求到主服务
        self.forward_request(client_socket)
    
    def start_listener(self):
        """启动请求监听器"""
        try:
            # 创建监听套接字
            self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listen_socket.bind(("0.0.0.0", self.listen_port))
            self.listen_socket.listen(5)
            
            logger.info(f"自动启动服务器已启动，监听端口: {self.listen_port}")
            logger.info(f"主服务脚本: {self.script_path}")
            logger.info(f"主服务端口: {self.target_port}")
            logger.info("等待外部请求...")
            
            while True:
                # 接受客户端连接
                client_socket, address = self.listen_socket.accept()
                
                # 处理客户端连接
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
        except KeyboardInterrupt:
            logger.info("收到中断信号，正在关闭...")
        except Exception as e:
            logger.error(f"启动监听器失败: {e}")
        finally:
            if self.listen_socket:
                self.listen_socket.close()
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait()
    
    def stop(self):
        """停止自动启动服务器"""
        if self.listen_socket:
            self.listen_socket.close()
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
        logger.info("自动启动服务器已停止")


def main():
    """主函数"""
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="语雀 MCP 服务器自动启动脚本")
    parser.add_argument("--listen-port", type=int, default=3000, help="监听端口，默认3000")
    parser.add_argument("--target-port", type=int, default=3000, help="主服务端口，默认3000")
    parser.add_argument("--target-script", type=str, default="app_async.py", help="主服务脚本，默认app_async.py")
    
    args = parser.parse_args()
    
    # 创建自动启动服务器实例
    auto_server = AutoStartServer(
        listen_port=args.listen_port,
        target_port=args.target_port,
        target_script=args.target_script
    )
    
    # 启动监听器
    auto_server.start_listener()


if __name__ == "__main__":
    main()
