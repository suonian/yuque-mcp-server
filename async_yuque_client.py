#!/usr/bin/env python3
"""
异步语雀API客户端
使用httpx库实现异步HTTP请求
"""

import httpx
from typing import Dict, Any, Optional, Union
from config import YUQUE_BASE_URL
from cache import cache_manager, generate_cache_key
import logging


logger = logging.getLogger(__name__)


class AsyncYuqueMCPClient:
    """异步语雀 API 客户端封装"""
    
    def __init__(self, token: str):
        """初始化客户端
        
        Args:
            token: 语雀 API Token
        """
        self.token: str = token
        self.base_url: str = YUQUE_BASE_URL
        self.client: httpx.AsyncClient = httpx.AsyncClient(
            headers={
                'X-Auth-Token': self.token,
                'Content-Type': 'application/json',
                'User-Agent': 'Yuque-MCP-Server/2.0'
            },
            timeout=30.0
        )
    
    async def __aenter__(self):
        """异步上下文管理器进入"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.client.aclose()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送异步请求到语雀 API，包含详细日志和缓存逻辑"""
        # 生成缓存键
        cache_key = generate_cache_key("yuque", method, endpoint, **kwargs)
        
        # 检查缓存
        cached_result = cache_manager.get(cache_key)
        if cached_result and method == "GET":
            return cached_result
        
        url: str = f"{self.base_url}{endpoint}"
        
        try:
            response: httpx.Response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            result: Dict[str, Any] = response.json()
            
            # 设置缓存，只缓存GET请求
            if method == "GET":
                # 根据不同的API设置不同的过期时间
                if endpoint == "/user":
                    # 用户信息：24小时过期
                    cache_manager.set(cache_key, result, expire=86400)
                elif "/repos/" in endpoint and "/docs" not in endpoint:
                    # 知识库详情：12小时过期
                    cache_manager.set(cache_key, result, expire=43200)
                elif "/docs" in endpoint and "/" not in endpoint.split("/docs")[1]:
                    # 文档列表：6小时过期
                    cache_manager.set(cache_key, result, expire=21600)
                elif "/docs/" in endpoint:
                    # 文档内容：3小时过期
                    cache_manager.set(cache_key, result, expire=10800)
                elif "/search" in endpoint:
                    # 搜索结果：1小时过期
                    cache_manager.set(cache_key, result, expire=3600)
                else:
                    # 其他GET请求：2小时过期
                    cache_manager.set(cache_key, result, expire=7200)
            
            return result
        except httpx.HTTPStatusError as e:
            raise
        except httpx.RequestError as e:
            raise
    
    async def get_user_info(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return await self._request('GET', '/user')
    
    async def list_repos(self) -> Dict[str, Any]:
        """列出用户的知识库"""
        user_info: Dict[str, Any] = await self.get_user_info()
        login: str = user_info["data"]["login"]
        return await self._request('GET', f'/users/{login}/repos')
    
    async def get_repo(self, namespace: str) -> Dict[str, Any]:
        """获取知识库详情"""
        return await self._request('GET', f'/repos/{namespace}')
    
    async def list_docs(self, namespace: str) -> Dict[str, Any]:
        """列出知识库中的文档"""
        return await self._request('GET', f'/repos/{namespace}/docs')
    
    async def get_doc(self, namespace: str, slug: str, raw: bool = False) -> Dict[str, Any]:
        """获取文档内容
        
        Args:
            namespace: 知识库命名空间
            slug: 文档标识
            raw: 是否获取原始 Markdown（完整内容），默认 False
        """
        endpoint: str = f'/repos/{namespace}/docs/{slug}'
        if raw:
            endpoint += '?raw=1'  # 支持 raw 参数
        return await self._request('GET', endpoint)
    
    async def create_doc(self, namespace: str, title: str, content: str, format_type: str = "markdown") -> Dict[str, Any]:
        """创建文档"""
        data: Dict[str, str] = {
            "title": title,
            "format": format_type,
            "body": content
        }
        return await self._request('POST', f'/repos/{namespace}/docs', json=data)
    
    async def update_doc(self, namespace: str, doc_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Dict[str, Any]:
        """更新文档"""
        data: Dict[str, str] = {}
        if title:
            data["title"] = title
        if content:
            data["body"] = content
        
        return await self._request('PUT', f'/repos/{namespace}/docs/{doc_id}', json=data)
    
    async def delete_doc(self, namespace: str, doc_id: int) -> Dict[str, Any]:
        """删除文档"""
        return await self._request('DELETE', f'/repos/{namespace}/docs/{doc_id}')
    
    async def search(self, query: str, type: str = "doc") -> Dict[str, Any]:
        """搜索文档或知识库"""
        return await self._request('GET', f'/search?q={query}&type={type}')
    
    async def get_doc_by_id(self, doc_id: int) -> Dict[str, Any]:
        """通过文档ID获取文档内容
        
        注意：语雀API不支持直接通过文档ID获取文档。
        此方法会尝试通过搜索找到文档的namespace和slug，然后获取完整内容。
        如果搜索失败，会返回错误提示，建议用户使用 get_doc(namespace, slug) 方式。
        
        Args:
            doc_id: 文档ID
            
        Returns:
            文档内容，如果找不到则返回错误信息
        """
        # 语雀API不支持直接通过文档ID获取文档
        # 需要通过搜索或其他方式找到文档的namespace和slug
        # 由于搜索API无法精确匹配文档ID，这里返回错误提示
        raise ValueError(
            f"语雀API不支持直接通过文档ID获取文档。\n"
            f"请使用以下方式之一：\n"
            f"1. 使用 get_doc(namespace, slug) 工具，从搜索结果中获取 namespace 和 slug\n"
            f"2. 使用 list_docs(namespace) 工具列出知识库中的文档，找到对应的 slug"
        )
    
    async def list_groups(self) -> Dict[str, Any]:
        """列出用户的团队"""
        user_info: Dict[str, Any] = await self.get_user_info()
        login: str = user_info["data"]["login"]
        return await self._request('GET', f'/users/{login}/groups')
    
    async def list_user_repos(self, login: str) -> Dict[str, Any]:
        """列出指定用户的知识库"""
        return await self._request('GET', f'/users/{login}/repos')
    
    async def list_group_repos(self, login: str) -> Dict[str, Any]:
        """列出指定团队的知识库"""
        return await self._request('GET', f'/groups/{login}/repos')
    
    async def create_repo(
        self,
        owner_login: str,
        name: str,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        public: int = 0,
        owner_type: str = "user"
    ) -> Dict[str, Any]:
        """创建知识库，可指定 owner_type=user/group"""
        data: Dict[str, Union[str, int]] = {
            "name": name,
            "public": public
        }
        if slug:
            data["slug"] = slug
        if description:
            data["description"] = description
        
        endpoint: str
        if owner_type == "group":
            endpoint = f'/groups/{owner_login}/repos'
        else:
            endpoint = f'/users/{owner_login}/repos'
        return await self._request('POST', endpoint, json=data)
    
    async def _build_repo_path(self, repo_id: Optional[int] = None, namespace: Optional[str] = None) -> str:
        """构建知识库路径"""
        if repo_id is not None:
            return f'/repos/{repo_id}'
        if namespace:
            if '/' not in namespace:
                raise ValueError("namespace 必须形如 owner/slug")
            owner, slug = namespace.split('/', 1)
            return f'/repos/{owner}/{slug}'
        raise ValueError("必须提供 repo_id 或 namespace")
    
    async def update_repo(
        self,
        repo_id: Optional[int] = None,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        slug: Optional[str] = None,
        description: Optional[str] = None,
        public: Optional[int] = None,
        toc: Optional[str] = None
    ) -> Dict[str, Any]:
        """更新知识库"""
        data: Dict[str, Union[str, int]] = {}
        if name:
            data["name"] = name
        if slug:
            data["slug"] = slug
        if description:
            data["description"] = description
        if public is not None:
            data["public"] = public
        if toc is not None:
            data["toc"] = toc
        path: str = await self._build_repo_path(repo_id, namespace)
        return await self._request('PUT', path, json=data)
    
    async def delete_repo(self, repo_id: Optional[int] = None, namespace: Optional[str] = None) -> Dict[str, Any]:
        """删除知识库"""
        path: str = await self._build_repo_path(repo_id, namespace)
        return await self._request('DELETE', path)
    
    async def get_user(self, login: str) -> Dict[str, Any]:
        """获取指定用户信息"""
        return await self._request('GET', f'/users/{login}')
    
    async def get_group(self, group_id: int) -> Dict[str, Any]:
        """获取团队信息"""
        return await self._request('GET', f'/groups/{group_id}')
    
    async def list_group_users(self, group_id: int) -> Dict[str, Any]:
        """列出团队成员"""
        return await self._request('GET', f'/groups/{group_id}/users')
    
    async def update_group_member(self, group_login: str, user_identity: str, role: int) -> Dict[str, Any]:
        """变更团队成员角色"""
        return await self._request(
            'PUT',
            f'/groups/{group_login}/users/{user_identity}',
            json={"role": role}
        )
    
    async def remove_group_member(self, group_login: str, user_identity: str) -> Dict[str, Any]:
        """删除团队成员"""
        return await self._request('DELETE', f'/groups/{group_login}/users/{user_identity}')
    
    async def get_group_statistics(self, login: str) -> Dict[str, Any]:
        """团队汇总统计"""
        return await self._request('GET', f'/groups/{login}/statistics')
    
    async def get_group_member_statistics(self, login: str, **params) -> Dict[str, Any]:
        """团队成员统计"""
        return await self._request('GET', f'/groups/{login}/statistics/members', params=params)
    
    async def get_group_book_statistics(self, login: str, **params) -> Dict[str, Any]:
        """团队知识库统计"""
        return await self._request('GET', f'/groups/{login}/statistics/books', params=params)
    
    async def get_group_doc_statistics(self, login: str, **params) -> Dict[str, Any]:
        """团队文档统计"""
        return await self._request('GET', f'/groups/{login}/statistics/docs', params=params)
    
    async def get_repo_toc(self, repo_id: Optional[int] = None, namespace: Optional[str] = None) -> Dict[str, Any]:
        """获取知识库目录"""
        path: str = await self._build_repo_path(repo_id, namespace)
        return await self._request('GET', f'{path}/toc')
    
    async def update_repo_toc(self, repo_id: Optional[int] = None, namespace: Optional[str] = None, toc_markdown: str = "") -> Dict[str, Any]:
        """更新知识库目录（整体替换）"""
        path: str = await self._build_repo_path(repo_id, namespace)
        return await self._request('PUT', path, json={"toc": toc_markdown})
    
    async def list_doc_versions(self, doc_id: int) -> Dict[str, Any]:
        """列出文档版本（最新100条）"""
        return await self._request('GET', '/doc_versions', params={"doc_id": doc_id})
    
    async def get_doc_version(self, version_id: int) -> Dict[str, Any]:
        """获取指定文档版本详情"""
        return await self._request('GET', f'/doc_versions/{version_id}')
