# 语雀 MCP 代理自动启动指南

## 📋 概述

现在提供了多种自动启动方案，您可以根据需求选择：

1. **启动脚本** - 手动控制，检测并启动服务
2. **系统服务** - 开机自启，系统自动管理
3. **自动启动包装器** - 智能检测，按需启动

---

## 🚀 方案一：启动脚本（推荐日常使用）

### 功能特点
- ✅ 自动检测服务是否运行
- ✅ 如果未运行则自动启动
- ✅ 支持启动/停止/重启/状态查看
- ✅ 日志管理

### 使用方法

```bash
# 进入项目目录
cd /path/to/yuque-mcpserver

# 启动服务（如果未运行）
./start_server.sh start

# 查看服务状态
./start_server.sh status

# 停止服务
./start_server.sh stop

# 重启服务
./start_server.sh restart

# 查看实时日志
./start_server.sh logs
```

### 工作原理

1. 检查 PID 文件和进程是否存在
2. 检查端口 3000 是否被占用
3. 如果服务未运行，自动启动
4. 保存 PID 到 `/tmp/yuque-proxy.pid`
5. 日志输出到 `/tmp/yuque-proxy.log`

### 集成到 Chatbox

您可以在 Chatbox 的 MCP Server 配置中，将 URL 设置为：
```
http://localhost:3000/mcp
```

然后在需要时运行启动脚本，或者使用方案二（系统服务）实现自动启动。

---

## 🔄 方案二：系统服务（推荐长期运行）

### 功能特点
- ✅ 开机自动启动
- ✅ 崩溃自动重启
- ✅ 系统级管理
- ✅ 无需手动干预

### 安装步骤

#### 1. 安装服务

```bash
cd /path/to/yuque-mcpserver
./install_service.sh
```

#### 2. 服务管理命令

```bash
# 启动服务
launchctl start com.yuque.mcp

# 停止服务
launchctl stop com.yuque.mcp

# 查看服务状态
launchctl list | grep com.yuque.mcp

# 查看日志
tail -f /tmp/yuque-proxy.log

# 卸载服务
launchctl unload ~/Library/LaunchAgents/com.yuque.mcp.plist
rm ~/Library/LaunchAgents/com.yuque.mcp.plist
```

#### 3. 验证安装

```bash
# 检查服务是否运行
curl http://localhost:3000/health

# 或使用启动脚本
./start_server.sh status
```

### 配置文件位置

- 服务配置: `~/Library/LaunchAgents/com.yuque.mcp.plist`
- 日志文件: `/tmp/yuque-proxy.log`
- 错误日志: `/tmp/yuque-proxy.error.log`

### 自定义配置

编辑 `com.yuque.mcp.plist` 文件可以修改：
- 工作目录
- 环境变量（如 `YUQUE_TOKEN`）
- 日志路径
- 端口号

---

## 🤖 方案三：自动启动包装器（智能检测）

### 功能特点
- ✅ 智能检测服务状态
- ✅ 按需自动启动
- ✅ 适合集成到其他脚本

### 使用方法

```bash
# 检查并自动启动服务
python3 auto_start_server.py

# 仅检查服务状态（不启动）
python3 auto_start_server.py --check
```

### 集成示例

#### 在 Chatbox 配置前运行

创建一个包装脚本 `chatbox_wrapper.sh`:

```bash
#!/bin/bash
cd /path/to/yuque-mcpserver
python3 auto_start_server.py
# 然后启动 Chatbox 或继续其他操作
```

#### 在定时任务中使用

```bash
# 添加到 crontab，每 5 分钟检查一次
*/5 * * * * cd /path/to/yuque-mcpserver && python3 auto_start_server.py --check
```

---

## 📊 方案对比

| 特性 | 启动脚本 | 系统服务 | 自动启动包装器 |
|------|---------|---------|---------------|
| 开机自启 | ❌ | ✅ | ❌ |
| 崩溃重启 | ❌ | ✅ | ❌ |
| 手动控制 | ✅ | ⚠️ | ✅ |
| 按需启动 | ✅ | ❌ | ✅ |
| 日志管理 | ✅ | ✅ | ❌ |
| 适合场景 | 日常开发 | 生产环境 | 脚本集成 |

---

## 🎯 推荐使用场景

### 场景1：日常开发使用
**推荐：启动脚本**

```bash
# 每次使用前
./start_server.sh start

# 使用后（可选）
./start_server.sh stop
```

### 场景2：长期运行服务
**推荐：系统服务**

```bash
# 一次性安装
./install_service.sh

# 之后系统会自动管理，无需手动操作
```

### 场景3：集成到其他工具
**推荐：自动启动包装器**

```bash
# 在脚本开头调用
python3 auto_start_server.py
```

---

## 🔧 故障排查

### 问题1：服务无法启动

**检查步骤**：
```bash
# 1. 检查端口是否被占用
lsof -i :3000

# 2. 检查 Python 环境
python3 --version

# 3. 检查脚本权限
ls -l start_server.sh

# 4. 查看详细日志
cat /tmp/yuque-proxy.log
```

### 问题2：系统服务无法加载

**检查步骤**：
```bash
# 1. 检查 plist 文件格式
plutil -lint ~/Library/LaunchAgents/com.yuque.mcp.plist

# 2. 检查路径是否正确
cat ~/Library/LaunchAgents/com.yuque.mcp.plist

# 3. 查看系统日志
log show --predicate 'process == "launchd"' --last 5m
```

### 问题3：服务启动但无法访问

**检查步骤**：
```bash
# 1. 检查服务状态
./start_server.sh status

# 2. 测试健康检查
curl http://localhost:3000/health

# 3. 检查防火墙
# macOS: 系统偏好设置 > 安全性与隐私 > 防火墙
```

---

## 📝 快速开始

### 最简单的方式（推荐）

1. **安装系统服务**（一次性）：
   ```bash
   cd /path/to/yuque-mcpserver
   ./install_service.sh
   ```

2. **配置 Chatbox**：
   - URL: `http://localhost:3000/mcp`
   - HTTP Header: `X-Yuque-Token=your-token`

3. **完成！** 服务会在系统启动时自动运行，无需手动操作。

### 手动控制方式

1. **使用启动脚本**：
   ```bash
   ./start_server.sh start
   ```

2. **配置 Chatbox**（同上）

3. **使用后停止**（可选）：
   ```bash
   ./start_server.sh stop
   ```

---

## 🔐 安全提示

1. **Token 安全**：
   - 使用环境变量或 HTTP Header 配置 Token
   - 不要将 Token 硬编码在脚本中

2. **端口安全**：
   - 默认端口 3000 仅监听本地（127.0.0.1）
   - 如需外网访问，请配置防火墙

3. **日志安全**：
   - 日志文件可能包含敏感信息
   - 定期清理或限制日志文件权限

---

## 📞 技术支持

如有问题，请检查：
1. 服务状态：`./start_server.sh status`
2. 日志文件：`/tmp/yuque-proxy.log`
3. 系统服务状态：`launchctl list | grep com.yuque.mcp`

---

**最后更新**: 2025-11-18

