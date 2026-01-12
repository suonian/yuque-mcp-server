#!/usr/bin/env python3
"""
文档相关模型定义
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class DocInfo(BaseModel):
    """文档信息模型"""
    id: int
    slug: str
    title: str
    description: Optional[str] = None
    book_id: int
    book_title: str
    user_id: int
    user_login: str
    user_name: str
    format: str
    body: Optional[str] = None
    body_draft: Optional[str] = None
    body_html: Optional[str] = None
    body_lake: Optional[str] = None
    public: int
    status: int
    created_at: str
    updated_at: str
    published_at: str
    word_count: int
    likes_count: int
    comment_count: int
    content_updated_at: str


class DocListResponse(BaseModel):
    """文档列表响应模型"""
    data: List[DocInfo]
    total: int
    limit: int
    offset: int


class DocResponse(BaseModel):
    """文档响应模型"""
    data: DocInfo
    message: Optional[str] = None
