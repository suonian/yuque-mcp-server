from typing import Dict, Any


def format_user_info(user_data: Dict[str, Any]) -> str:
    """格式化用户信息"""
    user: Dict[str, Any] = user_data.get("data", {})
    return f"""👤 语雀用户信息
姓名: {user.get('name', '未知')}
登录名: {user.get('login', '未知')}
用户ID: {user.get('id', '未知')}
知识库数量: {user.get('books_count', 0)}
关注: {user.get('following_count', 0)} | 粉丝: {user.get('followers_count', 0)}
注册时间: {user.get('created_at', '未知')}"""


def format_repos_list(repos_data: Dict[str, Any]) -> str:
    """格式化知识库列表"""
    repos: list[Dict[str, Any]] = repos_data.get("data", [])
    if not repos:
        return "暂无知识库"
    
    # 按文档数量排序
    repos.sort(key=lambda x: x.get('items_count', 0), reverse=True)
    
    result: list[str] = ["📚 您的语雀知识库列表 (按文档数量排序):"]
    for repo in repos:
        result.append(f"📖 {repo.get('name', '未知')}")
        result.append(f"  命名空间: {repo.get('namespace', '未知')}")
        result.append(f"  文档数: {repo.get('items_count', 0)} | 更新: {repo.get('updated_at', '未知')[:10]}")
        result.append("")
    
    return "\n".join(result)


def format_repo_info(repo_data: Dict[str, Any]) -> str:
    """格式化知识库信息"""
    repo: Dict[str, Any] = repo_data.get("data", {})
    return f"""知识库详情：
📖 名称: {repo.get('name', '未知')}
🔗 命名空间: {repo.get('namespace', '未知')}
📄 文档数量: {repo.get('items_count', 0)}
👀 关注数: {repo.get('watches_count', 0)}
❤️ 点赞数: {repo.get('likes_count', 0)}
📝 描述: {repo.get('description', '暂无描述')}
🕐 创建时间: {repo.get('created_at', '未知')}
✏️ 最后更新: {repo.get('updated_at', '未知')}"""


def format_docs_list(docs_data: Dict[str, Any], namespace: str) -> str:
    """格式化文档列表"""
    docs: list[Dict[str, Any]] = docs_data.get("data", [])
    if not docs:
        return f"知识库 '{namespace}' 暂无文档"
    
    result: list[str] = [f"📄 知识库 '{namespace}' 中的文档:"]
    for i, doc in enumerate(docs, 1):
        result.append(f"{i}. {doc.get('title', '未知标题')}")
        result.append(f"   文档ID: {doc.get('id', '未知')}")
        result.append(f"   最后更新: {doc.get('updated_at', '未知')[:10]}")
        result.append("")
    
    return "\n".join(result)


def format_doc_content(doc_data: Dict[str, Any], repo_info: Optional[Dict[str, Any]] = None, namespace: Optional[str] = None, slug: Optional[str] = None, include_full: bool = True) -> str:
    """格式化文档内容，支持完整内容显示和权限检测，包含所有相关信息"""
    doc = doc_data.get("data", {})
    body = doc.get('body', '')
    body_length = len(body) if body else 0
    
    # 检测内容是否完整（可能是预览内容）
    is_preview = False
    if body:
        is_preview = body_length < 500 or (body_length >= 500 and '...' in body[-50:])
    
    content_status = "⚠️ 仅预览内容" if is_preview else "✅ 完整内容"
    
    # 构建完整的文档信息
    result = f"""═══════════════════════════════════════
📄 文档详细信息
═══════════════════════════════════════

【基本信息】
📖 标题: {doc.get('title', '未知')}
🆔 文档ID: {doc.get('id', '未知')}
📝 格式: {doc.get('format', '未知')}
📅 创建时间: {doc.get('created_at', '未知')}
✏️ 更新时间: {doc.get('updated_at', '未知')}
👤 创建者: {doc.get('creator', {}).get('name', '未知') if doc.get('creator') else '未知'}

【知识库归属】
"""
    
    # 添加知识库信息
    if repo_info and repo_info.get("data"):
        repo = repo_info["data"]
        result += f"""📚 知识库名称: {repo.get('name', '未知')}
🔗 命名空间: {repo.get('namespace', namespace or '未知')}
📊 知识库类型: {repo.get('type', '未知')}
👥 所有者: {repo.get('user', {}).get('name', '未知') if repo.get('user') else '未知'}
🔒 可见性: {['私密', '团队可见', '公开'][repo.get('public', 0)] if repo.get('public') is not None else '未知'}
📈 文档数量: {repo.get('items_count', 0)}
⭐ 关注数: {repo.get('followers_count', 0)}
"""
    else:
        result += f"""📚 知识库命名空间: {namespace or '未知'}
🔗 文档路径: {slug or '未知'}
⚠️ 注意: 无法获取知识库详细信息（可能权限不足）
"""
    
    # 添加文档路径信息
    if namespace and slug:
        doc_url = f"https://www.yuque.com/{namespace}/{slug}"
        result += f"""
【访问信息】
🔗 完整路径: {namespace}/{slug}
🌐 访问链接: {doc_url}
💡 使用方法: get_doc(namespace="{namespace}", slug="{slug}")
"""
    
    result += f"""
【内容信息】
📊 内容状态: {content_status}
📏 内容长度: {body_length} 字符
"""
    
    # 添加文档统计信息
    if doc.get('read_count') is not None:
        result += f"👁️ 阅读数: {doc.get('read_count', 0)}\n"
    if doc.get('like_count') is not None:
        result += f"👍 点赞数: {doc.get('like_count', 0)}\n"
    if doc.get('comment_count') is not None:
        result += f"💬 评论数: {doc.get('comment_count', 0)}\n"
    
    result += "\n"
    
    if include_full and body:
        if is_preview:
            # 显示预览内容并给出提示
            preview_text = body[:500] if body_length > 500 else body
            result += f"内容预览:\n{preview_text}"
            if body_length > 500:
                result += "...\n\n"
            result += "\n⚠️ 提示：这是预览内容。如需完整内容，请：\n"
            result += "1. 检查文档的可见性设置（是否私有）\n"
            result += "2. 确认 Token 是否有完整访问权限\n"
            result += "3. 尝试使用 get_doc 工具并设置 raw=true 参数"
        else:
            # 显示完整内容
            result += f"完整内容:\n{body}"
    else:
        # 仅显示预览
        preview_text = body[:500] if body_length > 500 else body
        result += f"内容预览:\n{preview_text}"
        if body_length > 500:
            result += "..."
    
    return result


