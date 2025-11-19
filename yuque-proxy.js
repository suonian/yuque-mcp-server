from flask import Flask, request, jsonify, Response
import requests
import os
import logging
import json
import time
from typing import Dict, Any

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 语雀 API 配置
YUQUE_BASE_URL = "https://www.yuque.com/api/v2"

# MCP 协议配置
MCP_PROTOCOL_VERSION = "2024-11-05"
DEFAULT_CORS_ORIGIN = "*"

def get_yuque_token():
    """
    获取语雀 Token，优先级：
    1. HTTP Header: X-Yuque-Token
    2. 环境变量: YUQUE_TOKEN
    如果都没有，抛出异常
    """
    # 优先从 HTTP Header 读取
    token = request.headers.get('X-Yuque-Token')
    
    # 如果没有 Header，从环境变量读取
    if not token:
        token = os.getenv('YUQUE_TOKEN')
    
    # 如果都没有，返回错误
    if not token:
        raise ValueError(
            "缺少语雀 Token 配置。请通过以下方式之一提供：\n"
            "1. HTTP Header: X-Yuque-Token\n"
            "2. 环境变量: YUQUE_TOKEN"
        )
    
    return token

class YuqueMCPClient:
    """语雀 API 客户端封装"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = YUQUE_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'X-Auth-Token': self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Yuque-MCP-Server/2.0'
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """发送请求到语雀 API"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"语雀 API 请求失败: {e}")
            raise
    
    def get_user_info(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self._request('GET', '/user')
    
    def list_repos(self) -> Dict[str, Any]:
        """列出用户的知识库"""
        user_info = self.get_user_info()
        login = user_info["data"]["login"]
        return self._request('GET', f'/users/{login}/repos')
    
    def get_repo(self, namespace: str) -> Dict[str, Any]:
        """获取知识库详情"""
        return self._request('GET', f'/repos/{namespace}')
    
    def list_docs(self, namespace: str) -> Dict[str, Any]:
        """列出知识库中的文档"""
        return self._request('GET', f'/repos/{namespace}/docs')
    
    def get_doc(self, namespace: str, slug: str) -> Dict[str, Any]:
        """获取文档内容"""
        return self._request('GET', f'/repos/{namespace}/docs/{slug}')
    
    def create_doc(self, namespace: str, title: str, content: str, format: str = "markdown") -> Dict[str, Any]:
        """创建文档"""
        data = {
            "title": title,
            "format": format,
            "body": content
        }
        return self._request('POST', f'/repos/{namespace}/docs', json=data)
    
    def update_doc(self, namespace: str, doc_id: int, title: str = None, content: str = None) -> Dict[str, Any]:
        """更新文档"""
        data = {}
        if title:
            data["title"] = title
        if content:
            data["body"] = content
        
        return self._request('PUT', f'/repos/{namespace}/docs/{doc_id}', json=data)
    
    def delete_doc(self, namespace: str, doc_id: int) -> Dict[str, Any]:
        """删除文档"""
        return self._request('DELETE', f'/repos/{namespace}/docs/{doc_id}')
    
    def search(self, query: str, type: str = "doc") -> Dict[str, Any]:
        """搜索文档或知识库"""
        return self._request('GET', f'/search?q={query}&type={type}')
    
    def list_groups(self) -> Dict[str, Any]:
        """列出用户的团队"""
        user_info = self.get_user_info()
        login = user_info["data"]["login"]
        return self._request('GET', f'/users/{login}/groups')
    
    def list_user_repos(self, login: str) -> Dict[str, Any]:
        """列出指定用户的知识库"""
        return self._request('GET', f'/users/{login}/repos')
    
    def list_group_repos(self, login: str) -> Dict[str, Any]:
        """列出指定团队的知识库"""
        return self._request('GET', f'/groups/{login}/repos')
    
    def create_repo(
        self,
        owner_login: str,
        name: str,
        slug: str = None,
        description: str = None,
        public: int = 0,
        owner_type: str = "user"
    ) -> Dict[str, Any]:
        """创建知识库，可指定 owner_type=user/group"""
        data = {
            "name": name,
            "public": public
        }
        if slug:
            data["slug"] = slug
        if description:
            data["description"] = description
        
        if owner_type == "group":
            endpoint = f'/groups/{owner_login}/repos'
        else:
            endpoint = f'/users/{owner_login}/repos'
        return self._request('POST', endpoint, json=data)
    
    def _build_repo_path(self, repo_id: int = None, namespace: str = None) -> str:
        if repo_id is not None:
            return f'/repos/{repo_id}'
        if namespace:
            if '/' not in namespace:
                raise ValueError("namespace 必须形如 owner/slug")
            owner, slug = namespace.split('/', 1)
            return f'/repos/{owner}/{slug}'
        raise ValueError("必须提供 repo_id 或 namespace")
    
    def update_repo(
        self,
        repo_id: int = None,
        namespace: str = None,
        name: str = None,
        slug: str = None,
        description: str = None,
        public: int = None,
        toc: str = None
    ) -> Dict[str, Any]:
        """更新知识库"""
        data = {}
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
        path = self._build_repo_path(repo_id, namespace)
        return self._request('PUT', path, json=data)
    
    def delete_repo(self, repo_id: int = None, namespace: str = None) -> Dict[str, Any]:
        """删除知识库"""
        path = self._build_repo_path(repo_id, namespace)
        return self._request('DELETE', path)
    
    def get_user(self, login: str) -> Dict[str, Any]:
        """获取指定用户信息"""
        return self._request('GET', f'/users/{login}')
    
    def get_group(self, group_id: int) -> Dict[str, Any]:
        """获取团队信息"""
        return self._request('GET', f'/groups/{group_id}')
    
    def list_group_users(self, group_id: int) -> Dict[str, Any]:
        """列出团队成员"""
        return self._request('GET', f'/groups/{group_id}/users')
    
    def update_group_member(self, group_login: str, user_identity: str, role: int) -> Dict[str, Any]:
        """变更团队成员角色"""
        return self._request(
            'PUT',
            f'/groups/{group_login}/users/{user_identity}',
            json={"role": role}
        )
    
    def remove_group_member(self, group_login: str, user_identity: str) -> Dict[str, Any]:
        """删除团队成员"""
        return self._request('DELETE', f'/groups/{group_login}/users/{user_identity}')
    
    def get_group_statistics(self, login: str) -> Dict[str, Any]:
        """团队汇总统计"""
        return self._request('GET', f'/groups/{login}/statistics')
    
    def get_group_member_statistics(self, login: str, **params) -> Dict[str, Any]:
        """团队成员统计"""
        return self._request('GET', f'/groups/{login}/statistics/members', params=params)
    
    def get_group_book_statistics(self, login: str, **params) -> Dict[str, Any]:
        """团队知识库统计"""
        return self._request('GET', f'/groups/{login}/statistics/books', params=params)
    
    def get_group_doc_statistics(self, login: str, **params) -> Dict[str, Any]:
        """团队文档统计"""
        return self._request('GET', f'/groups/{login}/statistics/docs', params=params)
    
    def get_repo_toc(self, repo_id: int = None, namespace: str = None) -> Dict[str, Any]:
        """获取知识库目录"""
        path = self._build_repo_path(repo_id, namespace)
        return self._request('GET', f'{path}/toc')
    
    def update_repo_toc(self, repo_id: int = None, namespace: str = None, toc_markdown: str = "") -> Dict[str, Any]:
        """更新知识库目录（整体替换）"""
        path = self._build_repo_path(repo_id, namespace)
        return self._request('PUT', path, json={"toc": toc_markdown})
    
    def list_doc_versions(self, doc_id: int) -> Dict[str, Any]:
        """列出文档版本（最新100条）"""
        return self._request('GET', '/doc_versions', params={"doc_id": doc_id})
    
    def get_doc_version(self, version_id: int) -> Dict[str, Any]:
        """获取指定文档版本详情"""
        return self._request('GET', f'/doc_versions/{version_id}')


@app.after_request
def add_cors_headers(response):
    """为所有响应附加 CORS 头，便于 Chatbox 直接访问"""
    response.headers['Access-Control-Allow-Origin'] = DEFAULT_CORS_ORIGIN
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,X-Yuque-Token'
    response.headers['Access-Control-Max-Age'] = '86400'
    return response


@app.route('/mcp', methods=['GET', 'POST', 'OPTIONS'])
def handle_mcp():
    """处理 MCP 协议请求"""
    
    if request.method == 'OPTIONS':
        return '', 200
    
    elif request.method == 'POST':
        data = request.get_json(silent=True) or {}
        try:
            logger.info(
                "收到 MCP 请求: method=%s id=%s path=%s",
                data.get("method", "unknown"),
                data.get("id"),
                request.path
            )
            
            if data.get("jsonrpc") != "2.0":
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "error": {"code": -32600, "message": "Invalid Request"}
                }), 400
            
            method = data.get("method")
            request_id = data.get("id")
            
            if method != "notifications/initialized" and request_id is None:
                logger.warning("JSON-RPC 请求缺少 id 字段")
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32600, "message": "Missing id in request"}
                }), 400
            
            if method == "initialize":
                return handle_initialize(data)
            elif method == "tools/list":
                return handle_tools_list(data)
            elif method == "tools/call":
                return handle_tools_call(data)
            elif method == "ping":
                return handle_ping(data)
            elif method == "notifications/initialized":
                logger.info("收到 notifications/initialized 通知，已完成握手。")
                return '', 204
            else:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": data.get("id"),
                    "error": {"code": -32601, "message": f"Method not found: {method}"}
                }), 200
                
        except Exception as e:
            logger.error(f"处理请求时出错: {e}", exc_info=True)
            return jsonify({
                "jsonrpc": "2.0",
                "id": data.get("id") if 'data' in locals() else None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }), 500
    
    elif request.method == 'GET':
        # SSE 连接保持
        def generate_heartbeat():
            while True:
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': time.time()})}\n\n"
                time.sleep(30)
        
        headers = {
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
        return Response(
            generate_heartbeat(),
            content_type='text/event-stream',
            headers=headers
        )

def handle_initialize(data):
    """处理初始化请求"""
    response = {
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {
                "tools": {},
                "logs": {},
                "progress": {},
                "readers": {}
            },
            "serverInfo": {
                "name": "yuque-mcp-server",
                "version": "2.0.0"
            }
        }
    }
    return jsonify(response)

