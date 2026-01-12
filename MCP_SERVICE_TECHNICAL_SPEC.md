# MCP服务技术规范文档

## 1. 概述

本规范文档基于语雀MCP服务器的创建过程，定义了创建和配置Model Context Protocol (MCP)服务的标准流程和最佳实践。遵循本规范可以确保MCP服务具有良好的可维护性、可扩展性和易用性。

## 2. 项目结构设计

### 2.1 基本项目结构

```
mcp-service/
├── mcp_service/              # 主源码目录
│   ├── __init__.py           # 包初始化文件
│   ├── server.py             # MCP服务器主入口
│   ├── models/               # 数据模型目录
│   │   ├── __init__.py
│   │   └── *.py              # 数据模型定义
│   ├── tools/                # 工具函数目录
│   │   ├── __init__.py
│   │   └── *.py              # 工具函数定义
│   └── utils/                # 工具类目录
│       ├── __init__.py
│       └── *.py              # 工具类定义
├── .claude/                  # Claude Code配置目录
│   └── settings.local.json   # 本地配置文件
├── config.example.json       # 配置文件模板
├── config.json               # 实际配置文件
├── requirements.txt          # 依赖列表
├── INSTALL.md                # 安装指南
└── TROUBLESHOOTING.md        # 故障排除指南
```

### 2.2 目录说明

| 目录/文件 | 用途 |
|----------|------|
| `mcp_service/` | 主源码目录，包含所有业务逻辑 |
| `mcp_service/server.py` | MCP服务器主入口，负责启动服务和注册工具 |
| `mcp_service/models/` | 数据模型定义，用于描述API返回数据结构 |
| `mcp_service/tools/` | 工具函数实现，每个函数对应一个MCP工具 |
| `mcp_service/utils/` | 通用工具类，如API客户端、响应格式化器等 |
| `.claude/` | Claude Code配置目录 |
| `config.example.json` | 配置文件模板，供用户复制和修改 |
| `config.json` | 实际配置文件，包含敏感信息如API令牌 |
| `requirements.txt` | Python依赖列表 |
| `INSTALL.md` | 详细的安装和配置指南 |
| `TROUBLESHOOTING.md` | 常见问题和解决方案 |

## 3. 配置管理

### 3.1 配置文件设计

配置文件采用JSON格式，包含以下主要部分：

```json
{
  "service": {                    // 服务相关配置
    "token": "API_TOKEN",        // API令牌
    "base_url": "https://api.example.com"  // API基础URL
  },
  "server": {                     // 服务器相关配置
    "transport": "stdio",        // 传输方式（stdio/sse/http）
    "port": 3000,                 // 监听端口（仅SSE/HTTP模式）
    "host": "0.0.0.0",           // 监听地址（仅SSE/HTTP模式）
    "log_level": "CRITICAL"      // 日志级别
  }
}
```

### 3.2 配置加载机制

- 支持从JSON文件加载配置
- 支持从环境变量加载配置（优先级更高）
- 支持配置模板中的环境变量占位符（如 `$API_TOKEN`）

### 3.3 配置类实现

```python
import os
import json

class Config:
    def __init__(self):
        # 默认配置
        self.config = {
            "service": {
                "token": os.environ.get("SERVICE_TOKEN", ""),
                "base_url": "https://api.example.com"
            },
            "server": {
                "transport": "stdio",
                "port": 3000,
                "host": "0.0.0.0",
                "log_level": "CRITICAL"
            }
        }
        
        # 从配置文件加载
        config_path = os.path.join(project_root, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                # 合并配置
                # ...
    
    def get(self, key, default=None):
        # 获取配置值的方法
        # ...
```

## 4. 代码实现规范

### 4.1 服务器入口实现

#### 4.1.1 导入机制

实现双重导入机制，支持相对导入和绝对导入：

```python
# 导入项目内部模块
try:
    # 尝试相对导入（作为包运行时）
    from .utils.api_client import APIClient
except ImportError:
    # 尝试绝对导入（直接运行时）
    from mcp_service.utils.api_client import APIClient
```

#### 4.1.2 日志管理

- 配置详细的日志记录
- 支持不同日志级别
- 日志输出到文件，避免控制台污染
- 禁用第三方库的不必要日志

#### 4.1.3 工具注册

使用FastMCP装饰器注册工具：

