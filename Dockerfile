FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PORT=3000

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用文件
COPY app_async.py .
COPY app.py .
COPY async_yuque_client.py .
COPY yuque_client.py .
COPY config.py .
COPY cache.py .
COPY utils/ ./utils/
COPY yuque-config.env.example .

# 创建非 root 用户
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 暴露端口
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# 启动命令 - 使用 uvicorn 启动异步服务
CMD ["uvicorn", "app_async:app", "--host", "0.0.0.0", "--port", "3000"]
