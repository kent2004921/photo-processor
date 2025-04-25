# 使用官方 Python 3.10 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器
COPY . .

# 安装系统依赖（OpenCV 需要）
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口（Render 默认使用 8080）
EXPOSE 8080

# 使用 gunicorn 启动 Flask 应用，增加调试日志
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "debug", "lambda_function:app"]