```python
@mcp.tool()
async def tool_name(param1: type, param2: type = default) -> dict:
    """工具描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
    """
    # 工具实现
    # ...
```

### 4.2 API客户端实现

- 使用异步HTTP客户端（如httpx）
- 实现自动重试机制
- 统一错误处理
- 支持上下文管理器

### 4.3 响应格式化

- 统一的成功响应格式
- 统一的错误响应格式
- 包含错误代码和详细描述

## 5. 安装与部署流程

### 5.1 依赖管理

- 使用`requirements.txt`管理依赖
- 明确指定依赖版本
- 包含必要的开发依赖

### 5.2 安装脚本

- 提供Windows安装脚本（.ps1）
- 提供Linux/macOS安装脚本（.sh）
- 脚本包含环境检查、依赖安装、配置设置等步骤

### 5.3 配置流程

1. 复制配置文件模板：`cp config.example.json config.json`
2. 编辑配置文件，填写必要的配置项
3. 设置环境变量（可选）

## 6. Claude Code集成

### 6.1 项目级配置

创建`.mcp.json`文件，配置项目级MCP服务器：

```json
{
  "mcpServers": {
    "service-name": {
      "command": "python",
      "args": ["mcp_service/server.py"],
      "cwd": ".",
      "env": {
        "PYTHONPATH": "."
      },
      "transport": "stdio"
    }
  }
}
```

### 6.2 Claude Code配置

在`.claude/settings.local.json`中配置：

```json
{
  "enableAllProjectMcpServers": true,
  "mcpServers": {
    "service-name": {
      "command": "python",
      "args": ["mcp_service/server.py"],
      "cwd": ".",
      "env": {
        "PYTHONPATH": "."
      },
      "transport": "stdio"
    }
  }
}
```

### 6.3 全局配置

使用`claude mcp add`命令添加全局配置：

```bash
claude mcp add --scope user --transport stdio service-name "python" -- "path/to/server.py" --env PYTHONPATH="path/to/project"
```

## 7. 测试与验证

### 7.1 API客户端测试

创建测试脚本验证API客户端功能：

```python
# test_api_client.py
import asyncio
from mcp_service.utils.api_client import APIClient

async def main():
    # 测试API客户端
    token = "test_token"
    async with APIClient(token) as client:
        # 测试API调用
        result = await client.some_api_call()
        print("API调用结果:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

### 7.2 服务器启动测试

```bash
python mcp_service/server.py --show-banner
```

### 7.3 Claude Code集成测试

```bash
claude mcp list
```

## 8. 故障排除

### 8.1 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 模块导入错误 | 导入路径配置问题 | 实现双重导入机制 |
| API调用失败 | 配置错误或网络问题 | 检查配置文件和网络连接 |
| MCP服务器连接失败 | 配置错误或服务器未启动 | 检查配置文件和服务器状态 |
| 日志输出过多 | 日志级别设置不当 | 将日志级别设置为CRITICAL |

### 8.2 诊断工具

- 使用`claude mcp list`查看MCP服务器状态
- 检查日志文件获取详细错误信息
- 使用API客户端测试脚本验证API连接

## 9. 最佳实践

### 9.1 代码质量

- 遵循PEP 8代码风格指南
- 实现完整的类型注解
- 编写详细的文档字符串
- 使用异步编程提高性能

### 9.2 安全性

- 敏感配置（如API令牌）不硬编码到代码中
- 使用环境变量或配置文件管理敏感信息
- 配置文件模板不包含实际敏感数据

### 9.3 可维护性

- 模块化设计，分离关注点
- 统一的错误处理机制
- 详细的日志记录
- 完整的测试用例

### 9.4 易用性

- 提供详细的安装和配置指南
- 提供示例配置文件
- 实现自动配置检测
- 提供故障排除指南

## 10. 版本控制

- 使用Git进行版本控制
- 遵循语义化版本规范
- 定期更新依赖
- 维护CHANGELOG

## 11. 文档管理

- 维护详细的README.md文件
- 提供完整的API文档
- 维护安装和配置指南
- 维护故障排除指南

## 12. 总结

本规范文档定义了创建和配置MCP服务的标准流程和最佳实践。遵循本规范可以确保MCP服务具有良好的可维护性、可扩展性和易用性。

在实际应用中，应根据具体的业务需求和技术栈进行适当调整，但核心原则和架构设计应保持一致。