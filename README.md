# 语雀 MCP 服务器

<div align="center">

**让 AI 助手通过 MCP 协议访问语雀知识库**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![MCP Standard](https://img.shields.io/badge/MCP-2024--11--05-green.svg)](https://modelcontextprotocol.io/)

</div>

## 简介

语雀 MCP 服务器是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的代理服务器，让 AI 助手（如 Claude、Chatbox、Cursor 等）能够直接访问和操作语雀平台的内容。

## 功能特性

- 完全兼容 MCP 2024-11-05 标准
- 支持 Claude Code、Chatbox、Cursor 等主流 AI 工具
- 提供完整的语雀 API 功能
- 支持环境变量和配置文件双重配置
- 支持 stdio 和 SSE 两种传输模式
- 内置缓存优化，减少 API 调用
- 跨平台支持（Windows / macOS / Linux）

## 支持的工具

| 工具 | 描述 |
|------|------|
| `get_user_info` | 获取当前用户信息 |
| `list_repos` | 列出当前用户的知识库 |
| `get_repo` | 获取知识库详情 |
| `list_docs` | 列出知识库中的文档 |
| `get_doc` | 获取文档详情 |
| `create_doc` | 创建文档 |
| `update_doc` | 更新文档 |
| `delete_doc` | 删除文档 |
| `search` | 搜索文档或知识库 |

## 快速开始

### 1. 安装

```bash
# 克隆项目
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

#### 方式一：环境变量（推荐）

```bash
# Windows
setx YUQUE_TOKEN "你的语雀token"

# macOS / Linux
export YUQUE_TOKEN="你的语雀token"
```

#### 方式二：配置文件

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑 config.json，填入你的 token
```

### 3. 获取 Token

1. 登录 [语雀官网](https://www.yuque.com)
2. 进入「个人设置」>「Token」
3. 点击「生成新 Token」并复制

### 4. 运行

```bash
# stdio 模式（用于 Claude Code 等）
python -m yuque_mcp.server

# SSE 模式（HTTP 服务器）
python -m yuque_mcp.server --transport sse --port 3000
```

## 配置 Claude Code

在 Claude Code 的设置文件中添加：

```json
{
  "mcpServers": {
    "yuque": {
      "command": "python",
      "args": ["-m", "yuque_mcp.server"],
      "env": {
        "YUQUE_TOKEN": "你的token"
      }
    }
  }
}
```

## 使用示例

```
/mcp call yuque.get_user_info
/mcp call yuque.list_repos limit=10
/mcp call yuque.list_docs namespace="username/repo"
/mcp call yuque.get_doc namespace="username/repo" slug="doc-slug"
/mcp call yuque.create_doc namespace="username/repo" title="标题" body="# 内容"
/mcp call yuque.search q="搜索关键词"
```

## 项目结构

```
yuque-mcp-server/
├── yuque_mcp/
│   ├── __init__.py
│   ├── server.py          # MCP 服务器主文件
│   ├── models/            # 数据模型
│   ├── tools/             # 工具函数
│   └── utils/
│       ├── api_client.py  # 语雀 API 客户端
│       └── response_formatter.py
├── config.example.json    # 配置模板
├── requirements.txt       # Python 依赖
├── README.md              # 项目说明
└── LICENSE                # MIT 许可证
```

## 系统要求

- Python 3.7 或更高版本
- pip 20.0 或更高版本
- 网络连接到语雀 API

## 命令行参数

| 参数 | 描述 | 默认值 |
|------|------|--------|
| `--transport` | 传输方式 (stdio/sse) | stdio |
| `--port` | 监听端口（SSE 模式） | 3000 |
| `--host` | 监听地址（SSE 模式） | 0.0.0.0 |
| `--log-level` | 日志级别 | CRITICAL |
| `--show-banner` | 显示启动横幅 | False |

## 依赖项

- `fastmcp` - MCP 协议实现
- `httpx` - 异步 HTTP 客户端
- `pydantic` - 数据验证
- `python-dotenv` - 环境变量管理
- `cachetools` - 缓存工具

## 故障排除

详见 [故障排除文档](INSTALL.md#常见问题)。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 作者

[suonian](https://github.com/suonian)

## 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [语雀 API](https://www.yuque.com/yuque/developer)
