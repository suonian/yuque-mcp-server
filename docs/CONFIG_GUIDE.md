# 语雀 MCP 代理配置指南

## 📋 配置方式

语雀 Token 现在支持两种配置方式，按优先级排序：

1. **HTTP Header**（推荐用于 Chatbox）
2. **环境变量**（推荐用于服务器部署）

如果两种方式都未配置，系统会返回明确的错误提示。

---

## 🔧 方式一：HTTP Header 配置（Chatbox）

### 在 Chatbox 中配置

1. 打开 Chatbox 的 MCP Server 配置界面
2. 找到 "HTTP Header" 字段
3. 添加以下配置：

```
X-Yuque-Token=your-token-here
```

**格式说明**：
- 每行一个 Header，格式为 `NAME=VALUE`
- Header 名称：`X-Yuque-Token`
- 值：您的语雀 Token

### 配置示例

```
X-Yuque-Token=your-token-here
```

---

## 🔧 方式二：环境变量配置（服务器部署）

### Linux/macOS

```bash
# 临时设置（当前终端会话）
export YUQUE_TOKEN="your-token-here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export YUQUE_TOKEN="your-token-here"' >> ~/.zshrc
source ~/.zshrc
```

### Windows

```cmd
# 临时设置（当前命令提示符）
set YUQUE_TOKEN=your-token-here

# 永久设置（系统环境变量）
setx YUQUE_TOKEN "your-token-here"
```

### Docker 部署

```bash
# 方式1：命令行参数
docker run -e YUQUE_TOKEN="your-token-here" ...

# 方式2：docker-compose.yml
services:
  yuque-mcp:
    environment:
      - YUQUE_TOKEN=your-token-here
```

---

## ✅ 验证配置

### 方法1：健康检查端点

```bash
# 使用环境变量
curl http://localhost:3000/health

# 使用 HTTP Header
curl -H "X-Yuque-Token: your-token-here" http://localhost:3000/health
```

**成功响应**：
```json
{
  "status": "healthy",
  "message": "语雀MCP服务器运行正常",
  "user": "suonian-offxc",
  "token_source": "header"  // 或 "environment"
}
```

**配置缺失响应**：
```json
{
  "status": "configured",
  "message": "服务器运行正常，但缺少语雀 Token 配置",
  "error": "缺少语雀 Token 配置。请通过以下方式之一提供：..."
}
```

### 方法2：测试 MCP 工具

在 Chatbox 中调用 `get_user_info` 工具，如果配置正确，应该能返回用户信息。

---

## 🔒 安全建议

1. **不要将 Token 提交到代码仓库**
   - 已从代码中移除硬编码的 Token
   - 使用 `.gitignore` 排除包含敏感信息的文件

2. **优先使用环境变量**（服务器部署）
   - 更安全，不会在 HTTP 请求中暴露
   - 便于统一管理

3. **HTTP Header 适合个人使用**（Chatbox）
   - 方便快速配置
   - 每个用户可以使用自己的 Token

4. **定期轮换 Token**
   - 在语雀设置中定期更新 Token
   - 更新后同步更新配置

---

## ❌ 错误处理

### 错误：缺少 Token 配置

**错误信息**：
```
缺少语雀 Token 配置。请通过以下方式之一提供：
1. HTTP Header: X-Yuque-Token
2. 环境变量: YUQUE_TOKEN
```

**解决方法**：
1. 检查 Chatbox 的 HTTP Header 配置
2. 检查服务器环境变量设置
3. 确认 Token 值正确（无多余空格）

### 错误：Token 无效

**错误信息**：
```
语雀 API 请求失败: 401 Unauthorized
```

**解决方法**：
1. 确认 Token 是否正确
2. 检查 Token 是否已过期
3. 在语雀设置中重新生成 Token

---

## 📝 配置优先级

系统按以下顺序查找 Token：

1. ✅ **HTTP Header** (`X-Yuque-Token`) - 最高优先级
2. ✅ **环境变量** (`YUQUE_TOKEN`)
3. ❌ **无默认值** - 如果都未配置，返回错误

---

## 🔄 迁移指南

### 从旧版本迁移

如果您之前使用的是硬编码 Token 的版本：

1. **更新代码**：已自动移除硬编码 Token
2. **选择配置方式**：
   - Chatbox 用户：在 HTTP Header 中配置
   - 服务器部署：设置环境变量
3. **测试验证**：使用健康检查端点验证配置

### 旧代码（已移除）
```python
# ❌ 旧方式（已移除）
YUQUE_TOKEN = "your-token-here"  # 硬编码方式已移除
```

### 新方式
```python
# ✅ 新方式：从 Header 或环境变量读取
token = get_yuque_token()  # 自动处理优先级
```

---

## 📞 技术支持

如有问题，请检查：
1. Token 配置是否正确
2. 服务器日志中的错误信息
3. 健康检查端点的响应

---

**最后更新**: 2025-11-18

