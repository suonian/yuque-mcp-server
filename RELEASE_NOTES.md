# 🚀 语雀 MCP 代理服务器 v1.0.0

**发布日期**: 2025-11-19  
**仓库地址**: https://github.com/suonian/yuque-mcp-server

---

## 🎉 首次发布

这是语雀 Model Context Protocol (MCP) 代理服务器的首个正式版本。该项目实现了完整的 MCP 协议，让 AI 助手能够通过标准化的 MCP 协议与语雀平台进行交互。

---

## ✨ 核心特性

### 🔌 MCP 协议支持
- ✅ 完全兼容 **Model Context Protocol 2024-11-05**
- ✅ 标准 JSON-RPC 2.0 协议
- ✅ 支持所有标准 MCP 方法
- ✅ CORS 跨域支持

### 🌐 多客户端兼容
- ✅ **Chatbox** - 已验证支持
- ✅ **Claude Desktop** - 支持（需配置）
- ✅ **Cherry Studio** - 支持（需配置）
- ✅ **Cursor** - 支持（需配置）
- ✅ 所有符合 MCP 标准的客户端

### 🪟 跨平台支持
- ✅ **macOS** - 完整支持（启动脚本 + 系统服务）
- ✅ **Linux** - 完整支持（启动脚本）
- ✅ **Windows** - 完整支持（批处理 + PowerShell）

### 🐳 Docker 部署
- ✅ 一键部署，无需配置 Python 环境
- ✅ Docker Compose 支持
- ✅ 自动化测试脚本
- ✅ 健康检查机制

### 📚 语雀 API 功能

支持 **29+ 个语雀 API 工具**：

#### 用户管理
- `get_user_info` - 获取当前用户信息
- `get_user` - 获取指定用户信息

#### 知识库管理
- `list_repos` - 列出所有知识库
- `list_user_repos` - 列出指定用户的知识库
- `get_repo` - 获取知识库详情
- `create_repo` - 创建知识库
- `update_repo` - 更新知识库信息
- `delete_repo` - 删除知识库
- `get_repo_toc` - 获取知识库目录
- `update_repo_toc` - 更新知识库目录

#### 文档管理
- `list_docs` - 列出知识库中的文档
- `get_doc` - 获取文档内容
- `create_doc` - 创建文档
- `update_doc` - 更新文档
- `delete_doc` - 删除文档
- `list_doc_versions` - 列出文档版本历史

#### 搜索功能
- `search_docs` - 搜索文档

#### 团队管理（需要团队权限）
- `list_groups` - 列出团队
- `get_group` - 获取团队信息
- `list_group_users` - 列出团队成员
- `list_group_repos` - 列出团队知识库
- `update_group_member` - 变更团队成员角色
- `remove_group_member` - 删除团队成员
- `get_group_statistics` - 团队汇总统计
- `get_group_member_stats` - 团队成员统计
- `get_group_book_stats` - 团队知识库统计
- `get_group_doc_stats` - 团队文档统计

---

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 1. 克隆仓库
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server

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

```bash
# 1. 克隆仓库
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置 Token
cp yuque-config.env.example yuque-config.env
# 编辑 yuque-config.env，填入您的 Token

# 4. 启动服务
./start_server.sh start  # Linux/macOS
# 或
start_server.bat start    # Windows
```

---

## 📋 系统要求

- **Python**: 3.7 或更高版本
- **Docker**: 20.10+（如果使用 Docker 部署）
- **操作系统**: macOS 10.14+, Linux, Windows 10/11
- **网络**: 能够访问 `https://www.yuque.com`

---

## ⚙️ 配置说明

### Token 配置方式

支持三种配置方式（按优先级）：

1. **HTTP Header** (`X-Yuque-Token`) - 推荐用于 Chatbox
2. **环境变量** (`YUQUE_TOKEN`) - 推荐用于服务器部署
3. **配置文件** (`yuque-config.env`) - 推荐用于本地开发

### 获取 Token