def handle_tools_list(data):
    """返回可用的工具列表"""
    tools = [
        {
            "name": "get_user_info",
            "description": "获取当前语雀用户信息",
            "inputSchema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_user",
            "description": "根据登录名获取用户信息",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "login": {"type": "string", "description": "语雀登录名"}
                },
                "required": ["login"]
            }
        },
        {
            "name": "list_repos",
            "description": "列出当前用户的所有知识库",
            "inputSchema": {"type": "object", "properties": {}}
        },
        {
            "name": "list_user_repos",
            "description": "列出指定用户的知识库",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "login": {"type": "string", "description": "语雀登录名"}
                },
                "required": ["login"]
            }
        },
        {
            "name": "list_group_repos",
            "description": "列出指定团队的知识库",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "login": {"type": "string", "description": "团队登录名"}
                },
                "required": ["login"]
            }
        },
        {
            "name": "get_repo",
            "description": "获取知识库详细信息",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间"}
                },
                "required": ["namespace"]
            }
        },
        {
            "name": "create_repo",
            "description": "创建知识库",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "owner_login": {"type": "string", "description": "所属用户或团队登录名（推荐）"},
                    "login": {"type": "string", "description": "兼容旧版字段，与 owner_login 等价"},
                    "owner_type": {"type": "string", "description": "owner 类型 user 或 group", "enum": ["user", "group"]},
                    "name": {"type": "string", "description": "知识库名称"},
                    "slug": {"type": "string", "description": "知识库路径（可选）"},
                    "description": {"type": "string", "description": "知识库描述"},
                    "public": {
                        "type": "integer",
                        "description": "公开范围：0私密，1团队内，2公开",
                        "enum": [0, 1, 2]
                    }
                },
                "required": ["name"]
            }
        },
        {
            "name": "update_repo",
            "description": "更新知识库信息",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo_id": {"type": "integer", "description": "知识库ID（与 namespace 二选一）"},
                    "namespace": {"type": "string", "description": "知识库命名空间，如 team/book"},
                    "name": {"type": "string", "description": "新的名称"},
                    "slug": {"type": "string", "description": "新的路径"},
                    "description": {"type": "string", "description": "新的描述"},
                    "public": {
                        "type": "integer",
                        "description": "公开范围：0私密，1团队内，2公开",
                        "enum": [0, 1, 2]
                    },
                    "toc": {"type": "string", "description": "Markdown 目录文本"}
                },
                "required": []
            }
        },
        {
            "name": "delete_repo",
            "description": "删除知识库（谨慎操作）",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo_id": {"type": "integer", "description": "知识库ID（与 namespace 二选一）"},
                    "namespace": {"type": "string", "description": "知识库命名空间，如 team/book"}
                },
                "required": []
            }
        },
        {
            "name": "list_docs",
            "description": "列出知识库中的文档",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间"}
                },
                "required": ["namespace"]
            }
        },
        {
            "name": "get_doc",
            "description": "获取文档详细内容",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间"},
                    "slug": {"type": "string", "description": "文档标识"}
                },
                "required": ["namespace", "slug"]
            }
        },
        {
            "name": "list_doc_versions",
            "description": "查看文档版本历史",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "doc_id": {"type": "integer", "description": "文档ID"}
                },
                "required": ["doc_id"]
            }
        },
        {
            "name": "get_doc_version",
            "description": "获取指定版本详情",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "version_id": {"type": "integer", "description": "版本ID"}
                },
                "required": ["version_id"]
            }
        },
        {
            "name": "create_doc",
            "description": "创建新文档",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间"},
                    "title": {"type": "string", "description": "文档标题"},
                    "content": {"type": "string", "description": "文档内容"},
                    "format": {"type": "string", "description": "文档格式", "enum": ["markdown", "lake"]}
                },
                "required": ["namespace", "title", "content"]
            }
        },
        {
            "name": "update_doc",
            "description": "更新现有文档内容",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间"},
                    "doc_id": {"type": "integer", "description": "文档ID"},
                    "title": {"type": "string", "description": "新标题（可选）"},
                    "content": {"type": "string", "description": "新内容"},
                    "format": {"type": "string", "description": "文档格式", "enum": ["markdown", "lake"]}
                },
                "required": ["namespace", "doc_id"]
            }
        },
        {
            "name": "delete_doc",
            "description": "删除文档",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间"},
                    "doc_id": {"type": "integer", "description": "文档ID"}
                },
                "required": ["namespace", "doc_id"]
            }
        },
        {
            "name": "search_docs",
            "description": "搜索文档或知识库",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"},
                    "type": {"type": "string", "description": "搜索类型", "enum": ["doc", "repo"]}
                },
                "required": ["query"]
            }
        },
        {
            "name": "list_groups",
            "description": "列出用户的团队",
            "inputSchema": {"type": "object", "properties": {}}
        },
        {
            "name": "get_group",
            "description": "获取指定团队信息",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "团队ID"}
                },
                "required": ["group_id"]
            }
        },
        {
            "name": "list_group_users",
            "description": "列出团队成员列表",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_id": {"type": "integer", "description": "团队ID"}
                },
                "required": ["group_id"]
            }
        },
        {
            "name": "update_group_member",
            "description": "更新团队成员角色",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_login": {"type": "string", "description": "团队登录名或ID"},
                    "user_identity": {"type": "string", "description": "成员登录名或ID"},
                    "role": {
                        "type": "integer",
                        "description": "角色：0管理员 1成员 2只读",
                        "enum": [0, 1, 2]
                    }
                },
                "required": ["group_login", "user_identity", "role"]
            }
        },
        {
            "name": "remove_group_member",
            "description": "从团队移除成员",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_login": {"type": "string", "description": "团队登录名或ID"},
                    "user_identity": {"type": "string", "description": "成员登录名或ID"}
                },
                "required": ["group_login", "user_identity"]
            }
        },
        {
            "name": "get_group_statistics",
            "description": "获取团队汇总统计数据",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_login": {"type": "string", "description": "团队登录名或ID"}
                },
                "required": ["group_login"]
            }
        },
        {
            "name": "get_group_member_stats",
            "description": "获取团队成员统计数据",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_login": {"type": "string", "description": "团队登录名或ID"},
                    "name": {"type": "string", "description": "成员名（可选）"},
                    "range": {"type": "integer", "enum": [0, 30, 365], "description": "时间范围"},
                    "page": {"type": "integer", "description": "页码"},
                    "limit": {"type": "integer", "description": "分页数量"},
                    "sortField": {
                        "type": "string",
                        "description": "排序字段",
                        "enum": ["write_doc_count", "write_count", "read_count", "like_count"]
                    },
                    "sortOrder": {"type": "string", "enum": ["asc", "desc"], "description": "排序方向"}
                },
                "required": ["group_login"]
            }
        },
        {
            "name": "get_group_book_stats",
            "description": "获取团队知识库统计数据",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_login": {"type": "string", "description": "团队登录名或ID"},
                    "name": {"type": "string", "description": "知识库名（可选）"},
                    "range": {"type": "integer", "enum": [0, 30, 365], "description": "时间范围"},
                    "page": {"type": "integer", "description": "页码"},
                    "limit": {"type": "integer", "description": "分页数量"}
                },
                "required": ["group_login"]
            }
        },
        {
            "name": "get_group_doc_stats",
            "description": "获取团队文档统计数据",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "group_login": {"type": "string", "description": "团队登录名或ID"},
                    "title": {"type": "string", "description": "文档名（可选）"},
                    "range": {"type": "integer", "enum": [0, 30, 365], "description": "时间范围"},
                    "page": {"type": "integer", "description": "页码"},
                    "limit": {"type": "integer", "description": "分页数量"}
                },
                "required": ["group_login"]
            }
        },
        {
            "name": "get_repo_toc",
            "description": "查看知识库目录",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo_id": {"type": "integer", "description": "知识库ID"}
                },
                "required": ["repo_id"]
            }
        },
        {
            "name": "update_repo_toc",
            "description": "更新知识库目录（Markdown 格式）",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "repo_id": {"type": "integer", "description": "知识库ID"},
                    "toc": {"type": "string", "description": "Markdown 目录文本"}
                },
                "required": ["repo_id", "toc"]
            }
        }
    ]
    
    return jsonify({
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {"tools": tools}
    })

