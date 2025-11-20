# 语雀 MCP 代理服务器

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

语雀 Model Context Protocol (MCP) 代理服务器，让 AI 助手能够通过 MCP 协议与语雀平台交互。

**兼容性**: 支持所有符合 MCP 标准的客户端，包括 Chatbox、Claude Desktop、Cherry Studio、Cursor 等主流工具。

## ✨ 功能特性

- 🔌 **MCP 协议支持** - 完全兼容 Model Context Protocol 2024-11-05
- 🌐 **多客户端支持** - 支持 Chatbox、Claude Desktop、Cherry Studio、Cursor 等主流工具
- 🪟 **跨平台支持** - 支持 macOS、Linux 和 Windows 系统
- 📚 **知识库管理** - 创建、读取、更新、删除知识库
- 📄 **文档管理** - 完整的文档 CRUD 操作
- 🔍 **搜索功能** - 全文搜索、高级搜索
- 👥 **用户管理** - 获取用户信息、团队管理
- 🔐 **安全配置** - 支持 HTTP Header 和环境变量配置 Token
- 🚀 **自动启动** - 支持系统服务自动启动（macOS launchd / Windows Service）

## 📋 支持的工具

### 用户相关
- `get_user_info` - 获取当前用户信息
- `get_user` - 获取指定用户信息

### 知识库管理
- `list_repos` - 列出所有知识库
- `list_user_repos` - 列出指定用户的知识库
- `get_repo` - 获取知识库详情
- `create_repo` - 创建知识库
- `update_repo` - 更新知识库信息
- `delete_repo` - 删除知识库
- `get_repo_toc` - 获取知识库目录
- `update_repo_toc` - 更新知识库目录

### 文档管理
- `list_docs` - 列出知识库中的文档
- `get_doc` - 获取文档内容（自动获取知识库信息，包含完整元数据）
- `get_doc_by_id` - 通过文档ID获取文档（提供友好错误提示）
- `create_doc` - 创建文档
- `update_doc` - 更新文档
- `delete_doc` - 删除文档
- `list_doc_versions` - 列出文档版本历史

### 搜索功能
- `search_docs` - 搜索文档（返回完整路径信息，可直接用于获取文档）
- `get_doc_by_id` - 通过文档ID获取文档（提供友好错误提示和使用建议）

### 团队管理（需要团队权限）
- `list_groups` - 列出团队
- `get_group` - 获取团队信息
- `list_group_users` - 列出团队成员
- `list_group_repos` - 列出团队知识库
- ... 等更多功能

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/your-username/yuque-mcpserver.git
cd yuque-mcpserver

# 2. 设置 Token
export YUQUE_TOKEN=your-token-here

# 3. 启动服务
docker-compose up -d

# 4. 验证服务
curl http://localhost:3000/health

# 5. 运行自动化测试
./docker-test.sh
```

### 方式二：本地部署

#### 1. 克隆项目

```bash
git clone https://github.com/your-username/yuque-mcpserver.git
cd yuque-mcpserver
```

#### 2. 配置 Token

#### 方式一：配置文件（推荐）

```bash
# 复制配置示例文件
cp yuque-config.env.example yuque-config.env

# 编辑配置文件，填入您的语雀 Token
nano yuque-config.env
```

#### 方式二：环境变量

```bash
export YUQUE_TOKEN="your-token-here"
```

#### 方式三：HTTP Header（Chatbox 配置）

在 Chatbox 的 MCP Server 配置中，HTTP Header 字段添加：
```
X-Yuque-Token=your-token-here
```

**获取 Token**：语雀设置 > 个人设置 > Token

### 3. 启动服务

```bash
# 启动服务
./start_server.sh start

# 查看状态
./start_server.sh status
```

### 4. 验证服务

```bash
# 健康检查
curl http://localhost:3000/health
```

## 📝 常用命令

```bash
# 启动服务
./start_server.sh start

# 停止服务
./start_server.sh stop

# 重启服务
./start_server.sh restart

# 查看状态
./start_server.sh status

# 查看日志
./start_server.sh logs

# 管理配置
./start_server.sh config

# 安装系统服务（macOS，可选）
./install_service.sh
```

## ⚙️ 配置说明

### 配置文件格式

`yuque-config.env`:

```bash
# 语雀 Token（必需）
YUQUE_TOKEN=your-token-here

# 服务端口（可选，默认 3000）
PORT=3000
```

### 配置优先级

1. **HTTP Header** (`X-Yuque-Token`) - 最高优先级
2. **环境变量** (`YUQUE_TOKEN`)
3. **配置文件** (`yuque-config.env`)

如果都未配置，系统会返回明确的错误提示。

## 🔧 系统服务（macOS）

如果您希望服务在系统启动时自动运行：

```bash
./install_service.sh
```

安装后，服务会在开机时自动启动，无需手动操作。

### 服务管理

```bash
# 启动服务
launchctl start com.yuque.mcp

# 停止服务
launchctl stop com.yuque.mcp

# 查看状态
launchctl list | grep com.yuque.mcp
```

## 📚 文档

详细文档请查看 `docs/` 目录：

### 快速开始
- [`docs/QUICK_START.md`](docs/QUICK_START.md) - 快速开始指南
- [`docs/CONFIG_GUIDE.md`](docs/CONFIG_GUIDE.md) - 配置指南

### 部署指南
- [`docs/DOCKER_DEPLOYMENT.md`](docs/DOCKER_DEPLOYMENT.md) - **Docker 部署指南**（推荐）
- [`docs/AUTO_START_GUIDE.md`](docs/AUTO_START_GUIDE.md) - 自动启动指南（macOS）
- [`docs/WINDOWS_DEPLOYMENT.md`](docs/WINDOWS_DEPLOYMENT.md) - Windows 部署指南

### 使用指南
- [`docs/CLIENT_COMPATIBILITY.md`](docs/CLIENT_COMPATIBILITY.md) - **客户端兼容性指南**（多工具配置）
- [`docs/YUQUE_API_REFERENCE.md`](docs/YUQUE_API_REFERENCE.md) - **语雀 API 接口文档**（OpenAPI 规范）

### 故障排查
如遇到问题，请查看相关文档或提交 Issue。

## 🔒 安全提示

- ✅ 配置文件 `yuque-config.env` 已添加到 `.gitignore`，不会被提交到代码仓库
- ✅ 文件权限已设置为 600（仅所有者可读写）
- ⚠️ 请勿将 Token 提交到代码仓库
- ⚠️ 定期轮换 Token，确保安全

## 🐛 故障排查

### 服务无法启动

```bash
# 查看日志
./start_server.sh logs

# 或直接查看
tail -f /tmp/yuque-proxy.log
```

### Token 配置问题

```bash
# 检查配置
./start_server.sh config

# 验证 Token
curl -H "X-Yuque-Token: your-token" http://localhost:3000/health
```

### 端口被占用

```bash
# 检查端口占用
lsof -i :3000

# 修改端口（在 yuque-config.env 中设置 PORT）
```

## 📊 API 端点

- `POST /mcp` - MCP 协议端点
- `GET /health` - 健康检查
- `GET /test` - 测试端点

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [语雀 Open API](https://www.yuque.com/yuque/developer/api)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**提示**: 所有操作都在项目根目录中执行。