def format_created_doc(doc_data: Dict[str, Any], namespace: str) -> str:
    """格式化创建的文档信息"""
    doc: Dict[str, Any] = doc_data.get("data", {})
    doc_url: str = f"https://www.yuque.com/{namespace}/{doc.get('slug', '')}"
    return f"""✅ 文档创建成功！
📖 标题: {doc.get('title', '未知')}
🆔 文档ID: {doc.get('id', '未知')}
🔗 访问链接: {doc_url}
📅 创建时间: {doc.get('created_at', '未知')}"""


def format_repo_created(repo_data: Dict[str, Any], owner_login: str) -> str:
    repo: Dict[str, Any] = repo_data.get("data", {})
    namespace: str = repo.get("namespace", "未知")
    visibility: str = {0: "私密", 1: "团队可见", 2: "公开"}.get(repo.get("public", 0), "未知")
    return f"""✅ 知识库创建成功！
📚 名称: {repo.get('name', '未知')}
👤 所属: {owner_login}
🔗 命名空间: {namespace}
🌐 可见性: {visibility}
📅 创建时间: {repo.get('created_at', '未知')}"""


def format_doc_versions(versions_data: Dict[str, Any], doc_id: int) -> str:
    versions: list[Dict[str, Any]] = versions_data.get("data", [])
    if not versions:
        return f"文档 {doc_id} 暂无版本历史。"
    
    lines: list[str] = [f"📜 文档 {doc_id} 版本历史（最多 10 条）:"]
    for version in versions[:10]:
        creator = version.get("creator", {}).get("name") if isinstance(version.get("creator"), dict) else version.get("creator")
        lines.append(
            f"- 版本 {version.get('version', version.get('id', '未知'))} · "
            f"{version.get('title', '未命名')} · "
            f"{creator or '匿名'} @ {version.get('created_at', '未知')}"
        )
    if len(versions) > 10:
        lines.append("... 其余版本请在语雀查看。")
    return "\n".join(lines)


def format_doc_version_detail(version_data: Dict[str, Any]) -> str:
    version: Dict[str, Any] = version_data.get("data", {})
    creator: Dict[str, Any] = version.get("creator", {})
    return f"""📘 文档版本详情
版本号: {version.get('version', '未知')}
标题: {version.get('title', '未命名')}
作者: {creator.get('name') or creator.get('login', '未知')}
创建时间: {version.get('created_at', '未知')}

变更说明:
{version.get('description', '无')}"""


def format_search_results(search_data: Dict[str, Any], query: str) -> str:
    """格式化搜索结果，包含完整路径信息"""
    results: list[Dict[str, Any]] = search_data.get("data", [])
    if not results:
        return f"未找到与 '{query}' 相关的文档"
    
    result_list: list[str] = [f"🔍 搜索 '{query}' 的结果 (前10个):"]
    for item in results[:10]:
        # 语雀搜索API返回的数据结构：
        # - 顶层有 id, title, summary, url
        title: str = item.get('title', '未知标题')
        url: str = item.get('url', '')
        summary: str = item.get('summary', '')
        result_list.append(f"📖 {title}")
        result_list.append(f"  🔗 {url}")
        result_list.append(f"  📝 {summary[:100]}...")
        result_list.append("")
    
    return "\n".join(result_list)