def handle_tools_call(data):
    """处理工具调用请求"""
    params = data.get("params", {})
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    request_id = data.get("id")
    
    logger.info(f"调用工具: {tool_name}, 参数: {arguments}")
    
    # 获取 Token 并创建客户端
    try:
        token = get_yuque_token()
        yuque_client = YuqueMCPClient(token)
    except ValueError as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32602,
                "message": str(e)
            }
        }), 400
    
    try:
        if tool_name == "get_user_info":
            result = yuque_client.get_user_info()
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_user_info(result)}]
                }
            })
        
        elif tool_name == "get_user":
            login = arguments["login"]
            result = yuque_client.get_user(login)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_user_info(result)}]
                }
            })
        
        elif tool_name == "list_repos":
            result = yuque_client.list_repos()
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repos_list(result)}]
                }
            })
        
        elif tool_name == "list_user_repos":
            login = arguments["login"]
            result = yuque_client.list_user_repos(login)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repos_list(result)}]
                }
            })
        
        elif tool_name == "list_group_repos":
            login = arguments["login"]
            result = yuque_client.list_group_repos(login)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repos_list(result)}]
                }
            })
        
        elif tool_name == "get_repo":
            namespace = arguments["namespace"]
            result = yuque_client.get_repo(namespace)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repo_info(result)}]
                }
            })
        
        elif tool_name == "create_repo":
            owner_login = arguments.get("owner_login") or arguments.get("login")
            if not owner_login:
                raise ValueError("创建知识库需要提供 owner_login（或 login）字段")
            owner_type = arguments.get("owner_type", "user")
            name = arguments["name"]
            slug = arguments.get("slug")
            description = arguments.get("description")
            public = arguments.get("public", 0)
            result = yuque_client.create_repo(
                owner_login,
                name,
                slug,
                description,
                public,
                owner_type=owner_type
            )
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repo_created(result, owner_login)}]
                }
            })
        
        elif tool_name == "update_repo":
            repo_id = arguments.get("repo_id")
            namespace = arguments.get("namespace")
            if repo_id is None and not namespace:
                raise ValueError("需要提供 repo_id 或 namespace")
            result = yuque_client.update_repo(
                repo_id=repo_id,
                namespace=namespace,
                name=arguments.get("name"),
                slug=arguments.get("slug"),
                description=arguments.get("description"),
                public=arguments.get("public"),
                toc=arguments.get("toc")
            )
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repo_info(result)}]
                }
            })
        
        elif tool_name == "delete_repo":
            repo_id = arguments.get("repo_id")
            namespace = arguments.get("namespace")
            if repo_id is None and not namespace:
                raise ValueError("需要提供 repo_id 或 namespace")
            yuque_client.delete_repo(repo_id=repo_id, namespace=namespace)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": "知识库已删除"}]
                }
            })
        
        elif tool_name == "list_docs":
            namespace = arguments["namespace"]
            result = yuque_client.list_docs(namespace)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_docs_list(result, namespace)}]
                }
            })
        
        elif tool_name == "get_doc":
            namespace = arguments["namespace"]
            slug = arguments["slug"]
            result = yuque_client.get_doc(namespace, slug)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_doc_content(result)}]
                }
            })
        
        elif tool_name == "list_doc_versions":
            doc_id = arguments["doc_id"]
            result = yuque_client.list_doc_versions(doc_id)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_doc_versions(result, doc_id)}]
                }
            })
        
        elif tool_name == "get_doc_version":
            version_id = arguments["version_id"]
            result = yuque_client.get_doc_version(version_id)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_doc_version_detail(result)}]
                }
            })
        
        
        elif tool_name == "create_doc":
            namespace = arguments["namespace"]
            title = arguments["title"]
            content = arguments["content"]
            format_type = arguments.get("format", "markdown")
            result = yuque_client.create_doc(namespace, title, content, format_type)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_created_doc(result, namespace)}]
                }
            })
        
        elif tool_name == "update_doc":
            namespace = arguments["namespace"]
            doc_id = arguments["doc_id"]
            title = arguments.get("title")
            content = arguments.get("content")
            if not title and not content:
                raise ValueError("更新文档时至少提供 title 或 content 之一")
            result = yuque_client.update_doc(namespace, doc_id, title, content)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": f"文档更新成功！文档ID: {doc_id}"}]
                }
            })
        
        elif tool_name == "delete_doc":
            namespace = arguments["namespace"]
            doc_id = arguments["doc_id"]
            result = yuque_client.delete_doc(namespace, doc_id)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": f"文档删除成功！文档ID: {doc_id}"}]
                }
            })
        
        elif tool_name == "search_docs":
            query = arguments["query"]
            search_type = arguments.get("type", "doc")
            result = yuque_client.search(query, search_type)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_search_results(result, query)}]
                }
            })
        
        elif tool_name == "list_groups":
            result = yuque_client.list_groups()
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_groups_list(result)}]
                }
            })
        
        elif tool_name == "get_group":
            group_id = arguments["group_id"]
            result = yuque_client.get_group(group_id)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_group_info(result)}]
                }
            })
        
        elif tool_name == "list_group_users":
            group_id = arguments["group_id"]
            result = yuque_client.list_group_users(group_id)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_group_users(result, group_id)}]
                }
            })
        
        elif tool_name == "update_group_member":
            group_login = arguments["group_login"]
            user_identity = arguments["user_identity"]
            role = arguments["role"]
            yuque_client.update_group_member(group_login, user_identity, role)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": f"已更新 {user_identity} 在 {group_login} 的角色为 {role}"}]
                }
            })
        
        elif tool_name == "remove_group_member":
            group_login = arguments["group_login"]
            user_identity = arguments["user_identity"]
            yuque_client.remove_group_member(group_login, user_identity)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": f"已将 {user_identity} 从团队 {group_login} 移除"}]
                }
            })
        
        elif tool_name == "get_group_statistics":
            group_login = arguments["group_login"]
            result = yuque_client.get_group_statistics(group_login)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_group_statistics(result)}]
                }
            })
        
        elif tool_name == "get_group_member_stats":
            group_login = arguments["group_login"]
            params = {k: v for k, v in arguments.items() if k not in {"group_login"} and v is not None}
            result = yuque_client.get_group_member_statistics(group_login, **params)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_group_member_stats(result)}]
                }
            })
        
        elif tool_name == "get_group_book_stats":
            group_login = arguments["group_login"]
            params = {k: v for k, v in arguments.items() if k not in {"group_login"} and v is not None}
            result = yuque_client.get_group_book_statistics(group_login, **params)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_group_book_stats(result)}]
                }
            })
        
        elif tool_name == "get_group_doc_stats":
            group_login = arguments["group_login"]
            params = {k: v for k, v in arguments.items() if k not in {"group_login"} and v is not None}
            result = yuque_client.get_group_doc_statistics(group_login, **params)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_group_doc_stats(result)}]
                }
            })
        
        elif tool_name == "get_repo_toc":
            repo_id = arguments["repo_id"]
            result = yuque_client.get_repo_toc(repo_id=repo_id)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": format_repo_toc(result)}]
                }
            })
        
        elif tool_name == "update_repo_toc":
            repo_id = arguments["repo_id"]
            toc_markdown = arguments["toc"]
            yuque_client.update_repo_toc(repo_id=repo_id, toc_markdown=toc_markdown)
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": "目录更新成功"}]
                }
            })
        
        else:
            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"未知工具: {tool_name}"}
            })
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            error_msg = "语雀API权限不足：请检查Token是否有写权限"
        elif e.response.status_code == 404:
            error_msg = "资源未找到：请检查命名空间和文档ID"
        else:
            error_msg = f"HTTP错误: {e.response.status_code}"
        
        logger.error(f"语雀API错误: {error_msg}")
        return jsonify({
            "jsonrpc": "2.0",
                "id": request_id,
            "error": {
                "code": -32000,
                "message": error_msg,
                "data": {
                    "status_code": e.response.status_code,
                    "yuque_error": e.response.text
                }
            }
        })
    
    except Exception as e:
        logger.error(f"工具调用失败: {e}")
        return jsonify({
            "jsonrpc": "2.0",
                "id": request_id,
            "error": {"code": -32000, "message": f"工具执行失败: {str(e)}"}
        })

