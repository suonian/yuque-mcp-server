# 语雀MCP服务器故障排除指南

## 概述

本文档提供了语雀MCP服务器常见问题的解决方案和故障排除步骤。如果您在使用过程中遇到问题，请按照本文档的指导进行排查。

## 错误分类

### 1. 安装错误

#### 1.1 依赖安装失败

**错误现象**：
```
pip install -r requirements.txt 失败
```

**可能原因**：
- pip版本过低
- 网络连接问题
- 源镜像问题
- 权限不足

**解决方案**：

```bash
# 更新pip
pip install --upgrade pip

# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 以管理员权限安装
# Windows: 以管理员身份运行PowerShell
# macOS/Linux: sudo pip install -r requirements.txt
```

#### 1.2 安装脚本执行失败

**错误现象**：
```
.install.ps1: 无法加载文件，因为在此系统上禁止运行脚本。
```

**可能原因**：
- PowerShell执行策略限制

**解决方案**：

```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后重新运行安装脚本
.install.ps1
```

### 2. 配置错误

#### 2.1 缺少语雀API Token

**错误信息**：
```
缺少语雀API Token
```

**可能原因**：
- 未设置YUQUE_TOKEN环境变量
- 配置文件中token字段为空
- 配置文件中的环境变量占位符未被正确替换

**解决方案**：

```bash
# 方式1：设置环境变量
# Windows
setx YUQUE_TOKEN "your-token"

# macOS/Linux
export YUQUE_TOKEN="your-token"

# 方式2：直接在配置文件中设置
# 编辑config.json，将token字段替换为实际值
{
  "yuque": {
    "token": "your-actual-token",
    "base_url": "https://www.yuque.com/api/v2"
  }
}
```

#### 2.2 配置文件格式错误

**错误信息**：
```
配置文件解析错误: Expecting property name enclosed in double quotes: line 5 column 1 (char 8)
```

**可能原因**：
- JSON格式错误
- 使用了单引号而不是双引号
- 缺少逗号
- 多余的逗号

**解决方案**：
- 使用JSON验证工具检查配置文件
- 确保所有字符串使用双引号
- 确保正确的逗号分隔
- 重新复制配置模板：`cp config.example.json config.json`

### 3. 启动错误

#### 3.1 端口被占用

**错误信息**：
```
OSError: [Errno 48] Address already in use
```

**可能原因**：
- 指定端口已被其他进程占用

**解决方案**：

```bash
# 查看占用端口的进程
# Windows
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :3000

# 终止占用端口的进程
# Windows: 替换PID为实际进程ID
taskkill /PID 1234 /F

# macOS/Linux: 替换PID为实际进程ID
kill -9 1234

# 或使用不同端口启动
python yuque_mcp/server.py --port 3001
```

#### 3.2 模块导入错误

**错误信息**：
```
ModuleNotFoundError: No module named 'fastmcp'
```

**可能原因**：
- 依赖未正确安装
- Python路径配置错误
- 虚拟环境未激活

**解决方案**：

```bash
# 重新安装依赖
pip install -r requirements.txt

# 检查Python路径
python -c "import sys; print(sys.path)"

# 确保在项目根目录执行
cd /path/to/yuque-mcp-server
python yuque_mcp/server.py
```

### 4. 运行时错误

#### 4.1 语雀API连接失败

**错误信息**：
```
获取用户信息失败: ConnectionError
```

**可能原因**：
- 网络连接问题
- 防火墙拦截
- 语雀API Token无效
- 语雀API服务不可用

**解决方案**：

```bash
# 检查网络连接
ping www.yuque.com

# 检查Token有效性
# 手动调用语雀API测试
curl -H "X-Auth-Token: your-token" https://www.yuque.com/api/v2/user

# 检查防火墙设置
# 确保允许Python访问网络
```

#### 4.2 权限错误

**错误信息**：
```
PermissionError: [Errno 13] Permission denied: 'yuque_mcp.log'
```

**可能原因**：
- 日志文件写入权限不足
- 配置文件读取权限不足

**解决方案**：

```bash
# 检查文件权限
# Windows: 右键文件 > 属性 > 安全
# macOS/Linux: ls -l yuque_mcp.log

# 以管理员/root权限运行
# Windows: 以管理员身份运行PowerShell
# macOS/Linux: sudo python yuque_mcp/server.py
```

#### 4.3 内存不足

**错误信息**：
```
MemoryError: Unable to allocate memory for pool
```

**可能原因**：
- 系统内存不足
- 进程占用内存过高

**解决方案**：

```bash
# 关闭其他占用内存的进程
# 增加系统内存
# 调整Python内存限制（如果可能）
```

### 5. MCP客户端错误

#### 5.1 Claude Code无法连接

**错误信息**：
```
No MCP servers configured.
```

**可能原因**：
- MCP服务器未启动
- 配置文件错误
- Claude Code版本不兼容

**解决方案**：

```bash
# 确保MCP服务器正在运行
ps aux | grep yuque_mcp

# 检查Claude Code配置
# 确保在项目目录中启动Claude Code
# 检查settings.json中的mcpServers配置
```

#### 5.2 工具列表为空

**错误信息**：
```
yuque (stdio)
  - No tools available
```

**可能原因**：
- MCP服务器工具注册失败
- 服务器内部错误
- 版本不兼容

**解决方案**：

```bash
# 查看服务器日志
tail -f yuque_mcp.log

# 检查服务器启动输出
python yuque_mcp/server.py --show-banner

# 更新到最新版本
git pull
pip install -r requirements.txt
```

