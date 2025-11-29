#!/usr/bin/env python3
"""
stdio-wrapper.py - 将stdio请求转发到HTTP MCP服务器
用于Claude Code连接到HTTP MCP服务器
"""

import sys
import json
import httpx
import os
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger(__name__)

# 获取配置
YUQUE_MCP_URL = os.getenv("YUQUE_MCP_URL", "http://localhost:3000/mcp")
YUQUE_CONFIG_PATH = os.getenv("YUQUE_CONFIG_PATH")

def main():
    """主函数"""
    logger.info(f"🚀 启动stdio-wrapper，转发请求到: {YUQUE_MCP_URL}")
    logger.info(f"📁 配置文件路径: {YUQUE_CONFIG_PATH}")
    
    # 创建HTTP客户端
    client = httpx.Client(timeout=30.0)
    
    try:
        # 读取stdin
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                # 解析JSON请求
                request = json.loads(line)
                logger.debug(f"📥 收到请求: {json.dumps(request, ensure_ascii=False)}")
                
                # 转发请求到HTTP服务器
                response = client.post(YUQUE_MCP_URL, json=request)
                response.raise_for_status()
                
                # 读取响应
                response_data = response.json()
                logger.debug(f"📤 发送响应: {json.dumps(response_data, ensure_ascii=False)}")
                
                # 输出响应到stdout
                print(json.dumps(response_data, ensure_ascii=False))
                sys.stdout.flush()
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON解析失败: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"}
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()
            except httpx.HTTPError as e:
                logger.error(f"❌ HTTP请求失败: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"❌ 处理请求失败: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
                }
                print(json.dumps(error_response, ensure_ascii=False))
                sys.stdout.flush()
    except KeyboardInterrupt:
        logger.info("🔌 收到中断信号，退出")
    finally:
        client.close()

if __name__ == "__main__":
    main()