def handle_ping(data):
    """处理 ping 请求"""
    return jsonify({
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {}
    })

# 格式化函数
def format_user_info(user_data: Dict) -> str:
    """格式化用户信息"""
    user = user_data.get("data", {})
    return f"""👤 语雀用户信息
姓名: {user.get('name', '未知')}
登录名: {user.get('login', '未知')}
用户ID: {user.get('id', '未知')}
知识库数量: {user.get('books_count', 0)}
关注: {user.get('following_count', 0)} | 粉丝: {user.get('followers_count', 0)}
注册时间: {user.get('created_at', '未知')}"""

def format_repos_list(repos_data: Dict) -> str:
    """格式化知识库列表"""
    repos = repos_data.get("data", [])
    if not repos:
        return "暂无知识库"
    
    # 按文档数量排序
    repos.sort(key=lambda x: x.get('items_count', 0), reverse=True)
    
    result = ["📚 您的语雀知识库列表 (按文档数量排序):"]
    for repo in repos:
        result.append(f"📖 {repo.get('name', '未知')}")
        result.append(f"  命名空间: {repo.get('namespace', '未知')}")
        result.append(f"  文档数: {repo.get('items_count', 0)} | 更新: {repo.get('updated_at', '未知')[:10]}")
        result.append("")
    
    return "\n".join(result)

