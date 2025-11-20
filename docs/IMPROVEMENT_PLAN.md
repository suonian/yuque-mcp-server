# 🔧 语雀 MCP 代理服务器整改方案

> 基于实际使用问题排查的完整改进计划

---

## 📋 问题总结

根据 `/path/to/yuque-mcpserver 的分析，主要问题包括：

1. **知识库定位困难** - 搜索返回缺少完整的 namespace 路径
2. **文档内容获取受限** - 只能获取预览内容，无法获取完整 Markdown
3. **API 调用链路不明确** - 需要多步操作才能获取完整信息
4. **错误处理与重试机制缺失** - 缺少明确的错误码和权限提示

---

## 🎯 整改方案

### 问题 1：知识库定位困难

**现状**：
- `search_docs` 返回的文档信息中缺少完整的 `namespace` 路径
- 需要额外调用 `list_repos` 来匹配知识库

**改进方案**：
1. 增强 `format_search_results` 函数，提取并返回完整的 namespace
2. 在搜索结果中包含文档的完整路径信息
3. 添加 `full_path` 字段，方便直接调用 `get_doc`

**代码改进**：
```python
def format_search_results(search_data: Dict, query: str) -> str:
    """格式化搜索结果，包含完整路径信息"""
    results = search_data.get("data", [])
    if not results:
        return f"未找到与 '{query}' 相关的文档"
    
    result = [f"🔍 搜索 '{query}' 的结果 (前10个):"]
    for item in results[:10]:
        # 提取完整的 namespace
        book = item.get('book', {})
        namespace = book.get('namespace', '未知')
        slug = item.get('slug', '未知')
        full_path = f"{namespace}/{slug}" if namespace != '未知' else None
        
        result.append(f"📄 {item.get('title', '未知')}")
        result.append(f"   知识库: {book.get('name', '未知')}")
        result.append(f"   命名空间: {namespace}")
        result.append(f"   完整路径: {full_path}" if full_path else "   完整路径: 未知")
        result.append(f"   摘要: {item.get('summary', '')[:100]}...")
        result.append("")
    
    return "\n".join(result)
```

---

### 问题 2：文档内容获取受限

**现状**：
- `get_doc` 只能获取部分预览内容（前500字符）
- 无法判断是完整内容还是预览内容
- 缺少权限检查提示

**改进方案**：
1. 检查返回内容是否为完整内容
2. 添加内容完整性标识
3. 增强权限错误提示
4. 支持通过参数获取完整内容（如果 API 支持）

**代码改进**：
```python
def format_doc_content(doc_data: Dict) -> str:
    """格式化文档内容，包含完整性检查"""
    doc = doc_data.get("data", {})
    body = doc.get('body', '')
    body_length = len(body) if body else 0
    
    # 检查是否为完整内容
    # 如果内容被截断（通常语雀 API 会返回完整内容，但某些私有文档可能只返回摘要）
    is_preview = body_length < 100 or '...' in body[-10:] if body else True
    
    result = f"""文档内容：
📖 标题: {doc.get('title', '未知')}
🆔 ID: {doc.get('id', '未知')}
📝 格式: {doc.get('format', '未知')}
📅 创建: {doc.get('created_at', '未知')}
✏️ 更新: {doc.get('updated_at', '未知')}
🔗 命名空间: {doc.get('namespace', '未知')}
📏 内容长度: {body_length} 字符
"""
    
    if is_preview and body_length > 0:
        result += f"""
⚠️ 注意: 当前返回的可能是预览内容
💡 提示: 如果文档设置为私有或需要特殊权限，可能无法获取完整内容
   请检查文档的可见性设置或使用有完整权限的 Token
"""
    
    result += f"""
内容:
{body if body else '暂无内容'}
"""
    
    return result
```

**增强 `get_doc` 方法**：
```python
def get_doc(self, namespace: str, slug: str, raw: bool = False) -> Dict[str, Any]:
    """获取文档内容
    
    Args:
        namespace: 知识库命名空间
        slug: 文档标识
        raw: 是否返回原始数据（不格式化）
    """
    result = self._request('GET', f'/repos/{namespace}/docs/{slug}')
    
    # 检查内容完整性
    if not raw:
        doc_data = result.get("data", {})
        body = doc_data.get("body", "")
        if body:
            # 添加元数据标识
            result["_metadata"] = {
                "content_length": len(body),
                "is_full_content": True,  # 语雀 API 通常返回完整内容
                "format": doc_data.get("format", "markdown")
            }
    
    return result