def format_groups_list(groups_data: Dict[str, Any]) -> str:
    """格式化团队列表"""
    groups: list[Dict[str, Any]] = groups_data.get("data", [])
    if not groups:
        return "暂无团队"
    
    result: list[str] = ["👥 您的语雀团队列表:"]
    for group in groups:
        result.append(f"📊 {group.get('name', '未知')}")
        result.append(f"  ID: {group.get('id', '未知')}")
        result.append(f"  成员数: {group.get('members_count', 0)}")
        result.append("")
    
    return "\n".join(result)


def format_group_info(group_data: Dict[str, Any]) -> str:
    """格式化团队信息"""
    group: Dict[str, Any] = group_data.get("data", {})
    return f"""团队详情：
📊 名称: {group.get('name', '未知')}
🆔 ID: {group.get('id', '未知')}
👥 成员数: {group.get('members_count', 0)}
📝 描述: {group.get('description', '暂无描述')}
🕐 创建时间: {group.get('created_at', '未知')}"""


def format_group_users(group_users_data: Dict[str, Any], group_id: int) -> str:
    """格式化团队成员列表"""
    users: list[Dict[str, Any]] = group_users_data.get("data", [])
    if not users:
        return f"团队 {group_id} 暂无成员。"
    
    result: list[str] = [f"👥 团队 {group_id} 成员列表:"]
    for user in users:
        result.append(f"- {user.get('name', '未知')} ({user.get('login', '未知')}) 角色: {user.get('role', 'member')}")
    return "\n".join(result)


def format_group_statistics(statistics_data: Dict[str, Any]) -> str:
    """格式化团队统计数据"""
    stats: Dict[str, Any] = statistics_data.get("data", {})
    return f"""📊 团队统计数据：
📚 知识库数量: {stats.get('books_count', 0)}
📄 文档数量: {stats.get('docs_count', 0)}
👥 成员数量: {stats.get('members_count', 0)}
📈 本月新增文档: {stats.get('monthly_new_docs_count', 0)}
📈 本月活跃成员: {stats.get('monthly_active_members_count', 0)}"""


def format_group_member_stats(stats_data: Dict[str, Any]) -> str:
    """格式化团队成员统计数据"""
    stats: Dict[str, Any] = stats_data.get("data", {})
    members: list[Dict[str, Any]] = stats.get("items", [])
    if not members:
        return "暂无成员统计数据"
    
    result: list[str] = ["👥 团队成员统计数据:"]
    for member in members:
        result.append(f"- {member.get('name', '未知')} ({member.get('login', '未知')})")
        result.append(f"  文档数: {member.get('write_doc_count', 0)}")
        result.append(f"  编辑次数: {member.get('write_count', 0)}")
        result.append(f"  阅读次数: {member.get('read_count', 0)}")
        result.append(f"  点赞次数: {member.get('like_count', 0)}")
        result.append("")
    
    return "\n".join(result)


def format_group_book_stats(stats_data: Dict[str, Any]) -> str:
    """格式化团队知识库统计数据"""
    stats: Dict[str, Any] = stats_data.get("data", {})
    books: list[Dict[str, Any]] = stats.get("items", [])
    if not books:
        return "暂无知识库统计数据"
    
    result: list[str] = ["📚 团队知识库统计数据:"]
    for book in books:
        result.append(f"- {book.get('name', '未知')}")
        result.append(f"  文档数: {book.get('docs_count', 0)}")
        result.append(f"  阅读次数: {book.get('read_count', 0)}")
        result.append(f"  编辑次数: {book.get('write_count', 0)}")
        result.append("")
    
    return "\n".join(result)


def format_group_doc_stats(stats_data: Dict[str, Any]) -> str:
    """格式化团队文档统计数据"""
    stats: Dict[str, Any] = stats_data.get("data", {})
    docs: list[Dict[str, Any]] = stats.get("items", [])
    if not docs:
        return "暂无文档统计数据"
    
    result: list[str] = ["📄 团队文档统计数据:"]
    for doc in docs:
        result.append(f"- {doc.get('title', '未知')}")
        result.append(f"  阅读次数: {doc.get('read_count', 0)}")
        result.append(f"  编辑次数: {doc.get('write_count', 0)}")
        result.append(f"  点赞次数: {doc.get('like_count', 0)}")
        result.append("")
    
    return "\n".join(result)


def format_repo_toc(toc_data: Dict[str, Any]) -> str:
    """格式化知识库目录"""
    toc: Dict[str, Any] = toc_data.get("data", {})
    body: str = toc.get('body', '')
    return f"""📑 知识库目录：
{body}"""
