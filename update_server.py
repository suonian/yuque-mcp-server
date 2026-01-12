#!/usr/bin/env python3
import sys
import os

def main():
    server_path = "yuque_mcp/server.py"

    # 读取原文件
    with open(server_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 在文件开头插入代码
    new_code = '''#!/usr/bin/env python3
import os
import sys
from typing import Optional

try:
    # 完全禁用 stdout 和 stderr，防止任何输出干扰 MCP 协议
    class NullWriter:
        def write(self, text): pass
        def flush(self): pass
        def isatty(self): return False

    sys.stdout = NullWriter()
    sys.stderr = NullWriter()

    # 设置环境变量禁用 FastMCP 输出
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['FORCE_COLOR'] = '0'
    os.environ['NO_COLOR'] = '1'
except Exception:
    pass

import logging
from fastmcp import FastMCP

class QuietLogger:
    def __init__(self):
        try:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.CRITICAL)
            for handler in self.logger.handlers[:]:
                self.logger.removeHandler(handler)
            file_handler = logging.FileHandler('yuque_mcp.log', mode='a', encoding='utf-8')
            file_handler.setLevel(logging.CRITICAL)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception:
            pass

    def critical(self, msg, *args, **kwargs):
        try:
            if msg:
                self.logger.critical(msg, *args, **kwargs)
        except Exception:
            pass

    def error(self, msg, *args, **kwargs): pass
    def warning(self, msg, *args, **kwargs): pass
    def info(self, msg, *args, **kwargs): pass
    def debug(self, msg, *args, **kwargs): pass

try:
    logger = QuietLogger()
except Exception:
    logger = None

try:
    mcp = FastMCP(
        name='yuque-mcp-server',
        version='1.0.0',
        instructions='语雀MCP服务器，提供语雀API的MCP接口'
    )
except Exception:
    pass

try:
    logging.basicConfig(
        level=logging.CRITICAL,
        filename='yuque_mcp.log',
        filemode='a',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    for name in ['fastmcp', 'rich', 'uvicorn', 'httpx']:
        logging.getLogger(name).setLevel(logging.CRITICAL)

    for logger_name in logging.root.manager.loggerDict:
        logger_obj = logging.getLogger(logger_name)
        for handler in logger_obj.handlers[:]:
            if isinstance(handler, logging.StreamHandler):
                logger_obj.removeHandler(handler)
except Exception:
    pass
'''

    # 找到原始文件头部位置，在 """ 之后替换
    import_index = content.find('import os')
    if import_index > 0:
        content = new_code + content[import_index:]

    # 写入文件
    with open(server_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n✅ 成功更新 yuque_mcp/server.py")
    print("\n📝 主要修改：")
    print("   - 完全禁用 stdout/stderr 输出")
    print("   - 设置环境变量禁用颜色输出")
    print("   - 使用 QuietLogger 静默所有日志")
    print("   - MCP 服务器将完全静默运行")

if __name__ == "__main__":
    main()
