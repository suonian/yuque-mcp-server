#!/usr/bin/env python3
"""
用户相关模型定义
"""

from pydantic import BaseModel, Field
from typing import Optional


class UserInfo(BaseModel):
    """用户信息模型"""
    id: int
    login: str
    name: str
    avatar_url: str
    bio: Optional[str] = None
    email: Optional[str] = None
    created_at: str
    updated_at: str


class UserResponse(BaseModel):
    """用户响应模型"""
    data: UserInfo
    message: Optional[str] = None
