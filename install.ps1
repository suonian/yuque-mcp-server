#!/usr/bin/env powershell

Write-Host "=" * 60
Write-Host "语雀MCP服务器安装脚本"
Write-Host "=" * 60
Write-Host

# 检查Python版本
Write-Host "1. 检查Python环境..."
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 错误：未找到Python，请先安装Python 3.7+"
    exit 1
}

Write-Host "✅ Python版本：$pythonVersion"

# 检查pip
Write-Host "2. 检查pip..."
$pipVersion = pip --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 错误：未找到pip"
    exit 1
}

Write-Host "✅ pip版本：$pipVersion"

# 安装依赖
Write-Host "3. 安装依赖包..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 错误：依赖安装失败"
    exit 1
}

Write-Host "✅ 依赖安装成功"

# 创建配置文件
Write-Host "4. 创建配置文件..."
if (-not (Test-Path "config.json")) {
    Copy-Item "config.example.json" "config.json"
    Write-Host "✅ 已创建config.json配置文件"
    Write-Host "   请编辑config.json或设置YUQUE_TOKEN环境变量"
} else {
    Write-Host "ℹ️  config.json已存在，跳过创建"
}

# 设置环境变量提示
Write-Host "5. 环境变量设置..."
Write-Host "   建议设置YUQUE_TOKEN环境变量："
Write-Host "   方法1：在config.json中配置token字段"
Write-Host "   方法2：运行命令：setx YUQUE_TOKEN "你的语雀token""
Write-Host

# 启动选项
Write-Host "=" * 60
Write-Host "安装完成！"
Write-Host "=" * 60
Write-Host
Write-Host "启动服务："
Write-Host "  1. Claude Code模式：python yuque_mcp/server.py"
Write-Host "  2. HTTP服务器模式：python yuque_mcp/server.py --transport sse"
Write-Host
Write-Host "验证安装："
Write-Host "  在Claude Code中运行：/mcp list"
Write-Host
