# 语雀 MCP 代理服务器

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.2-blue.svg)](https://github.com/suonian/yuque-mcp-server/releases/tag/v1.2.2)

语雀 Model Context Protocol (MCP) 代理服务器，让 AI 助手能够通过 MCP 协议与语雀平台交互。

**技术栈**: Python 3.7+, Flask/FastAPI, Redis/内存缓存, httpx

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
- 📦 **缓存机制** - 支持 Redis 和内存缓存，减少 API 调用次数
- ⚡ **异步框架** - 支持 FastAPI 和 httpx，提高并发处理能力
- 🎯 **智能启动** - 支持按需启动，自动检测服务状态
- 🔄 **自动降级** - Redis 不可用时自动切换到内存缓存
- 📊 **缓存统计** - 支持查看缓存命中次数和命中率

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
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server

# 2. 设置 Token
export YUQUE_TOKEN=your-token-here

# 3. 启动服务
docker-compose up -d

# 4. 验证服务
curl http://localhost:3000/health
```

### 方式二：一键安装（推荐）

#### 1. 克隆项目

```bash
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server
```

#### 2. 运行一键安装脚本

```bash
# Linux/macOS
python3 install.py

# Windows
python install.py
```

#### 3. 安装选项

```bash
# 强制更新配置文件
python3 install.py --force

# 安装系统服务（需要管理员权限）
python3 install.py --service

# 安装完成后自动启动服务器
python3 install.py --start

# 组合选项
python3 install.py --service --start
```

### 方式三：本地部署

#### 1. 克隆项目

```bash
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server
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

#### 方式一：同步启动（默认）

```bash
# 启动服务
./start_server.sh start

# 查看状态
./start_server.sh status
```

#### 方式二：异步启动（推荐，性能更好）

```bash
# 使用启动脚本启动异步服务
./start_server.sh --async start

# 或直接使用 uvicorn 启动
uvicorn app_async:app --host 0.0.0.0 --port 3000

# 查看状态
./start_server.sh status
```

#### 方式三：自动启动模式

```bash
# 启动自动启动服务
./start_server.sh --auto start
```

### 4. 验证服务

```bash
# 健康检查
curl http://localhost:3000/health
```

## 📝 常用命令

### 基本命令

```bash
# 启动服务（默认同步模式）
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

### 异步模式命令

```bash
# 启动异步服务
./start_server.sh --async start

# 停止异步服务
./start_server.sh --async stop

# 重启异步服务
./start_server.sh --async restart

# 查看异步服务状态
./start_server.sh --async status
```

### 自动启动模式命令

```bash
# 启动自动启动服务
./start_server.sh --auto start

# 停止自动启动服务
./start_server.sh --auto stop

# 重启自动启动服务
./start_server.sh --auto restart
```

## ⚙️ 配置说明

### 配置文件格式

`yuque-config.env`:

```bash
# 语雀 Token（必需）
YUQUE_TOKEN=your-token-here

# 服务端口（可选，默认 3000）
PORT=3000

# Redis URL（可选，默认 redis://localhost:6379/0）
# REDIS_URL=redis://localhost:6379/0

# 缓存过期时间（秒，可选，默认根据 API 类型自动设置）
# CACHE_EXPIRE=3600

# 服务模式（可选，默认 sync，可选值：sync, async, auto）
# SERVICE_MODE=async
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

## 📋 最新变更

### Version 1.2.1（2025-11-29）

#### ✨ 新增功能

- **缓存机制实现**
  - 支持 Redis 和内存缓存两种模式
  - 为不同类型的 API 请求设置不同的过期时间
  - 自动降级机制，Redis 不可用时自动切换到内存缓存
  - 缓存统计功能，支持查看命中次数和命中率

- **异步框架集成**
  - 使用 FastAPI 和 httpx 实现异步 API 调用
  - 创建了异步版本的 API 客户端 `async_yuque_client.py`
  - 支持异步 Web 服务 `app_async.py`
  - 提高了系统的并发处理能力和响应速度

- **自动启动功能**
  - 实现了自动启动包装器 `auto_start_server.py`
  - 支持系统服务自动启动
  - 智能检测服务状态，按需启动
  - 支持多种启动模式：启动脚本、系统服务、自动启动包装器

#### 🔧 改进

- **项目结构优化**
  - 符合 GitHub 发布标准
  - 清晰的文件组织结构
  - 完整的 README 文档
  - 适当的许可证文件

- **文档更新**
  - 更新了所有文档，确保内容完整准确
  - 添加了 AUTO_START_GUIDE.md 自动启动指南
  - 更新了 DOCKER_DEPLOYMENT.md Docker 部署指南
  - 更新了 WINDOWS_DEPLOYMENT.md Windows 部署指南

- **启动脚本增强**
  - 支持三种启动模式：异步、同步、自动
  - 增强了命令行选项
  - 改进了日志管理

#### 🐛 修复

- 修复了 GitHub Actions 测试配置
- 修复了各种 bug 和配置问题
- 修复了 Windows 部署指南中的脚本路径错误
- 修复了 Dockerfile 中的脚本路径错误

#### 📦 依赖更新

- 添加了 fastapi>=0.100.0
- 添加了 uvicorn>=0.22.0
- 添加了 httpx>=0.24.0
- 添加了 redis>=5.0.0

[查看完整更新日志](./CHANGELOG.md)

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

## ❓ 常见问题解答(FAQ)

### 缓存相关问题

#### Q: 缓存机制是如何工作的？
A: 系统支持 Redis 和内存缓存两种模式。当 Redis 可用时，系统会使用 Redis 作为缓存存储；当 Redis 不可用时，系统会自动切换到内存缓存。对于不同类型的 API 请求，系统会设置不同的过期时间。

#### Q: 如何查看缓存统计信息？
A: 您可以通过异步服务的健康检查端点查看缓存统计信息，或者查看日志输出。

#### Q: 如何清除缓存？
A: 您可以重启服务来清除缓存，或者直接操作 Redis 清除缓存。

### 异步框架相关问题

#### Q: 异步模式和同步模式有什么区别？
A: 异步模式使用 FastAPI 和 httpx，具有更高的并发处理能力和响应速度，适合高并发场景；同步模式使用 Flask 和 requests，适合简单场景和调试。

#### Q: 如何切换到异步模式？
A: 您可以使用 `./start_server.sh --async start` 命令启动异步服务，或者直接使用 uvicorn 启动 `app_async:app`。

#### Q: 异步模式需要额外配置吗？
A: 不需要，异步模式使用与同步模式相同的配置文件和环境变量。

### 自动启动相关问题

#### Q: 自动启动功能是如何工作的？
A: 自动启动功能会智能检测服务状态，当服务未运行时自动启动服务。您可以使用 `./start_server.sh --auto start` 命令启动自动启动服务。

#### Q: 如何配置自动启动服务？
A: 您可以在配置文件中设置 `SERVICE_MODE=auto`，或者使用 `--auto` 命令行选项。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献流程

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

### 代码规范

- 遵循 PEP 8 代码风格
- 编写清晰的注释
- 确保所有测试通过
- 提交信息要清晰明了

### 测试要求

- 确保新功能有相应的测试用例
- 确保所有现有测试通过
- 运行 `python3 -m unittest discover tests` 进行测试

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

## 📄 许可证

MIT License

## 🙏 致谢

- [语雀 Open API](https://www.yuque.com/yuque/developer/api)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

**提示**: 所有操作都在项目根目录中执行。
