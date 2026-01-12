# 语雀MCP服务器安装指南

## 项目简介

语雀MCP服务器是一个基于Model Context Protocol (MCP)的代理服务器，让AI助手能够通过MCP协议与语雀平台交互。

## 功能特性

- ✅ 完全兼容MCP 2024-11-05标准
- ✅ 支持Claude Code、Chatbox、Cursor等主流AI工具
- ✅ 提供完整的语雀API功能
- ✅ 支持环境变量和配置文件双重配置
- ✅ 支持stdio和sse两种传输模式
- ✅ 完善的日志记录
- ✅ 跨平台支持（Windows/macOS/Linux）

## 环境准备

### 系统要求
- **操作系统**: Windows 10+, macOS 10.15+, Linux
- **Python版本**: 3.7+
- **网络连接**: 能够访问语雀API（https://www.yuque.com）

### 依赖需求
- Python 3.7+
- pip 20.0+

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/suonian/yuque-mcp-server.git
cd yuque-mcp-server
```

### 2. 安装依赖

#### 方式一：使用安装脚本（推荐，Windows）

```powershell
# 以管理员身份运行PowerShell
.install.ps1
```

#### 方式二：手动安装依赖

```bash
# 安装依赖包
pip install -r requirements.txt
```

### 3. 配置设置

#### 方式一：环境变量配置（推荐）

```bash
# Windows
setx YUQUE_TOKEN "你的语雀token"

# macOS/Linux
export YUQUE_TOKEN="你的语雀token"
```

#### 方式二：配置文件配置

```bash
# 复制配置模板
cp config.example.json config.json

# 编辑配置文件
# 替换token字段为你的语雀API Token
```

### 4. 获取语雀API Token

1. 登录语雀官网：https://www.yuque.com
2. 进入「个人设置」>「Token管理」
3. 点击「生成新Token」
4. 复制生成的Token

## 服务启动

### 方式一：Claude Code模式（stdio）

```bash
python yuque_mcp/server.py
```

### 方式二：HTTP服务器模式（sse）

```bash
python yuque_mcp/server.py --transport sse --port 3000
```

### 方式三：后台运行（Linux/macOS）

```bash
# 使用nohup后台运行
nohup python yuque_mcp/server.py > yuque_mcp.log 2>&1 &

# 查看进程
ps aux | grep yuque_mcp
```

## 验证安装

### 验证Claude Code连接

1. 启动Claude Code
2. 在项目目录中打开Claude Code
3. 运行命令：`/mcp list`
4. 应该看到类似输出：

```
yuque (stdio)
  - get_user_info: 获取当前用户信息
  - list_repos: 列出当前用户的知识库
  - get_repo: 获取知识库详情
  - list_docs: 列出知识库中的文档
  - get_doc: 获取文档详情
  - search: 搜索文档或知识库
  - create_doc: 创建文档
  - update_doc: 更新文档
  - delete_doc: 删除文档
```

### 验证HTTP服务器

```bash
curl http://localhost:3000/health
```

## 命令行参数

| 参数 | 类型 | 描述 | 默认值 |
|------|------|------|--------|
| `--transport` | string | 传输方式，可选值：stdio, sse | stdio |
| `--port` | integer | 监听端口（仅sse模式） | 3000 |
| `--host` | string | 监听地址（仅sse模式） | 0.0.0.0 |
| `--log-level` | string | 日志级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL | CRITICAL |
| `--show-banner` | boolean | 显示启动横幅 | False |

## 配置说明

### 配置文件结构

```json
{
  "yuque": {
    "token": "your-token-here",
    "base_url": "https://www.yuque.com/api/v2"
  },
  "server": {
    "transport": "stdio",
    "port": 3000,
    "host": "0.0.0.0",
    "log_level": "CRITICAL"
  }
}
```

### 环境变量

| 环境变量 | 描述 |
|----------|------|
| `YUQUE_TOKEN` | 语雀API Token |
| `PYTHONIOENCODING` | Python IO编码，默认utf-8 |
| `FORCE_COLOR` | 禁用颜色输出，默认0 |
| `NO_COLOR` | 禁用颜色输出，默认1 |

## 支持的工具列表

### 用户相关

- `get_user_info`: 获取当前用户信息

### 知识库管理

- `list_repos`: 列出当前用户的知识库
- `get_repo`: 获取知识库详情

### 文档管理

- `list_docs`: 列出知识库中的文档
- `get_doc`: 获取文档详情
- `create_doc`: 创建文档
- `update_doc`: 更新文档
- `delete_doc`: 删除文档

### 搜索功能

- `search`: 搜索文档或知识库

## 使用示例

### 在Claude Code中使用

```
/mcp call yuque.get_user_info
/mcp call yuque.list_repos limit=10
/mcp call yuque.get_doc namespace="username/repo" slug="doc-slug"
```

### 在Chatbox中使用

```
@yuque get_user_info
@yuque list_repos limit=10
@yuque get_doc namespace="username/repo" slug="doc-slug"
```

## 日志管理

- **日志文件**: `yuque_mcp.log`
- **日志级别**: 可通过`--log-level`参数或配置文件调整
- **日志格式**: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## 常见问题

### 1. 缺少语雀API Token

**错误信息**: `缺少语雀API Token`

**解决方案**: 
- 设置`YUQUE_TOKEN`环境变量
- 或在`config.json`中配置`token`字段

### 2. 无法连接到语雀API

**错误信息**: `获取用户信息失败: ConnectionError`

**解决方案**: 
- 检查网络连接
- 确保防火墙允许访问语雀API
- 检查语雀API Token是否有效

### 3. 依赖安装失败

**错误信息**: `依赖安装失败`

**解决方案**: 
- 更新pip: `pip install --upgrade pip`
- 使用国内镜像: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

### 4. 端口被占用

**错误信息**: `OSError: [Errno 48] Address already in use`

**解决方案**: 
- 更换端口: `python yuque_mcp/server.py --port 3001`
- 终止占用端口的进程: `lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill -9`

## 开发说明

### 项目结构

```
yuque-mcp-server/
├── yuque_mcp/              # 主代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── server.py           # 主服务器文件
│   ├── models/             # 数据模型
│   ├── tools/              # 工具函数
│   └── utils/              # 工具类
│       ├── api_client.py   # 语雀API客户端
│       └── response_formatter.py # 响应格式化
├── config.example.json     # 配置模板
├── requirements.txt        # 依赖列表
├── install.ps1             # Windows安装脚本
└── INSTALL.md              # 安装文档
```

### 开发依赖

```bash
# 安装开发依赖
pip install -r requirements-dev.txt
```

### 代码风格

- 使用Black进行代码格式化
- 使用Flake8进行代码检查
- 使用mypy进行类型检查

## 更新日志

### v1.0.0 (2026-01-03)

- ✅ 初始版本发布
- ✅ 支持9个核心语雀API功能
- ✅ 支持stdio和sse传输模式
- ✅ 支持环境变量和配置文件配置
- ✅ 完善的日志记录
- ✅ 跨平台支持

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题，请提交Issue或联系项目维护者。
