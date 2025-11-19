#!/bin/bash

# 安装语雀 MCP 代理为系统服务（macOS launchd）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_NAME="com.yuque.mcp.plist"
PLIST_SOURCE="$SCRIPT_DIR/$PLIST_NAME"
PLIST_DEST="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "📦 安装语雀 MCP 代理服务..."

# 检查 plist 文件是否存在
if [ ! -f "$PLIST_SOURCE" ]; then
    echo "❌ 错误: 找不到 $PLIST_SOURCE"
    exit 1
fi

# 更新 plist 文件中的路径占位符
echo "🔧 更新服务配置路径..."
# 创建临时副本进行修改，避免修改源文件
PLIST_TEMP=$(mktemp)
sed "s|__SCRIPT_DIR__|$SCRIPT_DIR|g" "$PLIST_SOURCE" > "$PLIST_TEMP"
mv "$PLIST_TEMP" "$PLIST_SOURCE"

# 复制到 LaunchAgents 目录
if [ ! -d "$HOME/Library/LaunchAgents" ]; then
    mkdir -p "$HOME/Library/LaunchAgents"
fi

cp "$PLIST_SOURCE" "$PLIST_DEST"
echo "✅ 已复制服务配置到: $PLIST_DEST"

# 加载服务
echo "🚀 加载服务..."
launchctl unload "$PLIST_DEST" 2>/dev/null
launchctl load "$PLIST_DEST"

if [ $? -eq 0 ]; then
    echo "✅ 服务安装成功！"
    echo ""
    echo "服务管理命令:"
    echo "  启动: launchctl start com.yuque.mcp"
    echo "  停止: launchctl stop com.yuque.mcp"
    echo "  状态: launchctl list | grep com.yuque.mcp"
    echo "  卸载: launchctl unload $PLIST_DEST && rm $PLIST_DEST"
    echo ""
    echo "查看日志:"
    echo "  tail -f /tmp/yuque-proxy.log"
else
    echo "❌ 服务加载失败"
    exit 1
fi

