#!/usr/bin/env python3
import os
import sys
import logging
import re
from typing import Optional

# 设置环境变量禁用 FastMCP 输出（不禁用 stdout/stderr，因为 MCP 协议需要它们）
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['FORCE_COLOR'] = '0'
os.environ['NO_COLOR'] = '1'

from fastmcp import FastMCP

# 导入项目内部模块
from yuque_mcp.utils.api_client import YuqueAPIClient
from yuque_mcp.utils.response_formatter import format_success_response, format_error_response

# 创建FastMCP实例
mcp = FastMCP(
    name="yuque-mcp-server",
    version="1.0.0",
    instructions="语雀MCP服务器，提供语雀API的MCP接口"
)

# 禁用所有日志输出到控制台
logging.basicConfig(
    level=logging.CRITICAL,
    filename="yuque_mcp.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 禁用FastMCP和rich的日志输出
logging.getLogger("fastmcp").setLevel(logging.CRITICAL)
logging.getLogger("rich").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

@mcp.tool()
async def get_user_info() -> dict:
    """获取当前用户信息"""
    token = os.environ.get("YUQUE_TOKEN")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")

    try:
        async with YuqueAPIClient(token) as client:
            result = await client.get_user_info()
            return format_success_response(result.get("data"), "获取用户信息成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取用户信息失败: {str(e)}")

@mcp.tool()
async def list_repos(limit: int = 20, offset: int = 0) -> dict:
    """列出当前用户的知识库"""
    token = os.environ.get("YUQUE_TOKEN")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")

    try:
        async with YuqueAPIClient(token) as client:
            result = await client.list_repos(limit=limit, offset=offset)
            return format_success_response(result, "获取知识库列表成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取知识库列表失败: {str(e)}")

if __name__ == "__main__":
    mcp.run(show_banner=False)
