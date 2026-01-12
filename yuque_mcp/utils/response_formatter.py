#!/usr/bin/env python3
"""
响应格式化工具
统一MCP服务器的响应格式
"""

from typing import Dict, Any, Optional, List


def format_success_response(data: Any, message: str = "操作成功") -> Dict[str, Any]:
    """格式化成功响应
    
    Args:
        data: 响应数据
        message: 响应消息
        
    Returns:
        格式化后的响应字典
    """
    return {
        "result": {
            "success": True,
            "message": message,
            "data": data
        }
    }


def format_error_response(code: str, message: str, details: Optional[Any] = None) -> Dict[str, Any]:
    """格式化错误响应
    
    Args:
        code: 错误代码
        message: 错误消息
        details: 错误详情
        
    Returns:
        格式化后的响应字典
    """
    error_data = {
        "code": code,
        "message": message
    }
    if details:
        error_data["details"] = details
    
    return {
        "result": {
            "success": False,
            "error": error_data
        }
    }


def create_mcp_response(status: str, message: str, data: Optional[Any] = None) -> Dict[str, Any]:
    """创建MCP响应对象
    
    Args:
        status: 响应状态
        message: 响应消息
        data: 响应数据
        
    Returns:
        MCP响应字典
    """
    return {
        "status": status,
        "message": message,
        "data": data
    }
