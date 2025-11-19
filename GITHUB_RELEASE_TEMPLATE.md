# 🚀 语雀 MCP 代理服务器 v1.0.0

**发布日期**: 2025-11-19

---

## 🎉 首次发布

语雀 Model Context Protocol (MCP) 代理服务器，让 AI 助手能够通过 MCP 协议与语雀平台交互。

---

## ✨ 主要特性

- 🔌 **完整的 MCP 协议支持** - 兼容 MCP 2024-11-05
- 🌐 **多客户端兼容** - 支持 Chatbox、Claude Desktop、Cherry Studio、Cursor 等
- 🪟 **跨平台支持** - macOS、Linux、Windows
- 🐳 **Docker 部署** - 一键部署，无需配置环境
- 📚 **29+ 个语雀 API 工具** - 用户、知识库、文档、搜索、团队管理

---

## 🚀 快速开始

### Docker 部署（推荐）

```bash
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server
export YUQUE_TOKEN=your-token-here
docker-compose up -d
```

### 本地部署

```bash
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server
pip install -r requirements.txt
cp yuque-config.env.example yuque-config.env
# 编辑 yuque-config.env，填入您的 Token
./start_server.sh start
```

---

## 📋 系统要求

- Python 3.7+ 或 Docker 20.10+
- 语雀 API Token

---

## 📚 文档

- [快速开始](docs/QUICK_START.md)
- [Docker 部署指南](docs/DOCKER_DEPLOYMENT.md)
- [配置指南](docs/CONFIG_GUIDE.md)
- [客户端兼容性](docs/CLIENT_COMPATIBILITY.md)

---

## 🔗 相关链接

- **GitHub**: https://github.com/suonian/yuque-mcp-server
- **语雀 API**: https://www.yuque.com/yuque/developer/api
- **MCP 协议**: https://modelcontextprotocol.io/

---

## 📝 完整功能列表

### 用户管理
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
- `get_doc` - 获取文档内容
- `create_doc` - 创建文档
- `update_doc` - 更新文档
- `delete_doc` - 删除文档
- `list_doc_versions` - 列出文档版本历史

### 搜索功能
- `search_docs` - 搜索文档

### 团队管理（需要团队权限）
- `list_groups` - 列出团队
- `get_group` - 获取团队信息
- `list_group_users` - 列出团队成员
- `list_group_repos` - 列出团队知识库
- 等更多功能...

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

