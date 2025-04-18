# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 数据库文件将保存在项目根目录下的 shortener.db 文件里
SQLALCHEMY_DATABASE_URL = "sqlite:///./shortener.db"
# 如果用 PostgreSQL: "postgresql://user:password@postgresserver/db"

# 创建 SQLAlchemy 引擎
# connect_args 是 SQLite 特有的，建议加上以提高并发性能
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建一个 SessionLocal 类，每个实例将是一个数据库会话
# autocommit=False 和 autoflush=False 是常用的设置
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 重新导入在 models.py 中定义的 Base
# (也可以直接从 models 导入 Base = models.Base)
Base = declarative_base()

def create_db_and_tables():
    # 这会查找所有继承自 Base 的类，并在数据库中创建对应的表
    # 如果表已存在，则不会重复创建
    Base.metadata.create_all(bind=engine)

# 我们可以在应用启动时调用 create_db_and_tables()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
