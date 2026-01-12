#!/usr/bin/env python3
"""
用户相关工具实现
"""

from typing import Dict, Any
from fastmcp import tool, Context
from yuque_mcp.utils.api_client import YuqueAPIClient
from yuque_mcp.utils.response_formatter import format_success_response, format_error_response
import os


@tool(name="get_user_info", description="获取当前用户信息")
async def get_user_info(ctx: Context) -> Dict[str, Any]:
    """
    获取当前用户信息
    
    Args:
        ctx: MCP上下文
        
    Returns:
        用户信息响应
    """
    try:
        token = os.environ.get("YUQUE_TOKEN")
        if not token:
            return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
        async with YuqueAPIClient(token) as client:
            result = await client.get_user_info()
            return format_success_response(result.get("data"), "获取用户信息成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取用户信息失败: {str(e)}")
