# 🔧 GitHub 推送问题排查

## 问题：HTTP2 错误或连接超时

### 解决方案 1：使用 SSH（推荐）

如果您的 GitHub 账户已配置 SSH 密钥：

```bash
# 1. 切换到 SSH URL
git remote set-url origin git@github.com:suonian/yuque-mcp-server.git

# 2. 推送代码
git push -u origin main
```

**检查 SSH 密钥**：
```bash
# 检查是否有 SSH 密钥
ls -la ~/.ssh/id_*.pub

# 如果没有，生成新的 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 复制公钥并添加到 GitHub
cat ~/.ssh/id_ed25519.pub
# 然后访问 https://github.com/settings/keys 添加
```

---

### 解决方案 2：使用 Personal Access Token

如果使用 HTTPS，需要使用 Personal Access Token 而不是密码：

```bash
# 1. 生成 Token
# 访问 https://github.com/settings/tokens
# 点击 "Generate new token (classic)"
# 勾选 "repo" 权限
# 复制生成的 Token

# 2. 推送时使用 Token 作为密码
git push -u origin main
# 用户名: suonian
# 密码: <粘贴您的 Token>
```

---

### 解决方案 3：配置 Git 使用 HTTP/1.1

```bash
# 临时禁用 HTTP2（仅当前仓库）
git config http.version HTTP/1.1

# 或全局配置
git config --global http.version HTTP/1.1

# 然后推送
git push -u origin main
```

---

### 解决方案 4：检查网络和代理

```bash
# 检查网络连接
ping github.com

# 如果使用代理，配置 Git 代理
git config --global http.proxy http://proxy.example.com:8080
git config --global https.proxy https://proxy.example.com:8080

# 如果不使用代理，取消代理设置
git config --global --unset http.proxy
git config --global --unset https.proxy
```

---

### 解决方案 5：使用 GitHub CLI

如果安装了 GitHub CLI：

```bash
# 安装 GitHub CLI（如果还没有）
# macOS: brew install gh

# 登录
gh auth login

# 推送代码
git push -u origin main
```

---

## 快速修复脚本

运行以下命令尝试所有方法：

```bash
cd /Users/suonian/Obs/程序/yuque-mcpserver

# 方法 1: 尝试 SSH
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH 已配置，切换到 SSH URL"
    git remote set-url origin git@github.com:suonian/yuque-mcp-server.git
    git push -u origin main
    exit 0
fi

# 方法 2: 使用 HTTP/1.1
echo "尝试使用 HTTP/1.1..."
git config http.version HTTP/1.1
git push -u origin main

# 如果还是失败，请手动使用 Personal Access Token
```

---

## 推荐方案

**最推荐**：使用 SSH 方式
- 更安全
- 不需要每次输入密码
- 连接更稳定

**备选方案**：使用 Personal Access Token
- 如果 SSH 未配置
- 使用 HTTPS 方式

---

**提示**：如果所有方法都失败，可能是网络问题，请检查：
1. 网络连接是否正常
2. 是否使用了 VPN 或代理
3. GitHub 服务是否正常（访问 https://www.githubstatus.com）

