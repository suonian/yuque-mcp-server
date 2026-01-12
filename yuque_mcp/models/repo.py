#!/usr/bin/env python3
"""
知识库相关模型定义
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class RepoInfo(BaseModel):
    """知识库信息模型"""
    id: int
    type: str
    namespace: str
    name: str
    slug: str
    description: Optional[str] = None
    user_id: int
    user_login: str
    user_name: str
    creator_id: int
    created_at: str
    updated_at: str
    public: int
    items_count: int
    likes_count: int
    watches_count: int


class RepoListResponse(BaseModel):
    """知识库列表响应模型"""
    data: List[RepoInfo]
    total: int
    limit: int
    offset: int


class RepoResponse(BaseModel):
    """知识库响应模型"""
    data: RepoInfo
    message: Optional[str] = None
