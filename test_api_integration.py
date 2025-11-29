#!/usr/bin/env python3
"""
语雀API集成测试脚本
使用提供的Access Token测试语雀API的全部功能
"""

import time
import json
from yuque_client import YuqueMCPClient


def test_api_functionality():
    """测试语雀API的全部功能"""
    # 提供的Access Token
    token = "vBmWs9xYDxvufuedUI0h6qEvzxAkLPEnOhoigmE1"
    
    # 初始化客户端
    client = YuqueMCPClient(token)
    
    # 测试结果记录
    test_results = {
        "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "token": token,
        "tests": [],
        "summary": {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0
        }
    }
    
    def run_test(test_name, test_func, *args, **kwargs):
        """运行单个测试用例"""
        test_result = {
            "test_name": test_name,
            "status": "pending",
            "response_time": 0,
            "result": None,
            "error": None
        }
        
        test_results["summary"]["total"] += 1
        
        try:
            start_time = time.time()
            result = test_func(*args, **kwargs)
            end_time = time.time()
            
            test_result["status"] = "passed"
            test_result["response_time"] = round(end_time - start_time, 3)
            test_result["result"] = result
            test_results["summary"]["passed"] += 1
            
            print(f"✅ {test_name}: 成功 ({test_result['response_time']}s)")
        except Exception as e:
            end_time = time.time()
            
            test_result["status"] = "failed"
            test_result["response_time"] = round(end_time - start_time, 3)
            test_result["error"] = str(e)
            test_results["summary"]["failed"] += 1
            
            print(f"❌ {test_name}: 失败 ({test_result['response_time']}s) - {str(e)}")
        
        test_results["tests"].append(test_result)
        return test_result
    
    # 1. 用户信息相关测试
    print("\n=== 用户信息相关测试 ===")
    run_test("获取当前用户信息", client.get_user_info)
    
    # 2. 知识库相关测试
    print("\n=== 知识库相关测试 ===")
    user_info = client.get_user_info()
    user_login = user_info["data"]["login"]
    
    run_test("列出用户知识库", client.list_repos)
    
    # 3. 文档相关测试
    print("\n=== 文档相关测试 ===")
    # 获取第一个知识库用于测试
    repos = client.list_repos()
    if repos["data"]:
        test_repo = repos["data"][0]
        test_repo_namespace = test_repo["namespace"]
        
        run_test("获取知识库详情", client.get_repo, test_repo_namespace)
        run_test("列出知识库文档", client.list_docs, test_repo_namespace)
        
        # 获取第一个文档用于测试
        docs = client.list_docs(test_repo_namespace)
        if docs["data"]:
            test_doc = docs["data"][0]
            test_doc_slug = test_doc["slug"]
            
            run_test("获取文档内容", client.get_doc, test_repo_namespace, test_doc_slug)
            run_test("获取原始文档内容", client.get_doc, test_repo_namespace, test_doc_slug, raw=True)
    
    # 4. 团队相关测试
    print("\n=== 团队相关测试 ===")
    run_test("列出用户团队", client.list_groups)
    
    # 获取第一个团队用于测试
    groups = client.list_groups()
    if groups["data"]:
        test_group = groups["data"][0]
        test_group_id = test_group["id"]
        test_group_login = test_group["login"]
        
        run_test("获取团队信息", client.get_group, test_group_id)
        run_test("列出团队成员", client.list_group_users, test_group_id)
        run_test("获取团队统计数据", client.get_group_statistics, test_group_login)
    
    # 5. 其他功能测试
    print("\n=== 其他功能测试 ===")
    run_test("搜索测试", client.search, "测试")
    
    # 6. 错误处理测试
    print("\n=== 错误处理测试 ===")
    run_test("获取不存在的知识库", client.get_repo, "invalid-namespace")
    run_test("获取不存在的文档", client.get_doc, "test-user/test-repo", "invalid-doc")
    
    # 结束测试
    test_results["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # 生成测试报告
    with open("yuque_api_test_report.json", "w", encoding="utf-8") as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    # 打印测试总结
    print("\n" + "="*50)
    print("测试总结")
    print("="*50)
    print(f"开始时间: {test_results['start_time']}")
    print(f"结束时间: {test_results['end_time']}")
    print(f"总测试数: {test_results['summary']['total']}")
    print(f"通过测试: {test_results['summary']['passed']}")
    print(f"失败测试: {test_results['summary']['failed']}")
    print(f"通过率: {round(test_results['summary']['passed'] / test_results['summary']['total'] * 100, 2)}%")
    print(f"测试报告已保存至: yuque_api_test_report.json")
    
    return test_results


if __name__ == "__main__":
    test_api_functionality()
