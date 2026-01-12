#!/usr/bin/env python3
"""
语雀 API 客户端
统一的语雀 API 调用封装，支持异步请求和连接池优化
"""

import httpx
from typing import Dict, Any, Optional
import logging
from cachetools import TTLCache

# 配置API客户端日志 - 禁用所有输出到stdout
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)  # 只记录严重错误，避免输出到stdout

class YuqueAPIClient:
    """语雀 API 客户端"""
    
    BASE_URL = "https://www.yuque.com/api/v2"
    
    def __init__(self, token: str, timeout: int = 30):
        """初始化 API 客户端
        
        Args:
            token: 语雀 API Token
            timeout: 请求超时时间（秒）
        """
        self.token = token
        self.timeout = timeout
        self.cache = TTLCache(maxsize=100, ttl=300)  # 5分钟过期
        
        # 初始化 HTTP 客户端，使用连接池
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.timeout),
            headers={
                "X-Auth-Token": self.token,
                "Content-Type": "application/json"
            },
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=50,
                keepalive_expiry=300
            )
        )
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        await self.close()
    
    async def close(self):
        """关闭 HTTP 客户端"""
        await self.client.aclose()
    
    async def _make_request(self, endpoint: str, method: str = "GET", **kwargs) -> Dict[str, Any]:
        """发送 HTTP 请求
        
        Args:
            endpoint: API 端点
            method: HTTP 方法
            **kwargs: 其他参数
        
        Returns:
            API 响应数据
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP错误: {e.response.status_code} - {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"请求错误: {e}")
            raise
        except Exception as e:
            logger.error(f"未知错误: {e}")
            raise
    
    async def get_user_info(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        cache_key = "user_info"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = await self._make_request("user")
        self.cache[cache_key] = result
        return result
    
    async def list_repos(self, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """列出当前用户的知识库
        
        Args:
            limit: 每页数量
            offset: 偏移量
        """
        cache_key = f"repos_{limit}_{offset}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 首先获取当前用户信息
        user_info = await self.get_user_info()
        login = user_info.get("data", {}).get("login", "")
        
        if not login:
            raise ValueError("无法获取当前用户登录名")
        
        params = {"limit": limit, "offset": offset}
        result = await self._make_request(f"users/{login}/repos", params=params)
        self.cache[cache_key] = result
        return result
    
    async def get_repo(self, namespace: str) -> Dict[str, Any]:
        """获取知识库详情
        
        Args:
            namespace: 知识库命名空间
        """
        cache_key = f"repo_{namespace}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = await self._make_request(f"repos/{namespace}")
        self.cache[cache_key] = result
        return result
    
    async def list_docs(self, namespace: str, limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """列出知识库中的文档
        
        Args:
            namespace: 知识库命名空间
            limit: 每页数量
            offset: 偏移量
        """
        cache_key = f"docs_{namespace}_{limit}_{offset}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {"limit": limit, "offset": offset}
        result = await self._make_request(f"repos/{namespace}/docs", params=params)
        self.cache[cache_key] = result
        return result
    
    async def get_doc(self, namespace: str, slug: str, raw: bool = False) -> Dict[str, Any]:
        """获取文档详情
        
        Args:
            namespace: 知识库命名空间
            slug: 文档标识
            raw: 是否获取原始 Markdown
        """
        cache_key = f"doc_{namespace}_{slug}_{raw}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        params = {}
        if raw:
            params["raw"] = "1"
        
        result = await self._make_request(f"repos/{namespace}/docs/{slug}", params=params)
        self.cache[cache_key] = result
        return result
    
    async def search(self, q: str, type: str = "doc", limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """搜索文档或知识库

        Args:
            q: 搜索关键词
            type: 搜索类型（doc, repo）
            limit: 每页数量
            offset: 偏移量
        """
        cache_key = f"search_{q}_{type}_{limit}_{offset}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 语雀搜索 API 要求 offset 必须大于等于 1
        if offset < 1:
            offset = 1

        params = {
            "q": q,
            "type": type,
            "limit": limit,
            "offset": offset
        }

        result = await self._make_request("search", params=params)
        self.cache[cache_key] = result
        return result

    async def create_doc(self, namespace: str, title: str, body: str, slug: Optional[str] = None,
                        format: str = "markdown", public: int = 0) -> Dict[str, Any]:
        """创建文档

        Args:
            namespace: 知识库命名空间
            title: 文档标题
            body: 文档内容
            slug: 文档路径标识（可选）
            format: 文档格式（markdown/lake）
            public: 是否公开（0-私密 1-公开）
        """
        data = {
            "title": title,
            "body": body,
            "format": format,
            "public": public
        }

        if slug:
            data["slug"] = slug

        result = await self._make_request(
            f"repos/{namespace}/docs",
            method="POST",
            json=data
        )

        # 清除缓存
        self._clear_cache(f"docs_{namespace}_")

        return result

    async def update_doc(self, namespace: str, doc_id: int, title: Optional[str] = None,
                        body: Optional[str] = None, slug: Optional[str] = None) -> Dict[str, Any]:
        """更新文档

        Args:
            namespace: 知识库命名空间
            doc_id: 文档ID
            title: 文档标题（可选）
            body: 文档内容（可选）
            slug: 文档路径标识（可选）
        """
        data = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if slug is not None:
            data["slug"] = slug

        if not data:
            raise ValueError("至少提供一个需要更新的字段（title, body, slug）")

        result = await self._make_request(
            f"repos/{namespace}/docs/{doc_id}",
            method="PUT",
            json=data
        )

        # 清除缓存
        self._clear_cache(f"docs_{namespace}_")

        return result

    async def delete_doc(self, namespace: str, doc_id: int) -> Dict[str, Any]:
        """删除文档

        Args:
            namespace: 知识库命名空间
            doc_id: 文档ID
        """
        result = await self._make_request(
            f"repos/{namespace}/docs/{doc_id}",
            method="DELETE"
        )

        # 清除缓存
        self._clear_cache(f"docs_{namespace}_")

        return result

    async def get_doc_by_slug(self, namespace: str, slug: str) -> Optional[Dict[str, Any]]:
        """通过 slug 获取文档（用于更新时查找 doc_id）

        Args:
            namespace: 知识库命名空间
            slug: 文档路径标识

        Returns:
            文档信息或 None
        """
        try:
            # 获取文档列表
            docs_result = await self.list_docs(namespace, limit=100)
            if not docs_result or "data" not in docs_result:
                return None

            # 查找匹配的文档
            for doc in docs_result["data"]:
                if doc.get("slug") == slug:
                    return doc

            return None
        except Exception as e:
            logger.error(f"通过 slug 获取文档失败: {e}")
            return None

    def _clear_cache(self, prefix: str):
        """清除指定前缀的缓存

        Args:
            prefix: 缓存键前缀
        """
        keys_to_remove = [key for key in self.cache.keys() if key.startswith(prefix)]
        for key in keys_to_remove:
            self.cache.pop(key, None)