def format_repo_info(repo_data: Dict) -> str:
    """格式化知识库信息"""
    repo = repo_data.get("data", {})
    return f"""知识库详情：
📖 名称: {repo.get('name', '未知')}
🔗 命名空间: {repo.get('namespace', '未知')}
📄 文档数量: {repo.get('items_count', 0)}
👀 关注数: {repo.get('watches_count', 0)}
❤️ 点赞数: {repo.get('likes_count', 0)}
📝 描述: {repo.get('description', '暂无描述')}
🕐 创建时间: {repo.get('created_at', '未知')}
✏️ 最后更新: {repo.get('updated_at', '未知')}"""

def format_docs_list(docs_data: Dict, namespace: str) -> str:
    """格式化文档列表"""
    docs = docs_data.get("data", [])
    if not docs:
        return f"知识库 '{namespace}' 暂无文档"
    
    result = [f"📄 知识库 '{namespace}' 中的文档:"]
    for i, doc in enumerate(docs, 1):
        result.append(f"{i}. {doc.get('title', '未知标题')}")
        result.append(f"   文档ID: {doc.get('id', '未知')}")
        result.append(f"   最后更新: {doc.get('updated_at', '未知')[:10]}")
        result.append("")
    
    return "\n".join(result)

def format_doc_content(doc_data: Dict) -> str:
    """格式化文档内容"""
    doc = doc_data.get("data", {})
    return f"""文档内容：
📖 标题: {doc.get('title', '未知')}
🆔 ID: {doc.get('id', '未知')}
📝 格式: {doc.get('format', '未知')}
📅 创建: {doc.get('created_at', '未知')}
✏️ 更新: {doc.get('updated_at', '未知')}

内容预览:
{doc.get('body', '暂无内容')[:500]}..."""

