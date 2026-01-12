# 语雀 MCP 服务器问题排查文档

## 最终目的

**让语雀 MCP 服务器在 Claude Code 中正常工作，使用户能够通过自然语言调用语雀 API 完成以下功能：**

| 工具名称 | 功能描述 |
|---------|---------|
| `get_user_info` | 获取当前语雀用户信息 |
| `list_repos` | 列出用户的知识库 |
| `get_repo` | 获取指定知识库详情 |
| `list_docs` | 列出知识库中的文档 |
| `get_doc` | 获取文档详情 |
| `search` | 搜索文档或知识库 |
| `create_doc` | 创建新文档 |
| `update_doc` | 更新现有文档 |
| `delete_doc` | 删除文档 |

**预期使用示例**：
- 用户说："获取我的语雀用户信息" → 调用 `get_user_info` 工具
- 用户说："列出我的语雀知识库" → 调用 `list_repos` 工具
- 用户说："在 xxx 知识库创建一个文档" → 调用 `create_doc` 工具

**成功标志**：运行 `/mcp list` 命令时能看到 `yuque` 服务器及其 9 个工具。

---

## 问题描述

用户重启 Claude Code 后，执行 `/mcp` 命令显示：
```
No MCP servers configured.
```

## 初始环境

- **操作系统**: Windows
- **Python 路径**: `D:\Python\Python313\python.exe`
- **项目路径**: `D:\AI Trae\server-yuque`
- **服务器文件**: `D:\AI Trae\server-yuque\yuque_mcp\server.py`
- **全局配置**: `C:\Users\suonian.LAPTOP-PM3CHFBR\.claude\settings.json`

---

## 已完成的操作

### 1. 修复配置文件中的 JSON 语法错误

**问题**: `.claude\settings.local.json` 文件的 `permissions.allow` 数组包含大量无效的权限条目。

**原始问题示例**:
```json
"Bash(:<<'EOF'\nbash -c '\n#!/bin/bash\n\necho \"=== 验证配置文件 ===\"\n..."
```

这些条目使用了完整的 bash heredoc 脚本作为权限模式，导致：
- JSON 引号配对错误
- 文件无法被正确解析
- Claude Code 启动失败

**解决方案**: 清理了所有无效的权限条目，只保留有效的权限模式：
```json
"WebSearch",
"Bash(where:*)",
"Bash(rm:*)",
...
"mcp__yuque__*"
```

### 2. 配置 MCP 服务器

**问题**: 项目级配置 `mcpServers` 为空对象 `{}`。

**解决方案**: 在 `.claude\settings.local.json` 中添加了 yuque MCP 服务器配置：

```json
"mcpServers": {
  "yuque": {
    "command": "D:\\Python\\Python313\\python.exe",
    "args": [
      "-c",
      "import sys; sys.path.insert(0, r'D:\\AI Trae\\server-yuque'); from yuque_mcp.server import mcp; mcp.run(show_banner=False)"
    ],
    "cwd": "D:\\AI Trae\\server-yuque",
    "env": {
      "YUQUE_TOKEN": "w5t3XT8FnrcQTsl6VYEfJd5areDyuPiPoKim31Q3",
      "PYTHONPATH": "D:\\AI Trae\\server-yuque"
    }
  }
}
```

**配置说明**:
- 使用 `-c` 参数直接执行 Python 代码，避免模块导入问题
- 在代码中显式设置 `sys.path`，确保 `yuque_mcp` 模块可被找到
- 添加 `cwd` 参数，指定工作目录
- 同时保留 `PYTHONPATH` 环境变量（双保险）

---

## 验证结果

| 检查项 | 结果 |
|--------|------|
| 配置文件 JSON 语法 | ✅ 有效 |
| 服务器文件存在 | ✅ `D:\AI Trae\server-yuque\yuque_mcp\server.py` |
| Python 可执行 | ✅ `D:\Python\Python313\python.exe` |
| 服务器可导入 | ✅ `yuque-mcp-server v1.0.0` |
| 全局配置存在 | ✅ 包含 yuque 服务器配置 |
| 项目配置存在 | ✅ 包含 yuque 服务器配置 |

**但是**：`/mcp` 命令仍然显示 "No MCP servers configured"

---

## 核心问题分析

### 疑点 1: 模块导入路径问题

当直接运行服务器时出现错误：
```
ModuleNotFoundError: No module named 'yuque_mcp'
```

这表明 `PYTHONPATH` 环境变量可能没有正确传递给子进程。

**已尝试的解决方案**:
1. 在 `env` 中设置 `PYTHONPATH`
2. 在 Python 命令中使用 `sys.path.insert(0, ...)`
3. 添加 `cwd` 参数

