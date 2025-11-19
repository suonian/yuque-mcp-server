#!/bin/bash

# GitHub 发布脚本
# 自动执行发布到 GitHub 的步骤

set -e

echo "=========================================="
echo "🚀 GitHub 发布助手"
echo "=========================================="
echo ""

# 检查是否已配置远程仓库
if git remote | grep -q origin; then
    echo "✅ 远程仓库已配置"
    git remote -v
    echo ""
    echo "直接推送代码..."
    git push -u origin main
    echo ""
    echo "✅ 代码已推送到 GitHub！"
    exit 0
fi

# 如果没有配置远程仓库，提示用户
echo "⚠️  远程仓库尚未配置"
echo ""
echo "请按照以下步骤操作："
echo ""
echo "1. 在 GitHub 上创建新仓库："
echo "   - 访问 https://github.com/new"
echo "   - 仓库名: yuque-mcpserver（或您喜欢的名称）"
echo "   - 不要初始化 README（我们已经有了）"
echo "   - 点击 'Create repository'"
echo ""
echo "2. 获取仓库 URL，然后运行以下命令："
echo ""
echo "   # HTTPS 方式（推荐）"
echo "   git remote add origin https://github.com/YOUR_USERNAME/yuque-mcpserver.git"
echo "   git push -u origin main"
echo ""
echo "   # 或 SSH 方式（如果已配置 SSH 密钥）"
echo "   git remote add origin git@github.com:YOUR_USERNAME/yuque-mcpserver.git"
echo "   git push -u origin main"
echo ""
echo "3. 或者直接运行此脚本，它会提示您输入仓库 URL："
echo ""
read -p "请输入 GitHub 仓库 URL（或按 Enter 跳过）: " repo_url

if [ -z "$repo_url" ]; then
    echo "已跳过，请稍后手动配置"
    exit 0
fi

# 添加远程仓库
git remote add origin "$repo_url"
echo "✅ 远程仓库已添加: $repo_url"
echo ""

# 推送代码
echo "正在推送代码到 GitHub..."
git push -u origin main

echo ""
echo "✅ 发布成功！"
echo ""
echo "您的项目已发布到: $repo_url"