```

---

### 问题 3：API 调用链路优化

**现状**：
- 搜索 → 列出知识库 → 获取文档，需要多步操作
- 缺少一站式查询接口

**改进方案**：
1. 增强搜索结果，直接包含可用的 namespace
2. 添加 `get_doc_by_search` 工具，支持通过搜索直接获取文档
3. 优化工具描述，明确调用路径

**新增工具**：
```python
{
    "name": "get_doc_by_search",
    "description": "通过搜索关键词直接获取文档完整内容（一站式查询）",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "limit": {"type": "integer", "description": "返回结果数量限制", "default": 1}
        },
        "required": ["query"]
    }
}
```

**实现逻辑**：
```python
elif tool_name == "get_doc_by_search":
    query = arguments["query"]
    limit = arguments.get("limit", 1)
    
    # 1. 搜索文档
    search_result = yuque_client.search(query, "doc")
    search_items = search_result.get("data", [])[:limit]
    
    if not search_items:
        return jsonify({
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": f"未找到与 '{query}' 相关的文档"}]
            }
        })
    
    # 2. 获取完整文档内容
    results = []
    for item in search_items:
        book = item.get('book', {})
        namespace = book.get('namespace')
        slug = item.get('slug')
        
        if namespace and slug:
            try:
                doc_result = yuque_client.get_doc(namespace, slug)
                results.append({
                    "title": item.get('title'),
                    "namespace": namespace,
                    "slug": slug,
                    "content": format_doc_content(doc_result)
                })
            except Exception as e:
                results.append({
                    "title": item.get('title'),
                    "error": f"获取文档内容失败: {str(e)}"
                })
    
    # 3. 格式化返回
    formatted_results = "\n\n".join([
        f"📄 {r['title']}\n{r.get('content', r.get('error', ''))}"
        for r in results
    ])
    
    return jsonify({
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "content": [{"type": "text", "text": formatted_results}]
        }
    })
```

---

### 问题 4：错误处理与重试机制

**现状**：
- 错误信息不够明确
- 缺少标准化的错误码
- 没有权限不足的明确提示

**改进方案**：
1. 实现标准化的 MCP 错误码扩展
2. 增强错误信息，包含解决建议
3. 添加权限检查逻辑
4. 实现重试机制（可选）

**标准化错误码**：
```python
# MCP 标准错误码扩展
MCP_ERROR_CODES = {
    # JSON-RPC 2.0 标准错误码
    -32700: "Parse error",              # JSON 解析失败
    -32600: "Invalid Request",          # 请求格式错误
    -32601: "Method not found",         # 方法不存在
    -32602: "Invalid params",           # 参数错误
    -32603: "Internal error",           # 内部错误
    
    # 自定义扩展错误码（-32000 到 -32099）
    -32000: "Tool execution failed",    # 工具执行失败（通用）
    -32001: "Authentication failed",    # 认证失败
    -32002: "Permission denied",        # 权限不足
    -32003: "Resource not found",       # 资源不存在
    -32004: "Preview only",             # 仅预览权限
    -32005: "Rate limit exceeded",       # 限流
    -32006: "Upstream service error",   # 上游服务错误
    -32007: "Content truncated",         # 内容被截断
    -32008: "Invalid namespace",         # 命名空间无效
}
```

**增强错误处理**：
```python
def handle_api_error(e: requests.exceptions.HTTPError, request_id: Any) -> Response:
    """处理 API 错误，返回标准化的错误响应"""
    status_code = e.response.status_code
    
    # 根据状态码确定错误类型
    if status_code == 401:
        error_code = -32001
        error_msg = "认证失败：Token 无效或已过期"
        suggestion = "请检查 Token 是否正确，或重新生成 Token"
    elif status_code == 403:
        error_code = -32002
        error_msg = "权限不足：当前 Token 没有访问此资源的权限"
        suggestion = "请检查文档/知识库的可见性设置，或使用有完整权限的 Token"
    elif status_code == 404:
        error_code = -32003
        error_msg = "资源未找到：请检查命名空间和文档标识是否正确"
        suggestion = "请确认 namespace 和 slug 参数是否正确"
    elif status_code == 429:
        error_code = -32005
        error_msg = "请求频率过高：已达到 API 限流阈值"
        suggestion = "请稍后重试，或降低请求频率"
    elif status_code >= 500:
        error_code = -32006
        error_msg = f"上游服务错误：语雀 API 返回 {status_code}"
        suggestion = "请稍后重试，或联系语雀技术支持"
    else:
        error_code = -32000
        error_msg = f"HTTP 错误: {status_code}"
        suggestion = "请检查请求参数和网络连接"
    
    logger.error(f"语雀API错误 [{status_code}]: {error_msg}")
    
    return jsonify({
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": error_code,
            "message": error_msg,
            "data": {
                "status_code": status_code,
                "suggestion": suggestion,
                "yuque_error": e.response.text[:500] if e.response.text else None
            }
        }
    })
