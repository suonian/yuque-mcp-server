# 🚀 GitHub 更新指南

## 📋 更新步骤

### 1. 检查更改

```bash
cd /Users/suonian/mcp/yuque-mcpserver
git status
```

### 2. 查看更改内容

```bash
git diff
```

### 3. 提交更改

```bash
git add .
git commit -m "feat: v1.1.0 - 增强文档查询和搜索功能"
```

### 4. 推送到 GitHub

```bash
# 如果是首次推送
git push -u origin main

# 或者强制推送（如果远程有冲突）
git push -u origin main --force
```

### 5. 创建 Release

1. 访问: https://github.com/suonian/yuque-mcp-server/releases/new
2. Tag: `v1.1.0`
3. Title: `v1.1.0 - 增强文档查询和搜索功能`
4. Description: 复制 `GITHUB_RELEASE_TEMPLATE.md` 的内容并更新版本号

## 📝 本次更新内容

### v1.1.0 (2025-11-20)

#### ✨ 新增功能
- `get_doc` 自动获取并显示知识库归属信息
- 文档返回包含完整元数据
- 新增 `get_doc_by_id` 工具

#### 🔧 改进
- 修复搜索API数据结构解析
- 增强错误处理
- 改进搜索结果展示

#### 🐛 修复
- 修复无法提取 namespace 和 slug 的问题
- 修复知识库信息显示问题

## ✅ 检查清单

- [x] 所有文件已提交
- [x] README.md 已更新
- [x] CHANGELOG.md 已创建
- [x] 文档已整理
- [x] .gitignore 配置正确
- [ ] 推送到 GitHub
- [ ] 创建 Release

