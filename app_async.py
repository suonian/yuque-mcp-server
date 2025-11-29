#!/usr/bin/env python3
"""
语雀 MCP 服务器 - 异步版本
使用 FastAPI 框架和异步 API 客户端
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import json
import time
from typing import Dict, Any

from config import CONFIG, MCP_ERROR_CODES, DEFAULT_CORS_ORIGIN, PORT
from async_yuque_client import AsyncYuqueMCPClient
from utils.formatters import *
from cache import cache_manager


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 创建 FastAPI 应用
app = FastAPI(
    title="Yuque MCP Server",
    description="语雀 MCP 服务器，支持 MCP 协议和语雀 API 调用",
    version="2.0.0"
)


# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_yuque_token(request: Request) -> str:
    """
    获取语雀 Token，优先级：
    1. HTTP Header: X-Yuque-Token
    2. 环境变量: YUQUE_TOKEN
    3. 配置文件: yuque-config.env
    如果都没有，抛出异常
    """
    # 优先从 HTTP Header 读取
    token = request.headers.get('X-Yuque-Token')
    
    # 如果没有 Header，从环境变量读取
    if not token:
        token = os.getenv('YUQUE_TOKEN')
    
    # 如果没有环境变量，从配置文件读取
    if not token:
        token = CONFIG.get('YUQUE_TOKEN')
    
    # 如果都没有，返回错误
    if not token:
        raise ValueError(
            "缺少语雀 Token 配置。请通过以下方式之一提供：\n"
            "1. HTTP Header: X-Yuque-Token\n"
            "2. 环境变量: YUQUE_TOKEN\n"
            "3. 配置文件: yuque-config.env"
        )
    
    return token


@app.post("/mcp")
async def handle_mcp(request: Request):
    """处理 MCP 协议请求"""
    try:
        data = await request.json()
        logger.info(
            "收到 MCP 请求: method=%s id=%s",
            data.get("method", "unknown"),
            data.get("id")
        )
        
        if data.get("jsonrpc") != "2.0":
            return {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {"code": -32600, "message": "Invalid Request"}
            }
        
        method = data.get("method")
        request_id = data.get("id")
        
        if method != "notifications/initialized" and request_id is None:
            logger.warning("JSON-RPC 请求缺少 id 字段")
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Missing id in request"}
            }
        
        if method == "initialize":
            return await handle_initialize(data)
        elif method == "tools/list":
            return await handle_tools_list(data)
        elif method == "tools/call":
            return await handle_tools_call(data, request)
        elif method == "ping":
            return await handle_ping(data)
        elif method == "notifications/initialized":
            logger.info("收到 notifications/initialized 通知，已完成握手。")
            return Response(status_code=204)
        else:
            return {
                "jsonrpc": "2.0",
                "id": data.get("id"),
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }
            
    except Exception as e:
        logger.error(f"处理请求时出错: {e}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": data.get("id") if 'data' in locals() else None,
            "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
        }


async def handle_initialize(data: Dict[str, Any]):
    """处理初始化请求"""
    response = {
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {
            "protocolVersion": "2024-11-05",
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
    return response


async def handle_tools_list(data: Dict[str, Any]):
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
            "description": "获取文档详细内容，支持获取完整 Markdown 源码。注意：需要从搜索结果中获取 namespace 和 slug 参数",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "namespace": {"type": "string", "description": "知识库命名空间（从搜索结果中获取）"},
                    "slug": {"type": "string", "description": "文档标识（从搜索结果中获取）"},
                    "raw": {"type": "boolean", "description": "是否获取原始 Markdown（完整内容），默认 false。设为 true 可尝试获取完整内容"}
                },
                "required": ["namespace", "slug"]
            }
        },
        {
            "name": "get_doc_by_id",
            "description": "通过文档ID获取文档内容。注意：语雀API不支持直接通过文档ID获取，此工具会提供使用建议",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "doc_id": {"type": "integer", "description": "文档ID（从搜索结果中获取）"}
                },
                "required": ["doc_id"]
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
    
    return {
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {"tools": tools}
    }


async def handle_tools_call(data: Dict[str, Any], request: Request):
    """处理工具调用请求"""
    params = data.get("params", {})
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    request_id = data.get("id")
    
    logger.info(f"调用工具: {tool_name}, 参数: {arguments}")
    
    # 获取 Token 并创建客户端
    try:
        token = await get_yuque_token(request)
        async with AsyncYuqueMCPClient(token) as yuque_client:
            # 工具调用逻辑
            if tool_name == "get_user_info":
                result = await yuque_client.get_user_info()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_user_info(result)}]
                    }
                }
            
            elif tool_name == "get_user":
                login = arguments["login"]
                result = await yuque_client.get_user(login)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_user_info(result)}]
                    }
                }
            
            elif tool_name == "list_repos":
                result = await yuque_client.list_repos()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repos_list(result)}]
                    }
                }
            
            elif tool_name == "list_user_repos":
                login = arguments["login"]
                result = await yuque_client.list_user_repos(login)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repos_list(result)}]
                    }
                }
            
            elif tool_name == "list_group_repos":
                login = arguments["login"]
                result = await yuque_client.list_group_repos(login)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repos_list(result)}]
                    }
                }
            
            elif tool_name == "get_repo":
                namespace = arguments["namespace"]
                result = await yuque_client.get_repo(namespace)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repo_info(result)}]
                    }
                }
            
            elif tool_name == "create_repo":
                owner_login = arguments.get("owner_login") or arguments.get("login")
                if not owner_login:
                    raise ValueError("创建知识库需要提供 owner_login（或 login）字段")
                owner_type = arguments.get("owner_type", "user")
                name = arguments["name"]
                slug = arguments.get("slug")
                description = arguments.get("description")
                public = arguments.get("public", 0)
                result = await yuque_client.create_repo(
                    owner_login,
                    name,
                    slug,
                    description,
                    public,
                    owner_type=owner_type
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repo_created(result, owner_login)}]
                    }
                }
            
            elif tool_name == "update_repo":
                repo_id = arguments.get("repo_id")
                namespace = arguments.get("namespace")
                if repo_id is None and not namespace:
                    raise ValueError("需要提供 repo_id 或 namespace")
                result = await yuque_client.update_repo(
                    repo_id=repo_id,
                    namespace=namespace,
                    name=arguments.get("name"),
                    slug=arguments.get("slug"),
                    description=arguments.get("description"),
                    public=arguments.get("public"),
                    toc=arguments.get("toc")
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repo_info(result)}]
                    }
                }
            
            elif tool_name == "delete_repo":
                repo_id = arguments.get("repo_id")
                namespace = arguments.get("namespace")
                if repo_id is None and not namespace:
                    raise ValueError("需要提供 repo_id 或 namespace")
                await yuque_client.delete_repo(repo_id=repo_id, namespace=namespace)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": "知识库已删除"}]
                    }
                }
            
            elif tool_name == "list_docs":
                namespace = arguments["namespace"]
                result = await yuque_client.list_docs(namespace)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_docs_list(result, namespace)}]
                    }
                }
            
            elif tool_name == "get_doc":
                namespace = arguments["namespace"]
                slug = arguments["slug"]
                raw = arguments.get("raw", False)  # 支持 raw 参数
                
                # 获取文档内容
                result = await yuque_client.get_doc(namespace, slug, raw=raw)
                
                # 获取知识库信息（用于显示完整元数据）
                repo_info = None
                try:
                    repo_info = await yuque_client.get_repo(namespace)
                except Exception as e:
                    logger.warning(f"获取知识库信息失败: {e}")
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_doc_content(result, repo_info, namespace, slug, include_full=True)}]
                    }
                }
            
            elif tool_name == "get_doc_by_id":
                doc_id = arguments["doc_id"]
                try:
                    # 尝试通过文档ID获取文档
                    result = await yuque_client.get_doc_by_id(doc_id)
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [{"type": "text", "text": format_doc_content(result, include_full=True)}]
                        }
                    }
                except ValueError as e:
                    # 返回友好的错误提示和使用建议
                    error_msg = str(e)
                    suggestion = f"""
