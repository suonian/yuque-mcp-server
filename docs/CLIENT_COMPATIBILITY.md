# 🔌 客户端兼容性指南

本指南说明如何在不同的 AI 工具中配置和使用语雀 MCP 代理服务器。

## ✅ 支持的客户端

理论上，任何支持 **Model Context Protocol (MCP)** 标准的客户端都可以连接本服务器。以下是已验证和可能支持的客户端：

### 已验证支持
- ✅ **Chatbox** - 完全支持，已验证

### 可能支持（需要配置）
- 🔄 **Claude Desktop** - 支持 MCP，需要配置
- 🔄 **Cherry Studio** - 支持 MCP，需要配置
- 🔄 **Cursor** - 支持 MCP，需要配置
- 🔄 **其他 MCP 客户端** - 理论上都支持

---

## 📋 MCP 协议标准

本服务器完全符合 **Model Context Protocol 2024-11-05** 标准：

- ✅ JSON-RPC 2.0 协议
- ✅ 标准 MCP 方法支持
- ✅ CORS 跨域支持
- ✅ HTTP/HTTPS 传输

### 支持的 MCP 方法

- `initialize` - 初始化连接
- `tools/list` - 获取工具列表
- `tools/call` - 调用工具
- `ping` - 心跳检测
- `notifications/initialized` - 初始化通知

---

## 🔧 配置方式

### 方式一：HTTP Header 配置（推荐）

适用于支持自定义 HTTP Header 的客户端。

**配置项**：
- **URL**: `http://localhost:3000/mcp`
- **HTTP Header**: `X-Yuque-Token: your-token-here`

### 方式二：环境变量配置

适用于服务器部署或命令行工具。

**配置项**：
- **环境变量**: `YUQUE_TOKEN=your-token-here`
- **URL**: `http://localhost:3000/mcp`

---

## 📱 各客户端配置指南

### 1. Chatbox

#### 配置步骤

1. 打开 Chatbox 设置
2. 进入 **MCP Servers** 配置
3. 添加新服务器：
   - **名称**: `Yuque MCP`
   - **URL**: `http://localhost:3000/mcp`
   - **HTTP Headers**:
     ```
     X-Yuque-Token: your-token-here
     ```

#### 验证

在 Chatbox 中调用 `get_user_info` 工具，应该能返回用户信息。

---

### 2. Claude Desktop

#### 配置步骤

1. 打开 Claude Desktop 的 MCP 配置文件
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. 添加服务器配置：

```json
{
  "mcpServers": {
    "yuque": {
      "command": "python3",
      "args": [
        "-m",
        "http.server",
        "3000"
      ],
      "env": {
        "YUQUE_TOKEN": "your-token-here"
      }
    }
  }
}
```

**注意**: Claude Desktop 通常使用 stdio 传输，可能需要额外的适配器。如果您的服务器只支持 HTTP，可能需要使用 HTTP-to-stdio 桥接工具。

---

### 3. Cherry Studio

#### 配置步骤

1. 打开 Cherry Studio 设置
2. 进入 **MCP Servers** 或 **Extensions** 配置
3. 添加 HTTP MCP 服务器：
   - **名称**: `Yuque MCP`
   - **类型**: `HTTP`
   - **URL**: `http://localhost:3000/mcp`
   - **Headers**:
     ```json
     {
       "X-Yuque-Token": "your-token-here"
     }
     ```

#### 验证

在 Cherry Studio 中测试调用 `list_repos` 工具。

---

### 4. Cursor

#### 配置步骤

1. 打开 Cursor 设置
2. 进入 **MCP** 或 **Extensions** 配置
3. 添加服务器：
   - **URL**: `http://localhost:3000/mcp`
   - **Headers**: 
     ```
     X-Yuque-Token: your-token-here
     ```

---

### 5. 其他 MCP 客户端

#### 通用配置

对于任何支持 MCP 的客户端，使用以下配置：

**连接信息**：
- **协议**: HTTP/HTTPS
- **端点**: `http://localhost:3000/mcp`
- **方法**: POST（JSON-RPC 2.0）

**认证方式**（二选一）：
1. HTTP Header: `X-Yuque-Token: your-token-here`
2. 环境变量: `YUQUE_TOKEN=your-token-here`

**示例请求**：

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "X-Yuque-Token: your-token-here" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {
        "name": "test-client",
        "version": "1.0.0"
      }
    }
  }'
```

---

## 🔍 验证连接

### 方法一：健康检查

```bash
curl http://localhost:3000/health
```

**成功响应**：
```json
{
  "status": "healthy",
  "message": "语雀MCP服务器运行正常",
  "user": "your-username",
  "token_source": "header"
}
```

### 方法二：MCP 初始化

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "X-Yuque-Token: your-token-here" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test", "version": "1.0.0"}
    }
  }'
```

**成功响应**：
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {},
      "logs": {},
      "progress": {},
      "readers": {}
    },
    "serverInfo": {
      "name": "yuque-mcp-server",
      "version": "2.0.0"
    }
  }
}
```

### 方法三：获取工具列表

```bash
curl -X POST http://localhost:3000/mcp \
  -H "Content-Type: application/json" \
  -H "X-Yuque-Token: your-token-here" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
```

---

## ⚠️ 常见问题

### 1. 客户端不支持 HTTP MCP

**问题**: 某些客户端（如 Claude Desktop）默认使用 stdio 传输，不支持 HTTP。

**解决方案**:
- 使用 HTTP-to-stdio 桥接工具
- 或等待客户端添加 HTTP 支持
- 或使用支持 HTTP 的客户端（如 Chatbox）

### 2. CORS 错误

**问题**: 浏览器中访问时出现 CORS 错误。

**解决方案**: 
- 服务器已配置 CORS，允许所有来源
- 如果仍有问题，检查客户端是否正确发送请求

### 3. Token 认证失败

**问题**: 返回 401 或 Token 相关错误。

**解决方案**:
- 确认 Token 正确配置
- 检查 HTTP Header 是否正确发送
- 验证环境变量是否正确设置

### 4. 连接被拒绝

**问题**: 无法连接到 `localhost:3000`。

**解决方案**:
- 确认服务器正在运行：`./start_server.sh status`
- 检查端口是否被占用：`lsof -i :3000`
- 确认防火墙设置

---

## 🔄 传输方式说明

### HTTP 传输（当前实现）

- ✅ 支持跨域访问
- ✅ 易于调试和测试
- ✅ 支持多客户端同时连接
- ⚠️ 需要客户端支持 HTTP MCP

### stdio 传输（未来可能支持）

- ✅ 更标准的 MCP 传输方式
- ✅ 更好的性能
- ⚠️ 需要修改服务器实现

---

## 📚 相关资源

- [Model Context Protocol 官方文档](https://modelcontextprotocol.io/)
- [MCP 规范](https://spec.modelcontextprotocol.io/)
- [语雀 Open API 文档](https://www.yuque.com/yuque/developer/api)

---

## 🤝 贡献

如果您在其他客户端中成功配置了本服务器，欢迎提交配置示例！

---

**最后更新**: 2025-11-18

