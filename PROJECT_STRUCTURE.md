# 📁 项目结构说明

本文档说明项目的文件结构和各文件的作用。

---

## 📂 目录结构

```
yuque-mcpserver/
├── 📄 核心文件
│   ├── yuque-proxy.js              # 主程序（Flask 服务器）
│   ├── requirements.txt            # Python 依赖列表
│   ├── Dockerfile                   # Docker 镜像构建文件
│   ├── docker-compose.yml           # Docker Compose 配置
│   ├── .dockerignore               # Docker 构建忽略规则
│   └── .gitignore                  # Git 忽略规则
│
├── 🚀 启动脚本
│   ├── start_server.sh             # Linux/macOS 启动脚本
│   ├── start_server.bat            # Windows 批处理脚本
│   ├── start_server.ps1            # Windows PowerShell 脚本
│   └── auto_start_server.py        # Python 自动启动包装器
│
├── 🔧 系统服务（可选）
│   ├── install_service.sh          # macOS 服务安装脚本
│   └── com.yuque.mcp.plist         # macOS launchd 配置
│
├── 🐳 Docker 测试
│   ├── docker-test.sh              # Bash 自动化测试脚本
│   └── docker-test.py              # Python 自动化测试脚本
│
├── ⚙️ 配置文件
│   ├── yuque-config.env.example    # 配置文件模板（可提交）
│   └── yuque-config.env            # 实际配置文件（已排除，需用户创建）
│
├── 📚 文档
│   ├── README.md                    # 主 README（GitHub 首页）
│   ├── GITHUB_RELEASE_CHECKLIST.md # GitHub 发布检查清单
│   ├── PROJECT_STRUCTURE.md        # 本文件
│   └── docs/                       # 详细文档目录
│       ├── QUICK_START.md          # 快速开始指南
│       ├── CONFIG_GUIDE.md         # 配置指南
│       ├── DOCKER_DEPLOYMENT.md    # Docker 部署指南
│       ├── AUTO_START_GUIDE.md     # 自动启动指南（macOS）
│       ├── WINDOWS_DEPLOYMENT.md   # Windows 部署指南
│       ├── CLIENT_COMPATIBILITY.md # 客户端兼容性指南
│       ├── YUQUE_API_REFERENCE.md  # 语雀 API 接口文档
│       └── README_AUTO_START.md    # 自动启动快速参考
│
└── 📝 其他
    └── (临时文件、日志等已排除)
```

---

## 📄 文件说明

### 核心文件

| 文件 | 说明 | 必需 |
|------|------|------|
| `yuque-proxy.js` | Flask 主程序，实现 MCP 协议和语雀 API 封装 | ✅ |
| `requirements.txt` | Python 依赖列表（flask, requests） | ✅ |
| `Dockerfile` | Docker 镜像构建文件 | ⚠️ Docker 部署需要 |
| `docker-compose.yml` | Docker Compose 配置 | ⚠️ Docker 部署需要 |
| `.dockerignore` | Docker 构建时忽略的文件 | ⚠️ Docker 部署需要 |
| `.gitignore` | Git 版本控制忽略规则 | ✅ |

### 启动脚本

| 文件 | 平台 | 说明 |
|------|------|------|
| `start_server.sh` | Linux/macOS | Bash 启动脚本，支持 start/stop/restart/status/logs/config |
| `start_server.bat` | Windows | 批处理启动脚本，基本功能 |
| `start_server.ps1` | Windows | PowerShell 启动脚本，功能更完整 |
| `auto_start_server.py` | 跨平台 | Python 自动启动包装器，可集成到其他脚本 |

### 系统服务（可选）

| 文件 | 平台 | 说明 |
|------|------|------|
| `install_service.sh` | macOS | 安装 launchd 系统服务 |
| `com.yuque.mcp.plist` | macOS | launchd 服务配置文件（使用占位符） |

### Docker 测试

