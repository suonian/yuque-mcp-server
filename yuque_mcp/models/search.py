#!/usr/bin/env python3
"""
搜索相关模型定义
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class SearchHit(BaseModel):
    """搜索结果模型"""
    id: int
    type: str
    title: str
    slug: str
    namespace: Optional[str] = None
    book_id: Optional[int] = None
    book_title: Optional[str] = None
    description: Optional[str] = None
    highlight: Optional[str] = None
    user_login: Optional[str] = None
    user_name: Optional[str] = None
    created_at: str
    updated_at: str
    public: Optional[int] = None


class SearchResponse(BaseModel):
    """搜索响应模型"""
    data: List[SearchHit]
    total: int
    limit: int
    offset: int
    q: str
    type: str