❌ 无法通过文档ID直接获取文档

📋 问题说明：
语雀API不支持直接通过文档ID获取文档内容，必须使用 namespace + slug 的方式。

💡 解决方案：
1. 使用 search_docs 工具搜索文档，从搜索结果中获取：
   - namespace（命名空间，如：your-username/repo-name）
   - slug（文档标识，如：doc-slug）

2. 然后使用 get_doc 工具获取完整内容：
   get_doc(namespace="从搜索结果中获取", slug="从搜索结果中获取")

📝 示例：
如果搜索结果中显示：
   🔗 完整路径: your-username/my-repo/my-doc
   那么：
   - namespace = "your-username/my-repo"
   - slug = "my-doc"

🔍 提示：搜索结果中已包含完整的 namespace 和 slug 信息，请直接使用。
"""
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32008,
                            "message": f"无法通过文档ID {doc_id} 直接获取文档",
                            "data": {
                                "doc_id": doc_id,
                                "suggestion": suggestion,
                                "alternative_method": "请使用 get_doc(namespace, slug) 工具，参数从搜索结果中获取"
                            }
                        }
                    }
            
            elif tool_name == "list_doc_versions":
                doc_id = arguments["doc_id"]
                result = await yuque_client.list_doc_versions(doc_id)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_doc_versions(result, doc_id)}]
                    }
                }
            
            elif tool_name == "get_doc_version":
                version_id = arguments["version_id"]
                result = await yuque_client.get_doc_version(version_id)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_doc_version_detail(result)}]
                    }
                }
            
            elif tool_name == "create_doc":
                namespace = arguments["namespace"]
                title = arguments["title"]
                content = arguments["content"]
                format_type = arguments.get("format", "markdown")
                result = await yuque_client.create_doc(namespace, title, content, format_type)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_created_doc(result, namespace)}]
                    }
                }
            
            elif tool_name == "update_doc":
                namespace = arguments["namespace"]
                doc_id = arguments["doc_id"]
                title = arguments.get("title")
                content = arguments.get("content")
                if not title and not content:
                    raise ValueError("更新文档时至少提供 title 或 content 之一")
                result = await yuque_client.update_doc(namespace, doc_id, title, content)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"文档更新成功！文档ID: {doc_id}"}]
                    }
                }
            
            elif tool_name == "delete_doc":
                namespace = arguments["namespace"]
                doc_id = arguments["doc_id"]
                result = await yuque_client.delete_doc(namespace, doc_id)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"文档删除成功！文档ID: {doc_id}"}]
                    }
                }
            
            elif tool_name == "search_docs":
                query = arguments["query"]
                search_type = arguments.get("type", "doc")
                result = await yuque_client.search(query, search_type)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_search_results(result, query)}]
                    }
                }
            
            elif tool_name == "list_groups":
                result = await yuque_client.list_groups()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_groups_list(result)}]
                    }
                }
            
            elif tool_name == "get_group":
                group_id = arguments["group_id"]
                result = await yuque_client.get_group(group_id)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_group_info(result)}]
                    }
                }
            
            elif tool_name == "list_group_users":
                group_id = arguments["group_id"]
                result = await yuque_client.list_group_users(group_id)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_group_users(result, group_id)}]
                    }
                }
            
            elif tool_name == "update_group_member":
                group_login = arguments["group_login"]
                user_identity = arguments["user_identity"]
                role = arguments["role"]
                await yuque_client.update_group_member(group_login, user_identity, role)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"已更新 {user_identity} 在 {group_login} 的角色为 {role}"}]
                    }
                }
            
            elif tool_name == "remove_group_member":
                group_login = arguments["group_login"]
                user_identity = arguments["user_identity"]
                await yuque_client.remove_group_member(group_login, user_identity)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"已将 {user_identity} 从团队 {group_login} 移除"}]
                    }
                }
            
            elif tool_name == "get_group_statistics":
                group_login = arguments["group_login"]
                result = await yuque_client.get_group_statistics(group_login)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_group_statistics(result)}]
                    }
                }
            
            elif tool_name == "get_group_member_stats":
                group_login = arguments["group_login"]
                params = {k: v for k, v in arguments.items() if k not in {"group_login"} and v is not None}
                result = await yuque_client.get_group_member_statistics(group_login, **params)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_group_member_stats(result)}]
                    }
                }
            
            elif tool_name == "get_group_book_stats":
                group_login = arguments["group_login"]
                params = {k: v for k, v in arguments.items() if k not in {"group_login"} and v is not None}
                result = await yuque_client.get_group_book_statistics(group_login, **params)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_group_book_stats(result)}]
                    }
                }
            
            elif tool_name == "get_group_doc_stats":
                group_login = arguments["group_login"]
                params = {k: v for k, v in arguments.items() if k not in {"group_login"} and v is not None}
                result = await yuque_client.get_group_doc_statistics(group_login, **params)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_group_doc_stats(result)}]
                    }
                }
            
            elif tool_name == "get_repo_toc":
                repo_id = arguments["repo_id"]
                result = await yuque_client.get_repo_toc(repo_id=repo_id)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": format_repo_toc(result)}]
                    }
                }
            
            elif tool_name == "update_repo_toc":
                repo_id = arguments["repo_id"]
                toc_markdown = arguments["toc"]
                await yuque_client.update_repo_toc(repo_id=repo_id, toc_markdown=toc_markdown)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": "目录更新成功"}]
                    }
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": f"未知工具: {tool_name}"}
                }
    
    except httpx.HTTPError as e:
        status_code = e.response.status_code
        
        # 根据状态码确定错误类型和解决建议
        if status_code == 401:
            error_code = -32001
            error_msg = "认证失败：Token 无效或已过期"
            suggestion = "请检查 Token 是否正确，或重新生成 Token"
        elif status_code == 403:
            error_code = -32002
            error_msg = "权限不足：当前 Token 没有访问此资源的权限"
            suggestion = "请检查文档/知识库的可见性设置，或使用有完整权限的 Token"
        elif status_code == 404:
            error_code = -32003
            error_msg = "资源未找到：请检查命名空间和文档标识是否正确"
            suggestion = "请确认 namespace 和 slug 参数是否正确，或资源可能已被删除"
        elif status_code == 429:
            error_code = -32005
            error_msg = "请求频率过高：已达到 API 限流阈值"
            suggestion = "请稍后重试，或降低请求频率"
        elif status_code >= 500:
            error_code = -32006
            error_msg = f"上游服务错误：语雀 API 返回 {status_code}"
            suggestion = "请稍后重试，或联系语雀技术支持"
        else:
            error_code = -32000
            error_msg = f"HTTP 错误: {status_code}"
            suggestion = "请检查请求参数和网络连接"
        
        # 解析错误响应
        error_data = {}
        try:
            error_data = e.response.json()
        except:
            error_data = {"message": e.response.text[:200]}  # 限制错误文本长度
        
        logger.error(f"[YuqueAPI] 错误 [{status_code}]: {error_msg}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": error_code,
                "message": error_msg,
                "data": {
                    "status_code": status_code,
                    "suggestion": suggestion,
                    "yuque_error": error_data.get("message", e.response.text[:500] if e.response.text else None)
                }
            }
        }
    
    except Exception as e:
        logger.error(f"工具调用失败: {e}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32000, "message": f"工具执行失败: {str(e)}"}
        }


@app.get("/ping")
async def handle_ping(data: Dict[str, Any]):
    """处理 ping 请求"""
    return {
        "jsonrpc": "2.0",
        "id": data.get("id"),
        "result": {}
    }


@app.get("/health")
async def health_check(request: Request):
    """健康检查端点"""
    try:
        # 尝试获取 Token 并创建客户端
        token = await get_yuque_token(request)
        async with AsyncYuqueMCPClient(token) as yuque_client:
            user_info = await yuque_client.get_user_info()
            user_login = user_info.get("data", {}).get("login", "unknown")
        
        # 确定 Token 来源
        if request.headers.get('X-Yuque-Token'):
            token_source = 'header'
        elif os.getenv('YUQUE_TOKEN'):
            token_source = 'environment'
        else:
            token_source = 'config_file'
            
        return {
            'status': 'healthy', 
            'message': '语雀MCP服务器运行正常',
            'user': user_login,
            'token_source': token_source,
            'cache_stats': cache_manager.get_stats()
        }
    except ValueError as e:
        # Token 配置缺失
        return {
            'status': 'configured', 
            'message': '服务器运行正常，但缺少语雀 Token 配置',
            'error': str(e),
            'cache_stats': cache_manager.get_stats()
        }
    except Exception as e:
        return {
            'status': 'error', 
            'error': str(e),
            'cache_stats': cache_manager.get_stats()
        }


@app.get("/test")
async def test_endpoint():
    """测试端点"""
    return {
        'server': 'yuque-mcp-server',
        'version': '2.0.0',
        'status': 'running',
        'mode': 'async',
        'cache_stats': cache_manager.get_stats()
    }


# 启动服务器
if __name__ == '__main__':
    import uvicorn
    
    print(f"🚀 语雀 MCP 服务器启动在 http://localhost:{PORT}")
    print(f"📊 健康检查: http://localhost:{PORT}/health")
    print(f"🔗 MCP 端点: http://localhost:{PORT}/mcp")
    print(f"🧪 测试端点: http://localhost:{PORT}/test")
    print(f"📚 支持功能: 用户信息、知识库管理、文档CRUD、搜索、团队管理")
    print(f"⚡ 运行模式: 异步")
    
    uvicorn.run(
        "app_async:app",
        host="0.0.0.0",
        port=PORT,
        reload=False,
        workers=4
    )
