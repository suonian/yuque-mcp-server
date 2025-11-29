#!/usr/bin/env python3
"""
缓存管理模块测试
重点验证Redis缓存功能的正确性和性能
"""

import time
import unittest
import threading
from cache import CacheManager, generate_cache_key


class TestCacheManager(unittest.TestCase):
    """测试缓存管理器"""
    
    def setUp(self):
        """设置测试环境"""
        self.cache_manager = CacheManager()
        # 清空缓存，确保测试环境干净
        self.cache_manager.clear()
    
    def test_cache_basic_operations(self):
        """测试缓存基本操作：设置、获取、删除"""
        # 测试数据
        test_key = "test:key"
        test_value = {"name": "test", "value": 123}
        
        # 设置缓存
        self.cache_manager.set(test_key, test_value)
        
        # 获取缓存
        result = self.cache_manager.get(test_key)
        self.assertEqual(result, test_value, "缓存获取失败")
        
        # 删除缓存
        self.cache_manager.delete(test_key)
        result = self.cache_manager.get(test_key)
        self.assertIsNone(result, "缓存删除失败")
    
    def test_cache_expire(self):
        """测试缓存过期策略"""
        # 测试数据
        test_key = "test:expire:key"
        test_value = {"name": "test", "value": 123}
        
        # 设置缓存，过期时间为2秒
        self.cache_manager.set(test_key, test_value, expire=2)
        
        # 立即获取，应该存在
        result = self.cache_manager.get(test_key)
        self.assertEqual(result, test_value, "缓存设置后立即获取失败")
        
        # 等待3秒，缓存应该过期
        time.sleep(3)
        result = self.cache_manager.get(test_key)
        self.assertIsNone(result, "缓存过期失败")
    
    def test_cache_pattern_delete(self):
        """测试按模式删除缓存"""
        # 设置多个缓存项
        self.cache_manager.set("test:user:1", {"id": 1, "name": "user1"})
        self.cache_manager.set("test:user:2", {"id": 2, "name": "user2"})
        self.cache_manager.set("test:repo:1", {"id": 1, "name": "repo1"})
        
        # 按模式删除用户相关缓存
        self.cache_manager.delete_pattern("test:user:*")
        
        # 验证用户缓存已删除，仓库缓存仍存在
        self.assertIsNone(self.cache_manager.get("test:user:1"), "用户1缓存未删除")
        self.assertIsNone(self.cache_manager.get("test:user:2"), "用户2缓存未删除")
        self.assertIsNotNone(self.cache_manager.get("test:repo:1"), "仓库缓存不应被删除")
    
    def test_cache_stats(self):
        """测试缓存统计功能"""
        # 测试数据
        test_key = "test:stats:key"
        test_value = {"name": "test"}
        
        # 第一次获取，应该未命中
        self.cache_manager.get(test_key)
        
        # 设置缓存
        self.cache_manager.set(test_key, test_value)
        
        # 第二次获取，应该命中
        self.cache_manager.get(test_key)
        self.cache_manager.get(test_key)
        
        # 获取统计信息
        stats = self.cache_manager.get_stats()
        
        # 验证统计信息
        self.assertEqual(stats["hit_count"], 2, "命中次数统计错误")
        self.assertEqual(stats["miss_count"], 1, "未命中次数统计错误")
        self.assertEqual(stats["total_count"], 3, "总次数统计错误")
        self.assertEqual(stats["hit_rate"], 66.67, "命中率计算错误")
    
    def test_cache_key_generation(self):
        """测试缓存键生成函数"""
        # 测试基本键生成
        key1 = generate_cache_key("yuque", "repo", id=123)
        self.assertEqual(key1, "yuque:repo:id=123", "缓存键生成错误")
        
        # 测试多个参数
        key2 = generate_cache_key("yuque", "doc", repo="test-repo", slug="test-doc")
        self.assertEqual(key2, "yuque:doc:repo=test-repo:slug=test-doc", "多参数缓存键生成错误")
        
        # 测试参数排序
        key3 = generate_cache_key("yuque", "search", q="test", page=1, per_page=20)
        self.assertEqual(key3, "yuque:search:page=1:per_page=20:q=test", "参数排序错误")
    
    def test_cache_clear(self):
        """测试清空缓存功能"""
        # 设置多个缓存项
        self.cache_manager.set("test:key1", {"value": 1})
        self.cache_manager.set("test:key2", {"value": 2})
        self.cache_manager.set("test:key3", {"value": 3})
        
        # 验证缓存存在
        self.assertIsNotNone(self.cache_manager.get("test:key1"))
        self.assertIsNotNone(self.cache_manager.get("test:key2"))
        self.assertIsNotNone(self.cache_manager.get("test:key3"))
        
        # 清空缓存
        self.cache_manager.clear()
        
        # 验证缓存已清空
        self.assertIsNone(self.cache_manager.get("test:key1"))
        self.assertIsNone(self.cache_manager.get("test:key2"))
        self.assertIsNone(self.cache_manager.get("test:key3"))
    
    def test_cache_penetration_protection(self):
        """测试缓存穿透防护机制"""
        # 测试不存在的键，验证不会导致缓存穿透
        non_existent_key = "test:non_existent:key"
        
        # 多次获取不存在的键
        for _ in range(5):
            result = self.cache_manager.get(non_existent_key)
            self.assertIsNone(result, "不存在的键应返回None")
        
        # 验证统计信息
        stats = self.cache_manager.get_stats()
        self.assertEqual(stats["miss_count"], 5, "缓存穿透防护失败")
    
    def test_cache_concurrency(self):
        """测试高并发场景下的缓存性能"""
        test_key = "test:concurrency:key"
        test_value = {"name": "test", "value": 123}
        
        # 设置初始缓存
        self.cache_manager.set(test_key, test_value)
        
        # 并发获取缓存的线程数
        thread_count = 50
        # 每个线程获取缓存的次数
        get_count = 100
        
        # 线程执行函数
        def thread_func():
            for _ in range(get_count):
                result = self.cache_manager.get(test_key)
                self.assertEqual(result, test_value, "并发获取缓存失败")
        
        # 创建并启动线程
        threads = []
        start_time = time.time()
        
        for _ in range(thread_count):
            t = threading.Thread(target=thread_func)
            threads.append(t)
            t.start()
        
        # 等待所有线程完成
        for t in threads:
            t.join()
        
        end_time = time.time()
        total_requests = thread_count * get_count
        
        # 验证统计信息
        stats = self.cache_manager.get_stats()
        self.assertEqual(stats["hit_count"], total_requests, "并发场景下缓存命中率错误")
        
        # 输出性能指标
        print(f"\n高并发测试结果:")
        print(f"  线程数: {thread_count}")
        print(f"  总请求数: {total_requests}")
        print(f"  总耗时: {end_time - start_time:.2f}秒")
        print(f"  QPS: {total_requests / (end_time - start_time):.2f}")
    
    def test_cache_data_types(self):
        """测试不同数据类型的缓存支持"""
        # 测试字符串
        self.cache_manager.set("test:string", "test_value")
        self.assertEqual(self.cache_manager.get("test:string"), "test_value", "字符串类型缓存失败")
        
        # 测试数字
        self.cache_manager.set("test:number", 123)
        self.assertEqual(self.cache_manager.get("test:number"), 123, "数字类型缓存失败")
        
        # 测试布尔值
        self.cache_manager.set("test:boolean", True)
        self.assertEqual(self.cache_manager.get("test:boolean"), True, "布尔值类型缓存失败")
        
        # 测试列表
        self.cache_manager.set("test:list", [1, 2, 3, 4, 5])
        self.assertEqual(self.cache_manager.get("test:list"), [1, 2, 3, 4, 5], "列表类型缓存失败")
        
        # 测试字典
        self.cache_manager.set("test:dict", {"name": "test", "age": 18})
        self.assertEqual(self.cache_manager.get("test:dict"), {"name": "test", "age": 18}, "字典类型缓存失败")
    
    def test_cache_error_handling(self):
        """测试缓存错误处理机制"""
        # 测试无效键
        result = self.cache_manager.get(None)
        self.assertIsNone(result, "无效键处理失败")
        
        # 测试无效值
        self.cache_manager.set("test:invalid", object())
        result = self.cache_manager.get("test:invalid")
        # 应该返回None或抛出异常，但不应导致程序崩溃
    
    def tearDown(self):
        """清理测试环境"""
        # 清空缓存
        self.cache_manager.clear()


if __name__ == '__main__':
    unittest.main(verbosity=2)
