import os
import tempfile
import unittest
from config import load_config


class TestConfig(unittest.TestCase):
    """测试配置模块"""
    
    def test_load_config_with_valid_file(self):
        """测试加载有效的配置文件"""
        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("""# 测试配置文件
YUQUE_TOKEN=test-token
PORT=8000
DEFAULT_CORS_ORIGIN=https://example.com
""")
            temp_config_file = f.name
        
        try:
            # 保存原始配置文件路径
            original_dir = os.getcwd()
            
            # 切换到临时目录
            temp_dir = os.path.dirname(temp_config_file)
            os.chdir(temp_dir)
            
            # 修改配置文件名为yuque-config.env
            os.rename(temp_config_file, os.path.join(temp_dir, 'yuque-config.env'))
            
            # 加载配置
            config = load_config()
            
            # 验证配置
            self.assertEqual(config.get('YUQUE_TOKEN'), 'test-token')
            self.assertEqual(config.get('PORT'), '8000')
            self.assertEqual(config.get('DEFAULT_CORS_ORIGIN'), 'https://example.com')
        finally:
            # 清理
            os.chdir(original_dir)
            if os.path.exists(os.path.join(temp_dir, 'yuque-config.env')):
                os.remove(os.path.join(temp_dir, 'yuque-config.env'))
    
    def test_load_config_without_file(self):
        """测试当配置文件不存在时的情况"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            original_dir = os.getcwd()
            os.chdir(temp_dir)
            
            # 加载配置
            config = load_config()
            
            # 验证配置为空
            self.assertEqual(len(config), 0)
            
            # 清理
            os.chdir(original_dir)
    
    def test_load_config_with_comments(self):
        """测试加载包含注释的配置文件"""
        # 创建临时配置文件
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write("""# 主配置
YUQUE_TOKEN=test-token

# 端口配置
PORT=8000

# 这是一个注释行
DEFAULT_CORS_ORIGIN=*
""")
            temp_config_file = f.name
        
        try:
            # 保存原始配置文件路径
            original_dir = os.getcwd()
            
            # 切换到临时目录
            temp_dir = os.path.dirname(temp_config_file)
            os.chdir(temp_dir)
            
            # 修改配置文件名为yuque-config.env
            os.rename(temp_config_file, os.path.join(temp_dir, 'yuque-config.env'))
            
            # 加载配置
            config = load_config()
            
            # 验证配置
            self.assertEqual(config.get('YUQUE_TOKEN'), 'test-token')
            self.assertEqual(config.get('PORT'), '8000')
            self.assertEqual(config.get('DEFAULT_CORS_ORIGIN'), '*')
        finally:
            # 清理
            os.chdir(original_dir)
            if os.path.exists(os.path.join(temp_dir, 'yuque-config.env')):
                os.remove(os.path.join(temp_dir, 'yuque-config.env'))


if __name__ == '__main__':
    unittest.main()
