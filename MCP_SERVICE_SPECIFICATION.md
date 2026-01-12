# MCP服务创建与配置规范

## 1. 文档目的

本文档规范基于 **Model Context Protocol (MCP)** 的外部服务在Claude Code中的创建流程、配置方式及调用标准。

**MCP** 是Anthropic定义的协议，用于让AI助手与外部工具、数据源集成。

## 2. 与mcp-builder技能的关系

本规范与 **mcp-builder** 技能配合使用：

| 技能 | 侧重点 |
|------|--------|
| **mcp-builder** | MCP服务开发技术规范（代码结构、工具设计、错误处理） |
| **本规范** | MCP服务部署与配置规范（目录结构、全局配置、调用标准） |

使用时请结合两个技能的指导：mcp-builder负责开发，本规范负责部署。

---

## 3. MCP服务类型

### 2.1 按传输协议分类

| 类型 | 配置字段 | 适用场景 |
|------|----------|----------|
| **stdio** | `command` + `args` | 本地可执行文件（Python脚本、NPM包、Docker容器） |
| **http/sse** | `url` + `transport` | 远程HTTP服务 |

### 2.2 按启动方式分类

```json
// 类型1：本地Python服务
{
  "command": "D:\\Python\\Python313\\python.exe",
  "args": ["yuque_mcp/server.py"],
  "cwd": "D:\\AI Trae\\server-yuque",
  "env": { "TOKEN": "xxx" },
  "transport": "stdio"
}

// 类型2：NPM包服务
{
  "command": "npx",
  "args": ["-y", "@package/mcp-server"],
  "transport": "stdio"
}

// 类型3：远程HTTP服务
{
  "url": "https://api.example.com/mcp",
  "transport": "http"
}
```

---

## 3. 全局配置规范

### 3.1 全局配置文件位置

```
C:\Users\{用户名}\.claude\settings.json
```

### 3.2 配置模板

```json
{
  "mcpServers": {
    "服务名称": {
      "command": "启动命令",
      "args": ["参数1", "参数2"],
      "cwd": "工作目录",
      "env": {
        "环境变量": "值"
      },
      "transport": "stdio"
    }
  }
}
```

### 3.3 配置字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `command` | stdio必须 | 可执行文件路径（如python、npx、docker） |
| `args` | stdio必须 | 命令行参数数组 |
| `cwd` | 推荐 | 工作目录，影响相对路径解析 |
| `env` | 可选 | 环境变量字典 |
| `url` | http必须 | 远程服务地址 |
| `transport` | 可选 | 传输协议（默认stdio） |

### 3.4 配置验证

```bash
claude mcp list
```

状态显示 `✓ Connected` 表示配置成功。

---

## 4. 服务目录结构

### 4.1 目录结构规范

```
D:\AI Trae\{服务名}\
├── config.json          # 服务配置（API Token等）
├── requirements.txt     # Python依赖
├── server.py            # MCP服务器入口（根目录）
└── tests/               # 测试文件
```

**说明**：
- `server.py` 放置在根目录，保持简洁
- `{服务名}_mcp/` 子目录可选，当项目较复杂时使用

### 4.2 Python服务结构（可选子目录）

```
D:\AI Trae\{服务名}\
├── config.json
├── requirements.txt
├── {服务名}_mcp/
│   ├── __init__.py
│   ├── server.py       # 服务器入口
│   ├── tools.py        # 工具定义
│   └── models.py       # 数据模型
└── tests/
```

### 4.3 Node.js服务结构

```
D:\AI Trae\{服务名}\
├── config.json          # 服务配置
├── package.json         # NPM配置
├── src/
│   └── index.js        # 服务器入口
└── node_modules/       # 依赖（自动生成）
```

---

## 5. 创建流程

### 5.1 准备阶段

1. 确定服务类型（本地/远程）
2. 确认传输协议（stdio/http）
3. 准备API凭证（Token、API Key）

### 5.2 开发阶段

