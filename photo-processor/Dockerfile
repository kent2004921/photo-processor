FROM python:3.9-slim

# 安装系统依赖（OpenCV 需要）
RUN apt-get update && apt-get install -y libsm6 libxext6 libxrender-dev

# 复制 requirements.txt 和 lambda_function.py
COPY requirements.txt .
COPY lambda_function.py .

# 安装 Python 依赖
RUN pip install -r requirements.txt

# 安装 Flask
RUN pip install flask

# 设置工作目录
WORKDIR /

# 启动 Flask 应用
CMD ["python", "lambda_function.py"]