def format_created_doc(doc_data: Dict, namespace: str) -> str:
    """格式化创建的文档信息"""
    doc = doc_data.get("data", {})
    doc_url = f"https://www.yuque.com/{namespace}/{doc.get('slug', '')}"
    return f"""✅ 文档创建成功！
📖 标题: {doc.get('title', '未知')}
🆔 文档ID: {doc.get('id', '未知')}
🔗 访问链接: {doc_url}
📅 创建时间: {doc.get('created_at', '未知')}"""

def format_repo_created(repo_data: Dict, owner_login: str) -> str:
    repo = repo_data.get("data", {})
    namespace = repo.get("namespace", "未知")
    visibility = {0: "私密", 1: "团队可见", 2: "公开"}.get(repo.get("public", 0), "未知")
    return f"""✅ 知识库创建成功！
📚 名称: {repo.get('name', '未知')}
👤 所属: {owner_login}
🔗 命名空间: {namespace}
🌐 可见性: {visibility}
📅 创建时间: {repo.get('created_at', '未知')}"""


def format_doc_versions(versions_data: Dict, doc_id: int) -> str:
    versions = versions_data.get("data", [])
    if not versions:
        return f"文档 {doc_id} 暂无版本历史。"
    
    lines = [f"📜 文档 {doc_id} 版本历史（最多 10 条）:"]
    for version in versions[:10]:
        creator = version.get("creator", {}).get("name") if isinstance(version.get("creator"), dict) else version.get("creator")
        lines.append(
            f"- 版本 {version.get('version', version.get('id', '未知'))} · "
            f"{version.get('title', '未命名')} · "
            f"{creator or '匿名'} @ {version.get('created_at', '未知')}"
        )
    if len(versions) > 10:
        lines.append("... 其余版本请在语雀查看。")
    return "\n".join(lines)