1. 创建服务目录
2. 编写MCP服务器代码（使用FastMCP、官方SDK）
3. 配置依赖文件（requirements.txt / package.json）
4. 本地测试验证

### 5.3 配置阶段

1. 编辑全局 `settings.json`
2. 添加mcpServers配置节点
3. 运行 `claude mcp list` 验证连接状态

### 5.4 验证阶段

1. 在Claude Code中测试工具调用
2. 检查日志确认正常工作
3. 记录服务配置信息

---

## 6. 质量要求

| 指标 | 要求 |
|------|------|
| 启动时间 | ≤10秒 |
| 错误处理 | 返回标准错误格式 |
| 日志记录 | 关键操作需记录 |
| 文档完善 | README包含使用说明 |

---

## 7. 常见问题

### Q1: 服务无法启动
```bash
# 手动测试命令
python your_server.py
# 检查依赖是否安装
pip install -r requirements.txt
```

### Q2: 配置不生效
```bash
# 重启Claude Code
# 重新运行
claude mcp list
```

### Q3: 多项目共用
全局配置后，所有项目自动共享，无需重复配置。

---

## 8. Claude Code配置示例

### 8.1 配置文件格式

支持两种格式，推荐使用 `.env`：

```bash
# .env 文件格式（推荐）
YUQUE_TOKEN=your-token-here
API_BASE_URL=https://api.example.com
```

```json
// config.json 格式
{
  "YUQUE_TOKEN": "your-token-here",
  "API_BASE_URL": "https://api.example.com"
}
```

### 8.2 虚拟环境策略

推荐使用系统Python + 独立pip依赖，不强制创建venv：

```bash
# 方案A：使用系统Python（推荐）
command: "D:\\Python\\Python313\\python.exe"
args: ["server.py"]

# 方案B：独立venv
command: "D:\\AI Trae\\{服务名}\\venv\\Scripts\\python.exe"
args: ["server.py"]
```

### 8.3 NPM包服务处理

第三方NPM包MCP服务无需移动到 `D:\AI Trae\`，直接在settings.json配置：

```json
{
  "command": "npx",
  "args": ["-y", "@package/mcp-server"],
  "transport": "stdio"
}
```

### 8.4 服务命名规范

**自研MCP服务**：使用简洁名称（小写字母）

```json
{
  "mcpServers": {
    "yuque": { /* ✅ 推荐 */ },
    "web-search": { /* ✅ 推荐 */ }
  }
}
```

**第三方MCP服务**：使用简短服务名称

```json
{
  "mcpServers": {
    "chrome-devtools": { /* ✅ 简短名称 */ },
    "web-reader": { /* ✅ 简短名称 */ },
    "web-search-prime": { /* ✅ 简短名称 */ },
    "zai-mcp-server": { /* ✅ 简短名称 */ }
  }
}
```

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| 自研服务 | 简洁名称（小写字母） | `yuque`, `web-search` |
| 第三方服务 | 简短服务名称 | `chrome-devtools`, `web-reader`, `zai-mcp-server` |

**说明**：第三方MCP服务的名称以 `claude mcp list` 显示的简短名称为准。

### 8.5 完整settings.json示例

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.anthropic.com"
  },
  "mcpServers": {
    "yuque": {
      "command": "D:\\Python\\Python313\\python.exe",
      "args": ["server.py"],
      "cwd": "D:\\AI Trae\\server-yuque",
      "env": {
        "YUQUE_TOKEN": "your-token",
        "PYTHONPATH": "D:\\AI Trae\\server-yuque"
      },
      "transport": "stdio"
    },
    "web-search": {
      "url": "https://api.example.com/mcp",
      "transport": "http"
    }
  }
}
```

---

## 9. 参考资源

- [MCP官方文档](https://modelcontextprotocol.io/)
- [FastMCP框架](https://github.com/jlowin/fastmcp)
- Claude Code CLI: `claude mcp --help`