1. 访问 [语雀设置](https://www.yuque.com/settings)
2. 进入 **个人设置** → **Token**
3. 生成新的 Token

---

## 📚 文档

完整的文档请查看 `docs/` 目录：

- [`QUICK_START.md`](docs/QUICK_START.md) - 快速开始指南
- [`CONFIG_GUIDE.md`](docs/CONFIG_GUIDE.md) - 配置指南
- [`DOCKER_DEPLOYMENT.md`](docs/DOCKER_DEPLOYMENT.md) - Docker 部署指南
- [`AUTO_START_GUIDE.md`](docs/AUTO_START_GUIDE.md) - 自动启动指南（macOS）
- [`WINDOWS_DEPLOYMENT.md`](docs/WINDOWS_DEPLOYMENT.md) - Windows 部署指南
- [`CLIENT_COMPATIBILITY.md`](docs/CLIENT_COMPATIBILITY.md) - 客户端兼容性指南
- [`YUQUE_API_REFERENCE.md`](docs/YUQUE_API_REFERENCE.md) - 语雀 API 接口文档

---

## 🧪 测试

项目提供了自动化测试脚本：

```bash
# Docker 测试
export YUQUE_TOKEN=your-token-here
./docker-test.sh
# 或
python3 docker-test.py
```

测试覆盖：
- ✅ 健康检查端点
- ✅ MCP 协议初始化
- ✅ 工具列表获取
- ✅ 用户信息获取
- ✅ 知识库列表
- ✅ CORS 支持
- ✅ 错误处理

---

## 🔒 安全提示

- ✅ 配置文件 `yuque-config.env` 已添加到 `.gitignore`
- ✅ 无硬编码 Token
- ✅ 支持通过 HTTP Header 传递 Token（更安全）
- ⚠️ 请勿将 Token 提交到代码仓库
- ⚠️ 定期轮换 Token

---

## 🛠️ 技术栈

- **语言**: Python 3.7+
- **框架**: Flask
- **协议**: Model Context Protocol 2024-11-05
- **API**: 语雀 Open API v2
- **部署**: Docker, Docker Compose

---

## 📦 文件结构

```
yuque-mcpserver/
├── yuque-proxy.js              # 主程序
├── requirements.txt            # Python 依赖
├── Dockerfile                   # Docker 镜像构建
├── docker-compose.yml           # Docker Compose 配置
├── start_server.sh              # Linux/macOS 启动脚本
├── start_server.bat             # Windows 批处理脚本
├── start_server.ps1            # Windows PowerShell 脚本
├── docker-test.sh              # Docker 测试脚本
├── docker-test.py              # Docker 测试脚本（Python）
├── README.md                   # 主 README
└── docs/                       # 详细文档
    ├── QUICK_START.md
    ├── CONFIG_GUIDE.md
    ├── DOCKER_DEPLOYMENT.md
    └── ...
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献方式

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

本项目采用 MIT License。详见 [LICENSE](LICENSE) 文件。

---

## 🙏 致谢

- [语雀 Open API](https://www.yuque.com/yuque/developer/api) - 提供强大的 API 支持
- [Model Context Protocol](https://modelcontextprotocol.io/) - 标准化的 MCP 协议
- 所有贡献者和用户

---

## 🔗 相关链接

- **GitHub 仓库**: https://github.com/suonian/yuque-mcp-server
- **语雀 API 文档**: https://www.yuque.com/yuque/developer/api
- **MCP 协议规范**: https://spec.modelcontextprotocol.io/

---

## 📝 更新日志

### v1.0.0 (2025-11-19)

#### ✨ 新增功能
- 完整的 MCP 协议实现（2024-11-05）
- 支持 29+ 个语雀 API 工具
- Docker 部署支持
- 跨平台支持（macOS/Linux/Windows）
- 自动化测试脚本
- 完整的文档

#### 🔧 技术特性
- 动态 Token 配置（HTTP Header + 环境变量）
- 相对路径支持（无硬编码路径）
- CORS 跨域支持
- 健康检查机制
- 错误处理完善

#### 📚 文档
- 8 个详细文档
- 语雀 API 接口文档
- 客户端兼容性指南
- Docker 部署指南
- Windows 部署指南

---

## 🐛 已知问题

- 部分团队功能需要团队权限才能使用
- Windows 系统服务需要使用 NSSM 或 Windows Service Manager

---

## 🚧 未来计划

- [ ] 支持更多语雀 API 功能
- [ ] 添加 Webhook 支持
- [ ] 性能优化
- [ ] 更多客户端兼容性测试
- [ ] CI/CD 自动化

---

## 📞 支持

如有问题或建议，请：
- 提交 [Issue](https://github.com/suonian/yuque-mcp-server/issues)
- 查看 [文档](docs/)
- 查看 [故障排查指南](TROUBLESHOOTING.md)

---

**感谢使用语雀 MCP 代理服务器！** 🎉

---

**下载**: [v1.0.0](https://github.com/suonian/yuque-mcp-server/releases/tag/v1.0.0) | [完整变更日志](CHANGELOG.md)

