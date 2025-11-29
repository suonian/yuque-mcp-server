import os
import logging
from typing import Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_file_path: Optional[str] = None) -> dict[str, str]:
    """
    从配置文件加载配置
    
    Args:
        config_file_path: 配置文件路径，默认在当前目录查找 yuque-config.env
    """
    config: dict[str, str] = {}
    
    if config_file_path:
        config_file = config_file_path
    else:
        # 先在当前目录查找
        config_file = os.path.join(os.getcwd(), 'yuque-config.env')
        # 如果当前目录没有，再在脚本所在目录查找
        if not os.path.exists(config_file):
            config_file = os.path.join(os.path.dirname(__file__), 'yuque-config.env')
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config


# 加载配置
CONFIG = load_config()

# 语雀 API 配置
YUQUE_BASE_URL = CONFIG.get("YUQUE_BASE_URL", "https://www.yuque.com/api/v2")

# MCP 协议配置
MCP_PROTOCOL_VERSION = CONFIG.get("MCP_PROTOCOL_VERSION", "2024-11-05")
DEFAULT_CORS_ORIGIN = CONFIG.get("DEFAULT_CORS_ORIGIN", "*")

# 服务配置
PORT = int(CONFIG.get("PORT", os.getenv("PORT", "3000")))

# MCP 标准错误码扩展
MCP_ERROR_CODES = {
    # JSON-RPC 2.0 标准错误码
    -32700: "Parse error",              # JSON 解析失败
    -32600: "Invalid Request",          # 请求格式错误
    -32601: "Method not found",         # 方法不存在
    -32602: "Invalid params",           # 参数错误
    -32603: "Internal error",           # 内部错误
    
    # 自定义扩展错误码（语雀相关）
    -32001: "Authentication failed",    # 认证失败
    -32002: "Permission denied",        # 权限不足
    -32003: "Resource not found",       # 资源不存在
    -32004: "Preview only",             # 仅预览权限
    -32005: "Rate limit exceeded",      # 限流
    -32006: "Upstream service error",   # 上游服务错误
    -32007: "Content truncated",        # 内容被截断
    -32008: "Namespace not found",      # 命名空间不存在
}