| 文件 | 说明 |
|------|------|
| `docker-test.sh` | Bash 自动化测试脚本，测试所有 MCP 功能 |
| `docker-test.py` | Python 自动化测试脚本，功能相同但错误处理更好 |

### 配置文件

| 文件 | 说明 | Git 状态 |
|------|------|----------|
| `yuque-config.env.example` | 配置文件模板，包含示例和说明 | ✅ 可提交 |
| `yuque-config.env` | 实际配置文件，包含真实 Token | ❌ 已排除 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `README.md` | 主 README，GitHub 首页显示 |
| `GITHUB_RELEASE_CHECKLIST.md` | GitHub 发布检查清单 |
| `PROJECT_STRUCTURE.md` | 项目结构说明（本文件） |
| `docs/QUICK_START.md` | 快速开始指南 |
| `docs/CONFIG_GUIDE.md` | 配置指南（HTTP Header + 环境变量） |
| `docs/DOCKER_DEPLOYMENT.md` | Docker 部署完整指南 |
| `docs/AUTO_START_GUIDE.md` | macOS 自动启动详细指南 |
| `docs/WINDOWS_DEPLOYMENT.md` | Windows 部署完整指南 |
| `docs/CLIENT_COMPATIBILITY.md` | 客户端兼容性指南（多工具配置） |
| `docs/YUQUE_API_REFERENCE.md` | 语雀 API 接口文档（OpenAPI 规范） |
| `docs/README_AUTO_START.md` | 自动启动功能快速参考 |

---

## 🗑️ 已删除的文件

以下文件已从项目中删除，因为它们对 GitHub 用户不必要：

- ❌ `MIGRATION.md` - 迁移说明（内部文档）
- ❌ `VERIFICATION_REPORT.md` - 验证报告（内部文档）
- ❌ `PROJECT_CHECK_REPORT.md` - 项目检查报告（内部文档）
- ❌ `README_WINDOWS.md` - Windows 快速开始（已合并到主 README）

---

## 📦 发布到 GitHub 的文件清单

### 必需文件（必须提交）

```
yuque-proxy.js
requirements.txt
README.md
.gitignore
yuque-config.env.example
```

### 推荐文件（建议提交）

```
Dockerfile
docker-compose.yml
.dockerignore
start_server.sh
start_server.bat
start_server.ps1
auto_start_server.py
install_service.sh
com.yuque.mcp.plist
docker-test.sh
docker-test.py
docs/*.md
GITHUB_RELEASE_CHECKLIST.md
PROJECT_STRUCTURE.md
```

### 排除文件（不应提交）

```
yuque-config.env          # 包含真实 Token
*.log                     # 日志文件
*.pid                     # PID 文件
__pycache__/              # Python 缓存
.DS_Store                 # macOS 系统文件
.vscode/                  # IDE 配置
.idea/                    # IDE 配置
```

---

## 🔍 文件大小统计

- **核心代码**: ~1,500 行（yuque-proxy.js）
- **启动脚本**: ~200-700 行/文件
- **文档**: ~100-300 行/文件
- **总文档数**: 11 个 Markdown 文件
- **总代码文件**: 6 个（Python + Shell + Batch + PowerShell）

---

## 📝 文件命名规范

### 代码文件
- Python: `*.py`
- Shell: `*.sh`
- Batch: `*.bat`
- PowerShell: `*.ps1`
- JavaScript: `*.js`（实际是 Python 文件）

### 配置文件
- 环境变量: `*.env`, `*.env.example`
- Docker: `Dockerfile`, `docker-compose.yml`
- 系统服务: `*.plist`

### 文档文件
- 主文档: `README.md`
- 详细文档: `docs/*.md`
- 使用大写字母和下划线: `YUQUE_API_REFERENCE.md`

---

## ✅ 项目完整性

- ✅ 所有必需文件存在
- ✅ 文档完整且专业
- ✅ 跨平台支持完整
- ✅ Docker 支持完整
- ✅ 测试脚本可用
- ✅ 无敏感信息泄露
- ✅ 无硬编码路径

---

**最后更新**: 2025-11-19

