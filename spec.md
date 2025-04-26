# 将 FastAPI 应用从 SQLite 迁移到 Supabase 并部署

## 需求分析

1.  将应用程序的数据库从本地 SQLite 文件迁移到云端的 Supabase (PostgreSQL) 数据库。
2.  确保应用能够在本地开发环境中连接并使用 Supabase 进行测试。
3.  将改造后的 FastAPI 应用部署到云服务器（例如 Vultr），使其可以通过公共域名访问。
4.  尽量利用 Supabase 的免费额度。

## 技术选型

*   **数据库**: Supabase (基于 PostgreSQL)
*   **后端框架**: FastAPI (Python)
*   **数据库交互**: `supabase-py` (推荐) 或 `psycopg2-binary`/`asyncpg`
*   **本地开发**: Supabase CLI + Docker
*   **部署平台**: Vultr (或其他云服务器/PaaS)

## 里程碑

### 1. Supabase 设置与本地开发环境

*   在 Supabase 官网 ([supabase.com](https://supabase.com/)) 创建一个新的项目。
*   安装 Supabase CLI ([Install the Supabase CLI](https://supabase.com/docs/guides/cli/getting-started/installation))。
*   在本地项目根目录下运行 `supabase init` 初始化项目。
*   运行 `supabase start` 启动本地 Supabase 开发环境 (需要 Docker)。
*   创建数据库迁移文件：
    *   将原 SQLite 的表结构 (`CREATE TABLE ...`) 转换为 PostgreSQL 兼容的 DDL 语句。
    *   使用 `supabase migration new <migration_name>` 创建新的迁移文件。
    *   将 DDL 语句写入迁移文件 (`supabase/migrations/<timestamp>_<migration_name>.sql`)。
    *   运行 `supabase db reset` (会应用本地迁移文件) 或等待后续 `supabase start` 时自动应用。

### 2. 应用程序代码改造

*   添加 Supabase Python 客户端库或其他 PostgreSQL 库到项目依赖 (`requirements.txt`)。
*   修改数据库连接逻辑：
    *   从环境变量读取 Supabase 项目 URL 和 API 密钥 (anon key, service role key)。
    *   使用 `supabase-py` 或所选库初始化数据库连接。
*   替换数据操作代码：
    *   将所有 `sqlite3` 相关的查询和操作替换为 `supabase-py` 的 API 调用 (如 `supabase.table('...').select('*').execute()`) 或相应 PostgreSQL 库的函数。
    *   确保 SQL 语法与 PostgreSQL 兼容。
    *   处理好同步/异步操作（如果使用 FastAPI 和 `asyncpg`）。

### 3. 本地测试

*   确保本地 Supabase 服务正在运行 (`supabase start`)。
*   配置 FastAPI 应用使用 **本地** Supabase 实例的 URL 和密钥 (Supabase CLI 启动时会显示这些信息)。
*   启动 FastAPI 应用 (`uvicorn main:app --reload` 或类似命令)。
*   通过浏览器或 API 测试工具 (如 Postman, Insomnia) 访问应用的各个接口，特别是涉及数据库 CRUD 操作的接口。
*   检查 Supabase Studio (本地实例通常在 `http://localhost:54323`) 或直接查询本地数据库，确认数据操作是否成功。

### 4. 部署

*   **数据库迁移应用到线上**: 运行 `supabase db push` 将本地 `supabase/migrations` 目录下的所有迁移文件应用到你的 **线上** Supabase 项目。
*   **应用部署准备**:
    *   在 Vultr (或其他平台) 上创建服务器实例并安装好 Python 环境、依赖管理工具 (如 pip)。
    *   配置防火墙规则，允许必要的端口访问 (如 HTTP/HTTPS)。
*   **部署代码**: 将你的 FastAPI 应用代码上传到服务器。
*   **配置生产环境变量**: 在服务器上设置环境变量，包含 **线上** Supabase 项目的 URL 和 API 密钥。 **注意：** 不要将敏感密钥硬编码在代码中或提交到版本控制。
*   **运行应用**: 使用 Gunicorn + Uvicorn (或其他 ASGI 服务器) 在后台运行 FastAPI 应用。可以考虑使用 Systemd 或 Supervisor 来管理进程。
*   **(可选) 配置反向代理**: 使用 Nginx 或 Caddy 作为反向代理，处理 HTTPS、负载均衡等。
*   **(可选) 配置域名**: 将你的域名指向服务器的 IP 地址。

### 5. 生产环境验证

*   通过你的公共域名访问部署的应用。
*   重复本地测试阶段的所有功能测试，确保应用在线上环境中与 Supabase 数据库正常交互。
*   检查应用日志和 Supabase 项目日志，排查潜在问题。
*   监控应用性能和 Supabase 资源使用情况。
