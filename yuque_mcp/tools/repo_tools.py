#!/usr/bin/env python3
"""
知识库相关工具实现
"""

from typing import Dict, Any
from fastmcp import tool, Context
from yuque_mcp.utils.api_client import YuqueAPIClient
from yuque_mcp.utils.response_formatter import format_success_response, format_error_response
import os


@tool(name="list_repos", description="列出当前用户的知识库")
async def list_repos(ctx: Context, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """
    列出当前用户的知识库
    
    Args:
        ctx: MCP上下文
        limit: 每页数量
        offset: 偏移量
        
    Returns:
        知识库列表响应
    """
    try:
        token = os.environ.get("YUQUE_TOKEN")
        if not token:
            return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
        async with YuqueAPIClient(token) as client:
            result = await client.list_repos(limit=limit, offset=offset)
            return format_success_response(result, "获取知识库列表成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取知识库列表失败: {str(e)}")


@tool(name="get_repo", description="获取知识库详情")
async def get_repo(ctx: Context, namespace: str) -> Dict[str, Any]:
    """
    获取知识库详情
    
    Args:
        ctx: MCP上下文
        namespace: 知识库命名空间
        
    Returns:
        知识库详情响应
    """
    try:
        token = os.environ.get("YUQUE_TOKEN")
        if not token:
            return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
        if not namespace:
            return format_error_response("PARAM_ERROR", "缺少知识库命名空间")
        
        async with YuqueAPIClient(token) as client:
            result = await client.get_repo(namespace)
            return format_success_response(result, "获取知识库详情成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取知识库详情失败: {str(e)}")
