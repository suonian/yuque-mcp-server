# 语雀 MCP 代理服务器启动脚本 (Windows PowerShell)
# 功能：检测服务是否运行，如果没有则自动启动

# 获取脚本所在目录
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$SCRIPT_NAME = "yuque-proxy.js"
$CONFIG_FILE = Join-Path $SCRIPT_DIR "yuque-config.env"
$PORT = if ($env:PORT) { $env:PORT } else { 3000 }
$PID_FILE = Join-Path $env:TEMP "yuque-proxy.pid"
$LOG_FILE = Join-Path $env:TEMP "yuque-proxy.log"

# 加载配置文件（如果存在）
function Load-Config {
    if (Test-Path $CONFIG_FILE) {
        Write-Host "📝 加载配置文件: $CONFIG_FILE"
        Get-Content $CONFIG_FILE | ForEach-Object {
            if ($_ -match '^\s*([^#=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                if ($key -and $value) {
                    [Environment]::SetEnvironmentVariable($key, $value, "Process")
                }
            }
        }
    }
}

# 检查服务是否运行
function Test-ServerRunning {
    if (Test-Path $PID_FILE) {
        $pid = Get-Content $PID_FILE -ErrorAction SilentlyContinue
        if ($pid) {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                # 检查端口是否被占用
                $listening = Get-NetTCPConnection -LocalPort $PORT -State Listen -ErrorAction SilentlyContinue
                if ($listening) {
                    return $true
                }
            }
        }
        # PID 文件存在但进程不存在，清理
        Remove-Item $PID_FILE -ErrorAction SilentlyContinue
    }
    return $false
}

# 启动服务
function Start-Server {
    if (Test-ServerRunning) {
        $pid = Get-Content $PID_FILE
        Write-Host "✅ 服务正在运行中 (PID: $pid)"
        return
    }
    
    # 加载配置文件
    Load-Config
    
    Write-Host "🚀 正在启动语雀 MCP 代理服务器..."
    
    # 检查 Token 配置
    if (-not $env:YUQUE_TOKEN) {
        Write-Host "⚠️  警告: 未设置 YUQUE_TOKEN 环境变量"
        Write-Host "   提示: 可以通过以下方式配置："
        Write-Host "   1. 创建配置文件: $CONFIG_FILE"
        Write-Host "   2. 设置环境变量: `$env:YUQUE_TOKEN='your-token'"
        Write-Host "   3. 在客户端的 HTTP Header 中配置: X-Yuque-Token"
        Write-Host ""
        Write-Host "   继续启动服务（Token 可通过 HTTP Header 提供）..."
    }
    
    # 切换到脚本目录
    Set-Location $SCRIPT_DIR
    
    # 启动服务（后台运行）
    $scriptPath = Join-Path $SCRIPT_DIR $SCRIPT_NAME
    $process = Start-Process -FilePath "python" -ArgumentList "`"$scriptPath`"" -PassThru -WindowStyle Hidden -RedirectStandardOutput $LOG_FILE -RedirectStandardError $LOG_FILE
    
    # 等待服务启动
    Start-Sleep -Seconds 2
    
    # 检查服务是否启动成功
    $listening = Get-NetTCPConnection -LocalPort $PORT -State Listen -ErrorAction SilentlyContinue
    if ($listening) {
        $processId = $process.Id
        $processId | Out-File -FilePath $PID_FILE -Encoding ASCII
        Write-Host "✅ 服务启动成功！"
        Write-Host "   PID: $processId"
        Write-Host "   端口: $PORT"
        Write-Host "   日志: $LOG_FILE"
        Write-Host "   健康检查: http://localhost:$PORT/health"
    } else {
        Write-Host "❌ 服务启动失败，请查看日志: $LOG_FILE"
        exit 1
    }
}

# 停止服务
function Stop-Server {
    if (Test-Path $PID_FILE) {
        $pid = Get-Content $PID_FILE -ErrorAction SilentlyContinue
        if ($pid) {
            $process = Get-Process -Id $pid -ErrorAction SilentlyContinue
            if ($process) {
                Write-Host "🛑 正在停止服务 (PID: $pid)..."
                Stop-Process -Id $pid -Force
                Remove-Item $PID_FILE -ErrorAction SilentlyContinue
                Write-Host "✅ 服务已停止"
            } else {
                Write-Host "⚠️  进程不存在，清理 PID 文件"
                Remove-Item $PID_FILE -ErrorAction SilentlyContinue
            }
        }
    } else {
        Write-Host "⚠️  服务未运行"
    }
}

# 查看服务状态
function Get-ServerStatus {
    if (Test-ServerRunning) {
        $pid = Get-Content $PID_FILE
        Write-Host "✅ 服务正在运行"
        Write-Host "   PID: $pid"
        Write-Host "   端口: $PORT"
        Write-Host "   日志: $LOG_FILE"
        
        # 健康检查
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:$PORT/health" -UseBasicParsing -TimeoutSec 2
            $health = $response.Content | ConvertFrom-Json
            Write-Host ""
            Write-Host "📊 健康检查:"
            Write-Host ($health | ConvertTo-Json -Depth 3)
        } catch {
            Write-Host "⚠️  健康检查失败: $_"
        }
    } else {
        Write-Host "❌ 服务未运行"
    }
}

# 查看日志
function Show-Logs {
    if (Test-Path $LOG_FILE) {
        Get-Content $LOG_FILE -Tail 50
    } else {
        Write-Host "⚠️  日志文件不存在: $LOG_FILE"
    }
}

# 主函数
$command = $args[0]

switch ($command) {
    "start" { Start-Server }
    "stop" { Stop-Server }
    "restart" { Stop-Server; Start-Sleep -Seconds 1; Start-Server }
    "status" { Get-ServerStatus }
    "logs" { Show-Logs }
    "config" {
        if (Test-Path $CONFIG_FILE) {
            Write-Host "📝 配置文件已存在: $CONFIG_FILE"
            Write-Host ""
            Write-Host "当前配置:"
            Get-Content $CONFIG_FILE
        } else {
            Write-Host "📝 创建配置文件: $CONFIG_FILE"
            @"
# 语雀 MCP 代理配置文件
# 此文件包含敏感信息，请勿提交到代码仓库

# 语雀 Token（必需）
# 获取方式：语雀设置 > 个人设置 > Token
YUQUE_TOKEN=your-token-here

# 服务端口（可选，默认 3000）
PORT=3000
"@ | Out-File -FilePath $CONFIG_FILE -Encoding UTF8
            Write-Host "✅ 配置文件已创建"
            Write-Host "⚠️  请编辑 $CONFIG_FILE 并填入您的 Token"
        }
    }
    default {
        Write-Host "用法: .\start_server.ps1 {start|stop|restart|status|logs|config}"
        Write-Host ""
        Write-Host "命令说明:"
        Write-Host "  start   - 启动服务"
        Write-Host "  stop    - 停止服务"
        Write-Host "  restart - 重启服务"
        Write-Host "  status  - 查看服务状态"
        Write-Host "  logs    - 查看日志"
        Write-Host "  config  - 管理配置文件"
    }
}

