#!/usr/bin/env python3
"""
Yuque MCP Server 一键安装脚本
支持 Windows、macOS 及 Linux 主流操作系统
"""

import os
import sys
import subprocess
import platform
import shutil
import time
import argparse
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('install.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 全局变量
CURRENT_DIR = Path(__file__).parent
CONFIG_FILE = CURRENT_DIR / 'yuque-config.env'
CONFIG_EXAMPLE_FILE = CURRENT_DIR / 'yuque-config.env.example'
REQUIREMENTS_FILE = CURRENT_DIR / 'requirements.txt'
SETUP_FILE = CURRENT_DIR / 'setup.py'

# 支持的操作系统
SUPPORTED_OS = {
    'Windows': ['win32'],
    'macOS': ['darwin'],
    'Linux': ['linux']
}

class Installer:
    """安装器类"""
    
    def __init__(self, args):
        self.args = args
        self.os_type = self.get_os_type()
        self.python_exec = self.get_python_exec()
        self.pip_exec = self.get_pip_exec()
        self.is_admin = self.check_admin()
    
    def get_os_type(self):
        """获取操作系统类型"""
        sys_platform = sys.platform
        for os_name, platforms in SUPPORTED_OS.items():
            if sys_platform in platforms:
                return os_name
        raise ValueError(f"不支持的操作系统: {sys_platform}")
    
    def get_python_exec(self):
        """获取Python可执行文件路径"""
        return sys.executable
    
    def get_pip_exec(self):
        """获取pip可执行文件路径"""
        return f"{self.python_exec} -m pip"
    
    def check_admin(self):
        """检查是否具有管理员权限"""
        try:
            if self.os_type == 'Windows':
                # Windows 检查管理员权限
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                # macOS/Linux 检查root权限
                return os.geteuid() == 0
        except Exception as e:
            logger.warning(f"检查管理员权限失败: {e}")
            return False
    
    def run_command(self, cmd, cwd=None, check=True, shell=True):
        """执行命令"""
        logger.info(f"执行命令: {cmd}")
        try:
            # 根据操作系统调整命令执行参数
            if self.os_type == 'Windows' and shell:
                # Windows 使用 cmd.exe 执行命令
                result = subprocess.run(
                    ['cmd.exe', '/c', cmd],
                    cwd=cwd or CURRENT_DIR,
                    check=check,
                    shell=False,
                    capture_output=True,
                    text=True
                )
            else:
                # macOS/Linux 使用默认 shell 执行命令
                result = subprocess.run(
                    cmd,
                    cwd=cwd or CURRENT_DIR,
                    check=check,
                    shell=shell,
                    capture_output=True,
                    text=True
                )
            
            if result.stdout.strip():
                logger.debug(f"命令输出: {result.stdout}")
            if result.stderr.strip():
                logger.warning(f"命令错误输出: {result.stderr}")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"命令执行失败: {e}")
            if e.stdout.strip():
                logger.error(f"命令输出: {e.stdout}")
            if e.stderr.strip():
                logger.error(f"命令错误输出: {e.stderr}")
            if check:
                raise
            return e
        except Exception as e:
            logger.error(f"命令执行异常: {e}")
            if check:
                raise
            return e
    
    def install_dependencies(self):
        """安装依赖"""
        logger.info("开始安装依赖...")
        
        # 更新pip
        self.run_command(f"{self.pip_exec} install --upgrade pip")
        
        # 安装依赖
        self.run_command(f"{self.pip_exec} install -r {REQUIREMENTS_FILE}")
        
        logger.info("依赖安装完成")
    
    def create_config(self):
        """创建配置文件"""
        logger.info("开始创建配置文件...")
        
        if CONFIG_FILE.exists():
            logger.info(f"配置文件已存在: {CONFIG_FILE}")
            if self.args.force:
                logger.info("强制更新配置文件")
                CONFIG_FILE.unlink()
            else:
                logger.info("跳过配置文件创建")
                return
        
        # 复制示例配置文件
        shutil.copy2(CONFIG_EXAMPLE_FILE, CONFIG_FILE)
        logger.info(f"配置文件已创建: {CONFIG_FILE}")
        
        # 提示用户配置YUQUE_TOKEN
        logger.info("\n请编辑配置文件，设置YUQUE_TOKEN:")
        logger.info(f"配置文件路径: {CONFIG_FILE}")
        logger.info("获取Token方式: 语雀设置 > 个人设置 > Token")
    
    def install_service(self):
        """安装服务"""
        logger.info("开始安装服务...")
        
        if self.os_type == 'Windows':
            self.install_windows_service()
        elif self.os_type == 'macOS':
            self.install_macos_service()
        elif self.os_type == 'Linux':
            self.install_linux_service()
        
        logger.info("服务安装完成")
    
    def install_windows_service(self):
        """安装Windows服务"""
        logger.info("Windows服务安装功能开发中")
        # TODO: 实现Windows服务安装
    
    def install_macos_service(self):
        """安装macOS服务"""
        logger.info("开始安装macOS服务...")
        
        # 检查install_service.sh脚本是否存在
        install_script = CURRENT_DIR / 'install_service.sh'
        if install_script.exists():
            self.run_command(f"chmod +x {install_script}")
            self.run_command(f"{install_script}")
        else:
            logger.warning("install_service.sh脚本不存在，跳过服务安装")
    
    def install_linux_service(self):
        """安装Linux服务"""
        logger.info("Linux服务安装功能开发中")
        # TODO: 实现Linux服务安装
    
    def install_python_package(self):
        """安装Python包"""
        logger.info("开始安装Python包...")
        self.run_command(f"{self.pip_exec} install -e .")
        logger.info("Python包安装完成")
    
    def verify_installation(self):
        """验证安装结果"""
        logger.info("开始验证安装结果...")
        
        # 验证依赖安装
        try:
            if self.os_type == 'Windows':
                # Windows 使用 findstr 命令替代 grep
                self.run_command(f"{self.pip_exec} list | findstr /R 'fastapi uvicorn redis httpx'")
            else:
                # macOS/Linux 使用 grep 命令
                self.run_command(f"{self.pip_exec} list | grep -E 'fastapi|uvicorn|redis|httpx'")
        except subprocess.CalledProcessError:
            # 如果命令执行失败，尝试直接检查依赖
            logger.warning("依赖验证命令执行失败，尝试直接检查依赖")
            try:
                import fastapi
                import uvicorn
                import redis
                import httpx
                logger.info("依赖验证通过")
            except ImportError as e:
                logger.error(f"依赖验证失败: {e}")
                return False
        
        # 验证配置文件
        if not CONFIG_FILE.exists():
            logger.error(f"配置文件不存在: {CONFIG_FILE}")
            return False
        
        logger.info("安装验证通过")
        return True
    
    def start_server(self):
        """启动服务器"""
        logger.info("开始启动服务器...")
        
        if self.os_type == 'Windows':
            # Windows使用start_server.bat
            start_script = CURRENT_DIR / 'start_server.bat'
            if start_script.exists():
                self.run_command(f"start {start_script}", shell=True, check=False)
            else:
                logger.warning("start_server.bat脚本不存在")
        else:
            # macOS/Linux使用start_server.sh
            start_script = CURRENT_DIR / 'start_server.sh'
            if start_script.exists():
                self.run_command(f"chmod +x {start_script}")
                self.run_command(f"{start_script} start async", check=False)
            else:
                logger.warning("start_server.sh脚本不存在")
        
        logger.info("服务器启动完成")
    
    def install(self):
        """执行安装流程"""
        try:
            logger.info(f"开始安装 Yuque MCP Server...")
            logger.info(f"操作系统: {self.os_type}")
            logger.info(f"Python路径: {self.python_exec}")
            logger.info(f"Pip路径: {self.pip_exec}")
            logger.info(f"管理员权限: {self.is_admin}")
            
            # 安装依赖
            self.install_dependencies()
            
            # 创建配置文件
            self.create_config()
            
            # 安装Python包
            self.install_python_package()
            
            # 安装服务（可选）
            if self.args.service:
                self.install_service()
            
            # 验证安装
            self.verify_installation()
            
            # 启动服务器（可选）
            if self.args.start:
                self.start_server()
            
            logger.info("\n🎉 Yuque MCP Server 安装完成！")
            logger.info("\n📋 后续步骤:")
            logger.info(f"1. 编辑配置文件: {CONFIG_FILE}")
            logger.info("2. 设置YUQUE_TOKEN")
            logger.info("3. 启动服务器: ./start_server.sh start async")
            logger.info("4. 访问健康检查: http://localhost:3000/health")
            
            return True
            
        except Exception as e:
            logger.error(f"安装失败: {e}")
            logger.error("请查看install.log文件获取详细错误信息")
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Yuque MCP Server 一键安装脚本')
    parser.add_argument('--force', action='store_true', help='强制更新配置文件')
    parser.add_argument('--service', action='store_true', help='安装系统服务')
    parser.add_argument('--start', action='store_true', help='安装完成后启动服务器')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        logger.setLevel(logging.DEBUG)
    
    logger.info("🚀 Yuque MCP Server 一键安装脚本")
    logger.info("=" * 60)
    
    installer = Installer(args)
    success = installer.install()
    
    logger.info("=" * 60)
    if success:
        logger.info("✅ 安装成功！")
        sys.exit(0)
    else:
        logger.error("❌ 安装失败！")
        sys.exit(1)

if __name__ == '__main__':
    main()