def format_doc_version_detail(version_data: Dict) -> str:
    version = version_data.get("data", {})
    creator = version.get("creator", {})
    return f"""📘 文档版本详情
版本号: {version.get('version', '未知')}
标题: {version.get('title', '未命名')}
作者: {creator.get('name') or creator.get('login', '未知')}
创建时间: {version.get('created_at', '未知')}

变更说明:
{version.get('description', '无')}
"""


def format_search_results(search_data: Dict, query: str) -> str:
    """格式化搜索结果"""
    results = search_data.get("data", [])
    if not results:
        return f"未找到与 '{query}' 相关的文档"
    
    result = [f"🔍 搜索 '{query}' 的结果 (前10个):"]
    for item in results[:10]:
        result.append(f"📄 {item.get('title', '未知')}")
        result.append(f"   知识库: {item.get('book', {}).get('name', '未知')}")
        result.append(f"   摘要: {item.get('summary', '')[:100]}...")
        result.append("")
    
    return "\n".join(result)

def format_groups_list(groups_data: Dict) -> str:
    """格式化团队列表"""
    groups = groups_data.get("data", [])
    if not groups:
        return "您尚未加入任何团队"
    
    result = ["👥 我的团队列表:"]
    for group in groups:
        result.append(f"- {group.get('name', '未知')} (ID: {group.get('id', '未知')})")
        result.append(f"  描述: {group.get('description', '暂无描述')}")
        result.append(f"  成员数: {group.get('members_count', 0)}")
    
    return "\n".join(result)


def format_group_info(group_data: Dict) -> str:
    group = group_data.get("data", {})
    return f"""👥 团队信息
名称: {group.get('name', '未知')}
ID: {group.get('id', '未知')}
描述: {group.get('description', '暂无描述')}
成员数: {group.get('members_count', 0)}
创建时间: {group.get('created_at', '未知')}
更新: {group.get('updated_at', '未知')}"""


def format_group_users(users_data: Dict, group_id: int) -> str:
    users = users_data.get("data", [])
    if not users:
        return f"团队 {group_id} 暂无成员信息。"
    
    result = [f"👤 团队 {group_id} 的成员:"]
    for user in users:
        result.append(f"- {user.get('name', '未知')} ({user.get('login', '未知')}) 角色: {user.get('role', 'member')}")
    return "\n".join(result)


def format_repo_toc(toc_data: Dict) -> str:
    data = toc_data.get("data")
    if not data:
        return "目录为空或未配置。"
    
    toc_text = ""
    if isinstance(data, dict):
        toc_text = data.get("toc_yml") or data.get("toc_yaml") or data.get("toc") or ""
    elif isinstance(data, str):
        toc_text = data
    
    if not toc_text:
        return "目录内容为空。"
    
    preview = "\n".join(toc_text.splitlines()[:40])
    if len(toc_text.splitlines()) > 40:
        preview += "\n..."
    return f"📚 当前目录（Markdown）:\n{preview}"