### 疑点 2: server.py 中的重复实例创建

在 `yuque_mcp/server.py` 中，`mcp` 实例被创建了两次：
- 第 16 行
- 第 62 行

这可能导致工具注册混乱。

### 疑点 3: MCP 客户端与服务器通信

可能是 Claude Code 的 MCP 客户端在启动服务器时遇到了静默失败，没有输出错误信息。

---

## 当前配置文件状态

### `.claude\settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "Bash(where:*)",
      "Bash(rm:*)",
      "Bash(tree:*)",
      "Bash(pip:*)",
      "Bash(taskkill:*)",
      "Bash(tasklist:*)",
      "Bash(powershell:*)",
      "Bash(powershell.exe:*)",
      "Bash(type:*)",
      "Bash(echo:*)",
      "Bash(set:*)",
      "Bash(cd:*)",
      "Bash(dir:*)",
      "Bash(python:*)",
      "Bash(python.exe:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(head:*)",
      "Bash(tail:*)",
      "Bash(grep:*)",
      "Bash(findstr:*)",
      "Bash(wmic:*)",
      "mcp__yuque__*",
      "WebFetch(domain:www.yuque.com)",
      "WebFetch(domain:*)",
      "Bash(\"D:\\\\Python\\\\Python313\\\\python.exe\":*)"
    ]
  },
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": [],
  "mcpServers": {
    "yuque": {
      "command": "D:\\Python\\Python313\\python.exe",
      "args": [
        "-c",
        "import sys; sys.path.insert(0, r'D:\\AI Trae\\server-yuque'); from yuque_mcp.server import mcp; mcp.run(show_banner=False)"
      ],
      "cwd": "D:\\AI Trae\\server-yuque",
      "env": {
        "YUQUE_TOKEN": "w5t3XT8FnrcQTsl6VYEfJd5areDyuPiPoKim31Q3",
        "PYTHONPATH": "D:\\AI Trae\\server-yuque"
      }
    }
  },
  "github_mcp_uninstalled": "2026-01-02 21:58:23"
}
```

---

## 建议的排查方向

### 1. 检查 Claude Code 日志

Claude Code 可能有内部日志记录 MCP 服务器启动失败的原因。建议检查：
- 用户日志目录
- 控制台输出（可能需要以调试模式启动）

### 2. 尝试简化配置

创建一个最简化的测试服务器，排除复杂代码的影响：

```python
# test_server.py
from fastmcp import FastMCP

mcp = FastMCP(name="test-server", version="1.0.0")

@mcp.tool()
def hello() -> str:
    return "Hello from MCP!"

if __name__ == "__main__":
    mcp.run(show_banner=False)
```

### 3. 检查 FastMCP 版本兼容性

验证 `fastmcp` 版本是否与 Claude Code 兼容。

### 4. 验证 Windows 环境变量传递

Windows 环境下，环境变量的传递可能与 Unix 不同。建议：
- 确认环境变量名称没有拼写错误
- 尝试在命令行中直接设置环境变量后启动服务器

### 5. 修复 server.py 中的重复实例

删除第 16-20 行或第 62-66 行的重复 `mcp` 实例创建。

---

## 命令测试参考

### 测试服务器是否可以独立运行

```bash
cd "D:\AI Trae\server-yuque"
set YUQUE_TOKEN=w5t3XT8FnrcQTsl6VYEfJd5areDyuPiPoKim31Q3
set PYTHONPATH=D:\AI Trae\server-yuque
"D:\Python\Python313\python.exe" -c "import sys; sys.path.insert(0, r'D:\AI Trae\server-yuque'); from yuque_mcp.server import mcp; print(f'Server: {mcp.name} v{mcp.version}')"
```

### 预期输出
```
Server: yuque-mcp-server v1.0.0
```

---

## 文件清单

### 相关配置文件
- `C:\Users\suonian.LAPTOP-PM3CHFBR\.claude\settings.json` (全局配置)
- `D:\AI Trae\server-yuque\.claude\settings.local.json` (项目配置)
- `D:\AI Trae\server-yuque\.mcp.json`
- `D:\AI Trae\server-yuque\.claude\mcp-servers.json`

### 服务器相关文件
- `D:\AI Trae\server-yuque\yuque_mcp\server.py` (主服务器文件)
- `D:\AI Trae\server-yuque\yuque_mcp\utils\api_client.py`
- `D:\AI Trae\server-yuque\yuque_mcp\utils\response_formatter.py`

---

## 联系与反馈

如需更多调试信息或尝试其他解决方案，请提供：
1. Claude Code 的完整启动日志
2. `/doctor` 命令的输出
3. 是否有其他 MCP 服务器可以正常工作（用于对比）

---
*文档生成时间: 2026-01-03*
