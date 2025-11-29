# 🐳 Docker 部署指南

本指南说明如何使用 Docker 部署和运行语雀 MCP 代理服务器。

## ✅ 优势

- ✅ **环境隔离** - 不污染主机环境
- ✅ **易于部署** - 一键启动，无需配置 Python 环境
- ✅ **跨平台** - 在任何支持 Docker 的系统上运行
- ✅ **自动验证** - 内置健康检查和测试脚本

---

## 📋 前置要求

- Docker 20.10+ 或 Docker Desktop
- 语雀 Token（用于 API 调用）

---

## 🚀 快速开始

### 方式一：使用 Docker Compose（推荐）

```bash
# 1. 设置 Token（可选，也可以通过 HTTP Header 提供）
export YUQUE_TOKEN=your-token-here

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

### 方式二：使用 Docker 命令

```bash
# 1. 构建镜像
docker build -t yuque-mcp .

# 2. 运行容器
docker run -d \
  --name yuque-mcp-server \
  -p 3000:3000 \
  -e YUQUE_TOKEN=your-token-here \
  yuque-mcp

# 3. 查看日志
docker logs -f yuque-mcp-server

# 4. 停止容器
docker stop yuque-mcp-server
docker rm yuque-mcp-server
```

---

## 🧪 自动功能验证

您可以使用项目中的集成测试脚本来验证功能：

```bash
# 设置 Token
export YUQUE_TOKEN=your-token-here

# 运行集成测试
python3 test_api_integration.py
```

### 测试内容

集成测试会验证：

1. ✅ 健康检查端点
2. ✅ 用户信息获取
3. ✅ 知识库列表
4. ✅ 文档列表
5. ✅ 文档内容获取
6. ✅ 搜索功能
7. ✅ 团队管理功能

---

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `YUQUE_TOKEN` | 语雀 API Token | 是* | - |
| `PORT` | 服务端口 | 否 | 3000 |

*注：Token 也可以通过 HTTP Header (`X-Yuque-Token`) 提供

### 配置文件

如果需要使用配置文件，可以挂载 `yuque-config.env`：

```bash
docker run -d \
  --name yuque-mcp-server \
  -p 3000:3000 \
  -v $(pwd)/yuque-config.env:/app/yuque-config.env:ro \
  yuque-mcp
```

---

## 📊 健康检查

Docker 镜像内置了健康检查：

```bash
# 查看健康状态
docker ps

# 手动健康检查
docker exec yuque-mcp-server curl -f http://localhost:3000/health
```

---

## 🔍 日志管理

### 查看日志

```bash
# 实时日志
docker logs -f yuque-mcp-server

# 最近 100 行
docker logs --tail 100 yuque-mcp-server

# 带时间戳
docker logs -f -t yuque-mcp-server
```

### 日志位置

容器内日志输出到标准输出，可以通过 Docker 日志查看。

---

## 🔄 更新和重启

### 更新镜像

```bash
# 1. 停止并删除旧容器
docker-compose down

# 2. 重新构建镜像
docker-compose build --no-cache

# 3. 启动新容器
docker-compose up -d
```

### 重启服务

```bash
# 使用 docker-compose
docker-compose restart

# 使用 docker 命令
docker restart yuque-mcp-server
```

---

## 🐛 故障排查

### 容器无法启动

```bash
# 查看容器日志
docker logs yuque-mcp-server

# 检查容器状态
docker ps -a | grep yuque-mcp-server
```

### 端口被占用

```bash
# 检查端口占用
netstat -ano | grep 3000  # Linux/macOS
netstat -ano | findstr 3000  # Windows

# 修改端口映射
docker run -d \
  --name yuque-mcp-server \
  -p 3001:3000 \  # 使用 3001 端口
  -e YUQUE_TOKEN=your-token \
  yuque-mcp
```

### Token 配置问题

```bash
# 检查环境变量
docker exec yuque-mcp-server env | grep YUQUE_TOKEN

# 测试健康检查
curl http://localhost:3000/health
```

---

## 📦 生产环境部署

### 使用 Docker Compose

创建 `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  yuque-mcp:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: yuque-mcp-server
    ports:
      - "3000:3000"
    environment:
      - PORT=3000
      - YUQUE_TOKEN=${YUQUE_TOKEN}
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

启动：

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 使用 Docker Swarm

```bash
# 创建服务
docker service create \
  --name yuque-mcp \
  --publish 3000:3000 \
  --env YUQUE_TOKEN=your-token \
  --replicas 1 \
  yuque-mcp
```

---

## 🔒 安全建议

1. **不要将 Token 硬编码在镜像中**
   - 使用环境变量或配置文件
   - 使用 Docker secrets（Docker Swarm）

2. **限制网络访问**
   ```bash
   # 只允许本地访问
   docker run -d \
     --name yuque-mcp-server \
     -p 127.0.0.1:3000:3000 \
     -e YUQUE_TOKEN=your-token \
     yuque-mcp
   ```

3. **使用非 root 用户**
   - 镜像已配置非 root 用户运行

4. **定期更新镜像**
   - 定期拉取最新镜像
   - 检查安全更新

---

## 📚 相关文档

- [`QUICK_START.md`](QUICK_START.md) - 快速开始指南
- [`CONFIG_GUIDE.md`](CONFIG_GUIDE.md) - 配置指南
- [`CLIENT_COMPATIBILITY.md`](CLIENT_COMPATIBILITY.md) - 客户端兼容性指南

---

## 🤝 贡献

如果您在使用 Docker 部署时遇到问题，欢迎提交 Issue！

---

**最后更新**: 2025-11-18

