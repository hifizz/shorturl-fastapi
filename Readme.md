# FastAPI URL Shortener Dockerized

这是一个使用 FastAPI 构建的简单 URL 短链接服务，并配置为可以通过 Docker 运行和部署。

## 功能

- 将长 URL 缩短为唯一的短代码。
- 通过访问短代码 URL 重定向到原始的长 URL。
- 提供一个简单的前端页面 (`static/index.html`) 进行交互。
- 使用 SQLite 数据库存储映射关系 (通过 SQLAlchemy)。

## 技术栈

- **后端**: Python, FastAPI
- **数据库**: SQLite
- **ORM**: SQLAlchemy
- **部署**: Docker

## 本地开发设置

1. **克隆仓库**: `git clone <your-repo-url>`
2. **进入项目目录**: `cd fastapi-project`
3. **(推荐) 设置 Python 版本**: 如果你使用 `pyenv`，可以运行 `pyenv local 3.11.x` (选择一个 3.11 或更高版本) 来确保环境一致性。
4. **创建虚拟环境**: `python -m venv .venv`
5. **激活虚拟环境**:
    - macOS/Linux: `source .venv/bin/activate`
    - Windows (Git Bash/WSL): `source .venv/Scripts/activate`
    - Windows (CMD): `.venv\Scripts\activate.bat`
    - Windows (PowerShell): `.venv\Scripts\Activate.ps1`
6. **安装依赖**: `pip install -r requirements.txt`

## 本地运行 (不使用 Docker)

激活虚拟环境后，可以直接使用 Uvicorn 运行 FastAPI 应用：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- `--reload`: 启用热重载，代码更改时服务器会自动重启（仅用于开发）。
- 访问 `http://localhost:8000` 查看应用。
- SQLite 数据库文件 (`shortener.db`) 会在项目根目录创建。

## 本地运行 (使用 Docker)

确保你已经安装了 Docker Desktop 或 Docker Engine。

1. **构建 Docker 镜像**:
    在项目根目录下运行：

    ```bash
    docker build -t fastapi-shortener .
    ```

    - `-t fastapi-shortener`: 给镜像命名（tag）为 `fastapi-shortener`。
    - `.`: 表示 Dockerfile 在当前目录。

2. **运行 Docker 容器**:

    ```bash
    docker run -d -p 8000:8000 --name shortener-app fastapi-shortener
    ```

    - `-d`: 在后台分离模式运行容器。
    - `-p 8000:8000`: 将宿主机的 8000 端口映射到容器的 8000 端口。
    - `--name shortener-app`: 给容器命名，方便管理。
    - `fastapi-shortener`: 使用我们之前构建的镜像。

3. **访问应用**: 访问 `http://localhost:8000`。

4. **查看日志**: `docker logs shortener-app`

5. **停止容器**: `docker stop shortener-app`

6. **移除容器**: `docker rm shortener-app`

**注意**: 使用 `docker run` 时，SQLite 数据库文件 (`shortener.db`) 会创建在**容器内部**的 `/app` 目录下。当容器被删除时，**数据会丢失**。如果需要持久化数据，请看下面的 Docker Compose 方法或使用 `-v` 参数挂载卷。

## 本地运行 (使用 Docker Compose - 推荐用于开发)

Docker Compose 可以更方便地管理容器配置和卷挂载，尤其适合开发。

1. **(可选) 创建 `docker-compose.yml` 文件** (我将在下一步提供内容)。
2. **启动服务**:
    在包含 `docker-compose.yml` 的目录下运行：

    ```bash
    docker-compose up --build
    ```

    - `up`: 创建并启动服务。
    - `--build`: 如果镜像不存在或 Dockerfile 有更改，则构建镜像。
3. **访问应用**: 访问 `http://localhost:8000`。
4. **实时代码重载**: 如果 `docker-compose.yml` 配置了卷挂载，修改本地代码会**自动触发**容器内 Uvicorn 服务器的重启 (因为 `Dockerfile` 中的 `CMD` 使用了 `uvicorn`，而它默认会监听文件变化，但更可靠的方式是在 Compose command 中添加 `--reload`)。
5. **停止服务**: 在运行 `docker-compose up` 的终端按 `Ctrl+C`，然后可以运行 `docker-compose down` 来停止并移除容器和网络。

## 部署 (基本思路)

将应用部署到服务器的基本步骤：

1. **构建镜像**: 在本地或 CI/CD 环境中构建生产镜像 (`docker build ...`)。
2. **推送镜像**: 将镜像推送到 Docker Hub、AWS ECR、Google GCR 或其他容器镜像仓库。
3. **服务器准备**: 在你的云服务器 (如 Vultr, AWS EC2, DigitalOcean Droplet) 上安装 Docker Engine。
4. **拉取镜像**: 在服务器上从仓库拉取你的应用镜像 (`docker pull <your-image-repo>:<tag>`)。
5. **运行容器**: 在服务器上运行容器 (`docker run ...`)。
    - **数据持久化**: 使用 `-v` 选项将服务器上的一个目录挂载到容器内 SQLite 数据库文件所在的位置，例如 `-v /path/on/server/data:/app` (假设数据库在 `/app/shortener.db`)。
    - **端口**: 确保服务器防火墙允许访问你映射的端口 (如 8000)。
    - **生产环境考虑**: 在生产中，通常不会直接暴露 Uvicorn。建议使用 Gunicorn + Uvicorn workers (`gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b 0.0.0.0:8000`) 并可能在前面加一个反向代理 (如 Nginx 或 Caddy) 来处理 HTTPS、请求缓冲、静态文件服务等。

## 项目结构 (示例)

```
fastapi-project/
├── .venv/               # Python 虚拟环境 (被 .gitignore 和 .dockerignore 忽略)
├── static/
│   └── index.html     # 简单的前端页面
├── .dockerignore        # Docker 构建时忽略的文件
├── .gitignore           # Git 忽略的文件
├── Dockerfile           # Docker 镜像构建说明
├── database.py          # SQLAlchemy 和数据库配置
├── crud.py              # 数据库操作函数
├── main.py              # FastAPI 应用入口
├── models.py            # SQLAlchemy 数据模型
├── README.md            # 项目文档 (就是这个文件)
├── requirements.txt     # Python 依赖
├── schemas.py           # Pydantic 数据模式
└── shortener.db         # 本地 SQLite 数据库文件 (被 .dockerignore 忽略)
```
