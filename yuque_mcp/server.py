#!/usr/bin/env python3
import os
import sys
import logging
import json
import argparse
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置Python路径以确保模块导入正确
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 设置环境变量禁用 FastMCP 输出
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['FORCE_COLOR'] = '0'
os.environ['NO_COLOR'] = '1'

from fastmcp import FastMCP

# 导入项目内部模块
try:
    # 尝试相对导入（作为包运行时）
    from .utils.api_client import YuqueAPIClient
    from .utils.response_formatter import format_success_response, format_error_response
except ImportError:
    # 尝试绝对导入（直接运行时）
    from yuque_mcp.utils.api_client import YuqueAPIClient
    from yuque_mcp.utils.response_formatter import format_success_response, format_error_response

# 加载配置
class Config:
    def __init__(self):
        self.config = {
            "yuque": {
                "token": os.environ.get("YUQUE_TOKEN", ""),
                "base_url": "https://www.yuque.com/api/v2"
            },
            "server": {
                "transport": "stdio",
                "port": 3000,
                "host": "0.0.0.0",
                "log_level": "CRITICAL"
            }
        }
        
        # 尝试从配置文件加载
        config_path = os.path.join(project_root, "config.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    file_config = json.load(f)
                    # 合并配置
                    if "yuque" in file_config:
                        self.config["yuque"].update(file_config["yuque"])
                    if "server" in file_config:
                        self.config["server"].update(file_config["server"])
                    # 处理环境变量占位符
                    if "$YUQUE_TOKEN" in self.config["yuque"]["token"]:
                        self.config["yuque"]["token"] = os.environ.get("YUQUE_TOKEN", "")
            except json.JSONDecodeError as e:
                logging.error(f"配置文件解析错误: {e}")
    
    def get(self, key, default=None):
        """获取配置值"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

config = Config()

# 禁用所有输出到stdout/stderr，除了MCP协议消息
class QuietLogger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.log_level = getattr(logging, config.get("server.log_level"), logging.CRITICAL)
        self.logger.setLevel(self.log_level)
        
        # 清理现有handler
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # 只保留文件handler
        file_handler = logging.FileHandler(os.path.join(project_root, "yuque_mcp.log"), mode='a', encoding='utf-8')
        file_handler.setLevel(self.log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def critical(self, msg, *args, **kwargs):
        if msg:
            self.logger.critical(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        if msg:
            self.logger.error(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        if msg:
            self.logger.warning(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        if msg:
            self.logger.info(msg, *args, **kwargs)
    
    def debug(self, msg, *args, **kwargs):
        if msg:
            self.logger.debug(msg, *args, **kwargs)

# 使用自定义的静默logger
logger = QuietLogger()

# 创建FastMCP实例
mcp = FastMCP(
    name="yuque-mcp-server",
    version="1.0.0",
    instructions="语雀MCP服务器，提供语雀API的MCP接口"
)

# 配置日志
logging.basicConfig(
    level=logger.log_level,
    filename=os.path.join(project_root, "yuque_mcp.log"),
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 禁用第三方库日志输出
for lib_name in ["fastmcp", "rich", "uvicorn", "httpx"]:
    logging.getLogger(lib_name).setLevel(logging.CRITICAL)

# 禁用所有控制台handler
for logger_name in logging.root.manager.loggerDict:
    logger_instance = logging.getLogger(logger_name)
    for handler in logger_instance.handlers[:]:
        if isinstance(handler, logging.StreamHandler):
            logger_instance.removeHandler(handler)

# 定义工具函数
@mcp.tool()
async def get_user_info() -> dict:
    """获取当前用户信息"""
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
        
    try:
        async with YuqueAPIClient(token) as client:
            result = await client.get_user_info()
            return format_success_response(result.get("data"), "获取用户信息成功")
    except Exception as e:
        logger.error(f"获取用户信息失败: {str(e)}")
        return format_error_response("API_ERROR", f"获取用户信息失败: {str(e)}")


@mcp.tool()
async def list_repos(limit: int = 20, offset: int = 0) -> dict:
    """列出当前用户的知识库"""
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    try:
        async with YuqueAPIClient(token) as client:
            result = await client.list_repos(limit=limit, offset=offset)
            return format_success_response(result, "获取知识库列表成功")
    except Exception as e:
        logger.error(f"获取知识库列表失败: {str(e)}")
        return format_error_response("API_ERROR", f"获取知识库列表失败: {str(e)}")


@mcp.tool()
async def get_repo(namespace: str) -> dict:
    """获取知识库详情"""
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not namespace:
        return format_error_response("PARAM_ERROR", "缺少知识库命名空间")

    try:
        async with YuqueAPIClient(token) as client:
            result = await client.get_repo(namespace)
            return format_success_response(result, "获取知识库详情成功")
    except Exception as e:
        logger.error(f"获取知识库详情失败: {str(e)}")
        return format_error_response("API_ERROR", f"获取知识库详情失败: {str(e)}")


@mcp.tool()
async def list_docs(namespace: str, limit: int = 20, offset: int = 0) -> dict:
    """列出知识库中的文档"""
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not namespace:
        return format_error_response("PARAM_ERROR", "缺少知识库命名空间")

    try:
        async with YuqueAPIClient(token) as client:
            result = await client.list_docs(namespace, limit=limit, offset=offset)
            return format_success_response(result, "获取文档列表成功")
    except Exception as e:
        logger.error(f"获取文档列表失败: {str(e)}")
        return format_error_response("API_ERROR", f"获取文档列表失败: {str(e)}")


@mcp.tool()
async def get_doc(namespace: str, slug: str, raw: bool = False) -> dict:
    """获取文档详情"""
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not namespace or not slug:
        return format_error_response("PARAM_ERROR", "缺少知识库命名空间或文档标识")

    try:
        async with YuqueAPIClient(token) as client:
            result = await client.get_doc(namespace, slug, raw=raw)
            return format_success_response(result, "获取文档详情成功")
    except Exception as e:
        logger.error(f"获取文档详情失败: {str(e)}")
        return format_error_response("API_ERROR", f"获取文档详情失败: {str(e)}")


@mcp.tool()
async def search(q: str, type: str = "doc", limit: int = 20, offset: int = 0) -> dict:
    """搜索文档或知识库"""
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not q:
        return format_error_response("PARAM_ERROR", "缺少搜索关键词")

    try:
        async with YuqueAPIClient(token) as client:
            result = await client.search(q, type=type, limit=limit, offset=offset)
            return format_success_response(result, "搜索成功")
    except Exception as e:
        logger.error(f"搜索失败: {str(e)}")
        return format_error_response("API_ERROR", f"搜索失败: {str(e)}")


@mcp.tool()
async def create_doc(namespace: str, title: str, body: str, slug: Optional[str] = None,
                    format: str = "markdown", public: int = 0) -> dict:
    """创建文档

    Args:
        namespace: 知识库命名空间（如：username/repo-name）
        title: 文档标题
        body: 文档内容（支持 Markdown）
        slug: 文档路径标识（可选，如：my-doc）
        format: 文档格式（markdown 或 lake）
        public: 是否公开（0-私密，1-公开）
    """
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not namespace or not title or not body:
        return format_error_response("PARAM_ERROR", "缺少必要参数（namespace, title, body）")

    try:
        async with YuqueAPIClient(token) as client:
            # 如果提供了 slug，检查是否已存在
            if slug:
                existing_doc = await client.get_doc_by_slug(namespace, slug)
                if existing_doc:
                    # 自动添加后缀
                    counter = 1
                    original_slug = slug
                    while existing_doc:
                        slug = f"{original_slug}-{counter}"
                        existing_doc = await client.get_doc_by_slug(namespace, slug)
                        counter += 1

            result = await client.create_doc(namespace, title, body, slug, format, public)
            return format_success_response(result, "文档创建成功")
    except Exception as e:
        logger.error(f"创建文档失败: {str(e)}")
        return format_error_response("API_ERROR", f"创建文档失败: {str(e)}")


@mcp.tool()
async def update_doc(namespace: str, slug: str, title: Optional[str] = None,
                    body: Optional[str] = None, slug_new: Optional[str] = None) -> dict:
    """更新文档

    Args:
        namespace: 知识库命名空间（如：username/repo-name）
        slug: 文档路径标识（用于查找文档）
        title: 新的文档标题（可选）
        body: 新的文档内容（可选）
        slug_new: 新的文档路径标识（可选）
    """
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not namespace or not slug:
        return format_error_response("PARAM_ERROR", "缺少必要参数（namespace, slug）")

    if title is None and body is None and slug_new is None:
        return format_error_response("PARAM_ERROR", "至少提供一个需要更新的字段（title, body, slug_new）")

    try:
        async with YuqueAPIClient(token) as client:
            # 通过 slug 查找文档
            doc_info = await client.get_doc_by_slug(namespace, slug)
            if not doc_info:
                return format_error_response("NOT_FOUND", f"未找到 slug 为 '{slug}' 的文档")

            doc_id = doc_info.get("id")
            if not doc_id:
                return format_error_response("API_ERROR", "无法获取文档ID")

            # 更新文档
            result = await client.update_doc(namespace, doc_id, title, body, slug_new)
            return format_success_response(result, "文档更新成功")
    except Exception as e:
        logger.error(f"更新文档失败: {str(e)}")
        return format_error_response("API_ERROR", f"更新文档失败: {str(e)}")


@mcp.tool()
async def delete_doc(namespace: str, slug: str) -> dict:
    """删除文档

    Args:
        namespace: 知识库命名空间（如：username/repo-name）
        slug: 文档路径标识
    """
    token = config.get("yuque.token")
    if not token:
        return format_error_response("AUTH_ERROR", "缺少语雀API Token")
    
    if not namespace or not slug:
        return format_error_response("PARAM_ERROR", "缺少必要参数（namespace, slug）")

    try:
        async with YuqueAPIClient(token) as client:
            # 通过 slug 查找文档
            doc_info = await client.get_doc_by_slug(namespace, slug)
            if not doc_info:
                return format_error_response("NOT_FOUND", f"未找到 slug 为 '{slug}' 的文档")

            doc_id = doc_info.get("id")
            if not doc_id:
                return format_error_response("API_ERROR", "无法获取文档ID")

            # 删除文档
            result = await client.delete_doc(namespace, doc_id)
            return format_success_response(result, "文档删除成功")
    except Exception as e:
        logger.error(f"删除文档失败: {str(e)}")
        return format_error_response("API_ERROR", f"删除文档失败: {str(e)}")


# 主函数
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="语雀MCP服务器")
    parser.add_argument("--transport", type=str, choices=["stdio", "sse"], 
                      default=config.get("server.transport"), help="传输方式")
    parser.add_argument("--port", type=int, default=config.get("server.port"), help="监听端口")
    parser.add_argument("--host", type=str, default=config.get("server.host"), help="监听地址")
    parser.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      default=config.get("server.log_level"), help="日志级别")
    parser.add_argument("--show-banner", action="store_true", help="显示启动横幅")
    
    args = parser.parse_args()
    
    try:
        logger.info(f"启动语雀MCP服务器，传输方式: {args.transport}")
        
        if args.transport == "sse":
            # SSE 模式（用于 HTTP 服务器）
            logger.info(f"监听地址: {args.host}:{args.port}")
            mcp.run(
                transport="sse", 
                host=args.host, 
                port=args.port, 
                show_banner=args.show_banner
            )
        else:
            # stdio 模式（用于 Claude Code 等 MCP 客户端）
            mcp.run(show_banner=args.show_banner)
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}")
        # 只在日志中记录错误，不输出到控制台
        sys.exit(1)
