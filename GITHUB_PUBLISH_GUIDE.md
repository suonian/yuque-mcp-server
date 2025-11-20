# 🚀 GitHub 发布指南

本指南将帮助您将项目发布到 GitHub。

---

## ✅ 本地 Git 仓库已初始化

本地 Git 仓库已创建并完成初始提交。

---

## 📋 发布步骤

### 步骤 1: 在 GitHub 上创建仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 **"+"** → **"New repository"**
3. 填写仓库信息：
   - **Repository name**: `yuque-mcpserver`（或您喜欢的名称）
   - **Description**: `语雀 Model Context Protocol (MCP) 代理服务器 - 让 AI 助手通过 MCP 协议与语雀平台交互`
   - **Visibility**: 选择 **Public**（公开）或 **Private**（私有）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
4. 点击 **"Create repository"**

---

### 步骤 2: 添加远程仓库并推送

在项目目录中执行以下命令：

```bash
cd /Users/suonian/Obs/程序/yuque-mcpserver

# 添加远程仓库（将 YOUR_USERNAME 替换为您的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/yuque-mcpserver.git

# 或者使用 SSH（如果您配置了 SSH 密钥）
# git remote add origin git@github.com:YOUR_USERNAME/yuque-mcpserver.git

# 重命名主分支为 main（如果还没有）
git branch -M main

# 推送代码到 GitHub
git push -u origin main
```

---

### 步骤 3: 验证发布

1. 访问您的 GitHub 仓库页面
2. 确认所有文件都已上传
3. 检查 README.md 是否正确显示

---

## 🔧 如果遇到问题

### 问题 1: 需要身份验证

如果推送时要求输入用户名和密码：

**解决方案 1**: 使用 Personal Access Token（推荐）
1. 访问 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 生成新 Token，勾选 `repo` 权限
3. 推送时使用 Token 作为密码

**解决方案 2**: 配置 SSH 密钥
```bash
# 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 复制输出，添加到 GitHub Settings → SSH and GPG keys
```

### 问题 2: 远程仓库已存在内容

如果 GitHub 仓库已初始化（有 README 等文件）：

```bash
# 先拉取远程内容
git pull origin main --allow-unrelated-histories

# 解决可能的冲突后，再推送
git push -u origin main
```

---

## 📝 发布后的建议

### 1. 添加 LICENSE

建议添加 MIT License：

```bash
# 创建 LICENSE 文件
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 提交 LICENSE
git add LICENSE
git commit -m "Add MIT License"
git push
```

### 2. 添加 GitHub Topics

在仓库页面点击 ⚙️ Settings → Topics，添加：
- `mcp`
- `model-context-protocol`
- `yuque`
- `api-proxy`
- `docker`
- `python`
- `flask`

### 3. 添加 GitHub Actions（可选）

可以添加 CI/CD 配置，自动测试和部署。

### 4. 创建 Release

当准备发布版本时：
1. 在仓库页面点击 **"Releases"** → **"Create a new release"**
2. 填写版本号（如 `v1.0.0`）
3. 添加发布说明
4. 发布

---

## 🎉 完成！

发布成功后，您的项目将在 GitHub 上可见，其他用户可以：
- 克隆仓库
- 查看文档
- 提交 Issue
- 提交 Pull Request

---

**提示**: 如果遇到任何问题，请查看 GitHub 的官方文档或联系我。

