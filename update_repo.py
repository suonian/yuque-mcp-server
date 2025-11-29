#!/usr/bin/env python3
"""
Yuque MCP Server 仓库更新脚本
功能：自动执行仓库更新流程，包括清理、优化、隐私检查和部署
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

CURRENT_DIR = Path(__file__).parent

def run_command(cmd, cwd=None, check=True):
    """执行命令"""
    logger.info(f"执行命令: {cmd}")
    result = subprocess.run(
        cmd,
        cwd=cwd or CURRENT_DIR,
        check=check,
        shell=True,
        capture_output=True,
        text=True
    )
    if result.stdout.strip():
        logger.debug(f"命令输出: {result.stdout}")
    if result.stderr.strip():
        logger.warning(f"命令错误输出: {result.stderr}")
    return result

def check_sensitive_info():
    """检查敏感信息"""
    logger.info("检查敏感信息...")
    
    # 检查硬编码的令牌
    sensitive_patterns = ["YUQUE_TOKEN=", "token=", "api_key=", "secret=", "password="]
    
    for pattern in sensitive_patterns:
        result = run_command(f"grep -r '{pattern}' --include='*.py' --include='*.env' --include='*.sh' --include='*.bat' --include='*.ps1' .", check=False)
        if result.returncode == 0:
            # 过滤掉测试文件和示例文件
            lines = result.stdout.split('\n')
            problematic_lines = []
            for line in lines:
                if line.strip() and not any(exclude in line for exclude in [
                    'test_', 'example', 'YUQUE_TOKEN=', 'token=test-token', 'token: str', '提示用户配置YUQUE_TOKEN'
                ]):
                    problematic_lines.append(line)
            
            if problematic_lines:
                logger.error(f"发现敏感信息: {pattern}")
                for line in problematic_lines:
                    logger.error(f"  {line}")
                return False
    
    logger.info("敏感信息检查通过")
    return True

def clean_repo():
    """清理仓库"""
    logger.info("清理仓库...")
    
    # 删除生成的文件
    clean_files = [
        'yuque_mcp_server.egg-info',
        'performance_test.py',
        'test_api_integration.py',
        '__pycache__',
        '*.pyc',
        '*.log',
        '/tmp/yuque-proxy.*',
        'yuque-config.env'
    ]
    
    for file_pattern in clean_files:
        run_command(f"rm -rf {file_pattern}", check=False)
    
    logger.info("仓库清理完成")

def update_dependencies():
    """更新依赖"""
    logger.info("更新依赖...")
    
    # 安装pip-tools
    run_command("pip install pip-tools")
    
    # 生成更新后的requirements.txt
    run_command("pip-compile requirements.in -o requirements.txt --upgrade")
    
    # 检查依赖兼容性
    run_command("pip check")
    
    logger.info("依赖更新完成")

def run_tests():
    """运行测试"""
    logger.info("运行测试...")
    
    result = run_command("python3 -m pytest tests/ -v")
    if result.returncode != 0:
        logger.error("测试失败")
        return False
    
    logger.info("测试通过")
    return True

def push_to_github():
    """推送到GitHub"""
    logger.info("推送到GitHub...")
    
    # 检查git状态
    result = run_command("git status")
    if "nothing to commit" in result.stdout:
        logger.info("没有需要提交的更改")
        return True
    
    # 提交更改
    run_command("git add .")
    run_command("git commit -m 'Update repository with optimized files and dependencies'")
    
    # 推送到GitHub
    result = run_command("git push", check=False)
    if result.returncode != 0:
        logger.error("推送到GitHub失败")
        logger.error(result.stderr)
        return False
    
    logger.info("推送到GitHub成功")
    return True

def main():
    """主函数"""
    logger.info("开始执行仓库更新流程...")
    
    try:
        # 1. 检查敏感信息
        if not check_sensitive_info():
            logger.error("敏感信息检查失败，终止更新")
            sys.exit(1)
        
        # 2. 清理仓库
        clean_repo()
        
        # 3. 更新依赖
        update_dependencies()
        
        # 4. 运行测试
        if not run_tests():
            logger.error("测试失败，终止更新")
            sys.exit(1)
        
        # 5. 推送到GitHub
        if not push_to_github():
            logger.error("推送到GitHub失败")
            sys.exit(1)
        
        logger.info("仓库更新流程执行完成")
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"更新过程中发生错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
