#!/usr/bin/env python3
"""验证语雀MCP服务器"""
import os
import sys

# 设置环境
sys.path.insert(0, 'D:\\AI Trae\\server-yuque')
os.environ['YUQUE_TOKEN'] = 'w5t3XT8FnrcQTsl6VYEfJd5areDyuPiPoKim31Q3'

try:
    from yuque_mcp.server import mcp

    print("=" * 60)
    print("语雀MCP服务器验证工具")
    print("=" * 60)
    print(f"服务器名称: {mcp.name}")
    print(f"版本: {mcp.version}")

    # 获取工具列表
    tools_count = 0

    # 方法1: 检查 _tools
    if hasattr(mcp, '_tools'):
        tools = mcp._tools
        tools_count = len(tools)
        print(f"\\n工具数量 (via _tools): {tools_count}")
        for name in tools:
            print(f"  - {name}")

    # 方法2: 检查 _tool_manager
    if hasattr(mcp, '_tool_manager'):
        tool_manager = mcp._tool_manager
        tools = tool_manager._tools
        tools_count = len(tools)
        print(f"\\n工具数量 (via _tool_manager): {tools_count}")
        for name in tools:
            print(f"  - {name}")

    # 方法3: 使用 mcp.list_tools()
    try:
        import asyncio

        async def list_tools():
            return await mcp.list_tools()

        tools = asyncio.run(list_tools())
        tools_count = len(tools)
        print(f"\\n工具数量 (via list_tools()): {tools_count}")
        for tool in tools:
            print(f"  - {tool.name}")
    except Exception as e:
        print(f"\\n无法通过 list_tools() 获取: {e}")

    if tools_count == 0:
        print("\\n⚠  警告: 未找到任何工具！")
        print("请在Claude Code中运行: /mcp list")
    else:
        print("\\n✓ 验证完成！服务器已准备好使用")
        print("请在Claude Code中运行: /mcp list")

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
