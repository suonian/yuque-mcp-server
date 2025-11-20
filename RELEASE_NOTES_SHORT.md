# 🚀 语雀 MCP 代理服务器 v1.0.0

**发布日期**: 2025-11-19

---

## 🎉 首次发布

语雀 Model Context Protocol (MCP) 代理服务器，让 AI 助手能够通过 MCP 协议与语雀平台交互。

---

## ✨ 主要特性

- 🔌 **完整的 MCP 协议支持** - 兼容 MCP 2024-11-05
- 🌐 **多客户端兼容** - 支持 Chatbox、Claude Desktop、Cherry Studio 等
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

## 📝 完整发布说明

查看 [RELEASE_NOTES.md](RELEASE_NOTES.md) 获取完整的发布说明。

---

**下载**: [v1.0.0](https://github.com/suonian/yuque-mcp-server/releases/tag/v1.0.0)

