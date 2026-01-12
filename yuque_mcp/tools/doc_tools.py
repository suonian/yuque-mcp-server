#!/usr/bin/env python3
"""
文档相关工具实现
"""

from typing import Dict, Any
from fastmcp import tool, Context
from yuque_mcp.utils.api_client import YuqueAPIClient
from yuque_mcp.utils.response_formatter import format_success_response, format_error_response
import os


@tool(name="list_docs", description="列出知识库中的文档")
async def list_docs(ctx: Context, namespace: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """
    列出知识库中的文档
    
    Args:
        ctx: MCP上下文
        namespace: 知识库命名空间
        limit: 每页数量
        offset: 偏移量
        
    Returns:
        文档列表响应
    """
    try:
        token = os.environ.get("YUQUE_TOKEN")
        if not token:
            return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
        if not namespace:
            return format_error_response("PARAM_ERROR", "缺少知识库命名空间")
        
        async with YuqueAPIClient(token) as client:
            result = await client.list_docs(namespace, limit=limit, offset=offset)
            return format_success_response(result, "获取文档列表成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取文档列表失败: {str(e)}")


@tool(name="get_doc", description="获取文档详情")
async def get_doc(ctx: Context, namespace: str, slug: str, raw: bool = False) -> Dict[str, Any]:
    """
    获取文档详情
    
    Args:
        ctx: MCP上下文
        namespace: 知识库命名空间
        slug: 文档标识
        raw: 是否获取原始Markdown
        
    Returns:
        文档详情响应
    """
    try:
        token = os.environ.get("YUQUE_TOKEN")
        if not token:
            return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
        if not namespace or not slug:
            return format_error_response("PARAM_ERROR", "缺少知识库命名空间或文档标识")
        
        async with YuqueAPIClient(token) as client:
            result = await client.get_doc(namespace, slug, raw=raw)
            return format_success_response(result, "获取文档详情成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"获取文档详情失败: {str(e)}")


@tool(name="search", description="搜索文档或知识库")
async def search(ctx: Context, q: str, type: str = "doc", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """
    搜索文档或知识库
    
    Args:
        ctx: MCP上下文
        q: 搜索关键词
        type: 搜索类型（doc, repo）
        limit: 每页数量
        offset: 偏移量
        
    Returns:
        搜索结果响应
    """
    try:
        token = os.environ.get("YUQUE_TOKEN")
        if not token:
            return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
        if not q:
            return format_error_response("PARAM_ERROR", "缺少搜索关键词")
        
        async with YuqueAPIClient(token) as client:
            result = await client.search(q, type=type, limit=limit, offset=offset)
            return format_success_response(result, "搜索成功")
    except Exception as e:
        return format_error_response("API_ERROR", f"搜索失败: {str(e)}")
