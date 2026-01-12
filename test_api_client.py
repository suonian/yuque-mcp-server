#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

# 设置Python路径
sys.path.insert(0, r'D:\AI Trae\server-yuque')

# 加载环境变量和配置
load_dotenv()

# 测试API客户端
async def test_api_client():
    from yuque_mcp.utils.api_client import YuqueAPIClient
    
    # 使用配置中的token
    token = "w5t3XT8FnrcQTsl6VYEfJd5areDyuPiPoKim31Q3"
    
    try:
        print(f"测试API客户端，Token: {token[:10]}...")
        async with YuqueAPIClient(token) as client:
            print("API客户端创建成功")
            # 测试获取用户信息
            result = await client.get_user_info()
            print(f"获取用户信息成功: {result}")
            return True
    except Exception as e:
        print(f"API客户端测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# 运行测试
import asyncio
if __name__ == "__main__":
    asyncio.run(test_api_client())
