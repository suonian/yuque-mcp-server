#!/usr/bin/env python3
"""
缓存管理模块
使用Redis作为缓存存储，实现API响应的缓存管理
"""

import json
import logging
from typing import Any, Optional, Dict
from config import CONFIG

# 尝试导入redis，如果失败则使用内存缓存
redis = None
try:
    import redis
except ImportError:
    logging.warning("❌ Redis模块未安装，将使用内存缓存作为备选方案")


logger = logging.getLogger(__name__)


class CacheManager:
    """缓存管理器，负责与Redis交互"""
    
    def __init__(self):
        """初始化缓存管理器"""
        self.redis_client = None
        self.memory_cache: Dict[str, Any] = {}
        
        # 从配置中获取Redis连接信息
        self.redis_url = CONFIG.get("REDIS_URL", "redis://localhost:6379/0")
        
        # 只有当redis模块可用时，才尝试连接Redis
        if redis:
            try:
                self.redis_client = redis.from_url(self.redis_url)
                # 测试Redis连接
                self.redis_client.ping()
                logger.info(f"✅ 成功连接到Redis: {self.redis_url}")
            except redis.ConnectionError as e:
                logger.warning(f"❌ Redis连接失败: {e}")
                logger.warning("⚠️ 将使用内存缓存作为备选方案")
                self.redis_client = None
            except Exception as e:
                logger.warning(f"❌ Redis初始化失败: {e}")
                logger.warning("⚠️ 将使用内存缓存作为备选方案")
                self.redis_client = None
        else:
            logger.info("⚠️ Redis模块未安装，将使用内存缓存")
        
        # 缓存统计
        self.hit_count = 0
        self.miss_count = 0
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存值
        
        Args:
            key: 缓存键
            
        Returns:
            缓存值，如果不存在则返回None
        """
        try:
            if self.redis_client:
                # 使用Redis缓存
                value = self.redis_client.get(key)
                if value:
                    self.hit_count += 1
                    return json.loads(value)
                else:
                    self.miss_count += 1
                    return None
            else:
                # 使用内存缓存
                if key in self.memory_cache:
                    self.hit_count += 1
                    return self.memory_cache[key]
                else:
                    self.miss_count += 1
                    return None
        except Exception as e:
            logger.error(f"获取缓存失败: {e}")
            self.miss_count += 1
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600) -> None:
        """设置缓存值
        
        Args:
            key: 缓存键
            value: 缓存值
            expire: 过期时间（秒），默认3600秒
        """
        try:
            if self.redis_client:
                # 使用Redis缓存
                self.redis_client.set(key, json.dumps(value), ex=expire)
            else:
                # 使用内存缓存
                self.memory_cache[key] = value
        except Exception as e:
            logger.error(f"设置缓存失败: {e}")
    
    def delete(self, key: str) -> None:
        """删除缓存值
        
        Args:
            key: 缓存键
        """
        try:
            if self.redis_client:
                # 使用Redis缓存
                self.redis_client.delete(key)
            else:
                # 使用内存缓存
                if key in self.memory_cache:
                    del self.memory_cache[key]
        except Exception as e:
            logger.error(f"删除缓存失败: {e}")
    
    def delete_pattern(self, pattern: str) -> None:
        """删除匹配模式的缓存值
        
        Args:
            pattern: 匹配模式，如 "yuque:repo:*"
        """
        try:
            if self.redis_client:
                # 使用Redis缓存
                keys = self.redis_client.keys(pattern)
                if keys:
                    self.redis_client.delete(*keys)
            else:
                # 使用内存缓存
                keys_to_delete = [key for key in self.memory_cache if pattern.replace("*", "") in key]
                for key in keys_to_delete:
                    del self.memory_cache[key]
        except Exception as e:
            logger.error(f"删除匹配缓存失败: {e}")
    
    def get_stats(self) -> Dict[str, int]:
        """获取缓存统计信息
        
        Returns:
            缓存统计字典，包含命中次数、未命中次数和命中率
        """
        total = self.hit_count + self.miss_count
        hit_rate = round(self.hit_count / total * 100, 2) if total > 0 else 0
        return {
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "total_count": total,
            "hit_rate": hit_rate
        }
    
    def clear(self) -> None:
        """清空所有缓存"""
        try:
            if self.redis_client:
                # 使用Redis缓存
                self.redis_client.flushdb()
            else:
                # 使用内存缓存
                self.memory_cache.clear()
            logger.info("✅ 缓存已清空")
        except Exception as e:
            logger.error(f"清空缓存失败: {e}")


# 创建全局缓存管理器实例
cache_manager = CacheManager()


# 缓存键生成函数
def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """生成缓存键
    
    Args:
        prefix: 缓存前缀
        *args: 位置参数，用于生成缓存键
        **kwargs: 关键字参数，用于生成缓存键
        
    Returns:
        生成的缓存键
    """
    key_parts = [prefix]
    
    # 添加位置参数
    for arg in args:
        key_parts.append(str(arg))
    
    # 添加关键字参数，按字母顺序排序
    for key, value in sorted(kwargs.items()):
        key_parts.append(f"{key}={value}")
    
    return ":".join(key_parts)