def format_group_statistics(stats_data: Dict) -> str:
    stats = stats_data.get("data", {})
    if not stats:
        return "暂无团队统计数据。"
    lines = [
        "📊 团队汇总统计",
        f"成员数: {stats.get('member_count', '未知')}",
        f"知识库数: {stats.get('book_count', '未知')} (公开 {stats.get('public_book_count', '未知')})",
        f"文档数: {stats.get('doc_count', '未知')}",
        f"近30天阅读: {stats.get('read_count_30', '未知')}, 写作: {stats.get('write_count_30', '未知')}",
        f"累计点赞: {stats.get('like_count', '未知')} · 评论: {stats.get('comment_count', '未知')}",
        f"数据占用: {stats.get('data_usage', '未知')}"
    ]
    return "\n".join(lines)


def format_group_member_stats(stats_data: Dict) -> str:
    members = stats_data.get("data", {}).get("members")
    if not members:
        return "未查询到成员统计信息。"
    
    if isinstance(members, dict):
        members = members.values()
    
    lines = ["👥 成员活跃度（前 10 条）:"]
    for item in list(members)[:10]:
        user = item.get("user", {})
        lines.append(
            f"- {user.get('name', '未知')} · 写作 {item.get('write_count', 0)} 次 · "
            f"阅读 {item.get('read_count', 0)} 次 · 点赞 {item.get('like_count', 0)}"
        )
    total = stats_data.get("data", {}).get("total")
    if total:
        lines.append(f"共 {total} 人")
    return "\n".join(lines)


def format_group_book_stats(stats_data: Dict) -> str:
    books = stats_data.get("data", {}).get("books") or stats_data.get("data", [])
    if isinstance(books, dict):
        books = books.values()
    books = list(books)
    if not books:
        return "未查询到知识库统计信息。"
    
    lines = ["📚 知识库统计（前 10 条）:"]
    for book in books[:10]:
        lines.append(
            f"- {book.get('name', '未命名')} · 阅读 {book.get('read_count', 0)} · "
            f"写作 {book.get('write_count', 0)} · 点赞 {book.get('like_count', 0)}"
        )
    total = stats_data.get("data", {}).get("total")
    if total:
        lines.append(f"共 {total} 个知识库")
    return "\n".join(lines)


def format_group_doc_stats(stats_data: Dict) -> str:
    docs = stats_data.get("data", {}).get("docs") or stats_data.get("data", {}).get("documents") or stats_data.get("data", [])
    if isinstance(docs, dict):
        docs = docs.values()
    docs = list(docs)
    if not docs:
        return "未查询到文档统计信息。"
    
    lines = ["📄 文档统计（前 10 条）:"]
    for doc in docs[:10]:
        lines.append(
            f"- {doc.get('title', '未命名')} · 阅读 {doc.get('read_count', 0)} · "
            f"评论 {doc.get('comment_count', 0)} · 点赞 {doc.get('like_count', 0)}"
        )
    total = stats_data.get("data", {}).get("total")
    if total:
        lines.append(f"共 {total} 篇文档统计数据")
    return "\n".join(lines)

    users = users_data.get("data", [])
    if not users:
        return f"团队 {group_id} 暂无成员信息。"
    
    result = [f"👤 团队 {group_id} 的成员:"]
    for user in users:
        result.append(f"- {user.get('name', '未知')} ({user.get('login', '未知')}) 角色: {user.get('role', 'member')}")
    return "\n".join(result)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    try:
        # 尝试获取 Token 并创建客户端
        token = get_yuque_token()
        yuque_client = YuqueMCPClient(token)
        user_info = yuque_client.get_user_info()
        user_login = user_info.get("data", {}).get("login", "unknown")
        return jsonify({
            'status': 'healthy', 
            'message': '语雀MCP服务器运行正常',
            'user': user_login,
            'token_source': 'header' if request.headers.get('X-Yuque-Token') else 'environment'
        })
    except ValueError as e:
        # Token 配置缺失
        return jsonify({
            'status': 'configured', 
            'message': '服务器运行正常，但缺少语雀 Token 配置',
            'error': str(e)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error', 
            'error': str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """测试端点"""
    return jsonify({
        'server': 'yuque-mcp-server',
        'version': '2.0.0',
        'status': 'running'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    print(f"🚀 语雀 MCP 服务器启动在 http://localhost:{port}")
    print(f"📊 健康检查: http://localhost:{port}/health")
    print(f"🔗 MCP 端点: http://localhost:{port}/mcp")
    print(f"🧪 测试端点: http://localhost:{port}/test")
    print(f"📚 支持功能: 用户信息、知识库管理、文档CRUD、搜索、团队管理")
    
    app.run(host='0.0.0.0', port=port, debug=False)