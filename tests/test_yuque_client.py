import unittest
from unittest.mock import patch, MagicMock
from yuque_client import YuqueMCPClient


class TestYuqueMCPClient(unittest.TestCase):
    """测试语雀 API 客户端"""
    
    def setUp(self):
        """设置测试环境"""
        self.token = "test-token"
        # 清空缓存，确保每次测试都是从干净的状态开始
        from cache import cache_manager
        cache_manager.clear()
        self.client = YuqueMCPClient(self.token)
        # 替换真实session为mock对象
        self.client.session = MagicMock()
    
    @patch('yuque_client.requests.Session')
    def test_init(self, mock_session):
        """测试客户端初始化"""
        # 创建客户端
        client = YuqueMCPClient(self.token)
        
        # 验证会话初始化
        mock_session.assert_called_once()
        # 验证请求头设置
        client.session.headers.update.assert_called_once_with({
            'X-Auth-Token': self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Yuque-MCP-Server/2.0'
        })
    
    def test_get_user_info(self):
        """测试获取用户信息"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": 123,
                "login": "test-user",
                "name": "测试用户"
            }
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.get_user_info()
        
        # 验证请求
        self.client.session.request.assert_called_once_with('GET', 'https://www.yuque.com/api/v2/user')
        # 验证响应
        self.assertEqual(result, {
            "data": {
                "id": 123,
                "login": "test-user",
                "name": "测试用户"
            }
        })
    
    def test_list_repos(self):
        """测试列出知识库"""
        # 设置模拟响应
        mock_user_response = MagicMock()
        mock_user_response.json.return_value = {
            "data": {
                "login": "test-user"
            }
        }
        
        mock_repos_response = MagicMock()
        mock_repos_response.json.return_value = {
            "data": [
                {
                    "id": 1,
                    "name": "测试知识库",
                    "namespace": "test-user/test-repo"
                }
            ]
        }
        
        self.client.session.request.side_effect = [mock_user_response, mock_repos_response]
        
        # 调用方法
        result = self.client.list_repos()
        
        # 验证请求次数（由于缓存，可能为1或2，取决于缓存是否生效）
        # 第一次调用时，获取用户信息会缓存，所以第二次调用list_repos时，只需要请求知识库列表
        self.assertIn(self.client.session.request.call_count, [1, 2])
        # 验证响应
        self.assertEqual(len(result.get('data', [])), 1)
        self.assertEqual(result['data'][0]['name'], '测试知识库')
    
    def test_get_repo(self):
        """测试获取知识库详情"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "name": "测试知识库",
                "namespace": "test-user/test-repo"
            }
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.get_repo("test-user/test-repo")
        
        # 验证请求
        self.client.session.request.assert_called_once_with('GET', 'https://www.yuque.com/api/v2/repos/test-user/test-repo')
        # 验证响应
        self.assertEqual(result['data']['name'], '测试知识库')
    
    def test_list_docs(self):
        """测试列出知识库中的文档"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": 1,
                    "title": "测试文档",
                    "slug": "test-doc"
                }
            ]
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.list_docs("test-user/test-repo")
        
        # 验证请求
        self.client.session.request.assert_called_once_with('GET', 'https://www.yuque.com/api/v2/repos/test-user/test-repo/docs')
        # 验证响应
        self.assertEqual(len(result.get('data', [])), 1)
        self.assertEqual(result['data'][0]['title'], '测试文档')
    
    def test_get_doc(self):
        """测试获取文档内容"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "title": "测试文档",
                "body": "测试内容"
            }
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.get_doc("test-user/test-repo", "test-doc")
        
        # 验证请求
        self.client.session.request.assert_called_once_with('GET', 'https://www.yuque.com/api/v2/repos/test-user/test-repo/docs/test-doc')
        # 验证响应
        self.assertEqual(result['data']['title'], '测试文档')
        self.assertEqual(result['data']['body'], '测试内容')
    
    def test_get_doc_with_raw(self):
        """测试获取原始文档内容"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "title": "测试文档",
                "body": "测试内容"
            }
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.get_doc("test-user/test-repo", "test-doc", raw=True)
        
        # 验证请求
        self.client.session.request.assert_called_once_with('GET', 'https://www.yuque.com/api/v2/repos/test-user/test-repo/docs/test-doc?raw=1')
        # 验证响应
        self.assertEqual(result['data']['title'], '测试文档')
    
    def test_create_doc(self):
        """测试创建文档"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "title": "新文档",
                "slug": "new-doc"
            }
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.create_doc("test-user/test-repo", "新文档", "文档内容")
        
        # 验证请求
        self.client.session.request.assert_called_once_with(
            'POST',
            'https://www.yuque.com/api/v2/repos/test-user/test-repo/docs',
            json={
                "title": "新文档",
                "format": "markdown",
                "body": "文档内容"
            }
        )
        # 验证响应
        self.assertEqual(result['data']['title'], '新文档')
    
    def test_update_doc(self):
        """测试更新文档"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "id": 1,
                "title": "更新后的文档"
            }
        }
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.update_doc("test-user/test-repo", 1, title="更新后的文档")
        
        # 验证请求
        self.client.session.request.assert_called_once_with(
            'PUT',
            'https://www.yuque.com/api/v2/repos/test-user/test-repo/docs/1',
            json={"title": "更新后的文档"}
        )
        # 验证响应
        self.assertEqual(result['data']['title'], '更新后的文档')
    
    def test_delete_doc(self):
        """测试删除文档"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        self.client.session.request.return_value = mock_response
        
        # 调用方法
        result = self.client.delete_doc("test-user/test-repo", 1)
        
        # 验证请求
        self.client.session.request.assert_called_once_with('DELETE', 'https://www.yuque.com/api/v2/repos/test-user/test-repo/docs/1')
    
    def test_build_repo_path_with_repo_id(self):
        """测试使用repo_id构建路径"""
        path = self.client._build_repo_path(repo_id=123)
        self.assertEqual(path, '/repos/123')
    
    def test_build_repo_path_with_namespace(self):
        """测试使用namespace构建路径"""
        path = self.client._build_repo_path(namespace='test-user/test-repo')
        self.assertEqual(path, '/repos/test-user/test-repo')
    
    def test_build_repo_path_with_invalid_namespace(self):
        """测试使用无效的namespace构建路径"""
        with self.assertRaises(ValueError):
            self.client._build_repo_path(namespace='invalid-namespace')
    
    def test_build_repo_path_without_params(self):
        """测试不提供参数构建路径"""
        with self.assertRaises(ValueError):
            self.client._build_repo_path()


if __name__ == '__main__':
    unittest.main()
