# 使用官方 Python 运行时作为父镜像
# 选择一个具体的 slim 版本以减小镜像体积
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装构建依赖（如果需要编译某些包）并清理缓存
# 例如：RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
# 这里暂时不需要额外系统依赖

# 将依赖文件复制到工作目录
COPY requirements.txt ./

# 安装 Python 依赖
# --no-cache-dir 避免缓存，减小镜像层体积
RUN pip install --no-cache-dir -r requirements.txt

# 将项目代码复制到工作目录
# 注意： .dockerignore 文件会控制哪些文件被复制
COPY . .

# 暴露 FastAPI 应用运行的端口 (默认 8000)
EXPOSE 8000

# 容器启动时运行 uvicorn 服务器
# 使用 0.0.0.0 使其可以从容器外部访问
# --host 0.0.0.0 --port 8000 是 uvicorn 的参数
# main:app 指向 main.py 文件中的 app 实例
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
