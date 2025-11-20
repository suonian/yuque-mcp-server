# 🚀 Release v1.1.0 - 增强文档查询和搜索功能

**发布日期**: 2025-11-20  
**版本**: v1.1.0

---

## 🎉 版本亮点

本次更新主要增强了文档查询和搜索功能，修复了搜索API数据结构解析问题，让用户能够更方便地获取文档完整信息。

---

## ✨ 新增功能

### 1. 增强文档查询功能

- **自动获取知识库信息**
  - `get_doc` 工具现在自动获取并显示知识库归属信息
  - 包含知识库名称、命名空间、类型、所有者、可见性等完整信息

- **完整元数据展示**
  - 文档返回包含创建者、阅读数、点赞数、评论数等统计信息
  - 显示完整的访问路径和使用方法
  - 内容完整性检测（完整内容/仅预览）

### 2. 新增 `get_doc_by_id` 工具

- 提供友好的错误提示和使用建议
- 明确说明语雀API的限制
- 引导用户使用正确的方式获取文档

---

## 🔧 改进

### 1. 修复搜索功能

- **修复数据结构解析问题**
  - 正确从语雀搜索API的 `target` 字段提取数据
  - 修复知识库信息显示为"未知"的问题
  - 修复无法提取 namespace 和 slug 的问题

- **改进搜索结果展示**
  - 搜索结果中直接显示完整路径和使用方法
  - 显示文档统计信息（阅读数、点赞数）
  - 处理信息缺失情况，提供友好的提示和替代方案

### 2. 增强错误处理

- 实现标准化的 MCP 错误码扩展（-32001 到 -32009）
- 根据HTTP状态码返回明确的错误码和解决建议
- 增强日志记录，包含详细的调试信息

### 3. 优化文档内容获取

- 添加内容完整性检测
- 当权限不足时提供明确的提示和解决建议
- 显示内容长度信息

---

## 🐛 修复

1. **修复搜索API数据结构解析**
   - 修复从 `item.get('book')` 读取数据的问题
   - 正确从 `item.get('target', {}).get('book', {})` 提取信息

2. **修复搜索结果展示**
   - 修复知识库信息显示为"未知"的问题
   - 修复无法获取完整路径的问题

3. **修复文档内容获取**
   - 改进权限不足时的错误提示
   - 优化内容完整性检测逻辑

---

## 📊 技术改进

### 代码质量

- 增强错误处理和日志记录
- 改进代码结构和可维护性
- 优化API调用逻辑

### 文档完善

- 新增 `CHANGELOG.md` 更新日志
- 更新 `README.md` 包含最新功能
- 整理故障排查文档到 `docs/troubleshooting/`

---

## 🚀 升级指南

### 从 v1.0.0 升级

1. **拉取最新代码**
   ```bash
   git pull origin main
   ```

2. **重启服务**
   ```bash
   ./start_server.sh restart
   ```

3. **验证功能**
   ```bash
   curl http://localhost:3000/health
   ```

### Docker 部署

```bash
# 拉取最新镜像
docker-compose pull

# 重启服务
docker-compose up -d
```

---

## 📝 使用示例

### 搜索并获取文档

```python
# 1. 搜索文档
search_docs(query="美团闪购")

# 2. 从搜索结果中获取完整路径
# 搜索结果会显示：
#   🔗 完整路径: your-username/poto7v/xchphoy1k7qofodp
#   💡 使用方法: get_doc(namespace="your-username/poto7v", slug="xchphoy1k7qofodp")

# 3. 获取完整文档（自动包含知识库信息）
get_doc(namespace="your-username/poto7v", slug="xchphoy1k7qofodp")
```

---

## 📚 相关文档

- [CHANGELOG.md](CHANGELOG.md) - 完整更新日志
- [README.md](README.md) - 项目文档
- [docs/troubleshooting/](docs/troubleshooting/) - 故障排查文档

---

## 🙏 致谢

感谢所有用户的使用和反馈，特别是对搜索和文档获取功能的建议。

---

**下载**: [v1.1.0](https://github.com/suonian/yuque-mcp-server/releases/tag/v1.1.0)  
**完整变更**: [CHANGELOG.md](CHANGELOG.md)

