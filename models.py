# models.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func # 用于获取数据库服务器时间

# 创建一个 Base 类，我们的模型类将继承它
Base = declarative_base()

class URLMap(Base):
    __tablename__ = "url_maps" # 指定映射的数据库表名

    # 定义表的列 (字段)
    id = Column(Integer, primary_key=True, index=True) # 主键，自增，加索引
    short_code = Column(String, unique=True, index=True) # 短码，唯一，加索引
    long_url = Column(String, index=True) # 原始长 URL，加索引方便查找
    # default=func.now() 让数据库在插入时自动设置当前时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # onupdate=func.now() 让数据库在更新时自动更新时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 这个 __repr__ 方法是为了方便打印对象时查看信息，可选
    def __repr__(self):
        return f"<URLMap(short_code='{self.short_code}', long_url='{self.long_url}')>"