## 日志分析

### 日志位置

- **主日志文件**: `yuque_mcp.log`
- **控制台输出**: 仅在使用`--show-banner`参数时显示

### 日志级别

- DEBUG: 详细调试信息
- INFO: 普通信息
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误

### 调整日志级别

```bash
# 命令行参数方式
python yuque_mcp/server.py --log-level DEBUG

# 配置文件方式
# 在config.json中设置
{
  "server": {
    "log_level": "DEBUG"
  }
}
```

### 常见日志错误模式

#### 1. Token错误
```
ERROR - yuque_mcp.server - 缺少语雀API Token
```

**解决方案**: 设置YUQUE_TOKEN环境变量或在配置文件中配置token字段

#### 2. API连接错误
```
ERROR - yuque_mcp.server - 获取用户信息失败: ConnectionError
```

**解决方案**: 检查网络连接和Token有效性

#### 3. 参数错误
```
ERROR - yuque_mcp.server - 缺少必要参数（namespace, title, body）
```

**解决方案**: 确保调用时提供了所有必要参数

## 诊断步骤

### 基本诊断流程

1. **检查依赖**：确保所有依赖已正确安装
2. **检查配置**：验证YUQUE_TOKEN和配置文件
3. **检查日志**：查看yuque_mcp.log获取详细错误信息
4. **测试连接**：手动测试语雀API连接
5. **重启服务**：尝试重启MCP服务器
6. **更新版本**：检查是否有最新版本

### 高级诊断

#### 1. 手动测试语雀API

```bash
# 测试获取用户信息
curl -H "X-Auth-Token: your-token" https://www.yuque.com/api/v2/user

# 测试获取知识库列表
curl -H "X-Auth-Token: your-token" https://www.yuque.com/api/v2/user/repos
```

#### 2. 检查MCP服务器状态

```bash
# 检查进程是否运行
ps aux | grep yuque_mcp

# 检查端口监听（仅sse模式）
# Windows
netstat -ano | findstr :3000

# macOS/Linux
lsof -i :3000
```

#### 3. 调试模式启动

```bash
# 以调试模式启动，查看详细输出
python yuque_mcp/server.py --log-level DEBUG --show-banner
```

## 常见问题解答

### Q1: 为什么Claude Code中显示"No MCP servers configured"？

**A1**: 可能原因：
- MCP服务器未启动
- 未在项目目录中打开Claude Code
- Claude Code版本不兼容
- 配置文件错误

**解决方案**：
- 确保MCP服务器正在运行：`python yuque_mcp/server.py`
- 在项目根目录中打开Claude Code
- 更新Claude Code到最新版本
- 检查配置文件格式和内容

### Q2: 为什么工具调用返回"缺少语雀API Token"？

**A2**: 可能原因：
- 未设置YUQUE_TOKEN环境变量
- 配置文件中token字段为空
- 环境变量未生效

**解决方案**：
- 重新设置环境变量
- 直接在配置文件中填写token
- 重启终端或计算机使环境变量生效

### Q3: 为什么启动时出现"端口被占用"错误？

**A3**: 可能原因：
- 其他进程正在使用该端口
- 之前的MCP服务器进程未正确关闭

**解决方案**：
- 终止占用端口的进程
- 使用不同端口启动：`python yuque_mcp/server.py --port 3001`

### Q4: 为什么API调用返回401错误？

**A4**: 可能原因：
- 语雀API Token无效
- Token已过期
- Token权限不足

**解决方案**：
- 生成新的语雀API Token
- 确保Token有足够的权限
- 检查Token是否被正确设置

## 版本兼容性

### MCP协议版本

- 支持MCP 2024-11-05标准
- 兼容所有符合MCP标准的客户端

### 客户端兼容性

| 客户端 | 兼容版本 | 测试状态 |
|--------|----------|----------|
| Claude Code | v2.0+ | ✅ 通过 |
| Chatbox | v1.0+ | ✅ 通过 |
| Cursor | v0.30+ | ✅ 通过 |
| Cherry Studio | v1.0+ | ✅ 通过 |

### Python版本

- 推荐：Python 3.9+  
- 最低：Python 3.7  
- 测试通过：Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13

## 获取支持

如果按照本文档无法解决问题，请通过以下方式获取支持：

1. **GitHub Issues**: [提交Issue](https://github.com/suonian/yuque-mcp-server/issues)
2. **语雀社区**: [语雀MCP服务器讨论区](https://www.yuque.com/community/yuque-mcp-server)
3. **开发者邮件**: suonian@example.com

### 提交Issue时请提供

- 操作系统和版本
- Python版本
- 客户端类型和版本
- 完整的错误信息
- 日志文件内容
- 复现步骤

## 最佳实践

1. **定期更新**：保持MCP服务器和依赖包为最新版本
2. **使用环境变量**：优先使用环境变量配置敏感信息
3. **备份配置**：定期备份config.json文件
4. **监控日志**：定期检查日志文件，及时发现问题
5. **使用虚拟环境**：推荐使用Python虚拟环境隔离依赖
6. **限制权限**：最小化MCP服务器的运行权限

## 总结

本文档提供了语雀MCP服务器常见问题的解决方案和故障排除步骤。如果您遇到了本文档未涵盖的问题，请提交Issue或联系开发者获取支持。

我们会持续更新本文档，添加新的问题和解决方案。