```

**增强日志记录**：
```python
def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
    """发送请求到语雀 API，包含详细日志"""
    url = f"{self.base_url}{endpoint}"
    
    logger.debug(f"[YuqueAPI] 请求: {method} {url}")
    logger.debug(f"[YuqueAPI] 参数: {kwargs.get('json', kwargs.get('params', {}))}")
    
    try:
        response = self.session.request(method, url, **kwargs)
        
        logger.debug(f"[YuqueAPI] 响应: {response.status_code}")
        
        response.raise_for_status()
        result = response.json()
        
        # 记录响应大小
        response_size = len(str(result))
        logger.debug(f"[YuqueAPI] 响应大小: {response_size} 字符")
        
        return result
    except requests.exceptions.HTTPError as e:
        logger.error(f"[YuqueAPI] HTTP错误: {e.response.status_code} - {e.response.text[:200]}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"[YuqueAPI] 请求异常: {type(e).__name__} - {str(e)}")
        raise
```

---

## 📊 实施优先级

| 问题 | 优先级 | 预计工作量 | 影响范围 |
|------|--------|-----------|----------|
| 问题 4：错误处理增强 | 🔴 高 | 2-3 小时 | 所有工具调用 |
| 问题 1：知识库定位 | 🟡 中 | 1-2 小时 | search_docs 工具 |
| 问题 2：文档内容获取 | 🟡 中 | 2-3 小时 | get_doc 工具 |
| 问题 3：API 调用链路 | 🟢 低 | 3-4 小时 | 新增工具 |

---

## 🚀 实施计划

### 第一阶段：错误处理增强（立即实施）
1. 实现标准化错误码
2. 增强错误处理函数
3. 添加详细日志记录
4. 更新错误响应格式

### 第二阶段：搜索结果优化（1-2 天）
1. 增强 `format_search_results` 函数
2. 提取并返回完整的 namespace
3. 添加完整路径信息
4. 更新工具描述

### 第三阶段：文档内容获取优化（2-3 天）
1. 增强 `format_doc_content` 函数
2. 添加内容完整性检查
3. 实现权限提示
4. 支持完整内容获取

### 第四阶段：一站式查询（可选，3-4 天）
1. 实现 `get_doc_by_search` 工具
2. 优化调用链路
3. 添加缓存机制（可选）
4. 性能优化

---

## 📝 测试计划

### 单元测试
- [ ] 错误处理函数测试
- [ ] 搜索结果格式化测试
- [ ] 文档内容格式化测试
- [ ] 权限检查测试

### 集成测试
- [ ] 完整搜索 → 获取文档流程
- [ ] 权限不足场景测试
- [ ] 错误恢复测试
- [ ] 性能测试

### 用户验收测试
- [ ] 实际使用场景验证
- [ ] 错误提示清晰度验证
- [ ] 文档完整性验证

---

## 📚 文档更新

需要更新的文档：
1. `README.md` - 添加错误处理说明
2. `docs/CONFIG_GUIDE.md` - 添加权限配置说明
3. `docs/YUQUE_API_REFERENCE.md` - 更新错误码说明
4. 新增 `docs/TROUBLESHOOTING.md` - 故障排查指南

---

## ✅ 验收标准

1. **错误处理**：
   - ✅ 所有错误都有明确的错误码
   - ✅ 错误信息包含解决建议
   - ✅ 日志记录完整

2. **搜索结果**：
   - ✅ 包含完整的 namespace 路径
   - ✅ 可以直接用于后续调用
   - ✅ 信息完整清晰

3. **文档内容**：
   - ✅ 能够获取完整内容（如果权限允许）
   - ✅ 明确标识预览内容
   - ✅ 提供权限提升建议

4. **调用链路**：
   - ✅ 支持一站式查询（可选）
   - ✅ 工具描述清晰
   - ✅ 调用路径明确

---

## 🔄 持续改进

- 监控错误日志，持续优化错误提示
- 收集用户反馈，改进用户体验
- 定期更新文档和示例
- 考虑添加缓存机制提升性能
