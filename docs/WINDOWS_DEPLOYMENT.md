# 🪟 Windows 部署指南

本指南说明如何在 Windows 系统上部署和运行语雀 MCP 代理服务器。

## ✅ Windows 兼容性

### 完全兼容的部分
- ✅ **主程序** (`yuque-proxy.py`) - Python + Flask，跨平台兼容
- ✅ **自动启动包装器** (`auto_start_server.py`) - Python，跨平台兼容
- ✅ **MCP 协议** - 标准协议，跨平台兼容

### Windows 特定脚本
- ✅ **启动脚本** - 提供 `start_server.bat` 和 `start_server.ps1`
- ⚠️ **系统服务** - 需要使用 Windows 服务管理器或 NSSM

---

## 📋 系统要求

- **操作系统**: Windows 10/11 或 Windows Server 2016+
- **Python**: 3.7 或更高版本
- **网络**: 能够访问 `https://www.yuque.com`

---

## 🚀 快速开始

### 1. 安装 Python

如果尚未安装 Python：

1. 访问 [Python 官网](https://www.python.org/downloads/)
2. 下载并安装 Python 3.7+
3. 安装时勾选 "Add Python to PATH"

验证安装：
```cmd
python --version
```

### 2. 安装依赖

```cmd
pip install flask requests
```

### 3. 配置 Token

#### 方式一：配置文件（推荐）

```cmd
# 复制配置示例文件
copy yuque-config.env.example yuque-config.env

# 编辑配置文件，填入您的语雀 Token
notepad yuque-config.env
```

#### 方式二：环境变量

```cmd
# 临时设置（当前命令提示符）
set YUQUE_TOKEN=your-token-here

# 永久设置（系统环境变量）
setx YUQUE_TOKEN "your-token-here"
```

### 4. 启动服务

#### 使用批处理脚本（推荐）

```cmd
start_server.bat start
```

#### 使用 PowerShell 脚本

```powershell
.\start_server.ps1 start
```

#### 直接运行 Python

```cmd
python yuque-proxy.py
```

---

## 📝 常用命令

### 批处理脚本 (start_server.bat)

```cmd
# 启动服务
start_server.bat start

# 停止服务
start_server.bat stop

# 重启服务
start_server.bat restart

# 查看状态
start_server.bat status

# 查看日志
type %TEMP%\yuque-proxy.log
```

### PowerShell 脚本 (start_server.ps1)

```powershell
# 启动服务
.\start_server.ps1 start

# 停止服务
.\start_server.ps1 stop

# 重启服务
.\start_server.ps1 restart

# 查看状态
.\start_server.ps1 status

# 查看日志
.\start_server.ps1 logs

# 管理配置
.\start_server.ps1 config
```

---

## 🔧 Windows 服务安装（可选）

如果您希望服务在系统启动时自动运行，可以将其安装为 Windows 服务。

### 方式一：使用 NSSM（推荐）

#### 1. 下载 NSSM

访问 [NSSM 官网](https://nssm.cc/download) 下载 Windows 版本。

#### 2. 安装服务

```cmd
# 解压 NSSM 到任意目录，例如 C:\nssm
cd C:\nssm\win64

# 安装服务
nssm install YuqueMCP "C:\Python3\python.exe" "C:\path\to\yuque-mcpserver\yuque-proxy.py"

# 设置工作目录
nssm set YuqueMCP AppDirectory "C:\path\to\yuque-mcpserver"

# 设置环境变量
nssm set YuqueMCP AppEnvironmentExtra "YUQUE_TOKEN=your-token-here" "PORT=3000"

# 设置日志
nssm set YuqueMCP AppStdout "C:\path\to\yuque-mcpserver\yuque-proxy.log"
nssm set YuqueMCP AppStderr "C:\path\to\yuque-mcpserver\yuque-proxy.error.log"

# 启动服务
nssm start YuqueMCP
```

#### 3. 服务管理

```cmd
# 启动服务
nssm start YuqueMCP

# 停止服务
nssm stop YuqueMCP

# 重启服务
nssm restart YuqueMCP

# 查看状态
nssm status YuqueMCP

# 卸载服务
nssm remove YuqueMCP confirm
```

### 方式二：使用 Windows 服务管理器

#### 1. 创建服务脚本

创建 `install_windows_service.ps1`：

```powershell
# 需要管理员权限运行
$serviceName = "YuqueMCP"
$displayName = "语雀 MCP 代理服务器"
$description = "语雀 Model Context Protocol 代理服务器"
$pythonPath = "C:\Python3\python.exe"
$scriptPath = "C:\path\to\yuque-mcpserver\yuque-proxy.py"
$workingDir = "C:\path\to\yuque-mcpserver"

# 创建服务
New-Service -Name $serviceName `
    -DisplayName $displayName `
    -Description $description `
    -BinaryPathName "$pythonPath `"$scriptPath`"" `
    -StartupType Automatic

# 设置工作目录（需要修改注册表）
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Services\$serviceName"
Set-ItemProperty -Path $regPath -Name "ImagePath" -Value "$pythonPath `"$scriptPath`""
```

#### 2. 安装服务

以管理员身份运行 PowerShell：

```powershell
.\install_windows_service.ps1
```

#### 3. 服务管理

```powershell
# 启动服务
Start-Service YuqueMCP

# 停止服务
Stop-Service YuqueMCP

# 查看状态
Get-Service YuqueMCP
```

---

## 🔍 验证服务

### 方法一：健康检查

```cmd
curl http://localhost:3000/health
```

或使用 PowerShell：

```powershell
Invoke-WebRequest -Uri http://localhost:3000/health | Select-Object -ExpandProperty Content
```

### 方法二：查看服务状态

```cmd
netstat -ano | findstr :3000
```

### 方法三：测试 MCP 协议

```powershell
$body = @{
    jsonrpc = "2.0"
    id = 1
    method = "initialize"
    params = @{
        protocolVersion = "2024-11-05"
        capabilities = @{}
        clientInfo = @{
            name = "test"
            version = "1.0.0"
        }
    }
} | ConvertTo-Json -Depth 10

Invoke-WebRequest -Uri http://localhost:3000/mcp `
    -Method POST `
    -ContentType "application/json" `
    -Headers @{"X-Yuque-Token"="your-token-here"} `
    -Body $body
```

---

## ⚠️ 常见问题

### 1. Python 未找到

**问题**: `'python' 不是内部或外部命令`

**解决方案**:
- 确认 Python 已安装
- 将 Python 添加到系统 PATH
- 或使用完整路径：`C:\Python3\python.exe`

### 2. 端口被占用

**问题**: 端口 3000 已被占用

**解决方案**:
```cmd
# 查看端口占用
netstat -ano | findstr :3000

# 修改端口（在 yuque-config.env 中设置）
PORT=3001
```

### 3. 防火墙阻止

**问题**: 无法从其他设备访问

**解决方案**:
1. 打开 Windows 防火墙设置
2. 添加入站规则，允许端口 3000
3. 或临时关闭防火墙测试

### 4. 权限不足

**问题**: 无法安装 Windows 服务

**解决方案**:
- 以管理员身份运行命令提示符或 PowerShell
- 右键点击脚本，选择"以管理员身份运行"

### 5. 脚本执行策略（PowerShell）

**问题**: PowerShell 脚本无法执行

**解决方案**:
```powershell
# 查看当前策略
Get-ExecutionPolicy

# 临时允许（当前会话）
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 或永久允许（需要管理员权限）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 文件位置说明

### Windows 特定路径

- **PID 文件**: `%TEMP%\yuque-proxy.pid`
- **日志文件**: `%TEMP%\yuque-proxy.log`
- **配置文件**: `项目目录\yuque-config.env`

### 环境变量

- `%TEMP%` - 临时文件目录（通常是 `C:\Users\用户名\AppData\Local\Temp`）
- `%USERPROFILE%` - 用户主目录

---

## 🔄 与 macOS/Linux 的差异

| 功能 | macOS/Linux | Windows |
|------|-------------|---------|
| 启动脚本 | `start_server.sh` | `start_server.bat` 或 `start_server.ps1` |
| 系统服务 | `launchd` (`.plist`) | Windows Service 或 NSSM |
| 进程管理 | `ps`, `kill` | `tasklist`, `taskkill` |
| 端口检查 | `lsof` | `netstat` |
| 后台运行 | `nohup` | `start /B` 或 PowerShell `Start-Process` |
| 路径分隔符 | `/` | `\` |

---

## 📚 相关文档

- [`QUICK_START.md`](QUICK_START.md) - 快速开始指南
- [`CONFIG_GUIDE.md`](CONFIG_GUIDE.md) - 配置指南
- [`CLIENT_COMPATIBILITY.md`](CLIENT_COMPATIBILITY.md) - 客户端兼容性指南

---

## 🤝 贡献

如果您在 Windows 部署过程中遇到问题，欢迎提交 Issue 或 Pull Request！

---

**最后更新**: 2025-11-18

