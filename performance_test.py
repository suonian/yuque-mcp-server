#!/usr/bin/env python3
"""
性能测试脚本，用于比较同步和异步版本的性能差异
"""

import time
import asyncio
import requests
from yuque_client import YuqueMCPClient
from async_yuque_client import AsyncYuqueMCPClient
from cache import cache_manager

# 测试配置
TEST_ITERATIONS = 10
BASE_URL = "http://localhost:5000"
ASYNC_BASE_URL = "http://localhost:8000"

# 测试API端点
TEST_ENDPOINTS = [
    "/api/v2/user",
    "/api/v2/repos",
    "/api/v2/repos/yuque/help/docs",
]


def test_sync_performance():
    """测试同步版本的性能"""
    print("=== 测试同步版本性能 ===")
    total_time = 0
    
    for i in range(TEST_ITERATIONS):
        start_time = time.time()
        for endpoint in TEST_ENDPOINTS:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}")
                response.raise_for_status()
            except Exception as e:
                print(f"❌ 同步请求失败 {endpoint}: {e}")
        iteration_time = time.time() - start_time
        total_time += iteration_time
        print(f"迭代 {i+1}/{TEST_ITERATIONS}: {iteration_time:.3f}秒")
    
    avg_time = total_time / TEST_ITERATIONS
    print(f"平均时间: {avg_time:.3f}秒")
    return avg_time


async def test_async_performance():
    """测试异步版本的性能"""
    print("\n=== 测试异步版本性能 ===")
    total_time = 0
    
    for i in range(TEST_ITERATIONS):
        start_time = time.time()
        tasks = []
        
        for endpoint in TEST_ENDPOINTS:
            tasks.append(fetch_async(f"{ASYNC_BASE_URL}{endpoint}"))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        iteration_time = time.time() - start_time
        total_time += iteration_time
        print(f"迭代 {i+1}/{TEST_ITERATIONS}: {iteration_time:.3f}秒")
    
    avg_time = total_time / TEST_ITERATIONS
    print(f"平均时间: {avg_time:.3f}秒")
    return avg_time


async def fetch_async(url):
    """异步请求函数"""
    import httpx
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"❌ 异步请求失败 {url}: {e}")
        return None


if __name__ == "__main__":
    # 先测试缓存性能
    print("=== 测试缓存性能 ===")
    
    # 创建客户端实例
    token = "test-token"
    sync_client = YuqueMCPClient(token)
    async_client = AsyncYuqueMCPClient(token)
    
    # 清空缓存
    cache_manager.clear()
    
    # 第一次请求（缓存未命中）
    print("\n1. 第一次请求（缓存未命中）:")
    start_time = time.time()
    try:
        sync_client.get_user_info()
        elapsed = time.time() - start_time
        print(f"   同步请求时间: {elapsed:.3f}秒")
    except Exception as e:
        print(f"   同步请求失败: {e}")
    
    # 第二次请求（缓存命中）
    print("\n2. 第二次请求（缓存命中）:")
    start_time = time.time()
    try:
        sync_client.get_user_info()
        elapsed = time.time() - start_time
        print(f"   同步请求时间: {elapsed:.3f}秒")
    except Exception as e:
        print(f"   同步请求失败: {e}")
    
    # 显示缓存统计
    stats = cache_manager.get_stats()
    print(f"\n3. 缓存统计:")
    print(f"   命中次数: {stats['hit_count']}")
    print(f"   未命中次数: {stats['miss_count']}")
    print(f"   命中率: {stats['hit_rate']}%")
    
    print("\n=== 性能测试完成 ===")
