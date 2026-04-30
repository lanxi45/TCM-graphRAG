# 使用轻量级 Python 3.8 镜像
FROM python:3.8-slim

# 设置工作目录
WORKDIR /app

# 复制依赖表并安装（针对你之前遇到的 OpenSSL 坑进行了优化）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制前端代码
COPY frontend.py .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 启动指令（固定写法）
CMD ["streamlit", "run", "frontend.py", "--server.address=0.0.0.0"]