@echo off
REM 语雀 MCP 代理服务器启动脚本 (Windows)
REM 功能：检测服务是否运行，如果没有则自动启动

setlocal enabledelayedexpansion

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "SCRIPT_NAME=app.py"
set "CONFIG_FILE=%SCRIPT_DIR%\yuque-config.env"
if defined PORT (
    set "PORT=%PORT%"
) else (
    set "PORT=3000"
)
set "PID_FILE=%TEMP%\yuque-proxy.pid"
set "LOG_FILE=%TEMP%\yuque-proxy.log"

REM 加载配置文件（如果存在）
if exist "%CONFIG_FILE%" (
    echo 📝 加载配置文件: %CONFIG_FILE%
    for /f "usebackq tokens=1,* delims==" %%a in ("%CONFIG_FILE%") do (
        if not "%%a"=="" (
            if not "%%a"=="#" (
                set "%%a=%%b"
            )
        )
    )
)

REM 检查服务是否运行
:check_server
if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    if defined PID (
        tasklist /FI "PID eq !PID!" 2>NUL | find /I /N "python.exe">NUL
        if "!ERRORLEVEL!"=="0" (
            netstat -ano | findstr ":!PORT!.*LISTENING" >NUL
            if "!ERRORLEVEL!"=="0" (
                echo ✅ 服务正在运行中 (PID: !PID!)
                goto :end
            )
        )
    )
    REM PID 文件存在但进程不存在，清理
    del "%PID_FILE%" 2>NUL
)

REM 启动服务
echo 🚀 正在启动语雀 MCP 代理服务器...

REM 检查 Token 配置
if not defined YUQUE_TOKEN (
    echo ⚠️  警告: 未设置 YUQUE_TOKEN 环境变量
    echo    提示: 可以通过以下方式配置：
    echo    1. 创建配置文件: %CONFIG_FILE%
    echo    2. 设置环境变量: set YUQUE_TOKEN=your-token
    echo    3. 在客户端的 HTTP Header 中配置: X-Yuque-Token
    echo.
    echo    继续启动服务（Token 可通过 HTTP Header 提供）...
)

REM 切换到脚本目录
cd /d "%SCRIPT_DIR%"

REM 启动服务（后台运行）
start /B python "%SCRIPT_NAME%" > "%LOG_FILE%" 2>&1

REM 等待服务启动
timeout /t 2 /nobreak >NUL

REM 检查服务是否启动成功
netstat -ano | findstr ":!PORT!.*LISTENING" >NUL
if "!ERRORLEVEL!"=="0" (
    REM 获取进程 PID
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":!PORT!.*LISTENING"') do (
        echo %%a > "%PID_FILE%"
        set /p PID=<"%PID_FILE%"
        echo ✅ 服务启动成功！
        echo    PID: !PID!
        echo    端口: !PORT!
        echo    日志: %LOG_FILE%
        echo    健康检查: http://localhost:!PORT!/health
        goto :end
    )
) else (
    echo ❌ 服务启动失败，请查看日志: %LOG_FILE%
    exit /b 1
)

:end
endlocal

